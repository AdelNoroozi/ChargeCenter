from rest_framework import serializers

from chargecenter.phones.models import PhoneNumber


class PhoneNumberInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ("name", "number")


class PhoneNumberOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = "__all__"
