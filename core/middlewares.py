from traceback import print_exc

from rest_framework.request import Request
from rest_framework.utils.encoders import JSONEncoder
from rest_framework.utils.json import dumps

from core.models import SystemLog


class SystemLogsMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        req = Request(request=request)
        response = self.get_response(request)
        if self.should_be_skipped(req):
            return response

        kwargs = {
            "method": req.method,
            "path": req.path,
            "full_path": req.build_absolute_uri(),
            "username": request.user.username if request.user else None,
            "status": response.status_code,
            "ip_address": request.META.get("REMOTE_ADDR"),
            "query_params": dict(req.query_params),
            "response_body": self.parse_response_body(req, response),
            "request_headers": self.parse_request_headers(req),
            "response_headers": dict(response.headers),
        }


        try:
            SystemLog.objects.create(**kwargs)
        except Exception:
            print_exc()

        return response

    def parse_request_headers(self, request):
        heads = dict(request.headers)
        for key in heads.copy():
            if "auth" in key.lower():
                del heads[key]
        return heads

    def parse_response_body(self, request, response):
        if request.method == "GET" and response.status_code == 200:
            return {}
        try:
            body = response.data
        except AttributeError:
            body = {}
        if not body:
            return {}
        if (
            self.is_endpoint_auth(request)
            and isinstance(body, dict)
            and "token" in "body"
        ):
            del body["token"]
        return dumps(body, cls=JSONEncoder)

    def is_endpoint_auth(self, request):
        if "login" in request.path:
            return True
        return False

    def should_be_skipped(self, request):
        if "static" in request.path:
            return True
        if request.method == "HEAD" and "health" in request.path:
            return True
        if request.method == "OPTIONS":
            return True
        return False
