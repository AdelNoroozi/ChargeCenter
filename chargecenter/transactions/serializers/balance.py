from rest_framework import serializers

from chargecenter.transactions.models import BalanceTransaction


class IncreaseBalanceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class BalanceTransactionPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceTransaction
        exclude = ("transaction_obj",)


class BalanceTransactionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceTransaction
        exclude = ("transaction_obj", "confirmed_by")
