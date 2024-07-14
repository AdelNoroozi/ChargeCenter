import json

import requests
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.generics import get_object_or_404

from chargecenter.phones.models import PhoneNumber
from chargecenter.transactions.models import Transaction
from chargecenter.transactions.selectors import create_transaction, create_charge
from chargecenter.transactions.serializers import ChargeInputSerializer, TransactionOutputSerializer
from chargecenter.users.models import BaseUser, SalesPerson
from chargecenter.users.services import update_salesperson_balance


def request_for_charge(amount: int, phone_number: str):
    token_url = "http://mock_charge_flask:8822/apis/token/"
    charge_url = "http://mock_charge_flask:8822/apis/charge/"

    token_headers = {
        "Token": "ChArG3C3nT3Rt0k3n",
        "Token-Issuer": "1"
    }
    access_token = requests.post(token_url, headers=token_headers).json().get("access_token")

    charge_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    charge_data = {
        "amount": amount,
        "phone_number": phone_number
    }
    response = requests.post(charge_url, headers=charge_headers, json=charge_data)
    if response.status_code == 200:
        return True
    else:
        print(response.json())
        raise ValidationError("something went wrong")


@transaction.atomic
def create_charge_transaction(user: BaseUser, data: dict):
    serializer = ChargeInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    salesperson = SalesPerson.objects.select_for_update().get(user=user)
    update_salesperson_balance(salesperson=salesperson, amount=-(serializer.validated_data.get("amount")))
    transaction_obj = create_transaction(salesperson=salesperson, amount=serializer.validated_data.get("amount"),
                                         is_charge=True)
    phone_number = get_object_or_404(PhoneNumber, id=serializer.validated_data.get("phone_number"))
    charge = create_charge(transaction=transaction_obj, phone_number=phone_number.number)
    request_for_charge(amount=serializer.validated_data.get("amount"), phone_number=str(phone_number.number))
    charge.transaction_obj.status = Transaction.DONE
    charge.transaction_obj.save()
    return TransactionOutputSerializer(instance=transaction_obj).data
