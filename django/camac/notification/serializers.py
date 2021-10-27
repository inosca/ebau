from collections import namedtuple
from datetime import date, timedelta
from html import escape
from logging import getLogger

import inflection
import jinja2
from caluma.caluma_form import models as caluma_form_models
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_noop
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.caluma.api import CalumaApi
from camac.constants import kt_bern as be_constants, kt_uri as uri_constants
from camac.core.models import (
    Activation,
    Answer,
    BillingV2Entry,
    Circulation,
    HistoryActionConfig,
    WorkflowEntry,
)
from camac.core.utils import create_history_entry
from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.instance.validators import transform_coordinates
from camac.user.models import Group, Role, Service, User
from camac.user.utils import unpack_service_emails
from camac.utils import flatten, get_responsible_koor_service_id

from ..core import models as core_models
from . import models

logger = getLogger(__name__)


class NoticeMergeSerializer(serializers.Serializer):
    service = serializers.StringRelatedField(source="activation.service")
    notice_type = serializers.StringRelatedField()
    notice_type_id = serializers.IntegerField(source="notice_type.pk")
    content = serializers.CharField()


class ActivationMergeSerializer(serializers.Serializer):
    deadline_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    start_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    end_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    circulation_state = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    reason = serializers.CharField()
    circulation_answer = serializers.StringRelatedField()
    notices = NoticeMergeSerializer(many=True)
    nfd_completion_date = serializers.SerializerMethodField()

    def get_nfd_completion_date(self, activation):
        completion_date = activation.nfd_completion_date
        if completion_date:
            return completion_date.strftime(settings.MERGE_DATE_FORMAT)
        return None


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
    activation = serializers.SerializerMethodField()
    activations = ActivationMergeSerializer(many=True)
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
    leitbehoerde_name = serializers.SerializerMethodField()
    form_name = serializers.SerializerMethodField()
    ebau_number = serializers.SerializerMethodField()
    base_url = serializers.SerializerMethodField()
    rejection_feedback = serializers.SerializerMethodField()
    current_service = serializers.SerializerMethodField()
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

    vorhaben = serializers.SerializerMethodField()
    parzelle = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    gesuchsteller = serializers.SerializerMethodField()

    # TODO: these is currently bern specific, as it depends on instance state
    # identifiers. This will likely need some client-specific switch logic
    # some time in the future
    total_activations = serializers.SerializerMethodField()
    completed_activations = serializers.SerializerMethodField()
    pending_activations = serializers.SerializerMethodField()
    activation_statement_de = serializers.SerializerMethodField()
    activation_statement_fr = serializers.SerializerMethodField()
    activation_answer_de = serializers.SerializerMethodField()
    activation_answer_fr = serializers.SerializerMethodField()

    def __init__(self, instance, *args, activation=None, escape=False, **kwargs):
        self.escape = escape

        lookup = {"circulation__instance": instance}
        if activation:
            self.activation = activation
            self.circulation = self.activation.circulation

            lookup.update(
                {
                    "circulation": self.activation.circulation,
                    "service_parent": self.activation.service_parent,
                }
            )

        instance.activations = Activation.objects.filter(**lookup)

        super().__init__(instance, *args, **kwargs)

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

    def get_activation(self, instance):
        if not hasattr(self, "activation"):
            return None
        return ActivationMergeSerializer(self.activation).data

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
                    "calendar_week": publication.publication_date.isocalendar()[1],
                }
            )

        return publications

    def get_leitbehoerde_name(self, instance):
        """Return current active service of the instance."""
        return instance.responsible_service(filter_type="municipality") or "-"

    def get_current_service(self, instance):
        """Return current service of the active user."""
        try:
            service = self.context["request"].group.service

            return service.get_name() if service else "-"
        except KeyError:
            return "-"

    def get_current_service_description(self, instance):
        """Return description of the current service of the active user."""
        try:
            service = self.context["request"].group.service
            description = None
            service_name = None

            if service:
                description = service.get_trans_attr("description")
                service_name = service.get_name()

            return description or service_name or "-"
        except KeyError:
            return "-"

    def get_activation_statement_de(self, instance):
        return self._get_activation_statement(instance, "de")

    def get_activation_statement_fr(self, instance):
        return self._get_activation_statement(instance, "fr")

    def _get_activation_statement(self, instance, language):
        if not getattr(self, "circulation", None):
            return ""

        total = self.get_total_activations(instance)
        pending = self.get_pending_activations(instance)

        try:
            created = date.fromtimestamp(int(self.circulation.name)).strftime(
                "%d.%m.%Y"
            )
            circulation_name = {"de": f" vom {created}", "fr": f" du {created}"}
        except ValueError:  # pragma: no cover
            circulation_name = {"de": "", "fr": ""}

        if total == 0:  # pragma: no cover (this should never happen)
            return ""
        elif pending == 0:
            message = {
                "de": f"Alle {total} Stellungnahmen der Zirkulation{circulation_name.get('de')} sind nun eingegangen.",
                "fr": f"Tous les {total} prises de position de la circulation{circulation_name.get('fr')} ont été reçues.",
            }
        else:  # pending > 0:
            message = {
                "de": f"{pending} von {total} Stellungnahmen der Zirkulation{circulation_name.get('de')} stehen noch aus.",
                "fr": f"{pending} de {total} prises de position de la circulation{circulation_name.get('fr')} sont toujours en attente.",
            }

        return message.get(language)

    def get_activation_answer_de(self, instance):
        return self._get_activation_answer(instance, "de")

    def get_activation_answer_fr(self, instance):
        return self._get_activation_answer(instance, "fr")

    def _get_activation_answer(self, instance, language):
        if (
            not getattr(self, "activation", None)
            or not self.activation.circulation_answer
        ):
            return ""

        return self.activation.circulation_answer.get_trans_attr("name", lang=language)

    def get_form_name(self, instance):
        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            return instance.form.get_name()

        return CalumaApi().get_form_name(instance) or "-"

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
        return self._get_workflow_entry_date(
            instance, settings.APPLICATION.get("WORKFLOW_ITEMS", {}).get("START_CIRC")
        )

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

    def get_my_activations(self, instance):
        if "request" not in self.context:
            return instance.activations.none()

        activations = ActivationMergeSerializer(
            instance.activations.filter(service=self.context["request"].group.service),
            many=True,
        ).data

        for activation in activations:
            activation["notices"] = sorted(
                activation["notices"], key=lambda k: k["notice_type_id"]
            )

        return activations

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

    def get_total_activations(self, instance):
        return instance.activations.count()

    def get_completed_activations(self, instance):
        return instance.activations.filter(
            circulation_state_id=be_constants.CIRCULATION_STATE_DONE
        ).count()

    def get_pending_activations(self, instance):
        return instance.activations.filter(
            circulation_state_id=be_constants.CIRCULATION_STATE_WORKING
        ).count()

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field in instance.fields.all():
            name = inflection.underscore("field-" + field.name)
            value = field.value

            if (
                field.name == settings.APPLICATION.get("COORDINATE_QUESTION", "")
                and value is not None
            ):
                value = "\n".join(transform_coordinates(value))
            elif field.name in settings.APPLICATION.get("QUESTIONS_WITH_OVERRIDE", []):
                override = instance.fields.filter(name=f"{field.name}-override").first()
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
        ret.update(InstanceMergeSerializer(issue.instance, context=self.context).data)

        return ret


