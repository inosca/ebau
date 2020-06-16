from math import trunc

import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from camac.caluma.api import CalumaApi
from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    INSTANCE_STATE_DONE,
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_FINISHED,
    INSTANCE_STATE_KOORDINATION,
    INSTANCE_STATE_REJECTED,
    INSTANCE_STATE_SB1,
    INSTANCE_STATE_SB2,
    INSTANCE_STATE_TO_BE_FINISHED,
    INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT,
    INSTANCE_STATE_ZIRKULATION,
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
from camac.user.models import Service
from camac.user.utils import set_baukontrolle

from .signals import (
    accompanying_report_send,
    change_responsibility,
    circulation_started,
    finished,
    ruling,
    task_send,
)
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
    def __init__(self, data, queryset, user, group, auth_header):
        self.data = data
        self.user = user
        self.group = group
        self.auth_header = auth_header
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

    def has_permission(self):
        return self.instance.responsible_service() == self.group.service, None

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(DocumentAccessibilityMixin, BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:
            return False, None

        if self.instance.instance_state.pk == INSTANCE_STATE_DOSSIERPRUEFUNG:
            if self.data.eventNotice.decisionRuling.judgement != 4:
                return (
                    False,
                    'For instances in the state "Dossierprüfung", only a NoticeRuling with judgement "4" is allowed.',
                )
            return True, None
        if self.instance.instance_state.pk not in [
            INSTANCE_STATE_KOORDINATION,
            INSTANCE_STATE_ZIRKULATION,
        ]:
            return (
                False,
                'NoticeRuling is only allowed for instances in the state "Dossierprüfung", "In Koordination" or "In Zirkulation".',
            )

        return True, None

    def apply(self):
        attachments = self.get_attachments(self.data.eventNotice.document)
        if not self.has_attachment_permissions(attachments):
            raise SendHandlerException(
                "You don't have permission for at least one document you provided.",
                status=403,
            )

        status = {
            1: INSTANCE_STATE_SB1,
            2: INSTANCE_STATE_SB1,
            3: INSTANCE_STATE_REJECTED,
            4: INSTANCE_STATE_REJECTED,
        }

        form_slug = CalumaApi().get_form_slug(self.instance)
        judgement = self.data.eventNotice.decisionRuling.judgement

        state_id = status[judgement]
        if form_slug.startswith("vorabklaerung"):
            state_id = INSTANCE_STATE_FINISHED

        try:
            decision = judgement_to_decision(judgement, form_slug)
        except KeyError:
            raise SendHandlerException(
                f'"{judgement}" is not a valid judgement for "{form_slug}"'
            )

        if state_id == INSTANCE_STATE_SB1:
            set_baukontrolle(self.instance)

        self.instance.instance_state = InstanceState.objects.get(pk=state_id)
        self.instance.save()
        # TODO: where should we write self.data.eventNotice.decisionRuling.ruling ?
        DocxDecision.objects.create(
            instance=self.instance.pk,
            decision=decision,
            decision_date=self.data.eventNotice.decisionRuling.date,
            decision_type="UNKNOWN_ECH",
        )

        self.link_to_section(attachments)

        ruling.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
        )


class ChangeResponsibilitySendHandler(BaseSendHandler):
    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if self.instance.instance_state.pk in [
            INSTANCE_STATE_SB1,
            INSTANCE_STATE_SB2,
            INSTANCE_STATE_TO_BE_FINISHED,
            INSTANCE_STATE_DONE,
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

        # no need for try/except here, as existence has already been assured
        # by `has_permission()`
        old_instance_service = InstanceService.objects.get(
            instance=self.instance, service=self.group.service
        )

        old_instance_service.active = 0
        old_instance_service.save()

        InstanceService.objects.create(
            instance=self.instance, service=new_service, active=1
        )

        change_responsibility.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
        )


class AccompanyingReportSendHandler(BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header):
        super().__init__(data, queryset, user, group, auth_header)
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
        if self.instance.instance_state.pk in [
            INSTANCE_STATE_SB1,
            INSTANCE_STATE_SB2,
            INSTANCE_STATE_TO_BE_FINISHED,
        ]:
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
        state = InstanceState.objects.get(pk=INSTANCE_STATE_FINISHED)
        self.instance.instance_state = state
        self.instance.save()
        finished.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
        )


class TaskSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return (
            self.data.eventRequest.planningPermissionApplicationIdentification.dossierIdentification
        )

    def has_permission(self):
        if not super().has_permission()[0]:  # pragma: no cover
            return False, None
        if not self.instance.instance_state.pk == INSTANCE_STATE_ZIRKULATION:
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
                pk=INSTANCE_STATE_ZIRKULATION
            )
            circulation = Circulation.objects.create(
                instance=self.instance,
                instance_resource_id=instance_resource.pk,
                name=trunc(timezone.now().timestamp()),
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
            service_parent=self.instance.active_service(),
            email_sent=0,
        )

    def apply(self):
        circulation = self._get_circulation()
        service = self._get_service()
        activation = self._create_activation(circulation, service)

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
    def __init__(self, data, queryset, user, group, auth_header):
        super().__init__(data, queryset, user, group, auth_header)
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

        if self.instance.instance_state.pk != INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT:
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
        instance_state = InstanceState.objects.get(pk=INSTANCE_STATE_ZIRKULATION)
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


def get_send_handler(data, instance, user, group, auth_header):
    return resolve_send_handler(data)(data, instance, user, group, auth_header)
