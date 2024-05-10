from drf_spectacular.extensions import OpenApiAuthenticationExtension


class TokenAuthenticationSchema(OpenApiAuthenticationExtension):
    target_class = "company_app.auth.TokenAuthentication"
    name = "TokenAuthentication"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "header", "name": "Authorization"}

class XApiKeyAuthenticationSchema(OpenApiAuthenticationExtension):
    target_class = "company_app.auth.XApiKeyAuthentication"
    name = "XApiKeyAuthentication"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "header", "name": "X-Api-Key"}