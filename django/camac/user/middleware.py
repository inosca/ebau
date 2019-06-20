import logging

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from . import models

request_logger = logging.getLogger("django.request")


def get_group(request):
    """
    Get group based on request.

    When a query param `group` is set group will be set on request in case
    user is member of this group; otherwise `None`.
    If no query param is passed on default group of user will be returned
    if any is set.
    """
    group_id = request.GET.get("group")
    if group_id:
        group = (
            request.user.groups.filter(pk=group_id)
            .select_related("role", "service")
            .first()
        )
    else:
        # no specific group is definied, default group of client is used
        # it is allowed that user may not be in this group
        group = None
        if request.auth:
            client = request.auth["aud"]
            filters = {"name": client.title()}
            if settings.APPLICATION.get("IS_MULTILINGUAL", False):
                filters = {"trans__name": client.title(), "trans__language": "de"}
            group = (
                models.Group.objects.filter(**filters)
                .select_related("role", "service")
                .first()
            )

        # fallback, default group of user
        if group is None:
            group_qs = models.UserGroup.objects.filter(
                user=request.user, default_group=1
            )
            group_qs = group_qs.select_related("group", "group__role", "group__service")
            user_group = group_qs.first()
            group = user_group and user_group.group

    request_logger.debug(f"group: {group.get_name()}")
    return group


class GroupMiddleware(object):
    """Middleware to determine current group."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.group = SimpleLazyObject(lambda: get_group(request))

        response = self.get_response(request)
        return response
