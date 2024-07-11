from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.authentication.permissions import IsSalesPerson
from chargecenter.transactions.serializers import IncreaseBalanceSerializer, ConfirmBalanceTransactionSerializer
from chargecenter.transactions.services import create_balance_transaction
from chargecenter.transactions.services.balance import confirm_balance_transaction


class CreateBalanceTransactionAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSalesPerson]
    }

    @extend_schema(tags=['transactions:balance'], request=IncreaseBalanceSerializer)
    def post(self, request):
        admin_data = create_balance_transaction(user=request.user, data=request.data)
        return Response(admin_data, status=status.HTTP_201_CREATED)


class ConfirmBalanceTransactionAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(tags=['transactions:balance'], request=ConfirmBalanceTransactionSerializer)
    def patch(self, request):
        confirm_balance_transaction(admin=request.user, data=request.data)
        return Response({"message": "done"}, status=status.HTTP_200_OK)
