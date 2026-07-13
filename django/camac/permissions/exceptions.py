from django.core import exceptions
from rest_framework.exceptions import ValidationError


class BasePermissionError(Exception):
    pass


class GrantRejected(BasePermissionError):
    pass


class GrantValidationError(GrantRejected, ValidationError):
    pass


class RevocationRejected(BasePermissionError, ValidationError):
    pass


class MissingEventHandler(exceptions.ImproperlyConfigured):
    pass
