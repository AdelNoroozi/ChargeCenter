from chargecenter.users.models import BaseUser
from chargecenter.users.serializers import AdminInputSerializer
from chargecenter.users.serializers.user import RegisterOutputSerializer


def create_admin(data: dict):
    serializer = AdminInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    admin = BaseUser.objects.create_admin(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )
    return RegisterOutputSerializer(instance=admin)
