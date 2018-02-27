from functools import wraps

from django.conf import settings
from rest_framework import permissions

from camac.request import get_request


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

    Decorator inspired by
    https://github.com/computer-lab/django-rest-framework-roles
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # on view request is directly on instance
        request = get_request(self)
        role = request.group.role
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


class ViewPermissions(permissions.BasePermission):
    """
    Check permissions based on methods defined on view.

    Lookup method name is `has_<action>_permission(self)` resp.
    `has_<action>_object_permission(self, obj)`.

    When no method can be found `True` will be returned.

    For simplicity action partial_update is mapped to update.

    Permission class inspired by
    https://github.com/dbkaplan/dry-rest-permissions
    """

    def has_permission(self, request, view):
        action = self._get_action(view)
        if action:
            method = "has_{action}_permission".format(action=action)
            if hasattr(view, method):
                return getattr(view, method)()

        return True

    def has_object_permission(self, request, view, obj):
        action = self._get_action(view)
        if action:
            method = "has_object_{action}_permission".format(action=action)
            if hasattr(view, method):
                return getattr(view, method)(obj)

        return True

    def _get_action(self, view):
        action = getattr(view, 'action', None)
        if action == 'partial_update':
            action = 'update'

        return action
