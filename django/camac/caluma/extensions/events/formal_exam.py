from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item
from django.db import transaction

from camac.permissions.events.core import Trigger


@on(post_complete_work_item, raise_exception=True)
@filter_events(lambda work_item: work_item.task.slug == "formal-exam")
@transaction.atomic
def post_complete_formal_exam(sender, work_item, user, context=None, **kwargs):
    Trigger.formal_exam_completed(None, work_item.case.family.instance, work_item)
