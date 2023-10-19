from functools import wraps

from django.conf import settings
from rest_framework import permissions

from camac.request import get_request


def get_group(obj):
    return get_request(obj).group


def is_public_access(request):
    header = request.META.get("HTTP_X_CAMAC_PUBLIC_ACCESS")
    return header in ["true", True]


def permission_aware(func):
    """
    Decorate view methods to be permission aware.

    Instead of decorated method permission aware method is called.
    Usually a for_permission is added to method name whereas
    permission is defined by reading `ROLE_PERMISSIONS` of current
    application and model.

    Example, `get_queryset` method is called and the permission is determined
    to be `canton` decorator will first try to call
    `get_queryset_for_canton` and only if not existent will call
    `get_queryset` as fallback.

    For unauthenticated users (which don't have a group or role as an
    effect), an implicit role named "public" is assumed, resulting in the
    suffix `_for_public`, eg. `get_queryset_for_public`.
    This function should return an empty queryset for non-configured projects.

    Be aware, that the fallback is still the base function, as a generic
    handling is not feasible (or would need to happen at the init stage, not
    during runtime). It's the responsibility of the developer that opens up the
    permission (removes IsAuthenticated, etc.) to ensure a _for_public handler
    is provided.

    Decorator inspired by
    https://github.com/computer-lab/django-rest-framework-roles
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # on view request is directly on instance
        group = kwargs.get("group") or get_group(self)
        permission_func = get_permission_func(self, func.__name__, group)
        if permission_func:
            return permission_func(*args, **kwargs)

        if not bool(group) and permission_func is None:  # pragma: no cover
            try:
                return self.queryset.none()
            except AttributeError:
                raise RuntimeError(
                    f"Bad configuration: Anonymous User accessing unguarded method `{func.__name__}`, "
                    f"should be handled by a `{func.__name__}_for_public` method."
                )

        return func(self, *args, **kwargs)

    return wrapper


def get_role_name(group):
    perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
    return perms.get(group.role.name) if group else "public"


def get_permission_func(cls, name, group):
    if getattr(cls, "swagger_fake_view", False):
        return None

    perm = get_role_name(group)

    if perm:
        perm_func = f"{name}_for_{perm}"
        if hasattr(cls, perm_func):
            return getattr(cls, perm_func)
        parent = settings.APPLICATION.get("ROLE_INHERITANCE", {}).get(perm)
        parent_perm_func = f"{name}_for_{parent}"
        if parent and hasattr(cls, parent_perm_func):
            return getattr(cls, parent_perm_func)

    return None


class IsGroupMember(permissions.BasePermission):
    """Verify that user is in a valid group.

    This will prevent access from users in the publication. "Normal" applicants
    have an automatically assigned group and won't be affected by this.
    """

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
        action = getattr(view, "action", None)
        if action == "partial_update":
            action = "update"

        return action


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsPublicAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_public_access(request)

    def has_object_permission(self, request, view, obj):
        return is_public_access(request)


DefaultPermission = (
    # identical to DEFAULT_PERMISSION_CLASSES
    permissions.IsAuthenticated
    & IsGroupMember
    & ViewPermissions
)


def IsApplication(*applications):
    class DynamicPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return settings.APPLICATION_NAME in applications

        def has_object_permission(self, request, view, obj):
            return settings.APPLICATION_NAME in applications

    return DynamicPermission


def IsView(*views):
    class DynamicPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return view.__class__.__name__ in views

        def has_object_permission(self, request, view, obj):
            return view.__class__.__name__ in views

    return DynamicPermission


PublicationBE = IsApplication("kt_bern") & permissions.IsAuthenticated & ReadOnly
PublicationSZ = IsApplication("kt_schwyz") & permissions.IsAuthenticated & ReadOnly
PublicationGR = IsApplication("kt_gr") & permissions.IsAuthenticated & ReadOnly
PublicationUR = IsApplication("kt_uri") & ReadOnly
PublicationSO = IsApplication("kt_so") & ReadOnly
PublicationTest = IsApplication("test") & ReadOnly

# If the application is not explicitly configured here, we don't allow any public access
PublicationPermission = IsPublicAccess & (
    (
        # Public caluma instances
        IsView("PublicCalumaInstanceView")
        & (
            PublicationBE
            | PublicationSZ
            | PublicationGR
            | PublicationUR
            | PublicationSO
            | PublicationTest
        )
    )
    | (
        # Documents
        IsView("AttachmentView", "AttachmentDownloadView")
        & (PublicationBE | PublicationSZ | PublicationUR | PublicationTest)
    )
    | (
        # Alexandria
        IsView("DocumentViewSet", "FileViewSet")
        & (PublicationGR | PublicationSO | PublicationTest)
    )
    | (
        # Form fields
        IsView("FormConfigDownloadView", "FormFieldView")
        & (PublicationSZ | PublicationTest)
    )
)
