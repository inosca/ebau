from django.conf import settings
from jwt import decode
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission


def get_token_data(request):
    try:
        _, token = get_authorization_header(request).split()
        return decode(token, options={"verify_signature": False})
    except ValueError:
        return {}


def get_lot(request):
    lot = get_token_data(request).get("lot")

    if lot is None:
        return None

    return int(lot)


def is_exchanged_token(request):
    return settings.TOKEN_EXCHANGE_SCOPE in get_token_data(request).get("scope", "")


def has_required_lot(request):
    from camac.user.permissions import get_role_name

    if not settings.ENABLE_TOKEN_EXCHANGE or not is_exchanged_token(request):
        return True

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
