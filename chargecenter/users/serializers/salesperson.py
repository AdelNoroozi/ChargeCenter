from rest_framework import serializers

from chargecenter.users.models import SalesPerson
from chargecenter.users.serializers.user import UserInputSerializer, UserOutputSerializer
from chargecenter.common.validators import name_validator


class SalesPersonInputSerializer(UserInputSerializer):
    first_name = serializers.CharField(max_length=256, validators=[name_validator])
    last_name = serializers.CharField(max_length=256, validators=[name_validator])


class SalesPersonOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(many=False)

    class Meta:
        model = SalesPerson
        fields = ("user", "first_name", "last_name")
