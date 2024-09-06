from django.conf import settings
from jwt import decode
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission


def get_lot(request):
    try:
        _, token = get_authorization_header(request).split()
        token_data = decode(token, options={"verify_signature": False})

        return int(token_data["lot"])
    except (ValueError, KeyError):
        return None


def has_required_lot(request):
    if not settings.ENABLE_TOKEN_EXCHANGE:
        return True

    from camac.user.permissions import get_role_name

    lot = get_lot(request)
    role = get_role_name(request.group)

    if role not in settings.TOKEN_EXCHANGE_LOT_MAPPING:
        return True

    if lot is None:
        return False

    return lot >= settings.TOKEN_EXCHANGE_LOT_MAPPING[role]


class RequireLoT(BasePermission):
    def has_permission(self, request, view):
        return has_required_lot(request)
