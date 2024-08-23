from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from django.db import transaction

from .general import get_caluma_setting, get_instance
from .simple_workflow import send_notification


def handle_notification(event_type, context, user, work_item):
    caluma_workflow_notifications_config = get_caluma_setting(
        "CALUMA_WORKFLOW_NOTIFICATIONS", {}
    )

    if not caluma_workflow_notifications_config:
        return  # pragma: no cover

    configs = caluma_workflow_notifications_config.get(work_item.task_id)

    if not configs:
        return  # pragma: no cover

    for config in configs:
        if config["event"] == event_type:
            instance = get_instance(work_item)
            notification = config.get("notification")
            send_notification(notification, context, instance, user, work_item)


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def post_create_caluma_workflow_notifications(
    sender, work_item, user, context, **kwargs
):
    handle_notification("created", context, user, work_item)


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_caluma_workflow_notifications(
    sender, work_item, user, context, **kwargs
):
    handle_notification("completed", context, user, work_item)
