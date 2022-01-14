from datetime import date

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core import mail
from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.user.models import Service, User


def get_task_trans(count, lang, controlling=False):
    if controlling:
        translations = {
            "de": {"singular": "Controlling-Aufgabe", "plural": "Controlling-Aufgaben"},
            "fr": {"singular": "tâche", "plural": "tâches"},
        }
    else:
        translations = {
            "de": {"singular": "Aufgabe", "plural": "Aufgaben"},
            "fr": {"singular": "tâche de contrôle", "plural": "tâches de contrôle"},
        }

    return translations[lang]["singular" if count == 1 else "plural"]


def render_service_template(
    addressed_overdue, addressed_not_viewed, controlling_overdue, service
):
    if settings.APPLICATION.get("IS_MULTILINGUAL"):
        name = service.trans.filter(language="de").first().name
    else:
        name = service.name

    text = f"""Guten Tag

Ihre Organisation ({name}) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- {addressed_overdue} überfällige {get_task_trans(addressed_overdue, "de")}
- {addressed_not_viewed} ungelesene {get_task_trans(addressed_not_viewed, "de")}
- {controlling_overdue} überfällige {get_task_trans(controlling_overdue, "de", True)}

{settings.INTERNAL_BASE_URL}

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
"""

    if settings.APPLICATION.get("IS_MULTILINGUAL", False):
        name_fr = service.trans.filter(language="fr").first().name
        text = (
            text
            + f"""
*** version française ***

Bonjour,

Votre organisation ({name_fr}) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- {addressed_overdue} {get_task_trans(addressed_overdue, "fr")} en retard
- {addressed_not_viewed} {get_task_trans(addressed_not_viewed, "fr")} non lue{"s" if addressed_not_viewed != 1 else ""}
- {controlling_overdue} {get_task_trans(controlling_overdue, "fr", True)} en retard

{settings.INTERNAL_BASE_URL}

Ce message a été généré automatiquement, veuillez ne pas y répondre.
"""
        )

    return text


def render_user_template(addressed_overdue, addressed_not_viewed, user):
    name = f"{user.surname} {user.name}"

    text = f"""Guten Tag {name}

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- {addressed_overdue} überfällige {get_task_trans(addressed_overdue, "de")}
- {addressed_not_viewed} ungelesene {get_task_trans(addressed_not_viewed, "de")}

{settings.INTERNAL_BASE_URL}

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
"""
    if settings.APPLICATION.get("IS_MULTILINGUAL", False):
        text = (
            text
            + f"""
*** version française ***

Bonjour {name},

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- {addressed_overdue} {get_task_trans(addressed_overdue, "fr")} en retard
- {addressed_not_viewed} {get_task_trans(addressed_not_viewed, "fr")} non lue{"s" if addressed_not_viewed != 1 else ""}

{settings.INTERNAL_BASE_URL}

Ce message a été généré automatiquement, veuillez ne pas y répondre.
"""
        )

    return text


class Command(BaseCommand):
    help = "Send reminders for unread or overdue work items."

    def handle(self, *args, **options):

        subject = "Erinnerung an Aufgaben"
        if settings.APPLICATION.get("IS_MULTILINGUAL", False):
            subject = subject + " / Rappel des tâches"

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
        all_assigned_usernames = set(
            username
            for item in work_items.values_list("assigned_users", flat=True)
            for username in item
        )
        all_assigned_users = (
            User.objects.exclude(disabled=1)
            .filter(username__in=all_assigned_usernames)
            .order_by("username")
        )

        for user in all_assigned_users:
            user_items = work_items.filter(assigned_users__contains=[user.username])

            not_viewed_items = user_items.filter(is_not_viewed).count()
            overdue_items = user_items.filter(is_overdue).count()

            if not_viewed_items + overdue_items > 0:
                emails.append(
                    mail.EmailMessage(
                        subject,
                        render_user_template(overdue_items, not_viewed_items, user),
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                    )
                )

        # addressed or controlling groups
        all_service_ids = set(
            group
            for item in work_items.values("addressed_groups", "controlling_groups")
            for group in item["addressed_groups"] + item["controlling_groups"]
        )
        all_services = (
            Service.objects.exclude(disabled=1)
            .filter(pk__in=all_service_ids)
            .order_by("pk")
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
                        subject,
                        render_service_template(
                            addressed_overdue,
                            addressed_not_viewed,
                            controlling_overdue,
                            service,
                        ),
                        settings.DEFAULT_FROM_EMAIL,
                        [service.email],
                    )
                )

        print(f"sending {len(emails)} reminders")

        if emails:
            connection = mail.get_connection()
            connection.send_messages(emails)
