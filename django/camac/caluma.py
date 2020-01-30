from base64 import urlsafe_b64encode
from hashlib import sha256

import requests
from caluma.caluma_form import models as caluma_form_models
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext as _
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from rest_framework import exceptions

APPLICANT_GROUP_ID = 6


class CalumaApi:
    """
    Class with methods to interact with the caluma apps.

    We try to not use caluma components (models, etc.) outside of this module.
    For some usecases this is too cumbersome (e.g. PDF generation).
    """

    def is_main_form(self, form_slug):
        forms = caluma_form_models.Form.objects.filter(
            slug=form_slug, **{"meta__is-main-form": True}
        )
        if not forms.count() == 1:  # pragma: no cover
            return False

        return True

    def get_form_name(self, instance):
        document = caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk},
            **{"form__meta__is-main-form": True},
        ).first()
        return document.form.name if document else None

    def get_document_by_form_slug(self, instance, form_slug: str):
        document = caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk}, form__slug=form_slug
        ).first()
        return document.pk if document else None

    def get_main_document(self, instance):
        document = caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk},
            **{"form__meta__is-main-form": True},
        ).first()
        return document.pk if document else None

    def get_ebau_number(self, instance):
        document = caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk}
        ).first()
        return document.meta.get("ebau-number", "-") if document else None

    def get_municipality(self, instance):
        caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk},
            **{"form__meta__is-main-form": True},
        ).first()

        answer = caluma_form_models.Answer.objects.filter(
            **{"document__meta__camac-instance-id": instance.pk},
            question__slug="gemeinde",
        ).first()

        return answer.value if answer else None

    def get_nfd_form_permissions(self, instance):
        permissions = set()

        try:
            nfd_document = caluma_form_models.Document.objects.get(
                **{"form_id": "nfd", "meta__camac-instance-id": instance.pk}
            )
            answers = caluma_form_models.Answer.objects.filter(
                question_id="nfd-tabelle-status", document__family=nfd_document.pk
            )
        except caluma_form_models.Document.DoesNotExist:
            return permissions

        if answers.exclude(value="nfd-tabelle-status-entwurf").exists():
            permissions.add("read")

        if answers.filter(value="nfd-tabelle-status-in-bearbeitung").exists():
            permissions.add("write")

        return permissions

    def create_document(self, form_slug, **kwargs):
        return caluma_form_models.Document.objects.create(form_id=form_slug, **kwargs)

    def update_or_create_answer(self, document_id, question_slug, value):
        return caluma_form_models.Answer.objects.update_or_create(
            document_id=document_id,
            question_id=question_slug,
            defaults={"value": value},
        )

    def set_submit_date(self, document_pk, submit_date):
        document = caluma_form_models.Document.objects.get(pk=document_pk)

        if "submit-date" in document.meta:  # pragma: no cover
            # instance was already submitted, this is probably a re-submit
            # after correction.
            return False

        new_meta = {
            **document.meta,
            # Caluma date is formatted yyyy-mm-dd so it can be sorted
            "submit-date": submit_date,
        }

        document.meta = new_meta
        document.save()
        return True

    def is_paper(self, instance):
        return caluma_form_models.Answer.objects.filter(
            **{
                "document__meta__camac-instance-id": instance.pk,
                "document__form__meta__is-main-form": True,
                "question_id": "papierdossier",
                "value": "papierdossier-ja",
            }
        ).exists()


class CalumaSession:
    """ContextManager for handling cached `requests.Session()`."""

    def __init__(self, token):
        if isinstance(token, str):
            token = token.encode()
        _hash = sha256(token)
        _id = urlsafe_b64encode(_hash.digest()).decode()
        self.key = f"caluma_session_{_id}"
        self.session = cache.get(self.key, requests.session())

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            cache.set(self.key, self.session, 7200)


class CalumaClient:
    def __init__(self, auth_token, group_id=None):
        self.auth_token = auth_token
        self.group_id = group_id

    def query_caluma(self, query, variables=None, add_headers=None):
        variables = variables if variables is not None else {}
        add_headers = add_headers if add_headers is not None else {}
        headers = {"authorization": self.auth_token}

        if self.group_id and self.group_id != APPLICANT_GROUP_ID:  # pragma: no cover
            headers["x-camac-group"] = str(self.group_id)

        headers.update(add_headers)

        with CalumaSession(self.auth_token) as session:
            response = session.post(
                settings.CALUMA_URL,
                json={"query": query, "variables": variables},
                headers=headers,
            )

        response.raise_for_status()
        result = response.json()
        if result.get("errors"):  # pragma: no cover
            raise exceptions.ValidationError(
                _("Error while querying caluma: %(errors)s")
                % {"errors": result.get("errors")}
            )

        return result


def get_admin_token():
    """
    If needed fetch a (new) token from the oidc provider.

    The threshold for fetching a new token is 1 minute before expiration.

    :return: dict
    """

    def get_new_token():
        client = BackendApplicationClient(client_id="camac-admin")
        oauth = OAuth2Session(client=client)
        return oauth.fetch_token(
            token_url=settings.KEYCLOAK_OIDC_TOKEN_URL,
            client_id="camac-admin",
            client_secret=settings.KEYCLOAK_CAMAC_ADMIN_CLIENT_SECRET,
        )

    auth_token = cache.get("camac-admin-auth-token")

    if auth_token is None:
        auth_token = get_new_token()
    else:
        expires = timezone.datetime.utcfromtimestamp(int(auth_token["expires_at"]))
        thresh = timezone.datetime.now() + timezone.timedelta(minutes=1)
        if expires <= thresh:
            auth_token = get_new_token()

    cache.set("camac-admin-auth-token", auth_token)

    return auth_token["access_token"]


def get_paper_settings(key=None):
    roles = settings.APPLICATION.get("PAPER", {}).get("ALLOWED_ROLES", {})
    service_groups = settings.APPLICATION.get("PAPER", {}).get(
        "ALLOWED_SERVICE_GROUPS", {}
    )

    if isinstance(key, str):
        key = key.upper()

    return {
        "ALLOWED_ROLES": roles.get(key, roles.get("DEFAULT", [])),
        "ALLOWED_SERVICE_GROUPS": service_groups.get(
            key, service_groups.get("DEFAULT", [])
        ),
    }
