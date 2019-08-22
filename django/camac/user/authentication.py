import hashlib
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation
from django.utils.encoding import force_bytes, smart_text
from django.utils.translation import ugettext as _
from jose.exceptions import ExpiredSignatureError, JOSEError
from keycloak import KeycloakOpenID
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from camac.user.models import Group, UserGroup

request_logger = logging.getLogger("django.request")


class JSONWebTokenKeycloakAuthentication(BaseAuthentication):
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        header_prefix = "Bearer"

        if not auth or smart_text(auth[0].lower()) != header_prefix.lower():
            return None

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided")
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Credentials string should "
                "not contain spaces."
            )
            raise AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        # token might be too long for key so we use hash sum instead.
        token_hash = hashlib.sha1(force_bytes(jwt_value)).hexdigest()

        userinfo = cache.get_or_set(
            "authentication.userinfo.%s" % token_hash,
            lambda: self._decode_jwt(jwt_value),
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

        return userinfo

    def _decode_jwt(self, jwt_value):
        keycloak = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT,
            realm_name=settings.KEYCLOAK_REALM,
        )

        options = {"exp": True, "verify_aud": False, "verify_signature": True}
        try:
            jwt_decoded = keycloak.decode_token(
                jwt_value, keycloak.certs(), options=options
            )
        except ExpiredSignatureError:
            msg = _("Signature has expired.")
            raise AuthenticationFailed(msg)
        except JOSEError:
            msg = _("Invalid token.")
            raise AuthenticationFailed(msg)

        language = translation.get_language()

        # always overwrite values of users
        user, created = get_user_model().objects.update_or_create(
            username=jwt_decoded["sub"],
            defaults={
                "language": language[:2],
                "email": jwt_decoded["email"],
                "name": jwt_decoded["family_name"],
                "surname": jwt_decoded["given_name"],
            },
        )

        demo_groups = settings.APPLICATION.get("DEMO_MODE_GROUPS")
        if created and settings.DEMO_MODE and demo_groups:
            for i, group_id in enumerate(demo_groups):
                default_group = 1 if i == 0 else 0
                try:
                    group = Group.objects.get(pk=group_id)
                    UserGroup.objects.create(
                        user=user, group=group, default_group=default_group
                    )
                except ObjectDoesNotExist:
                    request_logger.error(
                        f"Got invalid DEMO_MODE_GROUP ID ({group_id}), skipping"
                    )

        if not user.is_active:
            msg = _("User is deactivated.")
            raise AuthenticationFailed(msg)

        return user, jwt_decoded

    def authenticate_header(self, request):
        return 'JWT realm="{0}"'.format(settings.KEYCLOAK_REALM)
