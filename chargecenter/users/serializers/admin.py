from rest_framework import serializers

from chargecenter.users.serializers.user import UserInputSerializer


class AdminInputSerializer(UserInputSerializer):
    email = serializers.CharField(max_length=150, required=False)