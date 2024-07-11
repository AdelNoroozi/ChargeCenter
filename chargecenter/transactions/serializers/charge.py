from rest_framework import serializers


class CreateChargeSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    phone_number = serializers.UUIDField()
