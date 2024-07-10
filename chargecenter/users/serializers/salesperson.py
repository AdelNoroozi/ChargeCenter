from rest_framework import serializers

from chargecenter.users.serializers.user import RegisterInputSerializer
from chargecenter.users.validators import name_validator


class SalesPersonInputSerializer(RegisterInputSerializer):
    first_name = serializers.CharField(max_length=256, validators=[name_validator])
    last_name = serializers.CharField(max_length=256, validators=[name_validator])
