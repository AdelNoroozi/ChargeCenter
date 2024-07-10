from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chargecenter.api.mixins import ApiAuthMixin, BasePermissionsMixin
from chargecenter.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileOutputSerializer
from chargecenter.users.services import register, get_profile


class ProfileApi(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated]
    }

    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request):
        profile_data = get_profile(user=request.user)
        return Response(profile_data, status=status.HTTP_200_OK)


class RegisterApi(APIView):

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        register_data = register(data=request.data)

        return Response(register_data, status=status.HTTP_201_CREATED)
