from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from core.models import PasswordHistory, User, SystemLog
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (
            "General",
            {
                "fields": [
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "last_login",
                    "date_joined",
                    "is_deleted",
                ]
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = ("pk", "username", "is_staff", "is_active", "is_deleted")
    search_fields = (
        "username",
        "email",
    )
    ordering = ("username",)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if request.user.is_superuser:
            return self.fieldsets
        else:
            return (
                (
                    "General",
                    {
                        "fields": (
                            "username",
                            "email",
                            "password",
                            "last_login",
                            "date_joined",
                            "is_deleted",
                        )
                    },
                ),
                (_("Permissions"), {"fields": ("is_active",)}),
            )


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "last_used_date", "password_hash")
    ordering = ("last_used_date",)
    last_filter = ("user",)


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    search_fields = ("username",)
    list_per_page = 20
