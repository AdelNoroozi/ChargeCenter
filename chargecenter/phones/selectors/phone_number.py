from chargecenter.phones.models import PhoneNumber


def get_phone_numbers():
    return PhoneNumber.objects.all()
