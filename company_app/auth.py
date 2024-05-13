from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings


class TokenAuthentication(KnoxTokenAuthentication):
    def validate_user(self, auth_token):
        if not auth_token.user.is_active or auth_token.user.is_deleted:
            raise AuthenticationFailed(_("User inactive or deleted"))
        return auth_token.user, auth_token


class XApiKeyAuthentication(BaseAuthentication):
    api_header_key = "x-api-key"
    print("X-API-AUTH", settings.X_API_KEY)
    api_header_value = settings.X_API_KEY

    def authenticate_header(self, request):
        return self.api_header_key

    def authenticate(self, request):
        api_key = request.META.get(
            f'HTTP_{self.api_header_key.upper().replace("-", "_")}'
        )
        if api_key and self.api_header_value == api_key:
            return (None, None)
        raise AuthenticationFailed("Unauthorized")
