from logging import getLogger

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow.events import created_work_item

from camac.caluma.api import CalumaApi

log = getLogger()


@on(created_work_item)
def copy_sb_personal(sender, work_item, **kwargs):
    if work_item.task.slug == "sb1":
        CalumaApi().copy_table_answer(
            source_document=work_item.case.document,
            target_document=work_item.document,
            source_question="personalien-sb",
            target_question="personalien-sb1-sb2",
            source_question_fallback="personalien-gesuchstellerin",
        )

    if work_item.task.slug == "sb2":
        CalumaApi().copy_table_answer(
            source_document=work_item.case.work_items.get(task_id="sb1").document,
            target_document=work_item.document,
            source_question="personalien-sb1-sb2",
            target_question="personalien-sb1-sb2",
        )


@on(created_work_item)
def copy_paper_answer(sender, work_item, **kwargs):
    if work_item.task.slug in ["nfd", "sb1", "sb2"]:
        # copy answer to the papierdossier question in the case document to the
        # newly created work item document
        try:
            work_item.document.answers.create(
                question_id="papierdossier",
                value=work_item.case.document.answers.get(
                    question_id="papierdossier"
                ).value,
            )
        except caluma_form_models.Answer.DoesNotExist:
            log.warning(
                f"Could not find answer for question `papierdossier` in document for instance {work_item.case.meta.get('camac-instance-id')}"
            )


@on(created_work_item)
def post_complete_work_item(sender, work_item, **kwargs):
    if "not-viewed" not in work_item.meta:
        work_item.meta["not-viewed"] = True
        work_item.save()
