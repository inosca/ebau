from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import post_complete_case
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction

from .general import get_caluma_setting


@on(post_complete_case)
@transaction.atomic
def post_complete_circulation(sender, case, user, **kwargs):
    if case.workflow_id == get_caluma_setting("CIRCULATION_WORKFLOW"):
        parent_work_item = WorkItem.objects.filter(
            child_case=case,
            task_id=get_caluma_setting("CIRCULATION_TASK"),
            status=WorkItem.STATUS_READY,
        ).first()

        if parent_work_item:
            complete_work_item(parent_work_item, user)
