from collections import namedtuple
from logging import getLogger

from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_user.views import AuthenticationGraphQLView, HttpResponseUnauthorized
from django.conf import settings
from django.core.exceptions import (
    PermissionDenied as DjangoPermissionDenied,
    ValidationError as DjangoValidationError,
)
from django.http.response import HttpResponse
from graphene_django.views import HttpError
from graphql import GraphQLError
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    PermissionDenied,
)

from camac.caluma.utils import CamacRequest, extend_user
from camac.captcha.utils import validate_captcha_token
from camac.token_exchange.permissions import has_required_lot
from camac.user.authentication import build_camac_user
from camac.user.models import User
from camac.user.permissions import is_allowed_client

log = getLogger(__name__)


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
            self._attach_camac_request(request, oidc_user)
        except User.DoesNotExist:
            # The CAMAC user mirrors the keycloak user and is created lazily on
            # the first request.
            try:
                build_camac_user(
                    oidc_user.claims, request.headers.get("Accept-Language")
                )
                self._attach_camac_request(request, oidc_user)
            except (User.DoesNotExist, AuthenticationFailed) as e:
                # Raise a 401 error if the user could not be created or is
                # deactivated
                raise HttpError(HttpResponseUnauthorized()) from e

        if not has_required_lot(request.camac_request) or not is_allowed_client(
            request.camac_request
        ):
            raise HttpError(HttpResponseForbidden())

        return oidc_user

    def _attach_camac_request(self, request, oidc_user: OIDCUser) -> None:
        """Attach a fake, constructed camac request to the caluma request containing the camac user and group."""
        request.user = oidc_user
        Info = namedtuple("Info", "context")
        request.camac_request = CamacRequest(Info(context=request)).request

        extend_user(oidc_user, request.camac_request)

        # Set the camac_user property on the caluma request
        request.camac_user = request.camac_request.user

    def execute_graphql_request(self, request, *args, **kwargs):
        """Log GraphQL execution errors with their original traceback.

        `graphql-core` wraps every resolver exception into a `GraphQLError` and
        `graphene-django` only serializes its message, so unexpected errors
        would otherwise be returned as a bare message with an HTTP 200 and never
        show up in the logs.
        """
        result = super().execute_graphql_request(request, *args, **kwargs)
        errors = getattr(result, "errors", None)

        if settings.DEBUG and errors:
            for error in errors:
                while (
                    isinstance(error, GraphQLError) and error.original_error is not None
                ):
                    # Iterate over the original errors until we get to the root
                    # of the error
                    error = error.original_error

                if isinstance(
                    error,
                    (
                        GraphQLError,
                        APIException,
                        DjangoPermissionDenied,
                        DjangoValidationError,
                    ),
                ):
                    # Don't log anything for expected errors
                    continue

                log.exception(error, exc_info=error)

        return result
