from datetime import date, timedelta

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.utils import send_mail

TEMPLATE_REMINDER_CIRCULATION = "05-meldung-fristuberschreitung-fachstelle"


class Command(BaseCommand):
    help = "Send reminders for all inquiries that exceeded their deadline yesterday."

    def handle(self, *args, **options):
        for instance_id in WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
            status=WorkItem.STATUS_READY,
            deadline__date=date.today() - timedelta(days=1),
            case__family__instance__instance_state__name="circulation",
        ).values_list("case__family__instance__pk", flat=True):
            send_mail(
                TEMPLATE_REMINDER_CIRCULATION,
                {},
                PermissionlessNotificationTemplateSendmailSerializer,
                recipient_types=["inquiry_deadline_yesterday"],
                instance={"id": instance_id, "type": "instances"},
            )
