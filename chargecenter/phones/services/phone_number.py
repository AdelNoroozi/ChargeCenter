from chargecenter.phones.selectors import get_phone_numbers as get_phone_numbers_selector
from chargecenter.phones.serializers import PhoneNumberOutputSerializer


def get_phone_numbers():
    phone_numbers = get_phone_numbers_selector()
    return PhoneNumberOutputSerializer(phone_numbers).data
