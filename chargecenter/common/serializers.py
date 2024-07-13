from rest_framework import serializers


class PaginatedOutputSerializer(serializers.Serializer):
    class ResultsOutputSerializer(serializers.Serializer):
        ok = serializers.BooleanField()

    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)

    class Meta:
        abstract = True
