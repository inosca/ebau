from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from caluma.caluma_form.models import Answer, Document
from celery import shared_task
from django.db.models import Exists, OuterRef, Q

if TYPE_CHECKING:
    from camac.settings.modules.work_item_overdue_notifications_schema import (
        WorkItemOverdueNotificationsConfig,
    )

log = getLogger(__name__)


@shared_task(bind=True)
def send_notification_for_overdue_workitems(self):
    """
    Send notifications for overdue workitems with notification flag set.

    This is a refactor of the existing management command `send_work_item_reminders which doesn't reimplement
    the mailsending and follows the configuration we use for most notifications.
    Notifications are configured in the WORK_ITEM_OVERDUE_NOTIFICATIONS module:
    ```
    OverdueNotificationConfig(
        template_slug="expired-manual-work-item",
        recipient_types=["work_item_controlling"],
        work_item_allowlist=["create-manual-workitems"],
    )
    ```

    Each notification block must define either a work item allowlist or denylist.

    Make sure you never have more than one scheduler for this task.
    """
    from datetime import timedelta

    from caluma.caluma_workflow.models import WorkItem
    from django.conf import settings
    from django.utils import timezone
    from django_celery_beat.models import PeriodicTask

    from camac.caluma.extensions.events.general import get_instance_id
    from camac.notification.utils import send_mail_without_request
    from camac.settings.utils import is_module_enabled

    if not is_module_enabled("WORK_ITEM_OVERDUE_NOTIFICATIONS"):  # pragma: no cover
        return

    config: WorkItemOverdueNotificationsConfig = (
        settings.WORK_ITEM_OVERDUE_NOTIFICATIONS
    )
    task = PeriodicTask.objects.filter(task=self.name).first()
    now = timezone.now()
    # Dont send notification's for missed work items more than 2 days in the past
    # While this is running daily, givin one day additional might prevent missing
    # notifications if a server was restarted while the task would be running or
    # similar events.
    cut_off_date = now - timedelta(days=2)

    # When deploying for the first time, dont send a notification for all workitems in the past.
    if process_deadlines_from := config.process_deadlines_from:
        if timezone.is_naive(process_deadlines_from):
            process_deadlines_from = timezone.make_aware(process_deadlines_from)
        if process_deadlines_from > cut_off_date:
            cut_off_date = process_deadlines_from
            log.info(f"Use configured value for process_deadlines_from: {cut_off_date}")

    for notification in config.notifications:
        if notification.work_item_allowlist is not None:
            work_item_filter_text = f"allowlist={notification.work_item_allowlist!r}"
            work_item_filter = Q(task_id__in=notification.work_item_allowlist)
        else:
            work_item_filter_text = f"denylist={notification.work_item_denylist!r}"
            work_item_filter = ~Q(task_id__in=notification.work_item_denylist)

        try:
            work_items = WorkItem.objects.filter(
                **{
                    "meta__notify-deadline": True,
                    "meta__deadline_notification_sent_at__isnull": True,
                    "deadline__range": [cut_off_date, now],
                    "closed_at__isnull": True,
                }
            ).filter(work_item_filter)

            log.info(
                f"Send notifications for {work_items.count()} overdue WorkItems ({work_item_filter_text}) in range {cut_off_date} to {now}. Task last run at: {task.last_run_at or 'Never'}."
            )

            for work_item in work_items:
                try:
                    instance_id = get_instance_id(work_item)
                    send_mail_without_request(
                        notification.template_slug,
                        instance={"id": instance_id, "type": "instances"},
                        recipient_types=notification.recipient_types,
                        work_item={"id": work_item.pk, "type": "work-items"},
                    )
                    work_item.meta["deadline_notification_sent_at"] = now.isoformat()
                    work_item.save(update_fields=["meta"])
                except Exception as e:  # pragma: no cover
                    log.error(
                        f"Failed sending notification for WorkItem {work_item.pk}: {e}"
                    )
        except Exception as e:  # pragma: no cover
            log.error(
                f"Failed sending overdue WorkItem notifications ({work_item_filter_text}): {e}"
            )


