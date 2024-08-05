import json
import logging

from jwcrypto.common import JWException
from requests import HTTPError, JSONDecodeError
from rest_framework import exceptions, response, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from camac.token_exchange.keycloak import KeycloakClient
from camac.token_exchange.utils import build_username, extract_jwt_data

logger = logging.getLogger(__name__)


class TokenExchangeView(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        jwt_token = request.data.get("jwt-token")

        if not jwt_token:
            raise exceptions.AuthenticationFailed("JWT token must be passed")

        try:
            jwt_data = extract_jwt_data(jwt_token)
            username = build_username(jwt_data)

            keycloak_client = KeycloakClient()
            keycloak_client.update_or_create_user(username, jwt_data)

            token = keycloak_client.token_exchange(username)
        except HTTPError as e:
            try:
                result = e.response.json()
                message = result.get("errorMessage", json.dumps(result))
            except JSONDecodeError:  # pragma: no cover
                message = e.response.text
            logger.error(message)
            raise exceptions.AuthenticationFailed("Token could not be exchanged")
        except JWException as e:
            logger.error(e)
            raise exceptions.AuthenticationFailed("Invalid token")

        return response.Response(
            token,
            status=status.HTTP_200_OK,
        )
