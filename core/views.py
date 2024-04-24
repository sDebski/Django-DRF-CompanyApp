from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import AllowAny
from core import serializers
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, UpdateAPIView


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


class UserView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        print("request:", self.request)
        print("user:", self.request.user)
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return self.update(request, *args, **kwargs)
