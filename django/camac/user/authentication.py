import hashlib
import logging
import re

from caluma.caluma_user import models as caluma_user_models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import translation
from django.utils.encoding import force_bytes, smart_text
from django.utils.translation import ugettext as _
from jose.exceptions import ExpiredSignatureError, JOSEError
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from camac.applicants.models import Applicant
from camac.user.models import Group, UserGroup
from camac.instance.models import Instance
from camac.core.models import InstancePortal

request_logger = logging.getLogger("django.request")


class CalumaInfo:
    """A caluma info object built from the given camac request.

    Caluma requires an "info" object in various places, representing
    the GraphQL request, user, etc; similar to the context in
    DRF views.

    This info object is limited and only contains what's actually needed.
    It may need to be expanded in the future.
    """

    def __init__(self, userinfo, token=None):
        self.context = CalumaInfo._Context(userinfo, token)

    class _Context:
        def __init__(self, userinfo, token):
            self.user = caluma_user_models.OIDCUser(token=token, userinfo=userinfo)


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
            lambda: self._verify_token(jwt_value),
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )
        # attach caluma info to request, as it's possible to do in middleware
        # (requires token info)
        request.caluma_info = CalumaInfo(userinfo[1], jwt_value)

        return userinfo

    def _verify_token(self, jwt_value):  # noqa: C901
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

        try:
            resp = keycloak.userinfo(jwt_value.decode())
        except KeycloakAuthenticationError:  # pragma: no cover
            msg = _("User session not found or doesn't have client attached on it")
            raise AuthenticationFailed(msg)

        # TODO: don't use jwt token at all, once Middleware is refactored
        return self._build_user(resp), jwt_decoded

    def _build_user(self, data):
        language = translation.get_language()

        # always overwrite values of users
        username = data["sub"]
        defaults = {
            "language": language[:2],
            "email": data["email"],
            "username": username,
            "name": data.get("family_name", username),
            "surname": data.get("given_name", username)
        }


        # By default we check if a user with certain username exists
        lookup_attr = {
            "username": username
        }

        # Map a user to an existing camac user through their email address.
        if settings.OIDC_BOOTSTRAP_BY_EMAIL:
            lookup_attr = {
                "email": defaults["email"]
            }

        user, created = get_user_model().objects.update_or_create(
            **lookup_attr, defaults=defaults
        )

        demo_groups = settings.APPLICATION.get("DEMO_MODE_GROUPS")
        if created:

            if is_uri_portal_user(username):
                migrate_portal_instances(user)

            Applicant.objects.filter(email=user.email, invitee=None).update(
                invitee=user
            )
            if settings.DEMO_MODE and demo_groups:
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

        return user

    def authenticate_header(self, request):
        return 'JWT realm="{0}"'.format(settings.KEYCLOAK_REALM)


def is_uri_portal_user(username):
    """Check if username is valid i-web portal user identifier."""
    return re.match("^d12_\d+$", username) 


@transaction.atomic
def migrate_portal_instances(user):
    """Assign instance to portal user on first login.

    In Uri instances which are submitted through the portal are all owned by a
    single portal user. The mapping of which user created which instance is stored
    in the "INSTANCE_PORTAL" table.
    
    If a portal user signs in for the first time he automatically becomes owner
    of his submitted instances.
    """
    portal_instances = InstancePortal.objects.filter(portal_identifier=user.username)
    portal_instance_ids = [instance.pk for instance in portal_instances]
    instances = Instance.objects.filter(pk__in=portal_instance_ids).update(user=user)
    portal_instances.update(migrated=True)
