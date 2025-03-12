from rest_framework import permissions

from camac.user import permissions as user_permissions

HasEebaPermission = (
    user_permissions.IsApplication("kt_gr") & permissions.IsAuthenticated
)


HasEebaSharedSecretPermission = (
    HasEebaPermission
    & user_permissions.ReadOnly
    & user_permissions.HasSharedSecret(
        settings_key="EEBA_SHARED_SECRET", shared_secret_header="X-EBAU-EEBA-SECRET"
    )
)
