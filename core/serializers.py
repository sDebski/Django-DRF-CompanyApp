from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as DRFAuthTokenSerializer


class AuthTokenSerializer(DRFAuthTokenSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs