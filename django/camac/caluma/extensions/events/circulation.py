from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import (
    post_complete_case,
    post_complete_work_item,
    post_skip_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.core.utils import create_history_entry
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_case, raise_exception=True)
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


@on([post_complete_work_item, post_skip_work_item], raise_exception=True)
@transaction.atomic
def post_complete_circulation_work_item(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("CIRCULATION_TASK") and (
        not context or not context.get("no-history")
    ):
        text = gettext_noop("Circulation of %(date)s completed")

        if not settings.APPLICATION.get("IS_MULTILINGUAL", True):
            text = f"Zirkulation vom {work_item.created_at.strftime('%d.%m.%Y')} abgeschlossen"

        create_history_entry(
            get_instance(work_item),
            User.objects.get(username=user.username),
            text,
            lambda lang: {"date": work_item.created_at.strftime("%d.%m.%Y")},
        )
