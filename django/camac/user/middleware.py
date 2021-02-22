from django.utils.functional import SimpleLazyObject

from camac.user.utils import get_group


class GroupMiddleware(object):
    """Middleware to determine current group."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        request.group = SimpleLazyObject(lambda: get_group(request))

        response = self.get_response(request)
        return response
