from rest_framework import serializers

from chargecenter.transactions.models import Transaction
from chargecenter.transactions.serializers import BalanceTransactionPrivateSerializer, \
    BalanceTransactionPublicSerializer


class TransactionOutputSerializer(serializers.ModelSerializer):
    concrete_obj = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def get_concrete_obj(self, obj):
        if obj.is_charge:
            pass
        else:
            if self.context.get("full_access"):
                return BalanceTransactionPrivateSerializer(instance=obj.concrete_balance_obj).data
            else:
                return BalanceTransactionPublicSerializer(instance=obj.concrete_balance_obj).data

