from django.db import transaction
from rest_framework.utils.serializer_helpers import ReturnDict

from chargecenter.users.models import BaseUser
from chargecenter.users.selectors.profile import create_profile
from chargecenter.users.serializers import RegisterInputSerializer, RegisterOutputSerializer


def create_user(email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


@transaction.atomic
def register(data: dict) -> ReturnDict:
    serializer = RegisterInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    if "bio" in data:
        bio = data.pop("bio")
    else:
        bio = ""
    data.pop("confirm_password")
    user = create_user(email=data.get("email"), password=data.get("password"))

    create_profile(user=user, bio=bio)

    return RegisterOutputSerializer(user).data
