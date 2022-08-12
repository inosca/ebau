import re
from collections import namedtuple
from datetime import date, timedelta
from html import escape
from itertools import chain
from logging import getLogger

import inflection
import jinja2
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.mail import EmailMessage, get_connection
from django.db.models import Exists, Func, IntegerField, OuterRef, Q, Subquery, Sum
from django.db.models.functions import Cast
from django.utils import timezone, translation
from django.utils.text import slugify
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.caluma.api import CalumaApi
from camac.caluma.utils import find_answer, get_answer_display_value
from camac.constants import kt_uri as uri_constants
from camac.core.models import (
    Activation,
    Answer,
    BillingV2Entry,
    Circulation,
    HistoryActionConfig,
    WorkflowEntry,
)
from camac.core.utils import create_history_entry
from camac.instance.master_data import MasterData
from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.instance.validators import transform_coordinates
from camac.user.models import Group, Role, Service, User
from camac.user.utils import unpack_service_emails
from camac.utils import flatten, get_responsible_koor_service_id

from ..core import models as core_models
from . import models

logger = getLogger(__name__)


RECIPIENT_TYPE_NAMES = {
    "applicant": translation.gettext_noop("Applicant"),
    "municipality": translation.gettext_noop("Municipality"),
    "caluma_municipality": translation.gettext_noop("Municipality (from Caluma)"),
    "leitbehoerde": translation.gettext_noop("Authority"),
    "construction_control": translation.gettext_noop("Construction control"),
    "involved_in_distribution": translation.gettext_noop("Involved services"),
    "inquiry_deadline_yesterday": translation.gettext_noop(
        "Services with overdue inquiries"
    ),
    "unanswered_inquiries": translation.gettext_noop(
        "Services with unanswered inquiries"
    ),
    "inquiry_addressed": translation.gettext_noop("Addressed service of inquiry"),
    "inquiry_controlling": translation.gettext_noop("Controlling service of inquiry"),
}


class InquiryMergeSerializer(serializers.Serializer):
    deadline_date = serializers.DateTimeField(
        source="deadline", format=settings.MERGE_DATE_FORMAT
    )
    start_date = serializers.DateTimeField(
        source="created_at", format=settings.MERGE_DATE_FORMAT
    )
    end_date = serializers.DateTimeField(
        source="closed_at", format=settings.MERGE_DATE_FORMAT
    )
    circulation_state = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    reason = serializers.SerializerMethodField()
    circulation_answer = serializers.SerializerMethodField()
    notices = serializers.SerializerMethodField()

    def get_circulation_state(self, inquiry):
        if inquiry.status == caluma_workflow_models.WorkItem.STATUS_READY:
            return (
                "REVIEW"
                if inquiry.child_case.work_items.filter(
                    status=caluma_workflow_models.WorkItem.STATUS_READY,
                    task_id=settings.DISTRIBUTION.get("INQUIRY_ANSWER_CHECK_TASK", ""),
                ).exists()
                else "RUN"
            )

        return (
            "OK"
            if inquiry.case.parent_work_item.status
            == caluma_workflow_models.WorkItem.STATUS_READY
            else "DONE"
        )

    def get_service(self, inquiry):
        return Service.objects.get(pk=inquiry.addressed_groups[0]).get_name()

    def get_reason(self, inquiry):
        return find_answer(
            inquiry.document, settings.DISTRIBUTION["QUESTIONS"]["REMARK"]
        )

    def get_circulation_answer(self, inquiry):
        return find_answer(
            inquiry.child_case.document,
            settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
        )

    def get_notices(self, inquiry):
        return [
            {
                "notice_type": str(answer.question.label),
                "content": answer.value,
            }
            for answer in (
                inquiry.child_case.document.answers.select_related("question")
                .filter(question__type=caluma_form_models.Question.TYPE_TEXTAREA)
                .order_by("-question__formquestion__sort")
            )
        ]


class BillingEntryMergeSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    service = serializers.StringRelatedField()
    created = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    account = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    def get_account(self, billing_entry):
        billing_account = billing_entry.billing_account
        return "{0} / {1}".format(billing_account.department, billing_account.name)

    def get_account_number(self, billing_entry):
        return billing_entry.billing_account.account_number


