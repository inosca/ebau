"""Notify the responsible service in case of an overdue activation.

This command will look for overdue circulation activations and notifies the
responsible services, dependent on how long the activation is overdue:

* 2 weeks exceeded: Notify the Fachstelle that they should immediatley process
  this dossier and give feedback.

* 3 weeks exceeded: Notify the Leitbehörde that the Fachstelle has not responded
  yet. It is then up to the Leitbehörde to take further action.

An activation is overdue in one two cases:

* Either the "Dossier vollständig" answer is set to a date. This means that the
  service requested "Nachforderungen" which were sucessfully provided by the
  applicant, but they have not completed their feedback.

* The deadline of the activation that has been exceeded.

This has previously been a Camac Module known as "activation callback". The old
module worked differently. Instead of notifying the Leitbehörde after 3 weeks,
it automtically returned the activation to the Leitbehörde with a default feedback.

We had to change this behaviour because sometimes it would callback dossiers
which should not have been called back. That's why we only send reminder mails
here.
"""
from collections import namedtuple
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from camac.constants import kt_uri as constants
from camac.core.models import Activation, ActivationCallbackNotice
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.views import send_mail

Notification = namedtuple(
    "Notification", ["activation", "template_slug", "recipient_type"]
)


def notify_once(notification):
    """Send a notification if it has not been sent in the past."""

    already_sent = ActivationCallbackNotice.objects.filter(
        activation_id=notification.activation, reason=notification.template_slug
    ).exists()

    if already_sent:
        return False

    instance = notification.activation.circulation.instance
    activation = notification.activation

    send_mail(
        notification.template_slug,
        context={},
        serializer=PermissionlessNotificationTemplateSendmailSerializer,
        recipient_types=[notification.recipient_type],
        instance={"id": instance.pk, "type": "instances"},
        activation={"id": activation.pk, "type": "activations"},
    )

    # To ensure that we only send notifications once.
    ActivationCallbackNotice.objects.create(
        activation_id=activation.pk,
        circulation_id=activation.circulation.pk,
        send_date=timezone.now(),
        reason=notification.template_slug,
    )

    return True


def get_overdue_activations():
    """Return all overdue activations.

    An activation is considered overdue if the deadline has been exceeded. If
    the service of an activation is contained in
    ACTIVATION_CALLBACK_EXCLUDED_SERVICES it will not be considered.
    """
    excluded_services = settings.APPLICATION.get("NOTIFY_OVERDUE_EXCLUDED_SERVICES", [])

    return Activation.objects.filter(
        Q(circulation_state__name="RUN", deadline_date__lt=timezone.now()),
        ~Q(service__pk__in=excluded_services),
    )


def determine_notification(deadline_leitbehoerde, deadline_service, activation):

    # We can ignore the deadline completely when an
    # activation has a completion date set.
    completion_date = activation.nfd_completion_date

    if completion_date and completion_date < deadline_leitbehoerde:
        notification = Notification(
            activation,
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_LEITBEHOERDE,
            "circulation_service",
        )
    elif completion_date and completion_date < deadline_service:
        notification = Notification(
            activation,
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_FACHSTELLE,
            "activation_service",
        )
    elif activation.deadline_date < deadline_leitbehoerde:
        notification = Notification(
            activation,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_LEITBEHOERDE,
            "circulation_service",
        )
    elif activation.deadline_date < deadline_service:
        notification = Notification(
            activation,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_FACHSTELLE,
            "activation_service",
        )
    else:
        # The activations deadline has not exceeded the notification threshold.
        return None

    return notification


class Command(BaseCommand):

    help = """
    Notify the responsible service in case of a overdue activation.
    """

    def add_arguments(self, parser):
        parser.add_argument("--dryrun", default=False, action="store_true")
        parser.add_argument(
            "--leitbehoerde-deadline", type=int, default=21, action="store"
        )
        parser.add_argument("--service-deadline", type=int, default=14, action="store")

    def handle(self, *args, **options):
        dryrun = options["dryrun"]

        now = timezone.now()
        notification_deadline_leitbehoerde = now - timedelta(
            days=options["leitbehoerde_deadline"]
        )
        notification_deadline_service = now - timedelta(
            days=options["service_deadline"]
        )

        for activation in get_overdue_activations():

            notification = determine_notification(
                notification_deadline_leitbehoerde,
                notification_deadline_service,
                activation,
            )

            if notification is None:  # pragma: no cover
                # The activations deadline has not exceeded the notification threshold.
                self.stdout.write(
                    f"Activation {activation.pk} is overdue but has ",
                    "not exceeded the notification deadline.",
                )
                continue

            if dryrun:
                self.stdout.write(
                    f"activation_id={notification.activation.pk} "
                    f"template_slug={notification.template_slug} "
                    f"recipient_type={notification.recipient_type}"
                )
                continue

            notify_once(notification)
