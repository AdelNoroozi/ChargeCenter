from django.db import transaction
from rest_framework.generics import get_object_or_404

from chargecenter.transactions.models import BalanceTransaction, Transaction
from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.transactions.serializers import TransactionOutputSerializer, IncreaseBalanceSerializer, \
    ConfirmBalanceTransactionSerializer
from chargecenter.users.models import BaseUser
from chargecenter.users.services import update_salesperson_balance


@transaction.atomic
def create_balance_transaction(user: BaseUser, data: dict):
    serializer = IncreaseBalanceSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    salesperson = user.salesperson
    transaction_obj = create_transaction(salesperson=salesperson, amount=serializer.validated_data.get("amount"),
                                         is_charge=False)
    create_balance(transaction=transaction_obj)
    return TransactionOutputSerializer(instance=transaction_obj, context={"full_access": False}).data


@transaction.atomic
def confirm_balance_transaction(admin: BaseUser, data: dict):
    serializer = ConfirmBalanceTransactionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    balance_transaction = get_object_or_404(BalanceTransaction, id=serializer.validated_data.get("balance"))
    balance_transaction.is_confirmed = True
    balance_transaction.confirmed_by = admin
    balance_transaction.save()
    transaction_obj = balance_transaction.transaction_obj
    transaction_obj.status = Transaction.DONE
    update_salesperson_balance(salesperson=transaction_obj.salesperson, amount=transaction_obj.amount)
    transaction_obj.save()
