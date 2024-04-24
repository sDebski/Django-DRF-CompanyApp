from django.contrib.admin.apps import AdminConfig


class CompanyAppAdminConfig(AdminConfig):
    def ready(self) -> None:
        super().ready()
        from . import spectacular_schema  # noqa