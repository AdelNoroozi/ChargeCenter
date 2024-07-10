from chargecenter.users.models import BaseUser
from chargecenter.users.serializers import AdminInputSerializer


def create_admin(data: dict):
    serializer = AdminInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    BaseUser.objects.create_admin(username=data.get("username"), email=data.get("email"), password=data.get("password"))
