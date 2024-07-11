from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.authentication.permissions import IsSalesPerson
from chargecenter.transactions.serializers import IncreaseBalanceSerializer
from chargecenter.transactions.services import create_balance_transaction


class CreateBalanceTransaction(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSalesPerson]
    }

    @extend_schema(tags=['transactions'], request=IncreaseBalanceSerializer)
    def post(self, request):
        admin_data = create_balance_transaction(user=request.user, data=request.data)
        return Response(admin_data, status=status.HTTP_201_CREATED)
