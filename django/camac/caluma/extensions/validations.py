from __future__ import annotations

import typing
from datetime import timedelta

from caluma.caluma_core.events import send_event
from caluma.caluma_core.validations import BaseValidation, validation_for
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_form.schema import (
    SaveDocumentDateAnswer,
    SaveDocumentTableAnswer,
)
from caluma.caluma_workflow.events import post_create_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from caluma.caluma_workflow.schema import (
    CompleteWorkItem,
    SaveCase,
    SaveWorkItem,
)
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_noop
from rest_framework import exceptions

from camac.caluma.utils import (
    date_to_deadline,
    sync_inquiry_deadline,
)
from camac.core.translations import get_translations

if typing.TYPE_CHECKING:  # pragma: no cover
    from django.db.model import Model

RESETTABLE_META_VALUES: dict[typing.Type[Model], list[str]] = {
    Case: [
        # Users can reset paper-submit-date in dossier header
        "paper-submit-date",
    ],
    WorkItem: [
        # Some deadline & notification handling happens in the validation
        # layer automatically and therefore must be allowed to be reset
        "not-viewed",
        "notify-deadline",
        "notify-completed",
    ],
}


def validate_metainfo(model_obj: Model, value: dict):
    """Validate the metainfo for "lost" values.

    If an update comes from a client with expired data, we don't want to lose
    possibly already-entered data.

    Note: Expects a freshly-loaded model object as parameter, as it will use that
    for comparison to ensure the meta value is not lost
    """

    model_cls = type(model_obj)
    original_value = getattr(model_obj, "meta")

    resettable = RESETTABLE_META_VALUES.get(model_cls, [])

    # Check for fields being removed, or set to None
    for field, orig_value in original_value.items():
        if field in resettable:
            # resettable, we don't care
            continue
        if value.get(field, None) is None and orig_value is not None:
            # We had a value before, but now we don't; and the
            # field is not configured as being resettable
            raise exceptions.ValidationError(
                f"Cannot reset {field} from {model_cls.__name__}.meta"
            )
    return value


class CustomValidation(BaseValidation):
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
            and "calculatedPublicationDateSlug" in data["question"].meta
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
                lambda row: (
                    row.answers.filter(
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
                    == 2
                ),
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

    @validation_for(SaveCase)
    def validate_meta_case(self, mutation, data, info):
        # checking for metainfo key deletion
        if "meta" in data:
            if "id" in data:
                # this we only do for existing cases
                validate_metainfo(Case.objects.get(pk=data["id"]), data["meta"])

        return data

    @validation_for(SaveWorkItem)
    def validate_meta_workitem(self, mutation, data, info):
        if "meta" in data and "id" in data:
            # Only check for existing work items
            validate_metainfo(WorkItem.objects.get(pk=data["id"]), data["meta"])
        return data