class InstanceMergeSerializer(InstanceEditableMixin, serializers.Serializer):
    """Converts instance into a dict to be used with template merging."""

    # TODO: document.Template and notification.NotificationTemplate should
    # be moved to its own app template including this serializer.

    location = serializers.StringRelatedField()
    identifier = serializers.CharField()
    activations = serializers.SerializerMethodField()
    billing_entries = BillingEntryMergeSerializer(many=True)
    answer_period_date = serializers.SerializerMethodField()
    publication_date = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()
    instance_id = serializers.IntegerField()
    public_dossier_link = serializers.SerializerMethodField()
    internal_dossier_link = serializers.SerializerMethodField()
    registration_link = serializers.SerializerMethodField()
    dossier_nr = serializers.SerializerMethodField()
    portal_submission = serializers.SerializerMethodField()
    leitbehoerde_name_de = serializers.SerializerMethodField()
    leitbehoerde_name_fr = serializers.SerializerMethodField()
    municipality_de = serializers.SerializerMethodField()
    municipality_fr = serializers.SerializerMethodField()
    form_name_de = serializers.SerializerMethodField()
    form_name_fr = serializers.SerializerMethodField()
    ebau_number = serializers.SerializerMethodField()
    base_url = serializers.SerializerMethodField()
    rejection_feedback = serializers.SerializerMethodField()
    current_service = serializers.SerializerMethodField()
    current_service_de = serializers.SerializerMethodField()
    current_service_fr = serializers.SerializerMethodField()
    current_service_description = serializers.SerializerMethodField()
    date_dossiervollstandig = serializers.SerializerMethodField()
    date_dossiereingang = serializers.SerializerMethodField()
    date_start_zirkulation = serializers.SerializerMethodField()
    date_bau_einspracheentscheid = serializers.SerializerMethodField()
    billing_total_kommunal = serializers.SerializerMethodField()
    billing_total_kanton = serializers.SerializerMethodField()
    billing_total = serializers.SerializerMethodField()
    my_activations = serializers.SerializerMethodField()
    objections = serializers.SerializerMethodField()
    bauverwaltung = serializers.SerializerMethodField()

    vorhaben = serializers.SerializerMethodField()
    parzelle = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    gesuchsteller = serializers.SerializerMethodField()

    # TODO: these is currently bern specific, as it depends on instance state
    # identifiers. This will likely need some client-specific switch logic
    # some time in the future
    distribution_status_de = serializers.SerializerMethodField()
    distribution_status_fr = serializers.SerializerMethodField()
    inquiry_answer_de = serializers.SerializerMethodField()
    inquiry_answer_fr = serializers.SerializerMethodField()

    current_user_name = serializers.SerializerMethodField()
    work_item_name = serializers.SerializerMethodField()

    def __init__(
        self, instance=None, inquiry=None, work_item=None, escape=False, *args, **kwargs
    ):
        self.escape = escape
        self.inquiry = inquiry
        self.work_item = work_item

        super().__init__(instance=instance, *args, **kwargs)

        self.service = (
            self.context["request"].group.service if "request" in self.context else None
        )

    def _escape(self, data):
        result = data
        if isinstance(data, str):
            result = escape(data)
        elif isinstance(data, list):
            result = [self._escape(value) for value in data]
        elif isinstance(data, dict):
            result = {key: self._escape(value) for key, value in data.items()}

        return result

    def format_date(self, date):
        current_tz = timezone.get_current_timezone()
        return current_tz.normalize(date.astimezone(current_tz)).strftime(
            settings.MERGE_DATE_FORMAT
        )

    def get_vorhaben(self, instance):
        description_slugs = [
            "proposal-description",
            "beschreibung-zu-mbv",
            "bezeichnung",
            "vorhaben-proposal-description",
            "veranstaltung-beschrieb",
        ]
        descriptions = [
            CalumaApi().get_answer_value(slug, instance) for slug in description_slugs
        ]
        return ", ".join(filter(None, descriptions))

    def _get_row_answer_value(self, row, slug, fallback=None):
        try:
            return row.answers.get(question_id=slug).value
        except caluma_form_models.Answer.DoesNotExist:
            return fallback

    def get_parzelle(self, instance):
        rows = CalumaApi().get_table_answer("parcels", instance)
        if rows:
            numbers = [self._get_row_answer_value(row, "parcel-number") for row in rows]
            return ", ".join([n for n in numbers if n is not None])
        return None

    def get_street(self, instance):
        return CalumaApi().get_answer_value("parcel-street", instance)

    def get_gesuchsteller(self, instance):
        rows = CalumaApi().get_table_answer("applicant", instance)

        if not rows:
            return

        row = rows.first()

        first_name = self._get_row_answer_value(row, "first-name", "")
        last_name = self._get_row_answer_value(row, "last-name", "")
        organisation = self._get_row_answer_value(row, "juristic-person-name", "")
        street = self._get_row_answer_value(row, "street", "")
        number = self._get_row_answer_value(row, "street-number", "")
        zip = self._get_row_answer_value(row, "zip", "")
        city = self._get_row_answer_value(row, "city", "")

        return ", ".join(
            filter(
                None,
                [
                    organisation,
                    f"{first_name} {last_name}",
                    f"{street} {number}",
                    f"{zip} {city}",
                ],
            )
        )

    def get_rejection_feedback(self, instance):  # pragma: no cover
        rejection_config = settings.APPLICATION["REJECTION_FEEDBACK_QUESTION"]
        return Answer.get_value_by_cqi(
            instance,
            rejection_config.get("CHAPTER"),
            rejection_config.get("QUESTION"),
            rejection_config.get("ITEM"),
            default="",
        )

    def get_answer_period_date(self, instace):
        answer_period_date = date.today() + timedelta(days=settings.MERGE_ANSWER_PERIOD)
        return answer_period_date.strftime(settings.MERGE_DATE_FORMAT)

    def get_publication_date(self, instance):
        publication_entry = instance.publication_entries.first()

        return (
            publication_entry
            and self.format_date(publication_entry.publication_date)
            or ""
        )

    def get_publications(self, instance):
        publications = []

        for publication in instance.publication_entries.filter(is_published=1).order_by(
            "publication_date"
        ):
            publications.append(
                {
                    "date": self.format_date(publication.publication_date),
                    "end_date": self.format_date(publication.publication_end_date),
                    "calendar_week": publication.publication_date.isocalendar()[1],
                }
            )

        return publications

    def get_leitbehoerde_name_de(self, instance):
        """Return current active service of the instance in german."""
        service = instance.responsible_service(filter_type="municipality")

        return service.get_name("de") if service else "-"

    def get_leitbehoerde_name_fr(self, instance):
        """Return current active service of the instance in french."""
        service = instance.responsible_service(filter_type="municipality")

        return service.get_name("fr") if service else "-"

    def get_municipality_de(self, instance):
        """Return municipality in german."""
        try:
            master_data = MasterData(instance.case)

            with translation.override("de"):
                return f"Gemeinde {master_data.municipality.get('label')}"
        except (KeyError, AttributeError):
            return ""

    def get_municipality_fr(self, instance):
        """Return municipality in french."""
        try:
            master_data = MasterData(instance.case)

            with translation.override("fr"):
                return f"Municipalité {master_data.municipality.get('label')}"
        except (KeyError, AttributeError):
            return ""

    def get_current_service(self, instance):
        """Return current service of the active user."""
        return self.service.get_name() if self.service else "-"

    def get_current_service_de(self, instance):
        """Return current service of the active user in german."""
        return self.service.get_name("de") if self.service else "-"

    def get_current_service_fr(self, instance):
        """Return current service of the active user in french."""
        return self.service.get_name("fr") if self.service else "-"

    def get_current_service_description(self, instance):
        """Return description of the current service of the active user."""
        return (
            self.service.get_trans_attr("description") or self.service.get_name()
            if self.service
            else "-"
        )

    def get_distribution_status_de(self, instance):
        return self._get_distribution_status(instance, "de")

    def get_distribution_status_fr(self, instance):
        return self._get_distribution_status(instance, "fr")

    def _get_distribution_status(self, instance, language):
        if not settings.DISTRIBUTION or not self.inquiry:
            return ""

        all_inquiries = caluma_workflow_models.WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            case__family__instance=instance,
            controlling_groups=self.inquiry.controlling_groups,
        ).exclude(
            status__in=[
                caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
                caluma_workflow_models.WorkItem.STATUS_CANCELED,
            ]
        )
        all_inquiries_count = all_inquiries.count()
        pending_inquiries_count = all_inquiries.filter(
            status=caluma_workflow_models.WorkItem.STATUS_READY
        ).count()

        if not all_inquiries.exists():  # pragma: no cover (this should never happen)
            return ""

        with translation.override(language):
            return (
                translation.gettext(
                    "%(pending)d of %(total)d inquries are still pending."
                )
                if pending_inquiries_count > 0
                else translation.gettext("All %(total)d inquries were received.")
            ) % {"total": all_inquiries_count, "pending": pending_inquiries_count}

    def get_inquiry_answer_de(self, instance):
        return self._get_inquiry_answer("de")

    def get_inquiry_answer_fr(self, instance):
        return self._get_inquiry_answer("fr")

    def _get_inquiry_answer(self, language):
        if not self.inquiry or not settings.DISTRIBUTION:
            return ""

        return find_answer(
            self.inquiry.child_case.document,
            settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
            language=language,
        )

    def get_form_name_de(self, instance):
        return CalumaApi().get_form_name(instance).de or ""

    def get_form_name_fr(self, instance):
        return CalumaApi().get_form_name(instance).fr or ""

    def get_ebau_number(self, instance):
        """Dossier number - Kanton Bern."""
        if settings.APPLICATION["FORM_BACKEND"] != "caluma":
            return "-"

        return CalumaApi().get_ebau_number(instance) or "-"

    def get_portal_submission(self, instance):
        """Return `True` if the given instance is a portal submission."""
        try:
            Answer.get_value_by_cqi(
                instance,
                *NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_CQI,
                fail_on_not_found=True,
            )
            return True
        except Answer.DoesNotExist:
            return False

    def get_dossier_nr(self, instance):
        """Dossier number - Kanton Uri."""
        return CalumaApi().get_dossier_number(instance) or "-"

    def get_internal_dossier_link(self, instance):
        return settings.INTERNAL_INSTANCE_URL_TEMPLATE.format(instance_id=instance.pk)

    def get_public_dossier_link(self, instance):
        return settings.PUBLIC_INSTANCE_URL_TEMPLATE.format(instance_id=instance.pk)

    def get_registration_link(self, instance):
        return settings.REGISTRATION_URL

    def get_base_url(self, instance):
        return settings.INTERNAL_BASE_URL

    def _get_workflow_entry_date(self, instance, item_id):
        entry = WorkflowEntry.objects.filter(
            instance=instance, workflow_item=item_id
        ).first()
        if entry:
            return self.format_date(entry.workflow_date)
        return "---"

    def get_date_dossiervollstandig(self, instance):
        return self._get_workflow_entry_date(
            instance,
            settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get("INSTANCE_COMPLETE"),
        )

    def get_date_dossiereingang(self, instance):
        return self._get_workflow_entry_date(
            instance, settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get("SUBMIT")
        )

    def get_date_start_zirkulation(self, instance):
        if not settings.DISTRIBUTION:
            return "---"

        work_item = caluma_workflow_models.WorkItem.objects.filter(
            case__family__instance=instance,
            task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
        ).first()

        if work_item:
            return self.format_date(work_item.closed_at)

        return "---"

    def get_date_bau_einspracheentscheid(self, instance):
        return self._get_workflow_entry_date(
            instance, settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get("DECISION")
        )

    def get_billing_total_kommunal(self, instance):
        return BillingV2Entry.objects.filter(
            instance=instance, organization=BillingV2Entry.MUNICIPAL
        ).aggregate(total=Sum("final_rate"))["total"]

    def get_billing_total_kanton(self, instance):
        return BillingV2Entry.objects.filter(
            instance=instance, organization=BillingV2Entry.CANTONAL
        ).aggregate(total=Sum("final_rate"))["total"]

    def get_billing_total(self, instance):
        return BillingV2Entry.objects.filter(instance=instance).aggregate(
            total=Sum("final_rate")
        )["total"]

    def _get_inquiries(self, instance):
        if not settings.DISTRIBUTION:
            return caluma_workflow_models.WorkItem.objects.none()

        service_subquery = Service.objects.filter(
            # Use element = ANY(array) operator to check if
            # element is present in ArrayField, which requires
            # lhs and rhs of expression to be of same type
            pk=Func(
                Cast(
                    OuterRef("addressed_groups"),
                    output_field=ArrayField(IntegerField()),
                ),
                function="ANY",
            )
        )

        return (
            caluma_workflow_models.WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                case__family__instance=instance,
            )
            .exclude(
                status__in=[
                    caluma_workflow_models.WorkItem.STATUS_CANCELED,
                    caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
                ]
            )
            .annotate(
                service_group_id=Subquery(
                    service_subquery.values("service_group_id")[:1]
                ),
                service_group_sort=Subquery(
                    service_subquery.values("service_group__sort")[:1]
                ),
                service_sort=Subquery(service_subquery.values("sort")[:1]),
            )
            .order_by("service_group_sort", "controlling_groups", "service_sort")
        )

    def get_activations(self, instance):
        inquiries = self._get_inquiries(instance)

        visibility_config = settings.APPLICATION.get("INTER_SERVICE_GROUP_VISIBILITIES")
        if visibility_config:
            inquiries = (
                inquiries.filter(
                    service_group_id__in=visibility_config.get(
                        self.service.service_group_id, []
                    )
                )
                if self.service
                else inquiries.none()
            )

        return InquiryMergeSerializer(inquiries, many=True).data

    def get_my_activations(self, instance):
        inquiries = self._get_inquiries(instance)

        return InquiryMergeSerializer(
            (
                inquiries.filter(addressed_groups__contains=[str(self.service.pk)])
                if self.service
                else inquiries.none()
            ),
            many=True,
        ).data

    def get_objections(self, instance):
        objections = instance.objections.all()

        for objection in objections:
            objection.participants = objection.objection_participants.all()

            if objection.objection_participants.filter(representative=1).exists():
                objection.participants = objection.objection_participants.filter(
                    representative=1
                )

            objection.creation_date = objection.creation_date.strftime(
                settings.MERGE_DATE_FORMAT
            )

        return objections

    def get_bauverwaltung(self, instance):
        if not settings.APPLICATION.get("INSTANCE_MERGE_CONFIG"):
            return {}

        work_item_qs = instance.case.work_items.filter(
            task_id=settings.APPLICATION["INSTANCE_MERGE_CONFIG"]["BAUVERWALTUNG"][
                "TASK_SLUG"
            ]
        )

        if not work_item_qs.exists():  # pragma: no cover
            return {}

        document = work_item_qs.first().document
        answers = {
            inflection.underscore(answer.question.slug): get_answer_display_value(
                answer, option_separator="\n"
            )
            for answer in document.answers.filter(
                Q(value__isnull=False) | Q(date__isnull=False)
            )
        }

        # loop over table questions in sub form questions
        for question in caluma_form_models.Question.objects.filter(
            type=caluma_form_models.Question.TYPE_TABLE,
            forms__in=document.form.questions.filter(
                type=caluma_form_models.Question.TYPE_FORM
            ).values("sub_form"),
        ):
            question_answers = []
            # loop over table rows in table question
            for row in caluma_form_models.AnswerDocument.objects.filter(
                answer__question_id=question.slug, document__family=document
            ):
                row_answers = {}
                # loop over answers in table row to format the answer
                for answer in row.document.answers.all():
                    row_answers[
                        inflection.underscore(answer.question.slug)
                    ] = get_answer_display_value(answer, option_separator="\n")
                question_answers.append(row_answers)
            answers[inflection.underscore(question.slug)] = question_answers

        return answers

    def get_current_user_name(self, instance):
        return (
            self.context["request"].user.get_full_name()
            if "request" in self.context
            else None
        )

    def get_work_item_name(self, instance):
        return str(self.work_item.name) if self.work_item else None

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field in instance.fields.all():
            # remove versioning (-v3) from question names so the placeholders are backwards compatible
            name_without_version = re.sub(r"(-v\d+$)", "", field.name)
            name = inflection.underscore("field-" + name_without_version)
            value = field.value

            if (
                field.name == settings.APPLICATION.get("COORDINATE_QUESTION", "")
                and value is not None
            ):
                value = "\n".join(transform_coordinates(value))
            elif field.name in settings.APPLICATION.get("QUESTIONS_WITH_OVERRIDE", []):
                override = instance.fields.filter(
                    name=f"{name_without_version}-override"
                ).first()
                value = override.value if override else value
            elif field.name == settings.APPLICATION.get("LOCATION_NAME_QUESTION", ""):
                ret["field_standort_adresse"] = value

            ret[name] = value

        if self.escape:
            ret = self._escape(ret)

        return ret

    class Meta:
        resource_name = "instance-merges"


