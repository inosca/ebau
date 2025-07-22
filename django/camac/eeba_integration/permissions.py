from rest_framework import permissions

from camac.user import permissions as user_permissions

HasEebaPermission = (
    user_permissions.IsApplication("kt_gr") & permissions.IsAuthenticated
)


class HasEebaExportScope(permissions.BasePermission):
    def has_permission(self, request, view):
        scopes = request.auth.get("scope", "").split()
        return "eeba-export" in scopes


HasEebaExportPermission = (
    HasEebaPermission
    & user_permissions.ReadOnly
    & user_permissions.HasSharedSecret(
        settings_key="EEBA_SHARED_SECRET", shared_secret_header="X-EBAU-EEBA-SECRET"
    )
    & HasEebaExportScope
)
