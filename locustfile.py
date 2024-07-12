import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")
django.setup()

from django.db.models import Sum

from chargecenter.transactions.models import Transaction

from django.utils import timezone
from locust import HttpUser, task, TaskSet

from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.users.models import SalesPerson

user_counter = 0
start_time = 0


def validate_transaction_sum(salesperson, end_time, initial_salesperson_balance, ):
    sum_of_balance_increase = Transaction.objects.filter(
        salesperson=salesperson, created_at__gte=start_time, created_at__lt=end_time, is_charge=False,
        status=Transaction.DONE
    ).aggregate(sum_of_balance=Sum("amount"))["sum_of_balance"]
    sum_of_charge = Transaction.objects.filter(
        salesperson=salesperson, created_at__gte=start_time, created_at__lt=end_time, is_charge=True
    ).aggregate(sum_of_charge=Sum("amount"))["sum_of_charge"]
    expected_final_balance = initial_salesperson_balance + sum_of_balance_increase - sum_of_charge
    salesperson.refresh_from_db()
    final_balance = salesperson.balance
    print(salesperson.user.username)
    print(expected_final_balance)
    print(final_balance)
    print("*****************")
    assert final_balance == expected_final_balance, \
        f"{salesperson.user.username}: Expected {expected_final_balance}, got {final_balance}"


class TransactionsTask(TaskSet):
    admin_token = None
    sales1_token = None
    sales2_token = None
    balance_transactions = []

    salesperson1 = SalesPerson.objects.filter(user__username="jamshid").first()
    salesperson2 = SalesPerson.objects.filter(user__username="Hosein").first()
    initial_salesperson1_balance = 0
    initial_salesperson2_balance = 0

    def on_start(self):
        global user_counter
        global start_time

        if user_counter == 0:
            start_time = timezone.now()

        self.initial_salesperson1_balance = self.salesperson1.balance
        self.initial_salesperson2_balance = self.salesperson2.balance

        self.login_admin()
        self.login_sales(username="jamshid")
        self.login_sales(username="Hosein")

        for _ in range(10):
            transaction1 = create_transaction(salesperson=self.salesperson1,
                                              amount=1000, is_charge=False)
            transaction2 = create_transaction(salesperson=self.salesperson2,
                                              amount=2000, is_charge=False)
            balance_transaction1 = create_balance(transaction=transaction1)
            balance_transaction2 = create_balance(transaction=transaction2)
            self.balance_transactions.append(balance_transaction1)
            self.balance_transactions.append(balance_transaction2)
        user_counter += 1

    def login_admin(self):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": "admin",
            "password": "admin"
        })
        self.admin_token = response.json().get("access")

    def login_sales(self, username):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": username,
            "password": "stringstr123@"
        })

        if username == "jamshid":
            self.sales1_token = response.json().get("access")
        elif username == "Hosein":
            self.sales2_token = response.json().get("access")

    @task(1)
    def confirm_balance_transactions(self):
        for balance_transaction in self.balance_transactions:
            status_code = self.client.patch(f"/api/transaction/confirm-balance/",
                                            headers={"Authorization": f"Bearer {self.admin_token}"},
                                            data={"balance": balance_transaction.id}).status_code
            assert status_code == 200

    @task(100)
    def create_charge_transactions(self):
        response1 = self.client.post("/api/transaction/create-charge/",
                                     headers={"Authorization": f"Bearer {self.sales1_token}"},
                                     data={"phone_number": "cae70483-55ca-4db4-85b7-969cab42cfb7", "amount": 4})
        assert response1.status_code == 201

        response2 = self.client.post("/api/transaction/create-charge/",
                                     headers={"Authorization": f"Bearer {self.sales2_token}"},
                                     data={"phone_number": "cae70483-55ca-4db4-85b7-969cab42cfb7", "amount": 3})
        assert response2.status_code == 201

    def on_stop(self):
        global user_counter
        global start_time

        user_counter -= 1

        if user_counter == 0:
            time.sleep(0.1)
            end_time = timezone.now()
            validate_transaction_sum(salesperson=self.salesperson1, end_time=end_time,
                                     initial_salesperson_balance=self.initial_salesperson1_balance)
            validate_transaction_sum(salesperson=self.salesperson2, end_time=end_time,
                                     initial_salesperson_balance=self.initial_salesperson2_balance)


class TransactionUser(HttpUser):
    tasks = [TransactionsTask]
