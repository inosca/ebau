import sys

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from camac.constants.kt_bern import (
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_FINISHED,
    INSTANCE_STATE_KOORDINATION,
    INSTANCE_STATE_REJECTED,
    INSTANCE_STATE_ZIRKULATION,
)
from camac.core.models import (
    Activation,
    Circulation,
    CirculationState,
    DocxDecision,
    InstanceResource,
    InstanceService,
)
from camac.document.models import Attachment
from camac.instance.models import Instance, InstanceState
from camac.user.models import Service

from .data_preparation import get_form_slug
from .signals import accompanying_report_send, task_send

ECH_MESSAGE_MAPPING = {
    "5100004": "AccompanyingReport",
    "5100010": "NoticeRuling",
    "5100011": "ChangeResponsibility",
    "5100013": "CloseDossier",
}


class SendHandlerException(Exception):
    pass


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
        return self.data.eventNotice.planningPermissionApplicationIdentification.localID[
            0
        ].Id

    def has_permission(self):
        if not self.instance.active_service == self.group.service:
            return False
        return True

    def apply(self):  # pragma: no cover
        raise NotImplementedError()


class NoticeRulingSendHandler(BaseSendHandler):
    def has_permission(self):
        if not super().has_permission():
            return False
        if self.instance.instance_state.pk == INSTANCE_STATE_DOSSIERPRUEFUNG:
            if self.data.eventNotice.decisionRuling.judgement == 4:
                return True
            return False
        if not self.instance.instance_state.pk == INSTANCE_STATE_KOORDINATION:
            return False
        return True

    def apply(self):
        status = {
            1: INSTANCE_STATE_FINISHED,
            2: INSTANCE_STATE_FINISHED,
            3: INSTANCE_STATE_REJECTED,
            4: INSTANCE_STATE_REJECTED,
        }
        decision = {1: "accepted", 3: "writtenOff", 4: "denied"}
        form_slug = get_form_slug(self.instance, self.group.pk, self.auth_header)
        if form_slug.startswith("vorabklaerung"):
            decision = {1: "positive", 2: "conditionallyPositive", 4: "negative"}

        judgement = self.data.eventNotice.decisionRuling.judgement

        state_id = status[judgement]
        try:
            decision = decision[judgement]
        except KeyError:
            raise SendHandlerException(
                f'"{judgement}" is not a valid judgement for "{form_slug}"'
            )

        self.instance.instance_state = InstanceState.objects.get(pk=state_id)
        self.instance.save()
        # TODO: where should we write self.data.eventNotice.decisionRuling.ruling ?
        DocxDecision.objects.create(
            instance=self.instance.pk,
            decision=decision,
            decision_date=timezone.now().date(),
        )


class ChangeResponsibilitySendHandler(BaseSendHandler):
    def get_instance_id(self):
        return self.data.eventChangeResponsibility.planningPermissionApplicationIdentification.localID[
            0
        ].Id

    def apply(self):
        old_id = (
            self.data.eventChangeResponsibility.entryOffice.entryOfficeIdentification.localOrganisationId.organisationId
        )
        new_id = (
            self.data.eventChangeResponsibility.responsibleDecisionAuthority.decisionAuthority.buildingAuthorityIdentificationType.localOrganisationId.organisationId
        )

        try:
            new_service = Service.objects.get(pk=new_id)
            old_instance_service = InstanceService.objects.get(
                instance=self.instance, service__pk=old_id
            )
        except (Service.DoesNotExist, InstanceService.DoesNotExist):
            raise SendHandlerException("Unknown service!")

        old_instance_service.active = 0
        old_instance_service.save()

        InstanceService.objects.create(
            instance=self.instance, service=new_service, active=1
        )


class AccompanyingReportSendHandler(BaseSendHandler):
    def __init__(self, data, queryset, user, group, auth_header):
        super().__init__(data, queryset, user, group, auth_header)
        self.activation = self._get_activation()

    def has_permission(self):
        return bool(self.activation)

    def get_instance_id(self):
        return self.data.eventAccompanyingReport.planningPermissionApplicationIdentification.localID[
            0
        ].Id

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

        accompanying_report_send.send(
            sender=self.__class__,
            instance=self.instance,
            user_pk=self.user.pk,
            group_pk=self.group.pk,
            attachments=documents,
        )


class CloseDossierSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.localID[
            0
        ].Id

    def apply(self):
        state = InstanceState.objects.get(pk=INSTANCE_STATE_FINISHED)
        self.instance.instance_state = state
        self.instance.save()


class TaskSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return self.data.eventRequest.planningPermissionApplicationIdentification.localID[
            0
        ].Id

    def has_permission(self):
        if not super().has_permission():  # pragma: no cover
            return False
        if not self.instance.instance_state.pk == INSTANCE_STATE_ZIRKULATION:
            return False
        return True

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
                instance=self.instance, instance_resource_id=instance_resource.pk
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
        return Activation.objects.create(
            circulation=circulation,
            service=service,
            start_date=timezone.now(),
            deadline_date=timezone.now() + timezone.timedelta(weeks=4),
            version=1,
            circulation_state=circulation_state,
            service_parent=self.instance.active_service,
            email_sent=0,
        )

    def apply(self):
        circulation = self._get_circulation()
        service = self._get_service()
        self._create_activation(circulation, service)

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
                "attributes": {"recipient-types": ["unnotified_service"]},
                "relationships": {
                    "instance": {"data": {"type": "instances", "id": self.instance.pk}}
                },
            }
        }
        url = reverse("notificationtemplate-sendmail", args=[11])
        client = APIClient()
        client.force_authenticate(user=self.user)
        resp = client.post(url, data=mail_data)
        if not resp.status_code == 204:
            raise SendHandlerException("Failed to send mails!")

        # This doesn't happen in the NotificationTemplateSendmailSerializer but in php (ffs!). So we do it here.
        activations = Activation.objects.filter(
            circulation__instance_id=self.instance.pk, email_sent=0
        )
        for a in activations:
            a.email_sent = 1
            a.save()


def get_send_handler(data, instance, user, group, auth_header):
    try:
        prefix = ECH_MESSAGE_MAPPING[data.deliveryHeader.messageType]
    except KeyError:
        raise SendHandlerException("Message type not implemented!")
    sh = getattr(sys.modules[__name__], f"{prefix}SendHandler")(
        data, instance, user, group, auth_header
    )
    return sh