class IssueMergeSerializer(serializers.Serializer):
    deadline_date = serializers.DateField()
    text = serializers.CharField()

    def to_representation(self, issue):
        ret = super().to_representation(issue)

        # include instance merge fields
        ret.update(
            InstanceMergeSerializer(instance=issue.instance, context=self.context).data
        )

        return ret


class NotificationTemplateSerializer(serializers.ModelSerializer):
    notification_type = serializers.CharField(source="type")

    def create(self, validated_data):
        service = self.context["request"].group.service
        validated_data["service"] = service
        validated_data["slug"] = slugify(validated_data["slug"])
        return super().create(validated_data)

    def validate_slug(self, value):
        if self.instance:
            raise serializers.ValidationError("Updating a slug is not allowed!")
        return value

    class Meta:
        model = models.NotificationTemplate
        fields = ("slug", "purpose", "subject", "body", "notification_type", "service")


class NotificationTemplateMergeSerializer(
    InstanceEditableMixin, serializers.Serializer
):
    instance_editable_permission = None
    """
    No specific permission needed to send notification
    """

    instance = serializers.ResourceRelatedField(queryset=Instance.objects.all())
    inquiry = serializers.ResourceRelatedField(
        queryset=caluma_workflow_models.WorkItem.objects.all(),
        required=False,
    )
    work_item = serializers.ResourceRelatedField(
        queryset=caluma_workflow_models.WorkItem.objects.all(),
        required=False,
    )
    notification_template = serializers.ResourceRelatedField(
        queryset=models.NotificationTemplate.objects.all()
    )
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)

    def _merge(self, value, data):
        try:
            value_template = jinja2.Template(value)

            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def validate(self, data):
        notification_template = data["notification_template"]
        instance = data["instance"]

        placeholder_data = InstanceMergeSerializer(
            instance=instance,
            context=self.context,
            inquiry=data.get("inquiry"),
            work_item=data.get("work_item"),
        ).data

        # some cantons use uppercase placeholders. be as compatible as possible
        placeholder_data.update({k.upper(): v for k, v in placeholder_data.items()})

        data["subject"] = self._merge(
            data.get("subject", notification_template.get_trans_attr("subject")),
            placeholder_data,
        )
        data["body"] = self._merge(
            data.get("body", notification_template.get_trans_attr("body")),
            placeholder_data,
        )
        data["pk"] = "{0}-{1}".format(notification_template.slug, instance.pk)

        return data

    def create(self, validated_data):
        NotificationTemplateMerge = namedtuple(
            "NotificationTemplateMerge", validated_data.keys()
        )
        obj = NotificationTemplateMerge(**validated_data)

        return obj

    class Meta:
        resource_name = "notification-template-merges"


