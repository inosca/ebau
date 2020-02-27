from datetime import date

from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.core.models import Activation
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)

TEMPLATE_REMINDER_CIRCULATION = 17


class Command(BaseCommand):
    help = """
    (Bern): Send reminders for all activation which exceeded their deadline.
    """

    def handle(self, *args, **options):
        activations = Activation.objects.filter(
            ~Q(circulation_state__name="DONE"),
            deadline_date__date=date.today(),
            circulation__instance__instance_state__name="circulation",
        )
        instances = {a.circulation.instance for a in activations}
        for instance in instances:
            print(f"Sending reminders for instance {instance.pk}")
            sendmail_data = {
                "recipient_types": ["activation_deadline_today"],
                "notification_template": {
                    "type": "notification-templates",
                    "id": TEMPLATE_REMINDER_CIRCULATION,
                },
                "instance": {"id": instance.pk, "type": "instances"},
            }
            sendmail_serializer = PermissionlessNotificationTemplateSendmailSerializer(
                data=sendmail_data
            )
            sendmail_serializer.is_valid(raise_exception=True)
            sendmail_serializer.save()
