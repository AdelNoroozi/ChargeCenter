from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.permissions import IsSuperUser

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.authentication.permissions import IsSalesPerson
from chargecenter.users.serializers import AdminInputSerializer, SalesPersonInputSerializer, SalesPersonOutputSerializer
from chargecenter.users.serializers.user import UserOutputSerializer
from chargecenter.users.services import create_admin, create_salesperson, get_salesperson


class CreateAdminAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSuperUser]
    }

    @extend_schema(tags=['Users:Admins'], request=AdminInputSerializer, responses={201: UserOutputSerializer})
    def post(self, request):
        admin_data = create_admin(data=request.data)
        return Response(admin_data, status=status.HTTP_201_CREATED)


class CreateSalesPersonAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsAdminUser]
    }

    @extend_schema(tags=['Users:SalesPeople'], request=SalesPersonInputSerializer,
                   responses={201: SalesPersonOutputSerializer})
    def post(self, request):
        salesperson_data = create_salesperson(data=request.data)
        return Response(salesperson_data, status=status.HTTP_201_CREATED)


class GetSalesPersonInfoAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsSalesPerson]
    }

    @extend_schema(tags=['Users:SalesPeople'], responses={200: SalesPersonOutputSerializer})
    def get(self, request):
        salesperson_data = get_salesperson(user=request.user)
        return Response(salesperson_data, status=status.HTTP_200_OK)
