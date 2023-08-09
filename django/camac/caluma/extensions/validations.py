from datetime import datetime, timedelta

import pytz
from caluma.caluma_core.events import send_event
from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_form.schema import (
    SaveDocumentDateAnswer,
    SaveDocumentStringAnswer,
    SaveDocumentTableAnswer,
)
from caluma.caluma_workflow.events import post_create_work_item
from caluma.caluma_workflow.models import WorkItem
from caluma.caluma_workflow.schema import CompleteWorkItem
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_noop
from rest_framework import exceptions

from camac.caluma.utils import CamacRequest, sync_inquiry_deadline
from camac.core.translations import get_translations
from camac.ech0211.signals import file_subsequently
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


def date_to_deadline(date):
    return pytz.utc.localize(datetime.combine(date, datetime.min.time()))


class CustomValidation(BaseValidation):
    def _send_claim_notification(
        self, info, instance, template_slug, recipient_types
    ):  # pragma: no cover
        send_mail(
            template_slug,
            {"request": CamacRequest(info).request},
            recipient_types=recipient_types,
            instance={"type": "instances", "id": instance.pk},
        )

    def _send_claim_ech_event(self, info, instance):  # pragma: no cover
        file_subsequently.send(
            sender=self.__class__,
            instance=instance,
            user_pk=None,  # Not needed, hence not querying for it
            group_pk=None,  # Not needed, hence not querying for it
        )

    @validation_for(SaveDocumentStringAnswer)
    def validate_save_document_string_answer(
        self, mutation, data, info
    ):  # pragma: no cover
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

    @validation_for(CompleteWorkItem)
    def validate_complete_create_inquiry(self, mutation, data, info):
        work_item = WorkItem.objects.get(pk=data["id"])

        if (
            settings.DISTRIBUTION
            and work_item.task_id == settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]
        ):
            service_id = str(info.context.user.group)
            addressed_groups = mutation.get_params(info)["input"]["context"][
                "addressed_groups"
            ]

            if service_id in addressed_groups:
                raise exceptions.ValidationError(
                    "Services can't create inquiries for themselves!"
                )

        return data

    @validation_for(SaveDocumentDateAnswer)
    def validate_date_answer(self, mutation, data, info):
        if (
            settings.DISTRIBUTION
            and data["question"].slug == settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
        ):
            if not data["date"]:
                raise exceptions.ValidationError("Deadline is required")

            sync_inquiry_deadline(data["document"].work_item, data["date"])

            return data

        if (
            settings.APPEAL
            and data["question"].slug == settings.APPEAL["QUESTIONS"]["DATE"]
        ):
            # Update potentially existing work items linked to this answer
            WorkItem.objects.filter(
                **{
                    "task_id": settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
                    "meta__is-appeal-statement-deadline": True,
                    "meta__appeal-row-id": str(data["document"].pk),
                }
            ).update(deadline=date_to_deadline(data["date"]))

        if (
            settings.PUBLICATION.get("USE_CALCULATED_DATES", False)
            and data["question"].meta["calculatedPublicationDateSlug"]
        ):  # pragma: no cover
            end_question = Question.objects.get(
                pk=data["question"].meta["calculatedPublicationDateSlug"]
            )

            calculated_date = (
                data["date"] + timedelta(days=end_question.meta["publicationDuration"])
                if data["date"]
                else None
            )
            save_answer(
                document=data["document"],
                question=end_question,
                date=calculated_date,
                user=info.context.user,
            )

        return data

    @validation_for(SaveDocumentTableAnswer)
    def validate_table_answer(self, mutation, data, info):
        """Create a work item for a specific appeal row entry.

        For appeal rows of the type deadline (Frist der Stellungnahme) and the
        authority legal departement (Rechtsamt) we need to create a manual work
        item for the lead authority. The deadline of the work item is the one
        entered in the appeal row.
        """

        if (
            settings.APPEAL
            and data["question"].slug == settings.APPEAL["QUESTIONS"]["TABLE"]
        ):
            case = data["document"].work_item.case.family

            deadline_rows = filter(
                lambda row: row.answers.filter(
                    Q(
                        question_id=settings.APPEAL["QUESTIONS"]["AUTHORITY"],
                        value=settings.APPEAL["ANSWERS"]["AUTHORITY"][
                            "LEGAL_DEPARTEMENT"
                        ],
                    )
                    | Q(
                        question_id=settings.APPEAL["QUESTIONS"]["TYPE"],
                        value=settings.APPEAL["ANSWERS"]["TYPE"]["DEADLINE"],
                    )
                ).count()
                == 2,
                data["documents"],
            )

            existing_work_items = []

            for row in deadline_rows:
                deadline = date_to_deadline(
                    row.answers.filter(question_id=settings.APPEAL["QUESTIONS"]["DATE"])
                    .values_list("date", flat=True)
                    .first()
                )

                work_item, created = WorkItem.objects.get_or_create(
                    task_id=settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
                    meta={
                        "is-appeal-statement-deadline": True,
                        "appeal-row-id": str(row.pk),
                    },
                    defaults={
                        "name": get_translations(
                            gettext_noop("Issue statement on appeal")
                        ),
                        "created_by_user": info.context.user.username,
                        "created_by_group": info.context.user.group,
                        "deadline": deadline,
                        "case": case,
                        "status": WorkItem.STATUS_READY,
                        "addressed_groups": [str(info.context.user.group)],
                    },
                )

                if created:
                    send_event(
                        post_create_work_item,
                        sender="validate_table_answer",
                        work_item=work_item,
                        user=info.context.user,
                        context={},
                    )

                existing_work_items.append(work_item.pk)

            # Delete work items for deadline rows that don't exist anymore
            case.work_items.filter(
                **{
                    "task_id": settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
                    "meta__is-appeal-statement-deadline": True,
                }
            ).exclude(pk__in=existing_work_items).delete()

        return data
