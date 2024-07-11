from chargecenter.transactions.models import Transaction
from chargecenter.users.models import SalesPerson


def create_transaction(salesperson: SalesPerson, amount: int):
    return Transaction.objects.create(salesperson=salesperson, amount=amount)
