from django.core.validators import MinLengthValidator
from rest_framework import serializers

from chargecenter.users.models import BaseUser
from chargecenter.users.validators import number_validator, letter_validator, special_char_validator


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )

    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email Already Taken")
        return email

    def validate_username(self, username):
        if BaseUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("username Already Taken")
        return username

    class Meta:
        abstract = True


class AddAdminInputSerializer(RegisterInputSerializer):
    email = serializers.CharField(max_length=150, required=False)
