from datetime import timedelta

from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.utils import date_to_deadline

from .distribution import filter_by_task


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def set_bab_deadline(sender, work_item, user, context=None, **kwargs):
    if settings.APPLICATION_NAME != "kt_uri":  # pragma: no cover
        return

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
