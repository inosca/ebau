from collections import namedtuple
from datetime import date, timedelta
from html import escape
from logging import getLogger

import inflection
import jinja2
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.translation import gettext_noop
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_json_api import serializers

from camac.caluma import CalumaSerializerMixin
from camac.constants import kt_bern as be_constants
from camac.core.models import Activation, Answer, Journal, JournalT
from camac.core.translations import get_translations
from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.user.models import Service
from camac.utils import flatten

from ..core import models as core_models
from . import models

request_logger = getLogger("django.request")


class NoticeMergeSerializer(serializers.Serializer):
    service = serializers.StringRelatedField(source="activation.service")
    notice_type = serializers.StringRelatedField()
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
    activations = ActivationMergeSerializer(many=True)
    billing_entries = BillingEntryMergeSerializer(many=True)
    answer_period_date = serializers.SerializerMethodField()
    publication_date = serializers.SerializerMethodField()
    instance_id = serializers.IntegerField()
    public_dossier_link = serializers.SerializerMethodField()
    internal_dossier_link = serializers.SerializerMethodField()
    registration_link = serializers.SerializerMethodField()
    leitbehoerde_name = serializers.SerializerMethodField()
    form_name = serializers.SerializerMethodField()
    ebau_number = serializers.SerializerMethodField()
    base_url = serializers.SerializerMethodField()
    rejection_feedback = serializers.SerializerMethodField()

    # TODO: these is currently bern specific, as it depends on instance state
    # identifiers. This will likely need some client-specific switch logic
    # some time in the future
    total_activations = serializers.SerializerMethodField()
    completed_activations = serializers.SerializerMethodField()
    pending_activations = serializers.SerializerMethodField()

    def __init__(self, instance, *args, escape=False, **kwargs):
        self.escape = escape
        instance.activations = Activation.objects.filter(circulation__instance=instance)
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

    def get_rejection_feedback(self, instance):  # pragma: no cover
        feedback = Answer.objects.filter(
            instance=instance, chapter=20001, question=20037, item=1
        ).first()
        if feedback:
            return feedback.answer
        return ""

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
        return instance.active_service or "-"

    def get_form_name(self, instance):
        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            return instance.form.get_name()
        try:
            caluma_resp = requests.post(
                settings.CALUMA_URL,
                json={
                    "query": """,
                        query GetMainFormName($instanceId: GenericScalar!) {
                          allDocuments(metaValue: [{ key: "camac-instance-id", value: $instanceId}]) {
                            edges {
                              node {
                                id
                                form {
                                  name
                                  meta
                                }
                              }
                            }
                          }
                        }
                    """,
                    "variables": {"instanceId": instance.pk},
                },
                headers={
                    "Authorization": get_authorization_header(self.context["request"])
                },
            )
            documents = caluma_resp.json()["data"]["allDocuments"]["edges"]
            form_names = [
                doc["node"]["form"]["name"]
                for doc in documents
                if doc["node"]["form"]["meta"].get("is-main-form") is True
            ]
            return form_names[0]
        except (KeyError, IndexError):  # pragma: no cover
            request_logger.error(
                "get_form_name(): Caluma did not respond with a valid response"
            )
            return "-"

    def get_ebau_number(self, instance):
        if settings.APPLICATION["FORM_BACKEND"] != "caluma":
            return "-"

        try:
            resp = requests.post(
                settings.CALUMA_URL,
                json={
                    "query": """,
                        query GetEbauNumber($instanceId: GenericScalar!) {
                          allDocuments(
                            metaHasKey: "ebau-number"
                            metaValue: [{ key: "camac-instance-id", value: $instanceId}]
                          ) {
                            edges {
                              node {
                                id
                                form {
                                  name
                                  meta
                                }
                                meta
                              }
                            }
                          }
                        }
                    """,
                    "variables": {"instanceId": instance.pk},
                },
                headers={
                    "Authorization": get_authorization_header(self.context["request"])
                },
            )

            return resp.json()["data"]["allDocuments"]["edges"][0]["node"]["meta"][
                "ebau-number"
            ]
        except (KeyError, IndexError):  # pragma: no cover
            return "-"

    def get_internal_dossier_link(self, instance):
        return settings.INTERNAL_INSTANCE_URL_TEMPLATE.format(
            internal_base_url=settings.INTERNAL_BASE_URL, instance_id=(instance.pk)
        )

    def get_public_dossier_link(self, instance):
        return settings.PUBLIC_INSTANCE_URL_TEMPLATE.format(
            public_base_url=settings.PUBLIC_BASE_URL, instance_id=(instance.pk)
        )

    def get_registration_link(self, instance):
        return settings.REGISTRATION_URL

    def get_base_url(self, instance):
        return settings.INTERNAL_BASE_URL

    def _activations(self, instance):
        return core_models.Activation.objects.filter(circulation__instance=instance)

    def get_total_activations(self, instance):
        return self._activations(instance).count()

    def get_completed_activations(self, instance):
        return (
            self._activations(instance)
            .filter(circulation_state_id=be_constants.CIRCULATION_STATE_DONE)
            .count()
        )

    def get_pending_activations(self, instance):
        return (
            self._activations(instance)
            .filter(circulation_state_id=be_constants.CIRCULATION_STATE_WORKING)
            .count()
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field in instance.fields.all():
            name = inflection.underscore("field-" + field.name)
            ret[name] = field.value

        if self.escape:
            ret = self._escape(ret)

        return ret


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
        validated_data["service"] = self.context["request"].group.service
        return super().create(validated_data)

    class Meta:
        model = models.NotificationTemplate
        fields = ("purpose", "subject", "body", "type")


class NotificationTemplateMergeSerializer(
    InstanceEditableMixin, serializers.Serializer
):
    instance_editable_permission = None
    """
    No specific permission needed to send notificaion
    """

    instance = serializers.ResourceRelatedField(queryset=Instance.objects.all())
    notification_template = serializers.ResourceRelatedField(
        queryset=models.NotificationTemplate.objects.all()
    )
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)

    def _merge(self, value, instance):
        try:
            value_template = jinja2.Template(value)
            data = InstanceMergeSerializer(instance, context=self.context).data

            # some cantons use uppercase placeholders. be as compatible as possible
            data.update({k.upper(): v for k, v in data.items()})
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def validate(self, data):
        notification_template = data["notification_template"]
        instance = data["instance"]

        data["subject"] = self._merge(
            data.get("subject", notification_template.get_trans_attr("subject")),
            instance,
        )
        data["body"] = self._merge(
            data.get("body", notification_template.get_trans_attr("body")), instance
        )
        data["pk"] = "{0}-{1}".format(notification_template.pk, instance.pk)

        return data

    def create(self, validated_data):
        NotificationTemplateMerge = namedtuple(
            "NotificationTemplateMerge", validated_data.keys()
        )
        obj = NotificationTemplateMerge(**validated_data)

        return obj

    class Meta:
        resource_name = "notification-template-merges"


