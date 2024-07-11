from django.db import transaction

from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.transactions.serializers import TransactionOutputSerializer
from chargecenter.users.models import BaseUser


@transaction.atomic
def create_balance_transaction(user: BaseUser, amount: int):
    salesperson = user.salesperson
    transaction_obj = create_transaction(salesperson=salesperson, amount=amount)
    create_balance(transaction=transaction_obj)
    return TransactionOutputSerializer(instance=transaction_obj).data
