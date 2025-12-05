from logging import getLogger

from caluma.caluma_form.models import Answer
from celery import shared_task
from django.db.models import Exists, OuterRef

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


@shared_task(bind=True)
def send_notification_for_publication(self):
    """
    Send notifications for publication start.

    Settings for publication to enable the notification:
    - The condition can be set to False to disable, or the question/answer must be present in the answers.
    - The date_question answer must match today's date.
    - The work item with id fill_work_item must match the work item's task_id.
    - The notification is sent to the configured recipient_types with the template_slug as notificationtemplate pk.


    ```
    "PUBLICATION": {
        "NOTIFICATIONS": {
            "PUBLICATION_START": {
                "condition": {
                    "question": "oeffentliche-auflage-informieren",
                    "answer": ["oeffentliche-auflage-informieren-ja"],
                },
                "date_question": "beginn-publikationsorgan-gemeinde",
                "notification": {
                    "template_slug": "publication-start",
                    "recipient_types": ["applicant"],
                },
            }
        },
    }
    ```
    """

    from caluma.caluma_workflow.models import WorkItem
    from django.conf import settings
    from django.utils import timezone
    from django_celery_beat.models import PeriodicTask

    from camac.caluma.extensions.events.general import get_instance_id
    from camac.notification.utils import send_mail_without_request

    config = settings.PUBLICATION["NOTIFICATIONS"].get("PUBLICATION_START")
    if not config:  # pragma: no cover
        return

    now = timezone.now()

    task_id = settings.PUBLICATION["FILL_TASKS"]["PUBLIC"]
    notification = config["notification"]
    recipient_types = notification["recipient_types"]

    task = PeriodicTask.objects.filter(task=self.name).first()
    work_items = WorkItem.objects.filter(task_id=task_id)

    if settings.PUBLICATION.get("PUBLISH_QUESTION"):
        work_items = work_items.annotate(
            is_published=Exists(
                Answer.objects.filter(
                    document_id=OuterRef("document_id"),
                    question=settings.PUBLICATION["PUBLISH_QUESTION"],
                    value=settings.PUBLICATION["PUBLISH_ANSWER"],
                )
            )
        ).filter(is_published=True)

    # optionally add an extra condition answer to see if a notification should be sent.
    # e.g. checkbox if the applicant should be notified.
    if condition := config.get("condition"):
        work_items = work_items.annotate(
            has_matching_answer=Exists(
                Answer.objects.filter(
                    document_id=OuterRef("document_id"),
                    question=condition["question"],
                    value=condition["answer"],
                )
            )
        ).filter(has_matching_answer=True)

    # filter work items where the date_question answer matches today's date.
    work_items = work_items.annotate(
        has_matching_date=Exists(
            Answer.objects.filter(
                document_id=OuterRef("document_id"),
                question=config.get("date_question"),
                date=now.date(),
            )
        )
    ).filter(has_matching_date=True)

    log.info(
        f"Send {work_items.count()} publication-start notifications ({task_id}/{recipient_types}). Last run at {task.last_run_at}."
    )
    try:
        count = 0
        for work_item in work_items:
            instance_id = get_instance_id(work_item)
            try:
                log.info(
                    f"Sending publication start notification for {task_id} workitem {work_item.pk} on instance {instance_id}."
                )
                send_mail_without_request(
                    notification["template_slug"],
                    recipient_types=recipient_types,
                    instance={"id": instance_id, "type": "instances"},
                    work_item={"id": work_item.pk, "type": "work-items"},
                )
                count += 1
            except Exception as e:  # pragma: no cover
                log.error(
                    f"Failed sending notification for {task_id} workitem {work_item.pk} on instance {instance_id}: {e}"
                )

    except Exception as e:  # pragma: no cover
        log.error(f"Failed sending notification for {task_id} workitems: {e}")
