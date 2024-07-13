from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.api.pagination import FullPagination
from chargecenter.authentication.permissions import IsSalesPerson
from chargecenter.transactions.serializers import IncreaseBalanceSerializer, ConfirmBalanceTransactionSerializer, \
    ChargeInputSerializer
from chargecenter.transactions.services import create_balance_transaction, create_charge_transaction, get_transactions
from chargecenter.transactions.services.balance import confirm_balance_transaction


class CreateBalanceTransactionAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSalesPerson]
    }

    @extend_schema(tags=['transactions:balance'], request=IncreaseBalanceSerializer)
    def post(self, request):
        data = create_balance_transaction(user=request.user, data=request.data)
        return Response(data, status=status.HTTP_201_CREATED)


class ConfirmBalanceTransactionAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(tags=['transactions:balance'], request=ConfirmBalanceTransactionSerializer)
    def patch(self, request):
        confirm_balance_transaction(admin=request.user, data=request.data)
        return Response({"message": "done"}, status=status.HTTP_200_OK)


class CreateChargeTransactionAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSalesPerson]
    }

    @extend_schema(tags=['transactions:charge'], request=ChargeInputSerializer)
    def post(self, request):
        data = create_charge_transaction(user=request.user, data=request.data)
        return Response(data, status=status.HTTP_201_CREATED)


class TransactionsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated]
    }

    @extend_schema(tags=["transactions"])
    def get(self, request):
        query_dict = request.GET
        user = request.user
        if not user.is_admin and "concrete_balance_obj__confirmed_by" in query_dict:
            return Response({"error": "restricted request"}, status=status.HTTP_403_FORBIDDEN)
        data = get_transactions(user=user, query_dict=query_dict)
        paginator = FullPagination()
        paginated_data = paginator.paginate_queryset(queryset=data, request=request)
        return paginator.get_paginated_response(data={"ok": True, "data": paginated_data, "status": status.HTTP_200_OK})

