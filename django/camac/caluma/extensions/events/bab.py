from datetime import timedelta

from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import resume_work_item, suspend_work_item
from caluma.caluma_workflow.events import post_create_work_item, post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.event_utils import filter_by_canton, filter_by_task, setting
from camac.caluma.utils import date_to_deadline


@on(post_resume_work_item, raise_exception=True)
@filter_by_canton("kt_uri")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
@transaction.atomic
def set_bab_deadline(sender, work_item, user, context=None, **kwargs):
    bab_work_item = WorkItem.objects.filter(
        task_id="bab",
        status=WorkItem.STATUS_READY,
        case=work_item.case.family,
        deadline__isnull=True,
        addressed_groups=work_item.addressed_groups,
    ).first()

    if not bab_work_item:  # pragma: no cover
        return

    bab_work_item.deadline = date_to_deadline(now().date() + timedelta(days=30))
    bab_work_item.save(update_fields=["deadline"])


@on(post_create_work_item, raise_exception=True)
@filter_by_canton("kt_uri")
@filter_by_task("rpg")
@transaction.atomic
def suspend_rpg_work_item(sender, work_item, user, context=None, **kwargs):
    suspend_work_item(work_item, user)


@on(post_create_work_item, raise_exception=True)
@filter_by_canton("kt_uri")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
@transaction.atomic
def resume_rpg_work_item(sender, work_item, user, context=None, **kwargs):
    rpg_work_item = WorkItem.objects.filter(
        task_id="rpg",
        status=WorkItem.STATUS_SUSPENDED,
    ).first()

    if not rpg_work_item:  #  pragma: no cover
        return

    resume_work_item(rpg_work_item, user)
