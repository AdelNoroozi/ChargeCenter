from django.db import transaction
from rest_framework.generics import get_object_or_404

from chargecenter.phones.models import PhoneNumber
from chargecenter.transactions.selectors import create_transaction, create_charge
from chargecenter.transactions.serializers import ChargeInputSerializer, TransactionOutputSerializer
from chargecenter.users.models import BaseUser, SalesPerson
from chargecenter.users.services import update_salesperson_balance


@transaction.atomic
def create_charge_transaction(user: BaseUser, data: dict):
    serializer = ChargeInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    salesperson = SalesPerson.objects.select_for_update().get(user=user)
    update_salesperson_balance(salesperson=salesperson, amount=-(serializer.validated_data.get("amount")))
    transaction_obj = create_transaction(salesperson=salesperson, amount=serializer.validated_data.get("amount"),
                                         is_charge=True)
    phone_number = get_object_or_404(PhoneNumber, id=serializer.validated_data.get("phone_number"))
    create_charge(transaction=transaction_obj, phone_number=phone_number.number)
    return TransactionOutputSerializer(instance=transaction_obj).data