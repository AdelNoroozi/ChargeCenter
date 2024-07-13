from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.phones.services import get_phone_numbers


class PhoneNumbersAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated]
    }

    @extend_schema(
        tags=['Phone Numbers'], responses={200: ''}
    )
    def get(self, request):
        data = get_phone_numbers()
        return Response(data=data, status=status.HTTP_200_OK)
