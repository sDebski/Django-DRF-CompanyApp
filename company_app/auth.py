from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from rest_framework import exceptions

class TokenAuthentication(KnoxTokenAuthentication):
    def validate_user(self, auth_token):
        if not auth_token.user.is_active or auth_token.user.is_deleted:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted"))
        return auth_token.user, auth_token