class NotificationTemplateSerializer(serializers.ModelSerializer):
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
        fields = ("slug", "purpose", "subject", "body", "type", "service")


class NotificationTemplateMergeSerializer(
    InstanceEditableMixin, serializers.Serializer
):
    instance_editable_permission = None
    """
    No specific permission needed to send notification
    """

    instance = serializers.ResourceRelatedField(queryset=Instance.objects.all())
    activation = serializers.ResourceRelatedField(
        queryset=Activation.objects.all(), required=False
    )
    circulation = serializers.ResourceRelatedField(
        queryset=Circulation.objects.all(), required=False
    )
    notification_template = serializers.ResourceRelatedField(
        queryset=models.NotificationTemplate.objects.all()
    )
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)

    def _merge(self, value, instance, activation=None):
        try:
            value_template = jinja2.Template(value)
            data = InstanceMergeSerializer(
                instance, context=self.context, activation=activation
            ).data

            # some cantons use uppercase placeholders. be as compatible as possible
            data.update({k.upper(): v for k, v in data.items()})
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def validate(self, data):
        notification_template = data["notification_template"]
        instance = data["instance"]
        activation = data.get("activation")

        data["subject"] = self._merge(
            data.get("subject", notification_template.get_trans_attr("subject")),
            instance,
            activation=activation,
        )
        data["body"] = self._merge(
            data.get("body", notification_template.get_trans_attr("body")),
            instance,
            activation=activation,
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
    SUBMITTER_TYPE_APPLICANT = "0"
    SUBMITTER_TYPE_PROJECT_AUTHOR = "1"
    SUBMITTER_LIST_CQI_BY_TYPE = {
        SUBMITTER_TYPE_APPLICANT: (1, 66, 1),
        SUBMITTER_TYPE_PROJECT_AUTHOR: (1, 77, 1),
    }
    SUBMITTER_TYPE_CQI = (103, 257, 1)
    recipient_types = serializers.MultipleChoiceField(
        choices=(
            "activation_deadline_yesterday",
            "applicant",
            "municipality",
            "caluma_municipality",
            "service",
            "unnotified_service",
            "leitbehoerde",
            "construction_control",
            "email_list",
            "activation_service_parent",
            "circulation_service",
            "activation_service",
            "unanswered_activation",
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

    def _get_recipients_activation_deadline_yesterday(self, instance):
        """Return recipients of activations for an instance which deadline expired yesterday."""
        activations = Activation.objects.filter(
            ~Q(circulation_state__name="DONE"),
            deadline_date__date=date.today() - timedelta(days=1),
            circulation__instance__instance_state__name="circulation",
            circulation__instance=instance,
        )
        services = {a.service for a in activations}
        return flatten(
            [self._get_responsible(instance, service) for service in services]
        )

    def _get_responsible(self, instance, service):
        if not service.notification:
            return []

        responsible_old = instance.responsible_services.filter(
            service=service
        ).values_list("responsible_user__email", flat=True)
        responsible_new = instance.responsibilities.filter(service=service).values_list(
            "user__email", flat=True
        )
        responsibles = responsible_new.union(responsible_old)

        try:
            return [{"to": responsibles[0], "cc": service.email}]
        except IndexError:
            return [{"to": service.email}]

    def _get_recipients_leitbehoerde(self, instance):  # pragma: no cover
        return self._get_responsible(
            instance, instance.responsible_service(filter_type="municipality")
        )

    def _get_recipients_municipality(self, instance):
        return self._get_responsible(instance, instance.group.service)

    def _get_recipients_unnotified_service(self, instance):

        service = self.context["request"].group.service

        # Circulation and subcirculation share the same circulation object.
        # They can only be distinguished by their SERVICE_PARENT_ID.
        activations = Activation.objects.filter(
            circulation__instance_id=instance.pk,
            email_sent=0,
            service_parent=service,
        )
        services = {a.service for a in activations}

        return flatten(
            [self._get_responsible(instance, service) for service in services]
        )

    def _get_recipients_service(self, instance):
        services = Service.objects.filter(
            pk__in=instance.circulations.values("activations__service")
        )

        return flatten(
            [self._get_responsible(instance, service) for service in services]
        )

    def _get_recipients_unanswered_activation(self, instance):
        services = Service.objects.filter(
            pk__in=self.validated_data.get("circulation")
            .activations.values("service")
            .exclude(circulation_state__name="DONE")
            .values_list("service__pk", flat=True)
        )

        return flatten(
            [self._get_responsible(instance, service) for service in services]
        )

    def _get_recipients_activation_service(self, instance):
        """Return mail addresses of an circulation-invited service.

        In detail return all mail addresses of users of whichs default group has
        the same service as the activation.
        """
        activation = self.validated_data.get("activation")
        if not activation:
            raise exceptions.ValidationError(
                f"Recipient type requires you to provide activation for instance {instance.pk}"
            )

        if activation.service.notification:
            email = activation.service.email
            if email and "@" in email:
                return [{"to": addr} for addr in activation.service.email.split(",")]
        return []

    def _get_recipients_circulation_service(self, instance):
        """Return mail address of the service which created a circulation.

        In detail return all mail addresses of users of whichs default group has
        the same service as the circulation.
        """
        activation = self.validated_data.get("activation")
        if not activation:
            raise exceptions.ValidationError(
                f"Recipient type requires you to provide activation for instance {instance.pk}"
            )

        if activation.service.notification:
            email = activation.service.email
            if email and "@" in email:
                return [{"to": addr} for addr in activation.service.email.split(",")]
        return []

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

    def _recipient_log(self, recipient):
        return recipient["to"] or "" + (
            f" (CC: {recipient['cc']})" if "cc" in recipient else ""
        )

    def _post_send_unnotified_service(self, instance):
        Activation.objects.filter(
            circulation__instance_id=instance.pk,
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

            if settings.APPLICATION.get("LOG_NOTIFICATIONS"):
                title = gettext_noop("Notification sent to %(receiver)s (%(subject)s)")

                if not settings.APPLICATION.get("IS_MULTILINGUAL", False):
                    title = "Notifikation gesendet an {0} ({1})".format(
                        ", ".join([self._recipient_log(r) for r in recipients]), subject
                    )

                create_history_entry(
                    instance,
                    user,
                    title,
                    lambda lang: {
                        "receiver": ", ".join(
                            [self._recipient_log(r) for r in recipients]
                        ),
                        "subject": subject,
                    },
                    HistoryActionConfig.HISTORY_TYPE_NOTIFICATION,
                    body,
                )

        self._send_mails(emails, connection)

        for fn in post_send:
            fn(instance)

        return len(emails)

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
