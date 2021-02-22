from django.utils.functional import SimpleLazyObject

from camac.caluma.utils import CalumaInfo


class CalumaInfoMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # attach caluma info to request, as it's possible to do in middleware
        # (requires token info)
        request.caluma_info = SimpleLazyObject(lambda: CalumaInfo(request))

        response = self.get_response(request)
        return response
