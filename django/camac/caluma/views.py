from collections import namedtuple

from caluma.caluma_user.views import AuthenticationGraphQLView

from camac.caluma.api import CamacRequest


class CamacAuthenticatedGraphQLView(AuthenticationGraphQLView):
    def get_user(self, request, *args, **kwargs):
        oidc_user = super().get_user(request, *args, **kwargs)

        request.camac_user = None
        if oidc_user is not None:
            request.user = oidc_user

            Info = namedtuple("Info", "context")
            fake_info = Info(context=request)

            camac_request = CamacRequest(fake_info).request

            oidc_user.group = camac_request.group.service_id
            request.camac_user = camac_request.user
            request.user = oidc_user

        return oidc_user
