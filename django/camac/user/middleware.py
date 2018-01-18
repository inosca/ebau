from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import models


def get_user_jwt(request):
    """
    Get user based on authorization token.

    Replacement for django session auth get_user & auth.get_user for
    JSON Web Token authentication. Inspects the token for the user_id,
    attempts to get that user from the DB & assigns the user on the
    request object. Otherwise it defaults to AnonymousUser.
    This will work with existing decorators like LoginRequired, whereas
    the standard restframework_jwt auth only works at the view level
    forcing all authenticated users to appear as AnonymousUser ;)
    """
    user = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except Exception:  # pragma: no cover
        pass

    return user or AnonymousUser()


class JWTAuthenticationMiddleware(object):
    """Middleware for authenticating JSON Web Tokens in Authorize Header."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda : get_user_jwt(request))

        response = self.get_response(request)
        return response


def get_group(request):
    """
    Get group based on request.

    When a query param `group` is set group will be set on request in case
    user is member of this group; otherwise `None`.
    If no query param is passed on default group of user will be returned
    if any is set.
    """
    group_id = request.GET.get('group')
    if group_id is not None:
        group = models.Group.objects.filter(pk=group_id).first()
    else:
        group_qs = models.UserGroup.objects.filter(
            user=request.user, default_group=1)
        user_group = group_qs.first()
        group = user_group and user_group.group

    return group


class GroupMiddleware(object):
    """Middleware to determine current group."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.group = SimpleLazyObject(lambda : get_group(request))

        response = self.get_response(request)
        return response
