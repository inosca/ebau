from collections import namedtuple

from caluma.caluma_user.models import OIDCUser
from caluma.caluma_user.views import AuthenticationGraphQLView, HttpResponseUnauthorized
from graphene_django.views import HttpError

from camac.caluma.api import CamacRequest


class CamacAuthenticatedGraphQLView(AuthenticationGraphQLView):
    def get_user(self, request, *args, **kwargs):
        oidc_user = super().get_user(request, *args, **kwargs)

        if not isinstance(oidc_user, OIDCUser):
            # Raise a 401 error if the user is anything else than an OIDCUser
            # (e.g None, AnonymousUser)
            raise HttpError(HttpResponseUnauthorized())

        # Get the camac request containing the camac user and group
        request.user = oidc_user
        Info = namedtuple("Info", "context")
        camac_request = CamacRequest(Info(context=request)).request

        # Patch the caluma user to have the right group (which is the
        # service in camac)
        if camac_request.group and camac_request.group.service_id:
            oidc_user.group = camac_request.group.service_id

        # Set the camac_user property on the caluma request
        request.camac_user = camac_request.user

        return oidc_user
