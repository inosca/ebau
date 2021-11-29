from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.models import Answer
from caluma.caluma_form.schema import SaveDocumentStringAnswer

from camac.caluma.utils import CamacRequest
from camac.echbern.signals import file_subsequently
from camac.notification.utils import send_mail

CLAIM_QUESTION = "nfd-tabelle-table"
CLAIM_STATUS_QUESTION = "nfd-tabelle-status"
CLAIM_STATUS_IN_PROGRESS = "nfd-tabelle-status-in-bearbeitung"
CLAIM_STATUS_ANSWERED = "nfd-tabelle-status-beantwortet"

NOTIFICATION_CLAIM_IN_PROGRESS = "03-zusatzliche-unterlagen-notwendig-gesuchsteller"
NOTIFICATION_CLAIM_IN_PROGRESS_MUNICIPALITY = (
    "03-zusaetzliche-unterlagen-notwendig-gemeinde"
)
NOTIFICATION_CLAIM_ANSWERED = "03-nachforderung-beantwortet-leitbehorde"


class CustomValidation(BaseValidation):
    def _send_claim_notification(self, info, instance, template_slug, recipient_types):
        send_mail(
            template_slug,
            {"request": CamacRequest(info).request},
            recipient_types=recipient_types,
            instance={"type": "instances", "id": instance.pk},
        )

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
            instance = data["document"].family.work_item.case.instance
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
                self._send_claim_notification(
                    info,
                    instance,
                    NOTIFICATION_CLAIM_IN_PROGRESS_MUNICIPALITY,
                    ["inactive_municipality"],
                )

            if new_status == CLAIM_STATUS_ANSWERED:
                # claim is answered, inform the active service and create an
                # eCH event
                self._send_claim_notification(
                    info,
                    instance,
                    NOTIFICATION_CLAIM_ANSWERED,
                    ["leitbehoerde", "inactive_municipality"],
                )
                self._send_claim_ech_event(info, instance)

        return data
