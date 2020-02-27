from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.models import Answer
from caluma.caluma_form.schema import SaveDocumentStringAnswer

from camac.caluma.api import CamacRequest
from camac.echbern.signals import file_subsequently
from camac.instance.models import Instance
from camac.notification.serializers import NotificationTemplateSendmailSerializer

CLAIM_QUESTION = "nfd-tabelle-table"
CLAIM_STATUS_QUESTION = "nfd-tabelle-status"
CLAIM_STATUS_IN_PROGRESS = "nfd-tabelle-status-in-bearbeitung"
CLAIM_STATUS_ANSWERED = "nfd-tabelle-status-beantwortet"

NOTIFICATION_CLAIM_IN_PROGRESS = 31
NOTIFICATION_CLAIM_ANSWERED = 32


class CustomValidation(BaseValidation):
    def _send_claim_notification(self, info, instance, template_id, recipient_types):
        mail_data = {
            "instance": {"type": "instances", "id": instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": template_id,
            },
            "recipient_types": recipient_types,
        }

        mail_serializer = NotificationTemplateSendmailSerializer(
            instance, mail_data, context={"request": CamacRequest(info).request}
        )

        if not mail_serializer.is_valid():
            raise Exception()

        mail_serializer.create(mail_serializer.validated_data)

    def _send_claim_ech_event(self, info, instance):
        file_subsequently.send(
            sender=self.__class__,
            instance=instance,
            user_pk=None,  # Not needed, hence not querying for it
            group_pk=None,  # Not needed, hence not querying for it
        )

    @validation_for(SaveDocumentStringAnswer)
    def validate_save_document_string_answer(self, mutation, data, info):
        if data["question"].slug == CLAIM_STATUS_QUESTION:
            instance_id = data["document"].family.meta["camac-instance-id"]
            instance = Instance.objects.get(pk=instance_id)
            new_status = data["value"]

            try:
                old_status = (
                    data["document"].answers.get(question=CLAIM_STATUS_QUESTION).value
                )
            except Answer.DoesNotExist:
                old_status = None

            if old_status and new_status == old_status:
                # the status did not change, no further action
                return data

            if new_status == CLAIM_STATUS_IN_PROGRESS:
                # claim is now in progress, inform the applicant
                self._send_claim_notification(
                    info, instance, NOTIFICATION_CLAIM_IN_PROGRESS, ["applicant"]
                )

            if new_status == CLAIM_STATUS_ANSWERED:
                # claim is answered, inform the active service and create an
                # eCH event
                self._send_claim_notification(
                    info, instance, NOTIFICATION_CLAIM_ANSWERED, ["leitbehoerde"]
                )
                self._send_claim_ech_event(info, instance)

        return data
