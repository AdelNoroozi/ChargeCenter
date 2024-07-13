from chargecenter.phones.selectors import get_phone_numbers as get_phone_numbers_selector
from chargecenter.phones.serializers import PhoneNumberOutputSerializer, PhoneNumberInputSerializer


def get_phone_numbers():
    phone_numbers = get_phone_numbers_selector()
    return PhoneNumberOutputSerializer(phone_numbers, many=True).data


def create_phone_number(data: dict):
    serializer = PhoneNumberInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return PhoneNumberOutputSerializer(instance=serializer.instance).data
