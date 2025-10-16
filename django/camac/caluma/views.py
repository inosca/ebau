from collections import namedtuple

from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_user.views import AuthenticationGraphQLView, HttpResponseUnauthorized
from django.conf import settings
from django.http.response import HttpResponse
from graphene_django.views import HttpError
from rest_framework.exceptions import PermissionDenied

from camac.caluma.utils import CamacRequest, extend_user
from camac.captcha.utils import validate_captcha_token
from camac.token_exchange.permissions import has_required_lot
from camac.user.models import User
from camac.user.permissions import is_allowed_client


class HttpResponseForbidden(HttpResponse):
    status_code = PermissionDenied.status_code

    def __init__(self, *args, **kwargs):
        super().__init__(PermissionDenied.default_detail, *args, **kwargs)


class CamacAuthenticatedGraphQLView(AuthenticationGraphQLView):
    def get_user(self, request, *args, **kwargs):
        oidc_user = super().get_user(request, *args, **kwargs)

        if not isinstance(oidc_user, OIDCUser):
            if settings.APPLICATION.get("ENABLE_PUBLIC_CALUMA"):
                if settings.APPLICATION.get(
                    "ENABLE_PUBLIC_CALUMA_CAPTCHA"
                ) and not validate_captcha_token(request):
                    raise HttpError(HttpResponseForbidden())

                return AnonymousUser()
            else:
                # Raise a 401 error if the user is anything else than an OIDCUser
                # (e.g None, AnonymousUser)
                raise HttpError(HttpResponseUnauthorized())

        try:
            # Get the camac request containing the camac user and group
            request.user = oidc_user
            Info = namedtuple("Info", "context")
            request.camac_request = CamacRequest(Info(context=request)).request

            extend_user(oidc_user, request.camac_request)

            # Set the camac_user property on the caluma request
            request.camac_user = request.camac_request.user
        except User.DoesNotExist:
            # Raise a 401 error if the user was not found in the CAMAC database
            raise HttpError(HttpResponseUnauthorized())

        if not has_required_lot(request.camac_request) or not is_allowed_client(
            request.camac_request
        ):
            raise HttpError(HttpResponseForbidden())

        return oidc_user