class NotificationTemplateSendmailSerializer(
    NotificationTemplateMergeSerializer, CalumaSerializerMixin
):
    recipient_types = serializers.MultipleChoiceField(
        choices=(
            "applicant",
            "municipality",
            "caluma_municipality",
            "service",
            "unnotified_service",
            "leitbehoerde",
            "construction_control",
            "email_list",
        )
    )
    email_list = serializers.CharField(required=False)

    def _get_recipients_caluma_municipality(self, instance):  # pragma: no cover

        resp = self.query_caluma(
            """
            query GetMuniciaplity($instanceId: GenericScalar!) {
              allDocuments(metaValue: [{key: "camac-instance-id", value: $instanceId}]) {
                edges {
                  node {
                    answers(question: "gemeinde") {
                      edges {
                        node {
                          ...on StringAnswer {
                            value
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            """,
            {"instanceId": instance.pk},
        )

        municipality_service_id = int(
            resp["data"]["allDocuments"]["edges"][0]["node"]["answers"]["edges"][0][
                "node"
            ]["value"]
        )

        service = Service.objects.filter(pk=municipality_service_id).first()

        return [service.email]

    def _get_recipients_applicant(self, instance):
        return [
            {"to": applicant.invitee.email}
            for applicant in instance.involved_applicants.all()
            if applicant.invitee
        ]

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
        return self._get_responsible(instance, instance.active_service)

    def _get_recipients_municipality(self, instance):
        return self._get_responsible(instance, instance.group.service)

    def _get_recipients_unnotified_service(self, instance):
        activations = Activation.objects.filter(
            circulation__instance_id=instance.pk, email_sent=0
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

    def _recipient_log(self, recipient):
        return recipient["to"] + (
            f" (CC: {recipient['cc']})" if "cc" in recipient else ""
        )

    def create(self, validated_data):
        subj_prefix = settings.EMAIL_PREFIX_SUBJECT
        body_prefix = settings.EMAIL_PREFIX_BODY

        instance = validated_data["instance"]

        for recipient_type in sorted(validated_data["recipient_types"]):
            recipients = getattr(self, "_get_recipients_%s" % recipient_type)(instance)
            subject = subj_prefix + validated_data["subject"]
            body = body_prefix + validated_data["body"]

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

                result = email.send()

                request_logger.info(
                    f'Sent email "{subject}" to {self._recipient_log(recipient)}'
                )

            if settings.APPLICATION_NAME == "kt_bern":  # pragma: no cover
                journal_entry = Journal.objects.create(
                    instance=instance,
                    mode="auto",
                    additional_text=body,
                    created=timezone.now(),
                    user=self.context["request"].user,
                )
                for (lang, text) in get_translations(
                    gettext_noop("Notification sent to %(receiver)s (%(subject)s)")
                ):
                    recipients_log = ", ".join(
                        [self._recipient_log(r) for r in recipients]
                    )
                    JournalT.objects.create(
                        journal=journal_entry,
                        text=text % {"receiver": recipients_log, "subject": subject},
                        additional_text=body,
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

    def validate_instance(self, instance):
        return instance
