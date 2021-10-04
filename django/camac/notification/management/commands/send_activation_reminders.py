from datetime import date

from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.core.models import Activation
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.utils import send_mail

TEMPLATE_REMINDER_CIRCULATION = "05-meldung-fristuberschreitung-fachstelle"


class Command(BaseCommand):
    help = "Send reminders for all activations that exceeded their deadline today."

    def handle(self, *args, **options):
        activations = Activation.objects.filter(
            ~Q(circulation_state__name="DONE"),
            deadline_date__date=date.today(),
            circulation__instance__instance_state__name="circulation",
        )
        instances = {a.circulation.instance for a in activations}

        for instance in instances:
            print(f"Sending reminders for instance {instance.pk}")
            send_mail(
                TEMPLATE_REMINDER_CIRCULATION,
                {},
                PermissionlessNotificationTemplateSendmailSerializer,
                recipient_types=["activation_deadline_today"],
                instance={"id": instance.pk, "type": "instances"},
            )
