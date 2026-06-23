from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import suspend_work_item
from caluma.caluma_workflow.events import post_create_work_item
from django.db import transaction

from camac.caluma.event_utils import filter_by_canton, filter_by_task


@on(post_create_work_item, raise_exception=True)
@filter_by_canton("kt_uri")
@filter_by_task("check-gwr-relevancy")
@transaction.atomic
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
