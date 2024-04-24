from django.contrib.auth.mixins import LoginRequiredMixin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

class SchemaView(LoginRequiredMixin, SpectacularAPIView):
    login_url = "/admin/login/"
    authentication_classes = []
    permission_classes = []

class SwaggerView(LoginRequiredMixin, SpectacularSwaggerView):
    login_url = "/admin/login/"
    authentication_classes = []
    permission_classes = []