from base64 import b64decode
from copy import copy
from json import loads

from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_user import models as caluma_user_models

from camac.user.middleware import get_group
from camac.user.models import User

APPLICANT_GROUP_ID = 6


class CalumaApi:
    """
    Class with methods to interact with the caluma apps.

    We try to not use caluma components (models, etc.) outside of this module.
    For some usecases this is too cumbersome
    (e.g. PDF generation, ech data_preparation).
    """

    def is_main_form(self, form_slug):
        forms = caluma_form_models.Form.objects.filter(
            slug=form_slug, **{"meta__is-main-form": True}
        )
        if not forms.count() == 1:  # pragma: no cover
            return False

        return True

    def _get_main_form(self, instance):
        document = caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk},
            **{"form__meta__is-main-form": True},
        ).first()
        return document.form if document else None

    def get_form_name(self, instance):
        form = self._get_main_form(instance)
        return form.name if form else None

    def get_form_slug(self, instance):
        form = self._get_main_form(instance)
        return form.slug if form else None

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
            **{"meta__camac-instance-id": instance.pk, "form__meta__is-main-form": True}
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
                question_id="nfd-tabelle-status", document__family=nfd_document
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


class CalumaInfo:
    """A caluma info object built from the given camac request.

    Caluma requires an "info" object in various places, representing
    the GraphQL request, user, etc; similar to the context in
    DRF views.

    This info object is limited and only contains what's actually needed.
    It may need to be expanded in the future.
    """

    def __init__(self, camac_request):
        self._camac_request = camac_request
        self.context = CalumaInfo.Context(self)

    class Context:
        def __init__(self, info):
            self._info = info

        @property
        def user(self):
            camac_user = self._info._camac_request.user

            user = caluma_user_models.OIDCUser(
                token=None, userinfo={"sub": camac_user.username, "group": None}
            )
            return user


class CamacRequest:
    """
    A camac request object built from the given caluma info object.

    The request attribute holds a shallow copy of `info.context` with translated
    values where needed (user, group, etc.).
    """

    def __init__(self, info):
        self.request = copy(info.context)
        oidc_user = self.request.user
        self.request.user = self._get_camac_user(oidc_user)
        self.request.auth = self._parse_token(oidc_user.token)
        camac_group = get_group(self.request)
        self.request.group = camac_group
        self.request.oidc_user = oidc_user

    def _get_camac_user(self, oidc_user):
        return User.objects.get(username=oidc_user.username)

    def _parse_token(self, token):
        data = token.split(b".")[1]
        data += b"=" * (-len(data) % 4)

        return loads(b64decode(data))
