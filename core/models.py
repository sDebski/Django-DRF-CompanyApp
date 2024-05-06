from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from typing import Any
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username is not set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username: str | None) -> Any:
        kwargs = {self.model.USERNAME_FIELD: username, "is_deleted": False}
        return self.get(**kwargs)


class User(AbstractUser):
    first_name = models.CharField(_("first_name"), max_length=128, blank=True)
    last_name = models.CharField(_("last_name"), max_length=128, blank=True)
    email = models.EmailField(_("email_address"), unique=True)

    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def set_password(self, raw_password: str | None) -> None:
        if self.pk is not None:
            PasswordHistory.objects.create(password_hash=self.password, user=self)
        return super().set_password(raw_password)


class PasswordHistory(models.Model):
    password_hash = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_used_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "PasswordHistory"
        ordering = ["user", "-last_used_date"]

    def __str__(self) -> str:
        return self.password_hash


class SystemLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=256, null=True, blank=True)
    path = models.CharField(max_length=256, null=True, blank=True)
    full_path = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    ip_address = models.CharField(max_length=256, null=True, blank=True)
    query_params = models.JSONField(default=dict)
    request_body = models.JSONField(default=dict)
    response_body = models.JSONField(default=dict)
    request_headers = models.JSONField(default=dict)
    response_headers = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "SystemLog"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["path"]),
        ]
