from chargecenter.transactions.models import Transaction
from chargecenter.users.models import SalesPerson


def create_transaction(salesperson: SalesPerson, amount: int, is_charge: bool):
    return Transaction.objects.create(salesperson=salesperson, amount=amount, is_charge=is_charge)
