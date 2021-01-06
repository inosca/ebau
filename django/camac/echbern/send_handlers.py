from collections import namedtuple
from math import trunc

import pytz
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    INSTANCE_RESOURCE_ZIRKULATION,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
    NOTIFICATION_ECH,
)
from camac.core.models import (
    Activation,
    Circulation,
    CirculationState,
    DocxDecision,
    InstanceResource,
    InstanceService,
    Notice,
    NoticeType,
)
from camac.document.models import Attachment, AttachmentSection
from camac.instance.models import Instance, InstanceState
from camac.instance.serializers import CalumaInstanceChangeResponsibleServiceSerializer
from camac.user.models import Service

from .signals import accompanying_report_send, circulation_started, task_send
from .utils import judgement_to_decision


class SendHandlerException(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class DocumentAccessibilityMixin:
    def get_attachments(self, ech_documents):
        uuids = set([doc.uuid for doc in ech_documents])
        attachments = Attachment.objects.filter(uuid__in=uuids).distinct()
        if attachments.count() != len(uuids):
            attachment_uuids = set(attachments.values_list("uuid", flat=True))
            missing = ", ".join(uuids - attachment_uuids)
            raise SendHandlerException(
                f"No document found for uuids: {missing}.", status=404
            )
        return attachments

    def has_attachment_permissions(self, attachments):
        for attachment in attachments:
            if (
                self.instance != attachment.instance
                or attachment.instance.responsible_service() != self.group.service
            ):
                return False
        return True

    def link_to_section(self, attachments, target=ATTACHMENT_SECTION_ALLE_BETEILIGTEN):
        section_alle_beteiligten = AttachmentSection.objects.get(pk=target)
        for attachment in attachments:
            if not attachment.attachment_sections.filter(pk=target).exists():
                attachment.attachment_sections.add(section_alle_beteiligten)


class BaseSendHandler:
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        self.data = data
        self.user = user
        self.group = group
        self.auth_header = auth_header
        self.caluma_user = caluma_user
        self.instance = self._get_instance(queryset)

    def _get_instance(self, queryset):
        try:
            return queryset.get(pk=self.get_instance_id())
        except Instance.DoesNotExist:
            raise SendHandlerException("Unknown instance")

    def get_instance_id(self):
        return (
            self.data.eventNotice.planningPermissionApplicationIdentification.dossierIdentification
        )

    def get_case(self):
        return caluma_workflow_models.Case.objects.get(
            **{"meta__camac-instance-id": int(self.get_instance_id())}
        )

    def complete_work_item(self, task, context={}):
        return self._process_work_item("complete", task, context)

    def skip_work_item(self, task, context={}):
        return self._process_work_item("skip", task, context)

    def _process_work_item(self, action, task, context):
        fn = getattr(workflow_api, f"{action}_work_item")
        work_item = (
            self.get_case()
            .work_items.filter(
                task_id=task, status=caluma_workflow_models.WorkItem.STATUS_READY
            )
            .first()
        )

        if work_item and fn:
            fn(
                work_item=work_item,
                user=self.caluma_user,
                context={"group-id": self.group.pk, **context},
            )

    def has_permission(self):
        return self.instance.responsible_service() == self.group.service, None

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(DocumentAccessibilityMixin, BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:
            return False, None

        if self.instance.instance_state.name == "circulation_init":
            if self.data.eventNotice.decisionRuling.judgement != 4:
                return (
                    False,
                    'For instances in the state "Zirkulation initialisieren", only a NoticeRuling with judgement "4" is allowed.',
                )
            return True, None
        if self.instance.instance_state.name not in ["coordination", "circulation"]:
            return (
                False,
                'NoticeRuling is only allowed for instances in the state "In Koordination" or "In Zirkulation".',
            )

        return True, None

    def apply(self):
        attachments = self.get_attachments(self.data.eventNotice.document)
        if not self.has_attachment_permissions(attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        workflow_slug = self.get_case().workflow_id
        judgement = self.data.eventNotice.decisionRuling.judgement

        try:
            decision = judgement_to_decision(judgement, workflow_slug)
        except KeyError:
            raise SendHandlerException(
                f'"{judgement}" is not a valid judgement for "{workflow_slug}"'
            )

        # TODO: where should we write self.data.eventNotice.decisionRuling.ruling ?
        DocxDecision.objects.create(
            instance=self.instance.pk,
            decision=decision,
            decision_date=self.data.eventNotice.decisionRuling.date,
            decision_type="UNKNOWN_ECH",
        )

        # we might have a running circulation, skip it
        self.skip_work_item("circulation")
        self.skip_work_item("start-decision")
        # if we don't have one, skip the whole circulation
        self.skip_work_item("skip-circulation")

        # this handle status changes and assignment of the construction control
        # for "normal" judgements
        self.complete_work_item("decision")

        self.link_to_section(attachments)


class ChangeResponsibilitySendHandler(BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if self.instance.instance_state.name in [
            "sb1",
            "sb2",
            "conclusion",
            "finished",
        ]:
            return (
                False,
                (
                    "Changing responsibility is not possible after the building permit has been issued.",
                ),
            )
        return True, None

    def get_instance_id(self):
        return (
            self.data.eventChangeResponsibility.planningPermissionApplicationIdentification.dossierIdentification
        )

    def apply(self):
        new_service_id = (
            self.data.eventChangeResponsibility.responsibleDecisionAuthority.decisionAuthority.buildingAuthorityIdentificationType.localOrganisationId.organisationId
        )

        try:
            new_service = Service.objects.get(pk=new_service_id)
        except Service.DoesNotExist:
            raise SendHandlerException("Unknown target service!")

        data = {
            "service_type": "municipality",
            "to": {"id": new_service.pk, "type": "services"},
        }

        Request = namedtuple(
            "Request", ["user", "group", "caluma_info", "query_params"]
        )
        CalumaInfo = namedtuple("CalumaInfo", "context")
        Context = namedtuple("Context", "user")
        request = Request(
            self.user, self.group, CalumaInfo(Context(self.caluma_user)), {}
        )

        serializer = CalumaInstanceChangeResponsibleServiceSerializer(
            self.instance, data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class AccompanyingReportSendHandler(BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        super().__init__(data, queryset, user, group, auth_header, caluma_user)
        self.activation = self._get_activation()

    def has_permission(self):
        if bool(self.activation):
            return True, None
        return False, "There is no running activation for your service."

    def get_instance_id(self):
        return (
            self.data.eventAccompanyingReport.planningPermissionApplicationIdentification.dossierIdentification
        )

    def _get_documents(self):
        uuids = [d.uuid for d in self.data.eventAccompanyingReport.document]
        attachments = Attachment.objects.filter(uuid__in=uuids)
        if not attachments:
            raise SendHandlerException("Unknown document!")
        return attachments

    def _get_activation(self):
        service = self.group.service
        return (
            Activation.objects.filter(
                circulation__instance=self.instance,
                circulation_state__name="RUN",
                service=service,
            )
            .order_by("-circulation__pk")
            .first()
        )

    def apply(self):
        documents = self._get_documents()

        self.activation.circulation_state = CirculationState.objects.get(name="DONE")
        self.activation.save()

        CalumaApi().sync_circulation(self.activation.circulation, self.caluma_user)

        answer = "; ".join(self.data.eventAccompanyingReport.remark)
        clause = "; ".join(self.data.eventAccompanyingReport.ancillaryClauses)
        stellungnahme = NoticeType.objects.get(pk=NOTICE_TYPE_STELLUNGNAHME)
        nebenbestimmung = NoticeType.objects.get(pk=NOTICE_TYPE_NEBENBESTIMMUNG)

        Notice.objects.create(
            notice_type=stellungnahme, activation=self.activation, content=answer
        )

        Notice.objects.create(
            notice_type=nebenbestimmung, activation=self.activation, content=clause
        )

        accompanying_report_send.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
            attachments=documents,
            context={"activation-id": self.activation.pk},
        )


class CloseArchiveDossierSendHandler(BaseSendHandler):
    def has_permission(self):
        if not InstanceService.objects.filter(
            instance=self.instance, active=True, service=self.group.service
        ).exists():
            return False, None
        if self.instance.instance_state.name in ["sb1", "sb2", "conclusion"]:
            return True, None
        return (
            False,
            (
                '"CloseDossier" is only allowed for instances in the states '
                '"Selbstdeklaration (SB1)", "Abschluss (SB2)" and "Zum Abschluss".'
            ),
        )

    def get_instance_id(self):
        return (
            self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.dossierIdentification
        )

    def apply(self):
        self.skip_work_item("sb1")
        self.skip_work_item("sb2")
        self.complete_work_item("complete")


class TaskSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return (
            self.data.eventRequest.planningPermissionApplicationIdentification.dossierIdentification
        )

    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if not self.instance.instance_state.name == "circulation":
            return (
                False,
                'You can only send a "Task" for instances in the state "In Zirkulation".',
            )
        return True, None

    def _get_circulation(self):
        # we add the Activation to the most recent Circulation or start a new one
        circulation = (
            Circulation.objects.filter(instance=self.instance).order_by("-pk").first()
        )
        if not circulation:
            instance_resource = InstanceResource.objects.get(
                pk=INSTANCE_RESOURCE_ZIRKULATION
            )
            circulation = Circulation.objects.create(
                service=self.instance.responsible_service(filter_type="municipality"),
                instance=self.instance,
                instance_resource_id=instance_resource.pk,
                name=trunc(timezone.now().timestamp()),
            )
            self.complete_work_item(
                "init-circulation", {"circulation-id": circulation.pk}
            )
        return circulation

    def _get_service(self):
        try:
            return Service.objects.get(
                pk=int(
                    self.data.eventRequest.extension.wildcardElements()[
                        0
                    ].firstChild.value
                )
            )
        except (ValueError, Service.DoesNotExist):
            raise SendHandlerException("Unknown service!")

    def _create_activation(self, circulation, service):
        circulation_state = CirculationState.objects.get(pk=1)
        try:
            deadline_date_raw = self.data.eventRequest.directive.deadline
            deadline_date = deadline_date_raw.astimezone(pytz.UTC) + timezone.timedelta(
                hours=4
            )  # add 4 hours to prevent timezone problems
        # Fallback for messages with missing `directive`
        except AttributeError:  # pragma: no cover
            deadline_date = timezone.now().replace(
                hour=4, minute=0, second=0, microsecond=0
            ) + timezone.timedelta(weeks=4)

        start_date = timezone.now().replace(hour=4, minute=0, second=0, microsecond=0)

        return Activation.objects.create(
            circulation=circulation,
            service=service,
            start_date=start_date,
            deadline_date=deadline_date,
            version=1,
            circulation_state=circulation_state,
            service_parent=self.instance.responsible_service(
                filter_type="municipality"
            ),
            email_sent=0,
        )

    def apply(self):
        circulation = self._get_circulation()
        service = self._get_service()
        activation = self._create_activation(circulation, service)

        CalumaApi().sync_circulation(circulation, self.caluma_user)

        task_send.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
        )

        mail_data = {
            "data": {
                "type": "notification-template-sendmails",
                "id": None,
                "attributes": {
                    "template-slug": NOTIFICATION_ECH,
                    "recipient-types": ["unnotified_service"],
                },
                "relationships": {
                    "instance": {"data": {"type": "instances", "id": self.instance.pk}},
                    "activation": {
                        "data": {"type": "activations", "id": activation.pk}
                    },
                },
            }
        }
        url = reverse("notificationtemplate-sendmail")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        client.force_authenticate(user=self.user)
        resp = client.post(url, data=mail_data)
        if not resp.status_code == 204:
            raise SendHandlerException("Failed to send mails!")


class NoticeKindOfProceedingsSendHandler(DocumentAccessibilityMixin, TaskSendHandler):
    def __init__(self, data, queryset, user, group, auth_header, caluma_user):
        super().__init__(data, queryset, user, group, auth_header, caluma_user)
        self.attachments = self.get_attachments(
            self.data.eventKindOfProceedings.document
        )

    def get_instance_id(self):
        return (
            self.data.eventKindOfProceedings.planningPermissionApplicationIdentification.dossierIdentification
        )

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False, None

        if self.instance.instance_state.name != "circulation_init":
            return (
                False,
                'You can only send a "NoticeKindOfProceedings" for instances in the state "Zirkulation initialisieren".',
            )

        return True, None

    def apply(self):
        attachments = self.get_attachments(self.data.eventKindOfProceedings.document)

        if not self.has_attachment_permissions(attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        circulation = self._get_circulation()
        instance_state = InstanceState.objects.get(name="circulation")
        self.instance.instance_state = instance_state
        self.instance.save()

        circulation_started.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
        )

        self.link_to_section(attachments)

        return circulation


def resolve_send_handler(data):
    handler_mapping = {
        "eventAccompanyingReport": AccompanyingReportSendHandler,
        "eventChangeResponsibility": ChangeResponsibilitySendHandler,
        "eventCloseArchiveDossier": CloseArchiveDossierSendHandler,
        "eventNotice": NoticeRulingSendHandler,
        "eventRequest": TaskSendHandler,
        "eventKindOfProceedings": NoticeKindOfProceedingsSendHandler,
    }
    for event in handler_mapping:
        if getattr(data, event) is not None:
            return handler_mapping[event]
    raise SendHandlerException("Message type not supported!")


def get_send_handler(data, instance, user, group, auth_header, caluma_user):
    return resolve_send_handler(data)(
        data, instance, user, group, auth_header, caluma_user
    )
