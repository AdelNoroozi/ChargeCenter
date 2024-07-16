from django.db import transaction
from django.http import Http404

from chargecenter.transactions.models import BalanceTransaction, Transaction
from chargecenter.transactions.selectors import create_transaction, create_balance
from chargecenter.transactions.serializers import TransactionOutputSerializer, IncreaseBalanceSerializer, \
    ConfirmBalanceTransactionSerializer
from chargecenter.users.models import BaseUser, SalesPerson
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
    balance_transaction_qs = BalanceTransaction.objects.select_for_update().filter(
        id=serializer.validated_data.get("balance"), is_confirmed=False)
    if balance_transaction_qs.first() is None:
        raise Http404()
    else:
        balance_transaction = balance_transaction_qs.first()
    balance_transaction_qs.update(is_confirmed=True, confirmed_by=admin)
    transaction_obj = balance_transaction.transaction_obj
    transaction_obj.status = Transaction.DONE
    salesperson = SalesPerson.objects.select_for_update().get(id=transaction_obj.salesperson.id)
    update_salesperson_balance(salesperson=salesperson, amount=transaction_obj.amount)
    transaction_obj.save()
