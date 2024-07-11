from rest_framework import serializers

from chargecenter.transactions.models import Transaction
from chargecenter.transactions.serializers import BalanceTransactionPrivateSerializer, \
    BalanceTransactionPublicSerializer


class TransactionOutputSerializer(serializers.ModelSerializer):
    concrete_obj = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def get_concrete_obj(self):
        if self.instance.is_charge:
            pass
        else:
            if self.context.get("full_access"):
                return BalanceTransactionPrivateSerializer(instance=self.instance.concrete_balance_obj)
            else:
                return BalanceTransactionPublicSerializer(instance=self.instance.concrete_balance_obj)