@shared_task(bind=True)
def send_notification_for_publication(self, workitem_id=None):
    """
    Send notifications for publication start.

    Settings for publication to enable the notification:
    - The condition can be set to False to disable, or the question/answer must be present in the answers.
    - The date_question answer must match today's date.
    - The work item with id fill_work_item must match the work item's task_id.
    - The notification is sent to the configured recipient_types with the template_slug as notificationtemplate pk.

    The notifications can be confiured in django/camac/settings/django.py with the NOTIFICATIONS key:

    ```
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
    ```
    """

    from caluma.caluma_workflow.models import WorkItem
    from django.conf import settings
    from django.utils import timezone
    from django_celery_beat.models import PeriodicTask

    from camac.caluma.extensions.events.general import get_instance_id
    from camac.notification.utils import send_mail_without_request

    config = settings.APPLICATION["NOTIFICATIONS"].get("PUBLICATION_START")
    if not config:
        return

    now = timezone.now()

    task_id = settings.PUBLICATION["FILL_TASKS"]["PUBLIC"]
    notification = config["notification"]
    recipient_types = notification["recipient_types"]

    task = PeriodicTask.objects.filter(task=self.name).first()
    work_items = WorkItem.objects.filter(
        task_id=task_id,
        meta__publication_start_notification_sent_at__isnull=True,
    )

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

    if workitem_id:
        work_items = work_items.filter(pk=workitem_id)

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
                work_item.meta["publication_start_notification_sent_at"] = (
                    timezone.now().isoformat()
                )
                work_item.save(update_fields=["meta"])
                count += 1
            except Exception as e:  # pragma: no cover
                log.error(
                    f"Failed sending notification for {task_id} workitem {work_item.pk} on instance {instance_id}: {e}"
                )

    except Exception as e:  # pragma: no cover
        log.error(f"Failed sending notification for {task_id} workitems: {e}")


@shared_task(bind=True)
def send_notification_for_publication_end_legal_submissions(self, workitem_id=None):
    """
    Send notifications for publication end.

    Settings for publication to enable the notification:
    - The date_question answer must match yesterday's date.
    - The work item with id fill_work_item must match the work item's task_id.
    - The notification is sent to the configured recipient_types with the template_slug as notificationtemplate pk.

    The notifications can be confiured in django/camac/settings/django.py with the NOTIFICATIONS key:

    ```
    "NOTIFICATIONS": {
        "PUBLICATION_END_LEGAL_SUBMISSION": {
            "date_question": "ende-publikation-kantonsamtsblatt",
            "notification": {
                "template_slug": "publication-end",
                "recipient_types": ["are_bab"],
            },
        }
    },
    ```
    """

    from caluma.caluma_workflow.models import WorkItem
    from django.conf import settings
    from django.utils import timezone
    from django_celery_beat.models import PeriodicTask

    from camac.notification.utils import send_mail_without_request

    config = settings.APPLICATION["NOTIFICATIONS"].get(
        "PUBLICATION_END_LEGAL_SUBMISSION"
    )
    if not config:
        return

    now = timezone.now()

    task_id = settings.PUBLICATION["FILL_TASKS"]["PUBLIC"]
    notification = config["notification"]
    recipient_types = notification["recipient_types"]

    task = PeriodicTask.objects.filter(task=self.name).first()
    work_items = WorkItem.objects.filter(
        task_id=task_id,
        meta__publication_end_notification_sent_at__isnull=True,
    )

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

    # filter work items where the date_question answer matches yesterday's date.
    work_items = work_items.annotate(
        has_matching_date=Exists(
            Answer.objects.filter(
                document_id=OuterRef("document_id"),
                question=config.get("date_question"),
                date=(now - timezone.timedelta(days=1)).date(),
            )
        )
    ).filter(has_matching_date=True)

    if workitem_id:
        work_items = work_items.filter(pk=workitem_id)

    log.info(
        f"Send {work_items.count()} publication-end notifications ({task_id}/{recipient_types}). Last run at {task.last_run_at}."
    )
    try:
        count = 0
        for work_item in work_items:
            instance = work_item.case.family.instance

            # for the work items where all conditions match, check if there are any legal submissions,
            # otherwise just skip.
            objections = WorkItem.objects.filter(
                case__family=instance.case.family,
                task_id="objections",
            )
            legal_submissions = Document.objects.filter(
                family__in=objections.values_list("document_id", flat=True),
                form_id="einsprache",
            )

            if not legal_submissions.exists():
                log.info(
                    f"Skipping publication end notification for {task_id} workitem {work_item.pk} on instance {instance.pk} because no legal submissions were found."
                )
                continue

            try:
                log.info(
                    f"Sending publication end notification for {task_id} workitem {work_item.pk} on instance {instance.pk}."
                )
                send_mail_without_request(
                    notification["template_slug"],
                    recipient_types=recipient_types,
                    instance={"id": instance.pk, "type": "instances"},
                    work_item={"id": work_item.pk, "type": "work-items"},
                )
                work_item.meta["publication_end_notification_sent_at"] = (
                    timezone.now().isoformat()
                )
                work_item.save(update_fields=["meta"])
                count += 1
            except Exception as e:  # pragma: no cover
                log.error(
                    f"Failed sending notification for {task_id} workitem {work_item.pk} on instance {instance.pk}: {e}"
                )

    except Exception as e:  # pragma: no cover
        log.error(f"Failed sending notification for {task_id} workitems: {e}")


