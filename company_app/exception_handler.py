from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_handler


def get_error_codes(detail):
    codes = []
    if isinstance(detail, dict) and "code" in detail:
        codes.append(detail["code"])
    if isinstance(detail, dict) and "code" not in detail:
        for val in detail.values():
            codes.extend(get_error_codes(val))
    if isinstance(detail, list):
        for val in detail:
            codes.extend(get_error_codes(val))
    
    return codes


def exception_handler(exc, context):
    if isinstance(exc, APIException):
        detail = exc.get_full_details()
        exc.detail = {
            "errors": detail,
            "codes": get_error_codes(detail)
        }
    return drf_handler(exc, context)