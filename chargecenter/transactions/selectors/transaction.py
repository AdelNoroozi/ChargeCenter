from django.db.models import QuerySet

from chargecenter.transactions.models import Transaction
from chargecenter.users.models import SalesPerson


def create_transaction(salesperson: SalesPerson, amount: int, is_charge: bool):
    return Transaction.objects.create(salesperson=salesperson, amount=amount, is_charge=is_charge)


def get_transactions(return_all: bool, salesperson: SalesPerson = None):
    if return_all:
        return Transaction.objects.all()
    else:
        return Transaction.objects.filter(salesperson=salesperson)


def order_transactions(queryset: QuerySet[Transaction], order_param: str):
    return queryset.order_by(order_param)
