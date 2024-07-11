from rest_framework import serializers


class IncreaseBalanceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
