from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from chargecenter.users.models import BaseUser
from chargecenter.users.validators import number_validator, letter_validator, special_char_validator


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    bio = serializers.CharField(max_length=1000, required=False)
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )
    confirm_password = serializers.CharField(max_length=255)

    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email Already Taken")
        return email

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")
        return data


class RegisterOutputSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = BaseUser
        fields = ("email", "token", "created_at", "updated_at")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

