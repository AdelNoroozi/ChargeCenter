import os
import time

import django
from django.db.models.deletion import RestrictedError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")
django.setup()

from django.db import transaction

from chargecenter.phones.models import PhoneNumber

from django.db.models import Sum

from chargecenter.transactions.models import Transaction, BalanceTransaction, ChargeTransaction

from django.utils import timezone
from locust import HttpUser, task, TaskSet

from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.users.models import SalesPerson, BaseUser

user_counter = 0
start_time = 0
salesperson1 = SalesPerson()
salesperson2 = SalesPerson()
phone_number = PhoneNumber()


def flush_test_data():
    global salesperson1
    global salesperson2
    global phone_number

    print("flushing test data")

    retry = True
    while retry:
        try:
            transactions = Transaction.objects.filter(salesperson__in=[salesperson1, salesperson2])
            BalanceTransaction.objects.filter(transaction_obj__in=transactions).delete()
            ChargeTransaction.objects.filter(transaction_obj__in=transactions).delete()
            transactions.delete()
            PhoneNumber.objects.filter(id=phone_number.id).delete()
            user1_id = salesperson1.user.id
            user2_id = salesperson2.user.id
            SalesPerson.objects.filter(id=salesperson1.id).delete()
            SalesPerson.objects.filter(id=salesperson2.id).delete()
            BaseUser.objects.filter(id=user1_id).delete()
            BaseUser.objects.filter(id=user2_id).delete()
            BaseUser.objects.filter(username="test_admin").delete()
            retry = False
        except RestrictedError:
            print("db restriction occurred, retrying...")
            time.sleep(0.1)

    print("test data flushed")


def get_transaction_values(salesperson, end_time, initial_salesperson_balance):
    sum_of_balance_increase = Transaction.objects.filter(
        salesperson=salesperson, created_at__gte=start_time, created_at__lt=end_time, is_charge=False,
        status=Transaction.DONE
    ).aggregate(sum_of_balance=Sum("amount"))["sum_of_balance"]
    sum_of_charge = Transaction.objects.filter(
        salesperson=salesperson, created_at__gte=start_time, created_at__lt=end_time, is_charge=True,
        status=Transaction.DONE
    ).aggregate(sum_of_charge=Sum("amount"))["sum_of_charge"]
    if sum_of_charge is None:
        sum_of_charge = 0
    if sum_of_balance_increase is None:
        sum_of_balance_increase = 0
    expected_final_balance = initial_salesperson_balance + sum_of_balance_increase - sum_of_charge
    salesperson.refresh_from_db()
    final_balance = salesperson.balance
    print(salesperson.user.username)
    print(expected_final_balance)
    print(final_balance)
    print("*****************")
    return final_balance, expected_final_balance


class TransactionsTask(TaskSet):
    balance_transactions = []

    initial_salesperson1_balance = 0
    initial_salesperson2_balance = 0

    @transaction.atomic
    def on_start(self):
        global user_counter
        global start_time
        global salesperson1
        global salesperson2
        global phone_number

        if user_counter == 0:
            user1 = BaseUser.objects.create_user(username="test_sales1", email="sales1@testmail.com",
                                                 password="password")
            user2 = BaseUser.objects.create_user(username="test_sales2", email="sales2@testmail.com",
                                                 password="password")
            salesperson1 = SalesPerson.objects.create(user=user1, first_name="sales1", last_name="sales1",
                                                      balance=100000)
            salesperson2 = SalesPerson.objects.create(user=user2, first_name="sales2", last_name="sales2",
                                                      balance=80000)
            phone_number = PhoneNumber.objects.create(number="+13077685210")
            BaseUser.objects.create_superuser(username="test_admin", password="password")
            start_time = timezone.now()
            for _ in range(10):
                transaction1 = create_transaction(salesperson=salesperson1,
                                                  amount=1000, is_charge=False)
                transaction2 = create_transaction(salesperson=salesperson2,
                                                  amount=2000, is_charge=False)
                balance_transaction1 = create_balance(transaction=transaction1)
                balance_transaction2 = create_balance(transaction=transaction2)
                self.balance_transactions.append(balance_transaction1)
                self.balance_transactions.append(balance_transaction2)

        self.initial_salesperson1_balance = salesperson1.balance
        self.initial_salesperson2_balance = salesperson2.balance

        user_counter += 1

    def login_admin(self):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": "test_admin",
            "password": "password"
        })
        return response.json().get("access")

    def login_sales(self, username):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": username,
            "password": "password"
        })

        if username == "test_sales1":
            return response.json().get("access")
        elif username == "test_sales2":
            return response.json().get("access")

    @task(1)
    def confirm_balance_transactions(self):
        admin_token = self.login_admin()
        for balance_transaction in self.balance_transactions:
            status_code = self.client.patch(f"/api/transactions/confirm-balance/",
                                            headers={"Authorization": f"Bearer {admin_token}"},
                                            data={"balance": balance_transaction.id}).status_code
            assert status_code == 200

    @task(100)
    def create_charge_transactions(self):
        global phone_number

        sales1_token = self.login_sales(username="test_sales1")
        response1 = self.client.post("/api/transactions/create-charge/",
                                     headers={"Authorization": f"Bearer {sales1_token}"},
                                     data={"phone_number": phone_number.id, "amount": 4})
        assert response1.status_code == 201

        sales2_token = self.login_sales(username="test_sales2")
        response2 = self.client.post("/api/transactions/create-charge/",
                                     headers={"Authorization": f"Bearer {sales2_token}"},
                                     data={"phone_number": phone_number.id, "amount": 3})
        assert response2.status_code == 201

    def on_stop(self):
        global user_counter
        global start_time
        global salesperson1
        global salesperson2

        user_counter -= 1

        if user_counter == 0:
            time.sleep(0.1)
            end_time = timezone.now()
            final_balance1, expected_final_balance1 = get_transaction_values(
                salesperson=salesperson1,
                end_time=end_time,
                initial_salesperson_balance=self.initial_salesperson1_balance)
            final_balance2, expected_final_balance2 = get_transaction_values(
                salesperson=salesperson2,
                end_time=end_time,
                initial_salesperson_balance=self.initial_salesperson2_balance)
            flush_test_data()
            assert final_balance1 == expected_final_balance1, \
                f"{salesperson1.user.username}: Expected {expected_final_balance1}, got {final_balance1}"
            assert final_balance2 == expected_final_balance2, \
                f"{salesperson2.user.username}: Expected {expected_final_balance2}, got {final_balance2}"


class TransactionUser(HttpUser):
    tasks = [TransactionsTask]
