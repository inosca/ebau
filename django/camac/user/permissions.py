from functools import wraps

from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from camac.request import get_request
from camac.token_exchange.permissions import RequireLoT


def get_group(obj):
    return get_request(obj).group


def is_public_access(request):
    header = request.META.get("HTTP_X_CAMAC_PUBLIC_ACCESS")
    return header in ["true", True]


def is_allowed_client(request):
    if not hasattr(request, "auth") or request.auth is None:  # pragma: no cover
        return False

    azp = request.auth.get("azp")

    return azp in settings.KEYCLOAK_ALLOWED_CLIENTS


def _get_view_action(view):
    action = getattr(view, "action", None)
    if action == "partial_update":
        action = "update"

    return action


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

    code = "missing_group"

    def has_permission(self, request, view):
        return bool(request.group)


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
        action = _get_view_action(view)
        if action:
            method = "has_{action}_permission".format(action=action)
            if hasattr(view, method):
                return getattr(view, method)()

        return True

    def has_object_permission(self, request, view, obj):
        action = _get_view_action(view)
        if action:
            method = "has_object_{action}_permission".format(action=action)
            if hasattr(view, method):
                return getattr(view, method)(obj)

        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsPublicAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_public_access(request)


class IsAllowedClientToken(permissions.BasePermission):
    """Verify that the token is authorized by a known client.

    This permission verifies that the `azp` (authorized party) of the passed
    token is a known client that is used by eBau (e.g. "portal" and "camac").

    There are exceptions where endpoints should allow external clients like the
    eCH-0211 API. To allow external clients on an endpoint, add
    `allow_external_client = True` on the respective view. To only allow certain
    actions on an endpoint, you can also define a list, e.g.
    `allow_external_clients = ["retreive", "list"]`.

    This permission should be used on every single endpoint of the application
    that requires authentication! To make sure of that, the snapshot
    `django/camac/tests/__snapshots__/test_external_client_access.ambr` contains
    a list of all endpoints that allow external clients per canton.
    """

    code = "unallowed_azp"

    def allow_external_clients(self, view):
        allow = getattr(view, "allow_external_clients", None)

        # Some endpoints implement an `include_in_swagger` method to define
        # whether the endpoint appears in the swagger docs or not. Since all
        # endpoints that are documented in the swagger should also be accessible
        # by external clients, we use that method as fallback to reduce
        # redundancy.
        if allow is None and hasattr(view, "include_in_swagger"):
            allow = view.include_in_swagger()

        # If `allow_external_clients` is a list of allowed actions, we check
        # whether it current action is contained
        if isinstance(allow, list):
            return _get_view_action(view) in allow

        return bool(allow)

    def has_permission(self, request, view):
        return self.allow_external_clients(view) or is_allowed_client(request)


DefaultPermission = (
    # identical to DEFAULT_PERMISSION_CLASSES
    permissions.IsAuthenticated
    & IsAllowedClientToken
    & IsGroupMember
    & ViewPermissions
    & RequireLoT
)


def IsApplication(*applications):
    class DynamicPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return settings.APPLICATION_NAME in applications

    return DynamicPermission


def HasSharedSecret(**kwargs):
    class DynamicPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            shared_secret_header = kwargs.get("shared_secret_header")
            shared_secret_settings_key = kwargs.get("settings_key")

            shared_secret = request.headers.get(shared_secret_header)
            expected_secret = settings.EEBA_INTEGRATION.get(shared_secret_settings_key)

            if shared_secret != expected_secret:
                raise PermissionDenied(
                    f"Invalid or missing {shared_secret_header} header."
                )
            return True

    return DynamicPermission


def IsView(*views):
    class DynamicPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            return view.__class__.__name__ in views

    return DynamicPermission


AuthenticatedPublication = permissions.IsAuthenticated & IsAllowedClientToken & ReadOnly

PublicationBE = IsApplication("kt_bern") & AuthenticatedPublication
PublicationSZ = IsApplication("kt_schwyz") & AuthenticatedPublication
PublicationGR = IsApplication("kt_gr") & AuthenticatedPublication
PublicationSO = IsApplication("kt_so") & AuthenticatedPublication & RequireLoT
PublicationAG = IsApplication("kt_ag") & AuthenticatedPublication
PublicationUR = IsApplication("kt_uri") & ReadOnly
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
            | PublicationAG
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
        IsView("PatchedDocumentViewSet", "PatchedFileViewSet", "PatchedMarkViewSet")
        & (PublicationGR | PublicationSO | PublicationAG | PublicationTest)
    )
    | (
        # Form fields
        IsView("FormConfigDownloadView", "FormFieldView")
        & (PublicationSZ | PublicationTest)
    )
    | (
        # Static content
        IsView("StaticContentView") & (PublicationSO | PublicationTest)
    )
    | (
        # Publication access count
        IsView("PublicCalumaInstanceView")
        # Same as PublicationSZ but without `ReadOnly`
        & (
            IsApplication("kt_schwyz")
            & permissions.IsAuthenticated
            & IsAllowedClientToken
        )
    )
)

HasEebaPermission = (
    IsApplication("kt_gr")
    & permissions.IsAuthenticated
    & ReadOnly
    & HasSharedSecret(
        settings_key="EEBA_SHARED_SECRET", shared_secret_header="X-EBAU-EEBA-SECRET"
    )
)


class IsWilkenClientToken(permissions.BasePermission):
    """Verify that the token is authorized by the configured wilken client."""

    code = "unallowed_azp"

    def has_permission(self, request, view):
        try:
            return (
                request.auth.get("azp", "") == settings.BILLING.wilken.keycloak_client
            )
        except AttributeError:
            return False
