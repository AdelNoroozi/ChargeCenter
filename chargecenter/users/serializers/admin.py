from rest_framework import serializers

from chargecenter.users.serializers.user import RegisterInputSerializer


class AdminInputSerializer(RegisterInputSerializer):
    email = serializers.CharField(max_length=150, required=False)