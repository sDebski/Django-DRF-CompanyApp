from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("company/", include(("company.urls", "company"), namespace="company")),
    path("core/", include(("core.urls", "core"), namespace="core")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    from company_app.views import SwaggerView, SchemaView

    urlpatterns += [
        path("api/schema/", SchemaView.as_view(), name="schema"),
        path("swagger/", SwaggerView.as_view(url_name="schema"), name="swagger-ui")
    ]
