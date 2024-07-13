from rest_framework.generics import get_object_or_404

from chargecenter.phones.models import PhoneNumber
from chargecenter.phones.selectors import get_phone_numbers as get_phone_numbers_selector
from chargecenter.phones.serializers import PhoneNumberOutputSerializer, PhoneNumberInputSerializer


def get_phone_numbers(query_dict: dict):
    search_param = query_dict.get("search")
    phone_numbers = get_phone_numbers_selector(search_param=search_param)
    return PhoneNumberOutputSerializer(phone_numbers, many=True).data


def create_phone_number(data: dict):
    serializer = PhoneNumberInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return PhoneNumberOutputSerializer(instance=serializer.instance).data


def delete_phone_number(phone_number_id: str):
    phone_number = get_object_or_404(PhoneNumber, id=phone_number_id)
    phone_number.delete()
