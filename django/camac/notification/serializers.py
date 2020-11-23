from collections import namedtuple
from datetime import date, timedelta
from html import escape
from logging import getLogger

import inflection
import jinja2
from django.conf import settings
from django.core.mail import EmailMessage
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
from camac.core.translations import get_translations
from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import HistoryEntry, HistoryEntryT, Instance
from camac.instance.validators import transform_coordinates
from camac.user.models import Group, Role, Service
from camac.user.utils import unpack_service_emails
from camac.utils import flatten, get_responsible_koor_service_id

from ..core import models as core_models
from . import models

request_logger = getLogger("django.request")


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
    billing_total_kommunal = serializers.SerializerMethodField()
    billing_total_kanton = serializers.SerializerMethodField()
    billing_total = serializers.SerializerMethodField()
    my_activations = serializers.SerializerMethodField()

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

    def _get_first_available_answer(self, instance, cqi_list):
        """Return the value of the first answer found in the given list.

        The CQI list is a list of 3-tuples which represent a Camac
        chapter, question, item. The first triplet to that results in
        a matching answer for our instance is returned.
        """
        for cqi in cqi_list:
            try:
                return Answer.get_value_by_cqi(instance, *cqi, fail_on_not_found=True)

            except Answer.DoesNotExist:
                continue
        return ""

    def get_vorhaben(self, instance):
        proposal = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_PROPOSAL
        )
        description = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_PROPOSAL_DESCRIPTION
        )
        return ", ".join(filter(None, [proposal, description]))

    def get_parzelle(self, instance):
        return self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_PARZELLE
        )

    def get_street(self, instance):
        return self._get_first_available_answer(instance, uri_constants.CQI_FOR_STREET)

    def get_gesuchsteller(self, instance):
        organisation = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_APPLICANT_ORGANISATION
        )
        name = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_APPLICANT_NAME
        )
        street = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_APPLICANT_STREET
        )
        city = self._get_first_available_answer(
            instance, uri_constants.CQI_FOR_APPLICANT_ZIP_CITY
        )

        return ", ".join(filter(None, [organisation, name, street, city]))

    def get_activation(self, instance):
        if not hasattr(self, "activation"):
            return None
        return ActivationMergeSerializer(self.activation).data

    def get_rejection_feedback(self, instance):  # pragma: no cover
        return Answer.get_value_by_cqi(instance, 20001, 20037, 1, default="")

    def get_answer_period_date(self, instace):
        answer_period_date = date.today() + timedelta(days=settings.MERGE_ANSWER_PERIOD)
        return answer_period_date.strftime(settings.MERGE_DATE_FORMAT)

    def get_publication_date(self, instance):
        publication_entry = instance.publication_entries.first()

        return (
            publication_entry
            and publication_entry.publication_date.strftime(settings.MERGE_DATE_FORMAT)
            or ""
        )

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
        try:
            return Answer.get_value_by_cqi(instance, 2, 6, 1, fail_on_not_found=True)
        except Answer.DoesNotExist:
            return "-"

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
            return entry.workflow_date.strftime(settings.MERGE_DATE_FORMAT)
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
        fields = ("slug", "purpose", "subject", "body", "type")


class NotificationTemplateMergeSerializer(
    InstanceEditableMixin, serializers.Serializer
):
    instance_editable_permission = None
    """
    No specific permission needed to send notificaion
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
            "activation_deadline_today",
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
                Service.objects.filter(groups__in=groups)
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

        services = Service.objects.filter(pk__in=activations.values("service_id"))

        return [
            {"to": email}
            for value in services.values_list("email", flat=True)
            if value
            for email in value.split(",")
        ]

    def _notify_service(self, service_id):
        return [
            {"to": email}
            for email in unpack_service_emails(Service.objects.filter(pk=service_id))
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

    def _get_recipients_caluma_municipality(self, instance):
        municipality_service_id = CalumaApi().get_municipality(instance)

        if not municipality_service_id:  # pragma: no cover
            raise exceptions.ValidationError(
                f"Could not get Caluma municipality for instance {instance.pk}"
            )

        return self._get_responsible(
            instance, Service.objects.filter(pk=municipality_service_id).first()
        )

    def _get_recipients_applicant(self, instance):
        return [
            {"to": applicant.invitee.email}
            for applicant in instance.involved_applicants.all()
            if applicant.invitee
        ]

    def _get_recipients_activation_deadline_today(self, instance):
        """Return recipients of activations for an instance which  deadline expires exactly today."""
        activations = Activation.objects.filter(
            ~Q(circulation_state__name="DONE"),
            deadline_date__date=date.today(),
            circulation__instance__instance_state__name="circulation",
            circulation__instance=instance,
        )
        services = {a.service for a in activations}
        return flatten(
            [self._get_responsible(instance, service) for service in services]
        )

    def _get_responsible(self, instance, service):
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
            circulation__instance_id=instance.pk, email_sent=0, service_parent=service
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
        return recipient["to"] + (
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

        instance = validated_data["instance"]

        slug = CalumaApi().get_form_slug(instance)

        result = 0

        for recipient_type in sorted(validated_data["recipient_types"]):
            recipients = getattr(self, "_get_recipients_%s" % recipient_type)(instance)
            subject = subj_prefix + validated_data["subject"]
            body = body_prefix + validated_data["body"]
            if recipient_type != "applicant" and slug in settings.ECH_EXCLUDED_FORMS:
                body = (
                    body_prefix
                    + settings.EMAIL_PREFIX_BODY_SPECIAL_FORMS
                    + validated_data["body"]
                )

            valid_recipients = [r for r in recipients if r.get("to")]
            for recipient in valid_recipients:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    # EmailMessage needs "to" and "cc" to be lists
                    **{
                        k: [e.strip() for e in email.split(",")]
                        for (k, email) in recipient.items()
                        if email
                    },
                )

                result += email.send()

                request_logger.info(
                    f'Sent email "{subject}" to {self._recipient_log(recipient)}'
                )

            getattr(self, f"_post_send_{recipient_type}", lambda i: None)(instance)

            # If no request context was provided to the serializer we assume the
            # mail delivery is part of a batch job initalized by the system
            # operation user.

            if self.context:
                user = self.context["request"].user
            else:
                user = (
                    Role.objects.get(name__iexact="support")
                    .groups.order_by("group_id")
                    .first()
                    .users.first()
                )

            if settings.APPLICATION_NAME in (
                "kt_bern",
                "kt_schwyz",
                "demo",
            ):  # pragma: no cover
                recipients_log = ", ".join([self._recipient_log(r) for r in recipients])

                history_entry = HistoryEntry.objects.create(
                    instance=instance,
                    title=f"Notifikation gesendet an {recipients_log} ({subject})",
                    body=body,
                    created_at=timezone.now(),
                    user=user,
                    history_type=HistoryActionConfig.HISTORY_TYPE_NOTIFICATION,
                )
                for (lang, text) in get_translations(
                    gettext_noop("Notification sent to %(receiver)s (%(subject)s)")
                ):
                    HistoryEntryT.objects.create(
                        history_entry=history_entry,
                        title=text % {"receiver": recipients_log, "subject": subject},
                        body=body,
                        language=lang,
                    )

        return result

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
