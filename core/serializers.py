from rest_framework import serializers
from rest_framework.authtoken.serializers import (
    AuthTokenSerializer as DRFAuthTokenSerializer,
)
from core import models


class AuthTokenSerializer(DRFAuthTokenSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]

        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email": {"required": False, "allow_blank": True},
            "date_joined": {
                "read_only": True,
            },
        }
