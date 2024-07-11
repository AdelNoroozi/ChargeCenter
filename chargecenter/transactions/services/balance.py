from django.db import transaction

from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.transactions.serializers import TransactionOutputSerializer, IncreaseBalanceSerializer
from chargecenter.users.models import BaseUser


@transaction.atomic
def create_balance_transaction(user: BaseUser, data: dict):
    serializer = IncreaseBalanceSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    salesperson = user.salesperson
    transaction_obj = create_transaction(salesperson=salesperson, amount=serializer.data.get("amount"))
    create_balance(transaction=transaction_obj)
    return TransactionOutputSerializer(instance=transaction_obj, context={"full_access": False}).data
