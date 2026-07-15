from __future__ import annotations

from typing import TYPE_CHECKING, Any

from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    post_skip_work_item,
)
from django.conf import settings
from django.db import transaction
from django.utils.module_loading import import_string

from camac.caluma.event_utils import filter_by_canton, filter_by_task
from camac.core.utils import create_history_entry
from camac.notification.utils import send_mail_without_request
from camac.permissions.events import core as permissions_events
from camac.user.models import User

from .general import get_instance

if TYPE_CHECKING:
    from caluma.caluma_user.models import BaseUser
    from caluma.caluma_workflow.models import WorkItem

    from camac.settings.modules.caluma_simple_workflow_schema import (
        CalumaSimpleWorkflowConfig,
        EventType,
    )


def send_notification(notification, context, instance_id, user, work_item):
    """Send notifications according to the settings in the notification configuration."""

    if notification and (not context or not context.get("no-notification")):
        additional_data = (
            {"body": context.get("notification-body")}
            if context and context.get("notification-body")
            else {}
        )

        send_mail_without_request(
            notification["template_slug"],
            user.username,
            user.camac_group,
            instance={"id": instance_id, "type": "instances"},
            recipient_types=notification["recipient_types"],
            work_item={"id": work_item.pk, "type": "work-items"},
            **additional_data,
        )


def post_simple_workflow(
    event_type: EventType,
    sender: Any | None,
    work_item: WorkItem,
    user: BaseUser | None,
    context: dict[str, Any] | None,
    **kwargs,
) -> None:
    """Apply configured simple workflow side effects for a Caluma work item event.

    Matching configuration entries can update the instance state, emit eCH events,
    create history entries, and send notifications. Conditions are evaluated per
    entry before any side effect is executed.
    """
    simple_workflow_config: CalumaSimpleWorkflowConfig = settings.CALUMA_SIMPLE_WORKFLOW

    if configs := simple_workflow_config.get_events(work_item.task_id, event_type):
        instance = get_instance(work_item, context)

        # notifications can be sent without fetching the camac user.
        # for instance_state changes or ech_events we need to load it.
        camac_user = None
        if any(config.next_instance_state or config.ech_event for config in configs):
            camac_user = User.objects.get(username=user.username)

        for config in configs:
            if config.condition and not config.condition(work_item):
                continue

            if config.next_instance_state:
                # go to next instance state
                instance.set_instance_state(config.next_instance_state, camac_user)

            if config.ech_event:
                ech_event = import_string(config.ech_event)
                # trigger ech message for status change
                ech_event.send(
                    sender=f"post_{event_type}_{work_item.task_id.replace('-', '_')}",
                    instance=instance,
                    user_pk=camac_user.pk,
                    group_pk=user.camac_group,
                )

            if config.history_text and (not context or not context.get("no-history")):
                create_history_entry(instance, camac_user, config.history_text)

            for notification in config.notifications:
                send_notification(
                    {
                        "template_slug": notification.template_slug,
                        "recipient_types": notification.recipient_types,
                    },
                    context,
                    instance.pk,
                    user,
                    work_item,
                )


@on(post_skip_work_item, raise_exception=True)
@transaction.atomic
def post_skip_simple_workflow(sender, work_item, user, context, **kwargs):
    return post_simple_workflow("skipped", sender, work_item, user, context, **kwargs)


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def post_create_simple_workflow(sender, work_item, user, context, **kwargs):
    return post_simple_workflow("created", sender, work_item, user, context, **kwargs)


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_simple_workflow(sender, work_item, user, context, **kwargs):
    return post_simple_workflow("completed", sender, work_item, user, context, **kwargs)


@on(post_complete_work_item, raise_exception=True)
@filter_by_canton("kt_gr")
@filter_by_task("construction-acceptance")
def post_complete_construction_acceptance_gr(
    sender, work_item, user, context, **kwargs
):
    """For Kt. GR send the instance_completed event.

    Sent after completing construction-acceptance, when construction monitoring
    is not enabled.
    """

    permissions_events.Trigger.instance_completed(None, work_item.case.family.instance)
