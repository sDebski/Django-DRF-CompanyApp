from django.shortcuts import render
from django.db import connection
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from core import serializers
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from django_rest_passwordreset.views import (
    ResetPasswordConfirm as DjangoResetPasswordConfirm,
)


class HealthCheckAuth(APIView):
    @staticmethod
    def head(request, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({}, status=200)
        except Exception as error:
            return Response({"error", error}, status=500)


class HealthCheck(HealthCheckAuth):
    permission_classes = [AllowAny]


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    @extend_schema(request=serializers.AuthTokenSerializer)
    def post(self, request, format=None):
        serializer = serializers.AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.auth_token_set.all().delete()
        request.user = user
        return super().post(request, format=None)


class UserView(RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return self.update(request, *args, **kwargs)


class ResetPasswordConfirmView(DjangoResetPasswordConfirm):
    serializer_class = serializers.PassAndConfirmTokenSerializer
