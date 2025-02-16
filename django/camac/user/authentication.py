import functools
import hashlib
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.utils import translation
from django.utils.encoding import force_bytes, smart_str
from django.utils.translation import gettext as _
from jwcrypto.common import JWException
from jwcrypto.jwt import JWTExpired
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from camac.applicants.models import Applicant
from camac.core.models import InstancePortal
from camac.instance.models import Instance
from camac.permissions.events import Trigger
from camac.user.models import Group, UserGroup
from camac.utils import clean_join

request_logger = logging.getLogger("django.request")


class JSONWebTokenKeycloakAuthentication(BaseAuthentication):
    def __init__(self):
        self.keycloak = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT,
            realm_name=settings.KEYCLOAK_REALM,
            verify=settings.OIDC_VERIFY_SSL,
        )

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        header_prefix = "Bearer"

        if not auth or smart_str(auth[0].lower()) != header_prefix.lower():
            return None

        if len(auth) == 1:
            raise AuthenticationFailed(
                _("Invalid Authorization header. No credentials provided")
            )
        elif len(auth) > 2:
            raise AuthenticationFailed(
                _(
                    "Invalid Authorization header. Credentials string should "
                    "not contain spaces."
                )
            )

        return auth[1]

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        accept_language_header = request.headers.get("Accept-Language")
        if jwt_value is None:
            return None

        # token might be too long for key so we use hash sum instead.
        token_hash = hashlib.sha1(force_bytes(jwt_value)).hexdigest()

        return cache.get_or_set(
            "authentication.userinfo.%s" % token_hash,
            lambda: self._verify_token(jwt_value, accept_language_header),
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

    def _verify_token(self, jwt_value, accept_language_header):  # noqa: C901
        try:
            jwt_decoded = self.keycloak.decode_token(
                jwt_value.decode(), check_claims={"exp": None}
            )
        except JWTExpired:
            raise AuthenticationFailed(_("Signature has expired."))
        except JWException:
            raise AuthenticationFailed(_("Invalid token."))

        try:
            resp = self.keycloak.userinfo(jwt_value.decode())
        except KeycloakAuthenticationError:  # pragma: no cover
            raise AuthenticationFailed(
                _("User session not found or doesn't have client attached on it")
            )
        except KeycloakGetError as e:  # pragma: no cover
            request_logger.error(
                f"Error while fetching the userinfo endpoint of Keycloak: {str(e)}"
            )
            raise AuthenticationFailed(_("Error while fetching userinfo"))

        # TODO: don't use jwt token at all, once Middleware is refactored
        return self._build_user(resp, accept_language_header), jwt_decoded

    def _update_or_create_user(self, defaults, accept_language_header):
        user_model = get_user_model()
        filter_condition = Q(username=defaults["username"])

        # If enabled we also consider the email address
        if settings.OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK and defaults["email"]:
            filter_condition |= Q(email=defaults["email"])
        existing_users = user_model.objects.filter(filter_condition)
        if not accept_language_header and existing_users:
            defaults["language"] = existing_users[0].language
        return existing_users.update_or_create(defaults=defaults)

    def _build_user(self, data, accept_language_header):
        language = translation.get_language()

        # Different customers use different claims as their username
        username_claim = settings.OIDC_USERNAME_CLAIM

        # We used the keycloak user id as the username in camac
        username = data[username_claim]
        name_default = username

        if settings.ENABLE_TOKEN_EXCHANGE and username.startswith(
            settings.TOKEN_EXCHANGE_USERNAME_PREFIX
        ):
            # Token exchange users might have an empty value in either
            # given_name or family_name. If that is the case, the property must
            # remain empty as it's a company.
            name_default = ""

        all_defaults = {
            "language": language[:2],
            "email": data.get("email"),
            "username": username,
            "name": data.get("given_name", name_default),
            "surname": data.get("family_name", name_default),
            "city": data.get("city", ""),
            "zip": data.get("zip", ""),
            "address": clean_join(
                data.get("street"),
                data.get("streetNumber"),
                data.get("addressSupplement"),
            ),
            "phone": clean_join(
                data.get("phoneWork"),
                data.get("phonePrivate"),
                data.get("phoneMobile"),
                separator=", ",
            ),
        }
        if username.startswith("service-account-") and not data.get("email"):
            all_defaults["email"] = f"{username}@placeholder.org"

        defaults = {
            key: all_defaults[key]
            for key in settings.APPLICATION.get("OIDC_SYNC_USER_ATTRIBUTES")
        }

        user, created = self._update_or_create_user(defaults, accept_language_header)

        self._update_applicants(user)
        self._assign_demo_groups(user)

        if created:
            if settings.URI_MIGRATE_PORTAL_USER and "portalid" in data:
                migrate_portal_user(data.get("portalid"), user)

        if not user.is_active:
            msg = _("User is deactivated.")
            raise AuthenticationFailed(msg)
        return user

    def _assign_demo_groups(self, user):
        if not settings.DEMO_MODE:
            return

        group_ids = settings.APPLICATION.get("DEMO_MODE_GROUPS", [])

        for i, group_id in enumerate(group_ids):
            default_group = 1 if i == 0 else 0

            try:
                group = Group.objects.get(pk=group_id)
                UserGroup.objects.get_or_create(
                    user=user, group=group, defaults={"default_group": default_group}
                )
            except ObjectDoesNotExist:
                request_logger.error(
                    f"Got invalid DEMO_MODE_GROUP ID ({group_id}), skipping"
                )

    def _update_applicants(self, user):
        # If token exchange is enabled, this logic must only be executed if the
        # current user logged in via that method as all other users can't be
        # applicants.
        if settings.ENABLE_TOKEN_EXCHANGE and not user.username.startswith(
            settings.TOKEN_EXCHANGE_USERNAME_PREFIX
        ):
            return

        pending_applicants = Applicant.objects.filter(email=user.email, invitee=None)

        # Remove pending applicants that already have a connection to that user.
        # If we don't remove those, they will be updated in the next statement
        # which will cause an integrity error.
        pending_applicants.filter(
            Exists(
                Applicant.objects.filter(invitee=user, instance=OuterRef("instance"))
            )
        ).delete()

        for applicant in pending_applicants:
            applicant.invitee = user
            applicant.save()

            # no request, but can still trigger
            Trigger.applicant_added(None, applicant.instance, applicant)

    def authenticate_header(self, request):
        return 'JWT realm="{0}"'.format(settings.KEYCLOAK_REALM)


class DjangoAdminOIDCAuthenticationBackend(
    OIDCAuthenticationBackend
):  # pragma: no cover
    def get_userinfo_cached(self, access_token):
        return self.cached_request(self.get_userinfo, access_token, "auth.userinfo")

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.get_userinfo_cached(access_token)

        users = self.filter_users_by_claims(claims)

        user = users.get()
        self.update_user_from_claims(user, claims)

        return user

    def update_user_from_claims(self, user, claims):
        user.email = claims.get(settings.OIDC_EMAIL_CLAIM, "")
        user.first_name = claims.get(settings.OIDC_FIRSTNAME_CLAIM, "")
        user.last_name = claims.get(settings.OIDC_LASTNAME_CLAIM, "")
        user.save()

    def filter_users_by_claims(self, claims):
        username = self.get_username(claims)
        return self.UserModel.objects.filter(username__iexact=username)

    def cached_request(self, method, token, cache_prefix):
        token_hash = hashlib.sha256(force_bytes(token)).hexdigest()

        func = functools.partial(method, token, None, None)

        return cache.get_or_set(
            f"{cache_prefix}.{token_hash}",
            func,
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

    def get_username(self, claims):
        return claims[settings.OIDC_USERNAME_CLAIM]


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
