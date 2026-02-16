from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.api import suspend_work_item
from caluma.caluma_workflow.events import post_create_work_item
from django.conf import settings
from django.db import transaction


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: (
        work_item.task.slug == "check-gwr-relevancy"
        and settings.APPLICATION_NAME == "kt_uri"
    )
)
def suspend_task_for_additional_demand(sender, work_item, user, context=None, **kwargs):
    complete_check_work_item = work_item.case.family.work_items.get(
        task="complete-check"
    )
    complete_check_document = complete_check_work_item.document
    completeness_answer = complete_check_document.answers.get(
        question_id="complete-check-vollstaendigkeitspruefung"
    ).value

    if (
        completeness_answer
        == "complete-check-vollstaendigkeitspruefung-incomplete-wait"
    ):
        suspend_work_item(work_item, user)
