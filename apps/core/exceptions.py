from rest_framework.exceptions import APIException


class UnauthorizedException(APIException):
    status_code = 401
    default_detail = "Unauthorized"


class ForbiddenException(APIException):
    status_code = 403
    default_detail = "Forbidden"