class NotificationTemplateSendmailSerializer(NotificationTemplateMergeSerializer):
    # Activation and circulation are only needed for the recipient types
    activation = serializers.ResourceRelatedField(
        queryset=Activation.objects.all(), required=False
    )
    circulation = serializers.ResourceRelatedField(
        queryset=Circulation.objects.all(), required=False
    )

    SUBMITTER_TYPE_APPLICANT = "0"
    SUBMITTER_TYPE_PROJECT_AUTHOR = "1"
    SUBMITTER_LIST_CQI_BY_TYPE = {
        SUBMITTER_TYPE_APPLICANT: (1, 66, 1),
        SUBMITTER_TYPE_PROJECT_AUTHOR: (1, 77, 1),
    }
    SUBMITTER_TYPE_CQI = (103, 257, 1)
    recipient_types = serializers.MultipleChoiceField(
        choices=(
            "applicant",
            "municipality",
            "caluma_municipality",
            "leitbehoerde",
            "construction_control",
            "email_list",
            # Old circulation (UR)
            "unnotified_service",
            "activation_service_parent",
            # New circulation (BE, SZ)
            "involved_in_distribution",
            "inquiry_deadline_yesterday",
            "unanswered_inquiries",
            "inquiry_addressed",
            "inquiry_controlling",
            # Work items
            "work_item_addressed",
            "work_item_controlling",
            *settings.APPLICATION.get("CUSTOM_NOTIFICATION_TYPES", []),
        )
    )
    email_list = serializers.CharField(required=False)

    def _get_recipients_submitter_list(self, instance):

        if instance.form.pk not in uri_constants.PORTAL_FORMS:
            return []

        submitter_type = str(
            Answer.get_value_by_cqi(
                instance,
                *self.SUBMITTER_TYPE_CQI,
                # TODO needs to be confirmed with customer
                default=self.SUBMITTER_TYPE_APPLICANT,
            )
        )

        ans_cqi = self.SUBMITTER_LIST_CQI_BY_TYPE.get(submitter_type)
        ans = Answer.get_value_by_cqi(instance, *ans_cqi, fail_on_not_found=False)
        if not ans:
            raise exceptions.ValidationError(
                f"Instance {instance.pk}: Answer for submitter/applicant "
                f"email not found. Cannot send notification email"
            )

        return [{"to": ans}]

    def _group_service_recipients(self, groups):
        return [
            {"to": email}
            for email in unpack_service_emails(
                Service.objects.filter(groups__in=groups, notification=1)
            )
        ]

    def _get_recipients_municipality_users(self, instance):
        """Email addresses on the municipality's service email list."""
        groups = Group.objects.filter(
            locations=instance.location, role=uri_constants.ROLE_MUNICIPALITY
        )
        return self._group_service_recipients(groups)

    def _get_recipients_unnotified_service_users(self, instance):
        circulation = self.validated_data["circulation"]
        activations = circulation.activations.filter(
            circulation_state_id=uri_constants.CIRCULATION_STATE_IDLE
        )

        services = Service.objects.filter(
            pk__in=activations.values("service_id"), notification=1
        )

        return [
            {"to": email}
            for value in services.values_list("email", flat=True)
            if value
            for email in value.split(",")
        ]

    def _notify_service(self, service_id):
        return [
            {"to": email}
            for email in unpack_service_emails(
                Service.objects.filter(pk=service_id, notification=1)
            )
        ]

    def _get_recipients_koor_np_users(self, instance):
        return self._notify_service(uri_constants.KOOR_NP_SERVICE_ID)

    def _get_recipients_koor_bg_users(self, instance):
        return self._notify_service(uri_constants.KOOR_BG_SERVICE_ID)

    def _get_recipients_koor_bd_users(self, instance):
        return self._notify_service(uri_constants.KOOR_BD_SERVICE_ID)

    def _get_recipients_koor_sd_users(self, instance):
        return self._notify_service(uri_constants.KOOR_SD_SERVICE_ID)

    def _get_recipients_responsible_koor(self, instance):
        return self._notify_service(get_responsible_koor_service_id(instance.form.pk))

    def _get_recipients_lisag(self, instance):
        groups = Group.objects.filter(name="Lisag")
        return [{"to": group.email} for group in groups]

    def _get_recipients_inactive_municipality(self, instance):
        if (
            instance.responsible_service(filter_type="municipality").service_group.name
            != "district"
        ):
            return []

        return self._get_recipients_caluma_municipality(instance)

    def _get_recipients_caluma_municipality(self, instance):
        municipality_service_id = CalumaApi().get_municipality(instance)

        if not municipality_service_id:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not get Caluma municipality for instance {instance.pk}"
            )

        return self._get_responsible(
            instance,
            Service.objects.filter(pk=municipality_service_id, notification=1).first(),
        )

    def _get_recipients_applicant(self, instance):
        return [
            {"to": applicant.invitee.email}
            for applicant in instance.involved_applicants.all()
            if applicant.invitee
        ]

    def _get_responsible(self, instance, service, work_item=None):
        if not service.notification:
            return []

        # Responsible user for the instance from various responsibility modules
        responsible_user = User.objects.filter(
            pk__in=[
                *instance.responsible_services.filter(service=service).values_list(
                    "responsible_user", flat=True
                ),
                *instance.responsibilities.filter(service=service).values_list(
                    "user", flat=True
                ),
            ]
        ).first()

        # Assigned user from the work item
        assigned_user = (
            User.objects.filter(username__in=work_item.assigned_users).first()
            if work_item
            else None
        )

        if assigned_user or responsible_user:
            return [
                {
                    "to": assigned_user.email
                    if assigned_user
                    else responsible_user.email,
                    "cc": service.email,
                }
            ]

        return [{"to": service.email}]

    def _get_recipients_leitbehoerde(self, instance):  # pragma: no cover
        return self._get_responsible(
            instance, instance.responsible_service(filter_type="municipality")
        )

    def _get_recipients_municipality(self, instance):
        return self._get_responsible(instance, instance.group.service)

    def _get_recipients_unnotified_service(self, instance):
        # Circulation and subcirculation share the same circulation object.
        # They can only be distinguished by their SERVICE_PARENT_ID.
        activations = Activation.objects.filter(
            circulation=self.validated_data.get("circulation"),
            email_sent=0,
            service_parent=self.context["request"].group.service,
            service__notification=1,
        )

        return flatten(
            [
                self._get_responsible(instance, activation.service)
                for activation in activations
            ]
        )

    def _get_recipients_involved_in_distribution(self, instance):
        if not settings.DISTRIBUTION:  # pragma: no cover
            return []

        inquiries = caluma_workflow_models.WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            case__family__instance=instance,
        ).exclude(
            status__in=[
                caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
                caluma_workflow_models.WorkItem.STATUS_CANCELED,
            ],
        )

        not_involved_answer = (
            settings.DISTRIBUTION["ANSWERS"].get("STATUS", {}).get("NOT_INVOLVED")
        )

        if not_involved_answer:
            # don't involve services that responded the inquiry with "not involved"
            inquiries = inquiries.exclude(
                Exists(
                    caluma_form_models.Answer.objects.filter(
                        document__case__parent_work_item=OuterRef("pk"),
                        question_id=settings.DISTRIBUTION["QUESTIONS"]["STATUS"],
                        value=not_involved_answer,
                    )
                )
            )

        addressed_groups = inquiries.values_list("addressed_groups", flat=True)

        return flatten(
            [
                self._get_responsible(instance, service)
                for service in Service.objects.filter(
                    pk__in=list(chain(*addressed_groups))
                )
            ]
        )

    def _get_recipients_inquiry_deadline_yesterday(self, instance):
        """Return recipients of inquiries for an instance which deadline expired yesterday."""
        if not settings.DISTRIBUTION:  # pragma: no cover
            return []

        addressed_groups = caluma_workflow_models.WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            deadline__date=date.today() - timedelta(days=1),
            case__family__instance__instance_state__name="circulation",
            case__family__instance=instance,
        ).values_list("addressed_groups", flat=True)

        return flatten(
            [
                self._get_responsible(instance, service)
                for service in Service.objects.filter(
                    pk__in=list(chain(*addressed_groups))
                )
            ]
        )

    def _get_recipients_unanswered_inquiries(self, instance):
        if not settings.DISTRIBUTION:  # pragma: no cover
            return []

        addressed_groups = caluma_workflow_models.WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_SKIPPED,
            case__family__instance=instance,
        ).values_list("addressed_groups", flat=True)

        return flatten(
            [
                self._get_responsible(instance, service)
                for service in Service.objects.filter(
                    pk__in=list(chain(*addressed_groups))
                )
            ]
        )

    def _get_recipients_inquiry_addressed(self, instance):
        inquiry = self.validated_data.get("inquiry")

        if not settings.DISTRIBUTION or not inquiry:  # pragma: no cover
            return []

        return self._get_responsible(
            instance, Service.objects.get(pk=inquiry.addressed_groups[0])
        )

    def _get_recipients_inquiry_controlling(self, instance):
        inquiry = self.validated_data.get("inquiry")

        if not settings.DISTRIBUTION or not inquiry:  # pragma: no cover
            return []

        return self._get_responsible(
            instance, Service.objects.get(pk=inquiry.controlling_groups[0])
        )

    def _get_recipients_construction_control(self, instance):
        instance_services = core_models.InstanceService.objects.filter(
            instance=instance,
            service__service_group__name="construction-control",
            active=1,
        )
        return flatten(
            [
                self._get_responsible(instance, instance_service.service)
                for instance_service in instance_services
            ]
        )

    def _get_recipients_email_list(self, instance):
        return [{"to": to} for to in self.validated_data["email_list"].split(",")]

    def _get_recipients_activation_service_parent(self, instance):
        activation = self.validated_data.get("activation")

        if not activation or not activation.service_parent:  # pragma: no cover
            return []

        return self._get_responsible(instance, activation.service_parent)

    def _get_recipients_work_item_controlling(self, instance):
        return flatten(
            [
                self._get_responsible(instance, service)
                for service in Service.objects.filter(
                    pk__in=self.validated_data.get("work_item").controlling_groups
                )
            ]
        )

    def _get_recipients_work_item_addressed(self, instance):
        work_item = self.validated_data.get("work_item")

        return flatten(
            [
                self._get_responsible(instance, service, work_item)
                for service in Service.objects.filter(pk__in=work_item.addressed_groups)
            ]
        )

    def _recipient_log(self, recipients):
        return ", ".join(
            [
                recipient["to"]
                or "" + (f" (CC: {recipient['cc']})" if "cc" in recipient else "")
                for recipient in recipients
            ]
        )

    def _receiver_type(self, recipient_type, language):
        receiver_type = RECIPIENT_TYPE_NAMES.get(recipient_type)

        if receiver_type:
            with translation.override(language):
                return translation.gettext(receiver_type)

        return None

    def _post_send_unnotified_service(self, instance):
        Activation.objects.filter(
            circulation=self.validated_data.get("circulation"),
            email_sent=0,
            service_parent=self.context["request"].group.service,
        ).update(email_sent=1)

    def create(self, validated_data):
        subj_prefix = settings.EMAIL_PREFIX_SUBJECT
        body_prefix = settings.EMAIL_PREFIX_BODY
        special_forms_prefix = settings.EMAIL_PREFIX_BODY_SPECIAL_FORMS

        instance = validated_data["instance"]
        form_slug = CalumaApi().get_form_slug(instance)

        emails = []
        post_send = []

        connection = get_connection()

        for recipient_type in sorted(validated_data["recipient_types"]):
            recipients = getattr(self, "_get_recipients_%s" % recipient_type)(instance)
            subject = subj_prefix + validated_data["subject"]

            if (
                recipient_type != "applicant"
                and form_slug in settings.ECH_EXCLUDED_FORMS
            ):
                body = body_prefix + special_forms_prefix + validated_data["body"]
            else:
                body = body_prefix + validated_data["body"]

            for recipient in [r for r in recipients if r.get("to")]:
                emails.append(
                    EmailMessage(
                        subject=subject,
                        body=body,
                        connection=connection,
                        # EmailMessage needs "to" and "cc" to be lists
                        **{
                            k: [e.strip() for e in email.split(",")]
                            for (k, email) in recipient.items()
                            if email
                        },
                    )
                )

            post_send.append(
                getattr(self, f"_post_send_{recipient_type}", lambda instance: None)
            )

            # If no request context was provided to the serializer we assume the
            # mail delivery is part of a batch job initalized by the system
            # operation user.
            user = None

            if self.context:
                user = self.context["request"].user
            elif settings.APPLICATION.get("SYSTEM_USER"):
                user = User.objects.filter(
                    username=settings.APPLICATION.get("SYSTEM_USER")
                ).first()

            if not user:
                # This should be removed in the future since it's a really
                # strange fallback that does not really make sense in any case
                # to choose a random support user as sender. This can be removed
                # when the notifyoverdue command of UR is using the system user
                user = (
                    Role.objects.get(name__iexact="support")
                    .groups.order_by("group_id")
                    .first()
                    .users.first()
                )

            self._create_history_entry(
                instance, subject, body, recipients, recipient_type, user
            )

        self._send_mails(emails, connection)

        for fn in post_send:
            fn(instance)

        return len(emails)

    def _create_history_entry(
        self, instance, subject, body, recipients, recipient_type, user
    ):
        if settings.APPLICATION.get("LOG_NOTIFICATIONS"):
            receiver_emails = self._recipient_log(recipients)

            title = "Notifikation gesendet an {0} ({1})".format(
                receiver_emails, subject
            )

            if settings.APPLICATION.get("IS_MULTILINGUAL", False):
                if receiver_emails:
                    title = translation.gettext_noop(
                        "Notification sent to %(receiver_emails)s (%(receiver_type)s) (%(subject)s)"
                    )
                else:
                    title = translation.gettext_noop(
                        "Notification sent to %(receiver_type)s (no receivers) (%(subject)s)"
                    )

            create_history_entry(
                instance,
                user,
                title,
                lambda lang: {
                    "receiver_emails": receiver_emails,
                    "receiver_type": self._receiver_type(recipient_type, lang),
                    "subject": subject,
                },
                HistoryActionConfig.HISTORY_TYPE_NOTIFICATION,
                body,
            )

    def _send_mails(self, emails, connection):
        if emails:
            connection.open()
            exceptions = []
            for email in emails:
                try:
                    email.send()
                    logger.info(f'Sent email "{email.subject}" to {email.to}')
                except Exception as e:  # noqa: B902
                    exceptions.append((e, email))
            connection.close()

            if len(exceptions) > 0:
                error_msgs = "\n".join(
                    [
                        f"to {email.to}, cc {email.cc}: {str(exception)}"
                        for exception, email in exceptions
                    ]
                )
                logger.error(f"Failed to send {len(exceptions)} emails: {error_msgs}")

    class Meta:
        resource_name = "notification-template-sendmails"


class PermissionlessNotificationTemplateSendmailSerializer(
    NotificationTemplateSendmailSerializer
):
    """
    Send emails without checking for instance permission.

    This serializer subclasses NotificationTemplateSendmailSerializer and
    overloads the validate_instance method of the InstanceEditableMixin to
    disable permission checking the instance and allow anyone to send a email.
    """

    # Temporary pragma no cover, remove when publication permission endpoint is reenabled
    # revert !2353 to remove
    def validate_instance(self, instance):  # pragma: no cover
        return instance
