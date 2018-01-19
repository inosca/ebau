from functools import wraps

from django.conf import settings
from rest_framework import permissions


def permission_aware(func):
    """
    Decorate view methods to be permission aware.

    Instead of decorated method permission aware method is called.
    Usually a for_permission is added to method name whereas
    permission is defined by reading `ROLE_PERMISSIONS` of current
    application and model.


    Example, `get_queryset` method is called and the permission is determined
    to be `applicant` decorator will first try to call
    `get_queryset_for_applicant` and only if not existent will call
    `get_queryset` as fallback.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        role = self.request.group.role
        perms = settings.APPLICATION.get('ROLE_PERMISSIONS', {})
        perm = perms.get(role.name)
        if perm:
            perm_func = "{0}_for_{1}".format(func.__name__, perm)
            if hasattr(self, perm_func):
                return getattr(self, perm_func)(*args, **kwargs)

        return func(self, *args, **kwargs)

    return wrapper


class IsGroupMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.group)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
