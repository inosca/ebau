from django.conf import settings

from camac.notification import utils as notification_utils


def notify_receivers(message, context):
    # Currently, we do not send any notifications to internal services
    if "APPLICANT" in message.topic.involved_entities:
        _notify_applicants(message, context)


def _notify_applicants(message, context):
    # Don't notify applicants if they created the message to begin with
    if message.created_by == "APPLICANT":
        return

    instance = message.topic.instance

    notification_utils.send_mail(
        slug=settings.APPLICATION["COMMUNICATIONS"]["template_slug"],
        context=context,
        recipient_types=["applicant"],
        instance={"id": instance.pk, "type": "instances"},
    )