@shared_task(bind=True)
def automatic_inquiry_answer_for_expired_uso_inquiries(self):
    from caluma.caluma_form.api import save_answer
    from caluma.caluma_form.models import Question
    from caluma.caluma_user.models import BaseUser
    from caluma.caluma_workflow.api import complete_work_item
    from django.conf import settings
    from django.utils.timezone import now

    from camac.caluma.models import Inquiry
    from camac.instance.models import Service

    services = list(Service.objects.filter(service_group__slug="uso"))
    inquiries = (
        Inquiry.objects.only_pending().addressed_to(services).filter(deadline__lt=now())
    )

    log.info(
        f"Processing {len(inquiries)} expired USO inquiries for {len(services)} services"
    )

    status_question = Question.objects.get(
        pk=settings.DISTRIBUTION["QUESTIONS"]["STATUS"]
    )
    bemerkungen_question = Question.objects.get(
        pk=settings.DISTRIBUTION["QUESTIONS"]["COMMENTS"]
    )
    renounce_answer = settings.DISTRIBUTION["INQUIRY_ANSWER_AUTOMATIC_RENOUNCED"]

    for inquiry in inquiries:
        try:
            service = Service.objects.get(pk=inquiry.addressed_groups[0])
            group = service.groups.first()
            user = BaseUser(
                username="service-account-camac-admin", group=str(service.pk)
            )
            user.camac_group = str(group.pk)

            fill_inquiry = (
                inquiry.child_case.work_items.filter(
                    task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"]
                )
                .order_by("-created_at")
                .first()
            )

            save_answer(
                document=fill_inquiry.case.document,
                question=status_question,
                value=renounce_answer,
            )
            save_answer(
                document=fill_inquiry.case.document,
                question=bemerkungen_question,
                value="Die Antwort der Stellungnahme wurde automatisch mit «verzichtet» beantwortet, da die Anfrage durch USO nicht innerhalb der Frist beantwortet wurde. ---- La risposta alla richiesta di presa di posizione è stata automaticamente registrata come «rinunciato», poiché USO non ha risposto alla richiesta entro il termine previsto.",
            )
            complete_work_item(fill_inquiry, user)
            log.info(
                f"-> Completed fill_inquiry work item {fill_inquiry.pk} to set the answer and complete the inquiry {inquiry.pk}"
            )
        except Exception as e:  # pragma: no cover
            log.error(f"Failed processing inquiry {inquiry.pk}: {e}")
