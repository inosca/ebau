from datetime import date, timedelta

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.utils import send_mail

TEMPLATE_REMINDER_CIRCULATION = "05-meldung-fristuberschreitung-fachstelle"


class Command(BaseCommand):
    help = "Send reminders for all inquiries that exceeded their deadline yesterday."

    @transaction.atomic
    def handle(self, *args, **options):
        for work_item in WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=WorkItem.STATUS_READY,
            deadline__date=date.today() - timedelta(days=1),
            case__family__instance__instance_state__name="circulation",
        ):
            send_mail(
                TEMPLATE_REMINDER_CIRCULATION,
                {},
                PermissionlessNotificationTemplateSendmailSerializer,
                recipient_types=["inquiry_addressed"],
                instance={"id": work_item.case.family.instance.pk, "type": "instances"},
                inquiry={"id": work_item.pk, "type": "work-items"},
            )
            work_item.meta = {
                **work_item.meta,
                "reminders": [now().isoformat(), *work_item.meta.get("reminders", [])],
            }
            work_item.save()
