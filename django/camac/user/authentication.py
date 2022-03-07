import hashlib
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils import translation
from django.utils.encoding import force_bytes, smart_str
from django.utils.translation import gettext as _
from jose.exceptions import ExpiredSignatureError, JOSEError
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from camac.applicants.models import Applicant
from camac.core.models import InstancePortal
from camac.instance.models import Instance
from camac.user.models import Group, UserGroup

request_logger = logging.getLogger("django.request")


class JSONWebTokenKeycloakAuthentication(BaseAuthentication):
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        header_prefix = "Bearer"

        if not auth or smart_str(auth[0].lower()) != header_prefix.lower():
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

        return cache.get_or_set(
            "authentication.userinfo.%s" % token_hash,
            lambda: self._verify_token(jwt_value),
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

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

    def _update_or_create_user(self, defaults):
        user_model = get_user_model()
        filter_condition = Q(username=defaults["username"])

        # If enabled we also consider the email address
        if settings.OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK and defaults["email"]:
            filter_condition |= Q(email=defaults["email"])

        existing_users = user_model.objects.filter(filter_condition)
        return existing_users.update_or_create(defaults=defaults)

    def _build_user(self, data):
        language = translation.get_language()

        # Different customers use different claims as their username
        username_claim = settings.OIDC_USERNAME_CLAIM

        # We used the keycloak user id as the username in camac
        username = data[username_claim]
        all_defaults = {
            "language": language[:2],
            "email": data.get("email"),
            "username": username,
            "name": data.get("family_name", username),
            "surname": data.get("given_name", username),
            "city": data.get("city", ""),
            "zip": data.get("zip", ""),
            "address": " ".join(
                filter(
                    None,
                    [
                        data.get("street"),
                        data.get("streetNumber"),
                        data.get("addressSupplement"),
                    ],
                )
            ),
            "phone": ", ".join(
                filter(
                    None,
                    [
                        data.get("phoneWork"),
                        data.get("phonePrivate"),
                        data.get("phoneMobile"),
                    ],
                )
            ),
        }
        defaults = {
            key: all_defaults[key]
            for key in settings.APPLICATION.get("OIDC_SYNC_USER_ATTRIBUTES")
        }

        user, created = self._update_or_create_user(defaults)

        if created:
            if settings.URI_MIGRATE_PORTAL_USER and "portalid" in data:
                migrate_portal_user(data.get("portalid"), user)

            Applicant.objects.filter(email=user.email, invitee=None).update(
                invitee=user
            )

            demo_groups = settings.APPLICATION.get("DEMO_MODE_GROUPS")
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


@transaction.atomic
def migrate_portal_user(portal_identifier, user):
    """Assign instance to portal user on first login.

    In Uri instances which are submitted through the portal are all owned by a
    single portal user. The mapping of which user created which instance is stored
    in the "INSTANCE_PORTAL" table.

    If a portal user signs in for the first time through keycloak he
    automatically becomes owner of his submitted instances. He also gets added
    to the applicant user group.
    """

    portal_instances = InstancePortal.objects.filter(
        portal_identifier=portal_identifier
    )
    portal_instance_ids = portal_instances.values_list("instance_id")

    Instance.objects.filter(pk__in=portal_instance_ids).update(user=user)
    portal_instances.update(migrated=True)

    applicant_group_id = settings.APPLICATION["APPLICANT_GROUP_ID"]
    group = Group.objects.get(pk=applicant_group_id)
    UserGroup.objects.create(user=user, group=group, default_group=1)
