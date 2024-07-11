from django.db import transaction

from chargecenter.users.models import BaseUser
from chargecenter.users.selectors import create_salesperson as create_salesperson_selector
from chargecenter.users.serializers import SalesPersonInputSerializer, SalesPersonOutputSerializer


@transaction.atomic
def create_salesperson(data: dict):
    serializer = SalesPersonInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user_obj = BaseUser.objects.create_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    salesperson = create_salesperson_selector(user=user_obj, first_name=data.pop("first_name"),
                                              last_name=data.pop("last_name"))
    return SalesPersonOutputSerializer(instance=salesperson).data
