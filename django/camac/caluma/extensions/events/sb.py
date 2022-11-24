from datetime import timedelta

from caluma.caluma_core.events import on, send_event
from caluma.caluma_form.models import Answer
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_noop

from camac.core.translations import get_translations

from .general import get_caluma_setting


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def custom_sb2_work_item(sender, work_item, user, context, **kwargs):
    if (
        work_item.task_id == get_caluma_setting("FINALIZE_TASK")
        and Answer.objects.filter(
            question_id="lagerung-von-stoffen-v2",
            document__case=work_item.case,
        ).exists()
    ):
        construction_control = work_item.case.family.instance.responsible_service(
            filter_type="construction_control"
        ).pk

        work_item = WorkItem.objects.create(
            task_id=get_caluma_setting("MANUAL_WORK_ITEM_TASK"),
            name=get_translations(gettext_noop("Send registration form to AWA")),
            created_by_user=user.username,
            created_by_group=user.group,
            deadline=timezone.now() + timedelta(days=10),
            case=work_item.case,
            status=WorkItem.STATUS_READY,
            addressed_groups=[str(construction_control)],
        )

        send_event(
            post_create_work_item,
            sender="finalize",
            work_item=work_item,
            user=user,
            context=context,
        )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def custom_sb1_work_item(sender, work_item, user, context, **kwargs):
    if (
        work_item.task_id == get_caluma_setting("REPORT_TASK")
        and Answer.objects.filter(
            question_id="legal-submission-type",
            value__contains="legal-submission-type-load-compensation-request",
            document__family__work_item__case__family=work_item.case.family,
        ).exists()
    ):
        construction_control = work_item.case.instance.responsible_service(
            filter_type="construction_control"
        ).pk

        work_item = WorkItem.objects.create(
            task_id=get_caluma_setting("MANUAL_WORK_ITEM_TASK"),
            name=get_translations(gettext_noop("Informin burden compensation bodies")),
            created_by_user=user.username,
            created_by_group=user.group,
            deadline=timezone.now() + timedelta(days=10),
            case=work_item.case,
            status=WorkItem.STATUS_READY,
            addressed_groups=[str(construction_control)],
        )

        send_event(
            post_create_work_item,
            sender="report",
            work_item=work_item,
            user=user,
            context=context,
        )
