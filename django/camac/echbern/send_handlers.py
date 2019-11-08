import sys

from django.utils import timezone

from camac.constants.kt_bern import (
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_FINISHED,
    INSTANCE_STATE_KOORDINATION,
    INSTANCE_STATE_REJECTED,
)
from camac.core.models import DocxDecision, InstanceService
from camac.instance.models import Instance, InstanceState
from camac.user.models import Service

from .data_preparation import get_form_slug

ECH_MESSAGE_MAPPING = {
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


class CloseDossierSendHandler(BaseSendHandler):
    def get_instance_id(self):
        return self.data.eventCloseArchiveDossier.planningPermissionApplicationIdentification.localID[
            0
        ].Id

    def apply(self):
        state = InstanceState.objects.get(pk=INSTANCE_STATE_FINISHED)
        self.instance.instance_state = state
        self.instance.save()


def get_send_handler(data, instance, user, group, auth_header):
    try:
        prefix = ECH_MESSAGE_MAPPING[data.deliveryHeader.messageType]
    except KeyError:
        raise SendHandlerException("Message type not implemented!")
    sh = getattr(sys.modules[__name__], f"{prefix}SendHandler")(
        data, instance, user, group, auth_header
    )
    return sh
