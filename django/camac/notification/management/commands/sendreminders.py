from datetime import date

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.core.models import Activation
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.views import send_mail
from camac.user.models import Service, User

TEMPLATE_REMINDER_CIRCULATION = "05-meldung-fristuberschreitung-fachstelle"

CALUMA_SUBJECT = "Erinnerung an Aufgaben / TODO francais"


def render_service_template(
    addressed_overdue, addressed_not_viewed, controlling_overdue
):
    return f"""Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- {addressed_overdue} überfällige Aufgaben
- {addressed_not_viewed} ungelesene Aufgaben
- {controlling_overdue} überfällige Controlling-Aufgaben

{settings.INTERNAL_BASE_URL}

*** version française ***

TODO
"""


def render_user_template(addressed_overdue, addressed_not_viewed):
    return f"""Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- {addressed_overdue} überfällige Aufgabe{"n" if addressed_overdue > 1 else ""}
- {addressed_not_viewed} ungelesene Aufgabe{"n" if addressed_not_viewed > 1 else ""}

{settings.INTERNAL_BASE_URL}

*** version française ***

TODO
"""


class Command(BaseCommand):
    help = """
    (Bern): Send reminders for all activation which exceeded their deadline.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--caluma",
            action="store_true",
            default=False,
            help="Use caluma WorkItems for determining reminders",
        )

    def handle(self, *args, **options):
        if options["caluma"]:
            self.handle_caluma(*args, **options)
            return

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

    def handle_caluma(self, *args, **options):

        is_overdue = Q(deadline__lte=date.today())
        is_not_viewed = Q(**{"meta__not-viewed": True})

        # get all work items which are overdue or not viewed
        work_items = (
            WorkItem.objects.filter(status=WorkItem.STATUS_READY)
            .exclude(
                task_id__in=settings.APPLICATION.get("NOTIFICATIONS_EXCLUDED_TASKS", [])
            )
            .filter(deadline__isnull=False)
            .filter(is_overdue | is_not_viewed)
            .order_by("deadline", "name")
        )

        emails = []

        # assigned_users
        all_assigned_users = set(
            User.objects.get(username=username)
            for item in work_items.values_list("assigned_users", flat=True)
            for username in item
        )

        for user in all_assigned_users:
            user_items = work_items.filter(assigned_users__contains=[user.username])

            not_viewed_items = user_items.filter(is_not_viewed).count()
            overdue_items = user_items.filter(is_overdue).count()

            if not_viewed_items + overdue_items > 0:
                emails.append(
                    mail.EmailMessage(
                        CALUMA_SUBJECT,
                        render_user_template(overdue_items, not_viewed_items),
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                )

        # addressed or controlling groups
        all_services = set(
            Service.objects.get(pk=group)
            for item in work_items.values("addressed_groups", "controlling_groups")
            for group in item["addressed_groups"] + item["controlling_groups"]
        )

        for service in all_services:
            addressed = work_items.filter(addressed_groups__contains=[str(service.pk)])
            controlling = work_items.filter(
                controlling_groups__contains=[str(service.pk)]
            )

            addressed_overdue = addressed.filter(is_overdue).count()
            addressed_not_viewed = addressed.filter(is_not_viewed).count()
            controlling_overdue = controlling.filter(is_overdue).count()

            if addressed_overdue + addressed_not_viewed + controlling_overdue > 0:
                emails.append(
                    mail.EmailMessage(
                        CALUMA_SUBJECT,
                        render_service_template(
                            addressed_overdue, addressed_not_viewed, controlling_overdue
                        ),
                        settings.DEFAULT_FROM_EMAIL,
                        [service.email],
                    )
                )

        print(f"sendreminders: sending {len(emails)} reminders")

        if emails:
            connection = mail.get_connection()
            connection.open()
            connection.send_messages(emails)
            connection.close()
