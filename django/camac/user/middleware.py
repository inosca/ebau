from django.utils.functional import SimpleLazyObject

from . import models


def get_group(request):
    """
    Get group based on request.

    When a query param `group` is set group will be set on request in case
    user is member of this group; otherwise `None`.
    If no query param is passed on default group of user will be returned
    if any is set.
    """
    group_id = request.GET.get('group')
    if group_id:
        group = request.user.groups.filter(pk=group_id).select_related(
            'role', 'service').first()
    else:
        # no specific group is definied, default group of client is used
        # it is allowed that user may not be in this group
        client = request.auth['aud']
        group = models.Group.objects.filter(
            name=client.title()).select_related('role', 'service').first()

        # fallback, default group of user
        if group is None:
            group_qs = models.UserGroup.objects.filter(
                user=request.user, default_group=1)
            group_qs = group_qs.select_related('group', 'group__role',
                                               'group__service')
            user_group = group_qs.first()
            group = user_group and user_group.group

    return group


class GroupMiddleware(object):
    """Middleware to determine current group."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.group = SimpleLazyObject(lambda: get_group(request))

        response = self.get_response(request)
        return response
