from collections import namedtuple

from caluma.caluma_user.models import OIDCUser
from caluma.caluma_user.views import AuthenticationGraphQLView, HttpResponseUnauthorized
from graphene_django.views import HttpError

from camac.caluma.utils import CamacRequest, extend_user
from camac.user.models import User


class CamacAuthenticatedGraphQLView(AuthenticationGraphQLView):
    def get_user(self, request, *args, **kwargs):
        oidc_user = super().get_user(request, *args, **kwargs)

        if not isinstance(oidc_user, OIDCUser):
            # Raise a 401 error if the user is anything else than an OIDCUser
            # (e.g None, AnonymousUser)
            raise HttpError(HttpResponseUnauthorized())

        try:
            # Get the camac request containing the camac user and group
            request.user = oidc_user
            Info = namedtuple("Info", "context")
            camac_request = CamacRequest(Info(context=request)).request

            extend_user(oidc_user, camac_request)

            # Set the camac_user property on the caluma request
            request.camac_user = camac_request.user
        except User.DoesNotExist:
            # Raise a 401 error if the user was not found in the CAMAC database
            raise HttpError(HttpResponseUnauthorized())

        return oidc_user
