from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.phones.serializers import PhoneNumberInputSerializer
from chargecenter.phones.services import get_phone_numbers, create_phone_number


class PhoneNumbersAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "POST": [IsAdminUser]
    }

    @extend_schema(
        tags=['Phone Numbers'], responses={200: ''}
    )
    def get(self, request):
        data = get_phone_numbers(query_dict=request.GET)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Phone Numbers'], request=PhoneNumberInputSerializer
    )
    def post(self, request):
        data = create_phone_number(data=request.data)
        return Response(data=data, status=status.HTTP_201_CREATED)
