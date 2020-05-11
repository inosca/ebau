from copy import copy
from functools import reduce

from caluma.caluma_form import models as caluma_form_models
from django.conf import settings
from django.db.models import Q
from jwt import decode as jwt_decode

from camac.user.middleware import get_group
from camac.user.models import User

APPLICANT_GROUP_ID = 6


class CalumaApi:
    """
    Class with helper methods to interact with Caluma.

    Initially this was meant as a wrapper for all interactions with Caluma (including
    the models). This is not the case anymore. Instead this class is meant to contain
    convenience methods for more involved caluma interactions or project specific
    meta lookups.
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

    def _get_main_document(self, instance):
        return caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance.pk},
            **{"form__meta__is-main-form": True},
        ).first()

    def get_main_document(self, instance):
        document = self._get_main_document(instance)
        return document.pk if document else None

    def get_source_document_value(self, document_id, field):
        source = caluma_form_models.Document.objects.get(pk=document_id).source
        return getattr(source, field, None) if source else None

    def _get_instance_documents(self, instance_id):
        return caluma_form_models.Document.objects.filter(
            **{"meta__camac-instance-id": instance_id}
        )

    def delete_instance_documents(self, instance_id):
        self._get_instance_documents(instance_id).delete()

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

        answers = caluma_form_models.Answer.objects.filter(
            **{
                "question_id": "nfd-tabelle-status",
                "document__family__form_id": "nfd",
                "document__family__meta__camac-instance-id": instance.pk,
            }
        )

        if answers.exclude(value="nfd-tabelle-status-entwurf").exists():
            permissions.add("read")

        if answers.filter(value="nfd-tabelle-status-in-bearbeitung").exists():
            permissions.add("write")

        return permissions

    def create_document(self, form_slug, **kwargs):
        return caluma_form_models.Document.objects.create(form_id=form_slug, **kwargs)

    def copy_document(self, source_pk, exclude_form_slugs=None, meta=None, **kwargs):
        """Use to `copy()` function on a document and do some clean-up.

        Caution: `exclude_form_slugs` is only excluding top-level questions
        and doesn't do additional clean-up on nested documents from
        table questions. That's based on the assumption that there are no table
        questions in the excluded form.
        """
        source = caluma_form_models.Document.objects.get(pk=source_pk)
        document = source.copy(**kwargs)

        if meta is not None:
            document.meta = meta

        if exclude_form_slugs:
            document.answers.filter(question__forms__in=exclude_form_slugs).delete()

        # prevent creating a historical record
        document.skip_history_when_saving = True
        try:
            document.save()
        finally:
            del document.skip_history_when_saving

        return document

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

    def is_modification(self, instance):
        return caluma_form_models.Answer.objects.filter(
            **{
                "document__meta__camac-instance-id": instance.pk,
                "document__form__meta__is-main-form": True,
                "question_id": "projektaenderung",
                "value": "projektaenderung-ja",
            }
        ).exists()

    def get_circulation_proposals(self, instance):
        # [(question_id, option, suggested service), ... ]
        suggestions = settings.APPLICATION.get("SUGGESTIONS", [])
        if not suggestions:  # pragma: no cover
            return set()

        suggestion_map = {
            (q_slug, answer): services for q_slug, answer, services in suggestions
        }

        document = self._get_main_document(instance)
        answers = caluma_form_models.Answer.objects.filter(
            document__family=document.family
        )

        _filter = reduce(
            lambda a, b: a | b,
            [
                Q(question_id=q_slug, value=answer)
                | Q(question_id=q_slug, value__contains=answer)
                for q_slug, answer, _ in suggestions
            ],
            Q(pk=None),
        )
        answers = answers.filter(_filter)

        suggestions_out = {
            service
            for ans in answers.filter(
                question__type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
            )
            for choice in ans.value
            for service in suggestion_map.get((ans.question_id, choice), [])
        }
        suggestions_out.update(
            {
                service
                for ans in answers.exclude(
                    question__type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
                )
                for service in suggestion_map.get((ans.question_id, ans.value), [])
            }
        )
        return suggestions_out


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
        self.request.auth = jwt_decode(oidc_user.token, verify=False)
        camac_group = get_group(self.request)
        self.request.group = camac_group
        self.request.oidc_user = oidc_user

    def _get_camac_user(self, oidc_user):
        return User.objects.get(username=oidc_user.username)
