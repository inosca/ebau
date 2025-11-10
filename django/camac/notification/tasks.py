from logging import getLogger

from celery import shared_task

log = getLogger(__name__)


@shared_task(bind=True)
def send_notification_for_overdue_workitems(self):
    """
    Send notifications for overdue workitems with notification flag set.

    This is a refactor of the existing management command `send_work_item_reminders which doesn't reimplement
    the mailsending and follows the configuration we use for most notifications.
    The notifications can be confiured in django/camac/settings/django.py with the  NOTIFICATIONS key:
    ```
    "NOTIFICATIONS": {
        "WORKITEM_DEADLINE_OVERDUE": {
            "create-manual-workitems": {
                "template_slug": "expired-manual-work-item",
                "recipient_types": ["work_item_controlling"],
            }
        }
    }
    ```

    Notifications can be configured by task:
    "WORKITEM_DEADLINE_OVERDUE": {
        "task_id_1": {
            ...
        },
        "task_id_2": {
            ...
        }
    }

    Make sure you never have more than one scheduler for this task.
    """
    from datetime import timedelta

    from caluma.caluma_workflow.models import WorkItem
    from django.conf import settings
    from django.utils import timezone
    from django_celery_beat.models import PeriodicTask

    from camac.caluma.extensions.events.general import get_instance_id
    from camac.notification.utils import send_mail_without_request

    config = settings.APPLICATION["NOTIFICATIONS"].get("WORKITEM_DEADLINE_OVERDUE")
    if not config:  # pragma: no cover
        return

    task = PeriodicTask.objects.filter(task=self.name).first()

    now = timezone.now()
    check_deadlines_since = task.last_run_at or (now - timedelta(hours=24))

    log.info(
        f"Send notifications for WorkItems since {check_deadlines_since}. Last run at {task.last_run_at}."
    )

    for task_id in config.keys():
        try:
            for work_item in WorkItem.objects.filter(
                **{
                    "task": task_id,
                    "meta__notify-deadline": True,
                    "deadline__gt": check_deadlines_since,
                    "closed_at__isnull": True,
                }
            ):
                try:
                    instance_id = get_instance_id(work_item)
                    notification = config[task_id]
                    send_mail_without_request(
                        notification["template_slug"],
                        instance={"id": instance_id, "type": "instances"},
                        recipient_types=notification["recipient_types"],
                        work_item={"id": work_item.pk, "type": "work-items"},
                    )
                except Exception as e:  # pragma: no cover
                    log.error(
                        f"Failed sending notification for WorkItem {work_item.pk}: {e}"
                    )
        except Exception as e:  # pragma: no cover
            log.error(
                f"Failed sending notification for WorkItem's for Task {task_id}: {e}"
            )
