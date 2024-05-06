from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.serializers import (
    AuthTokenSerializer as DRFAuthTokenSerializer,
)
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from core import models, validators
from django.utils.translation import gettext_lazy as _


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
            "email",
            "date_joined",
            "last_login",
        ]

        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False, "allow_blank": True},
            "date_joined": {
                "read_only": True,
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirmation = serializers.CharField(required=True)

    def raise_error(self, reason: str = "default"):
        default = ("Failed to change Password", None)
        messages = {
            "default": default,
            "not_forced": ("Forbidden to change your password", "not-forced"),
            "invalid_old_password": (
                "Provided old password is invalid",
                "invalid-old-password",
            ),
            "invalid_confirmation": (
                "Confirmation and new password do not match",
                "nvalid-confirmation",
            ),
        }

        message, code = messages.get(reason, default)
        raise serializers.ValidationError(detail=message, code=code)

    def validate_old_password(self, value):
        user = self.instance
        if not user.check_password(value):
            self.raise_error("invalid_old_password")
        return value

    def validate(self, data):
        old_password = data.get("old_password", "")
        new_password = data.get("new_password", "")
        confirmation = data.get("confirmation", "")

        if old_password == new_password:
            self.raise_error()

        if new_password != confirmation:
            self.raise_error("invalid_confirmation")

        validate_password(new_password, self.instance)

        return data

    def update(self, instance, validated_data):
        new_password = validated_data["new_password"]
        instance.set_password(new_password)
        instance.save()
        return instance

    @property
    def data(self):
        return {
            "message": "Passoword changed successfully!",
            "user": UserSerializer(self.instance, read_only=True).data,
        }


class PassAndConfirmTokenSerializer(PasswordTokenSerializer):
    confirmation = serializers.CharField(
        label=_("Password confirmation"), style={"input_type": "password"}
    )

    def validate(self, data):
        password = data.get("password")
        confirmation = data.get("confirmation")

        if not password or not confirmation:
            message = "Fields 'Password' and 'Password Confirmation' are required"
            raise serializers.ValidationError(detail=message, code="required")
        if password != confirmation:
            message = "'Password' and 'Password confirmation' do not match"
            raise serializers.ValidationError(
                detail=message, code="invalid-confirmation"
            )
        return super().validate(data)
