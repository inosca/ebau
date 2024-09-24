from caluma.caluma_core.events import on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import post_complete_work_item, post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction

from .distribution import filter_by_task


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def send_direct_inquiry(sender, work_item, user, context=None, **kwargs):
    if not (direct_question := settings.DISTRIBUTION["QUESTIONS"].get("DIRECT")):
        return

    if work_item.document.answers.filter(
        question_id=direct_question,
        value__contains=settings.DISTRIBUTION["ANSWERS"]["DIRECT"]["YES"],
    ).exists():
        work_item.meta["is-direct"] = True
        work_item.save()


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def complete_direct_inquiry(sender, work_item, user, context=None, **kwargs):
    if not work_item.meta.get("is-direct"):
        return

    parent_inquiries = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=work_item.controlling_groups,
    )

    status_question = Question.objects.get(
        pk=settings.DISTRIBUTION["QUESTIONS"]["STATUS"]
    )

    for parent_inquiry in parent_inquiries:
        document = parent_inquiry.child_case.document

        # Delete any existing answers
        document.answers.all().delete()

        # Set the status to "direct"
        save_answer(
            question=status_question,
            document=document,
            value=settings.DISTRIBUTION["ANSWERS"]["STATUS"]["DIRECT"],
            user=user,
            context=context,
        )

        # Complete inquiry
        complete_work_item(
            work_item=parent_inquiry.child_case.work_items.get(
                task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"]
            ),
            user=user,
            context=context,
        )
