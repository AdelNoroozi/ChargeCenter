import os

import django
from locust import HttpUser, task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")
django.setup()

from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.users.models import SalesPerson


class TransactionsUser(HttpUser):
    admin_token = None
    sales1_token = None
    sales2_token = None
    balance_transactions1 = []
    balance_transactions2 = []

    salesperson1 = SalesPerson.objects.filter(user__username="jamshid").first()
    salesperson2 = SalesPerson.objects.filter(user__username="Hosein").first()
    initial_salesperson1_balance = 0
    initial_salesperson2_balance = 0
    charge_transaction_count1 = 0
    charge_transaction_count2 = 0
    balance_transaction_count1 = 0
    balance_transaction_count2 = 0

    def on_start(self):
        self.login_admin()
        self.login_sales1()
        self.login_sales2()
        self.initial_salesperson1_balance = self.salesperson1.balance
        self.initial_salesperson2_balance = self.salesperson2.balance
        for _ in range(10):
            transaction1 = create_transaction(salesperson=self.salesperson1,
                                              amount=1000, is_charge=False)
            transaction2 = create_transaction(salesperson=self.salesperson2,
                                              amount=2000, is_charge=False)
            balance_transaction1 = create_balance(transaction=transaction1)
            balance_transaction2 = create_balance(transaction=transaction2)
            self.balance_transactions2.append(balance_transaction1)
            self.balance_transactions2.append(balance_transaction2)

    def login_admin(self):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": "admin",
            "password": "admin"
        })
        self.admin_token = response.json().get("access")

    def login_sales1(self):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": "jamshid",
            "password": "stringstr123@"
        })
        self.sales1_token = response.json().get("access")

    def login_sales2(self):
        response = self.client.post("/api/auth/jwt/login/", {
            "username": "Hosein",
            "password": "stringstr123@"
        })
        self.sales2_token = response.json().get("access")

    def confirm_balance_request(self, balance_transaction_id):
        response = self.client.patch(f"/api/transaction/confirm-balance/",
                                     headers={"Authorization": f"Bearer {self.admin_token}"},
                                     data={"balance": balance_transaction_id})
        return response.status_code

    @task
    def confirm_balance_transaction(self):
        for balance_transaction in self.balance_transactions1 + self.balance_transactions2:
            status_code = self.confirm_balance_request(balance_transaction.id)
            assert status_code == 200
            if status_code == 200:
                if balance_transaction in self.balance_transactions1:
                    self.balance_transaction_count1 += 1
                elif balance_transaction in self.balance_transactions2:
                    self.balance_transaction_count2 += 1

    @task
    def create_charge_transaction1(self):
        response1 = self.client.post("/api/transaction/create-charge/",
                                     headers={"Authorization": f"Bearer {self.sales1_token}"},
                                     data={"phone_number": "cae70483-55ca-4db4-85b7-969cab42cfb7", "amount": 4})
        assert response1.status_code == 201
        if response1.status_code == 201:
            self.charge_transaction_count1 += 1

        response2 = self.client.post("/api/transaction/create-charge/",
                                     headers={"Authorization": f"Bearer {self.sales2_token}"},
                                     data={"phone_number": "cae70483-55ca-4db4-85b7-969cab42cfb7", "amount": 3})
        assert response2.status_code == 201
        if response2.status_code == 201:
            self.charge_transaction_count2 += 1

    def on_stop(self):
        expected_final_balance1 = self.initial_salesperson1_balance + (1000 * self.balance_transaction_count1) - (
                4 * self.charge_transaction_count1)
        self.salesperson1.refresh_from_db()
        final_balance1 = self.salesperson1.balance
        assert final_balance1 == expected_final_balance1, f"Expected {expected_final_balance1}, got {final_balance1}"

        expected_final_balance2 = self.initial_salesperson1_balance + (2000 * self.balance_transaction_count1) - (
                3 * self.charge_transaction_count1)
        self.salesperson2.refresh_from_db()
        final_balance2 = self.salesperson2.balance
        assert final_balance2 == expected_final_balance2, f"Expected {expected_final_balance1}, got {final_balance1}"

