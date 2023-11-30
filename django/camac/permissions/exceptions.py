from django.core import exceptions
from rest_framework.exceptions import ValidationError


class PermissionError(Exception):
    pass


class GrantRejected(PermissionError):
    pass


class GrantValidationError(GrantRejected, ValidationError):
    pass


class RevocationRejected(PermissionError, ValidationError):
    pass


class MissingEventHandler(exceptions.ImproperlyConfigured):
    pass
