from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.permissions import IsSuperUser

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.users.serializers import AdminInputSerializer, SalesPersonInputSerializer
from chargecenter.users.services import create_admin, create_salesperson


class CreateAdminAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSuperUser]
    }

    @extend_schema(tags=['Users:Admins'], request=AdminInputSerializer)
    def post(self, request):
        admin_data = create_admin(data=request.data)
        return Response(admin_data, status=status.HTTP_201_CREATED)


class CreateSalesPersonAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsAdminUser]
    }

    @extend_schema(tags=['Users:SalesPeople'], request=SalesPersonInputSerializer)
    def post(self, request):
        salesperson_data = create_salesperson(data=request.data)
        return Response(salesperson_data, status=status.HTTP_201_CREATED)
