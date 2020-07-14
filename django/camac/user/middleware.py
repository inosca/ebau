import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from . import models

request_logger = logging.getLogger("django.request")


def get_group(request):
    """
    Get group based on request.

    Group will be determined in following order:
    1. query param `group`
    2. request header `X-CAMAC-GROUP`
    3. default group of client using `aud` claim
    4. user's default group
    """
    group_id = request.GET.get("group", request.META.get("HTTP_X_CAMAC_GROUP"))

    if group_id:
        group = (
            request.user.groups.filter(pk=group_id)
            .select_related("role", "service")
            .first()
        )
    else:
        group = _get_group_for_portal(request)

        # fallback, default group of user
        if group is None:
            user = getattr(request, "user", None)
            if user is None or isinstance(user, AnonymousUser):
                user = models.User.objects.get(username="guest").pk
            group_qs = models.UserGroup.objects.filter(user=user, default_group=1)
            group_qs = group_qs.select_related("group", "group__role", "group__service")
            user_group = group_qs.first()
            group = user_group and user_group.group

    request_logger.debug(f"group: {group and group.get_name()}")
    return group


def _get_group_for_portal(request):
    """
    Get group for portal users.

    Users who log into the public-facing "portal" have no group assignment in
    CAMAC. Instead, identify them based on the OIDC client given in the token's
    "aud" (audience) claim, and programatically assign the correct group for
    them.
    """
    if not settings.APPLICATION.get("PORTAL_GROUP", None):
        return None

    if not getattr(request, "auth", False):
        return None

    portal_client = settings.KEYCLOAK_PORTAL_CLIENT
    if not portal_client:  # pragma: no cover
        return None

    clients = request.auth["aud"]
    if not isinstance(clients, list):
        clients = [clients]

    if portal_client not in clients:
        return None

    return models.Group.objects.select_related("role", "service").get(
        pk=settings.APPLICATION["PORTAL_GROUP"]
    )


class GroupMiddleware(object):
    """Middleware to determine current group."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.group = SimpleLazyObject(lambda: get_group(request))

        response = self.get_response(request)
        return response
