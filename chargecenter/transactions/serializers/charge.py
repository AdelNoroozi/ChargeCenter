from rest_framework import serializers

from chargecenter.transactions.models import ChargeTransaction


class ChargeInputSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    phone_number = serializers.UUIDField()


class ChargeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeTransaction
        exclude = ("transaction_obj",)
