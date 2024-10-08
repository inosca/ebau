from django.conf import settings

from camac.notification import utils as notification_utils
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)


def notify_receivers(message, context):
    # Don't notify applicants if they created the message to begin with
    if (
        "APPLICANT" in message.topic.involved_entities
        and message.created_by != "APPLICANT"
    ):
        _notify_applicants(message, context)

    # Only notify internal services, if there is at least one other service
    # involved, that isn't the sender of the message
    if set(["APPLICANT", message.created_by]) != set(message.topic.involved_entities):
        _notify_internal_involved_entities(message, context)


def _notify_internal_involved_entities(message, context):
    notification_utils.send_mail(
        slug=settings.COMMUNICATIONS["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
            "template_slug"
        ],
        context=context,
        serializer=PermissionlessNotificationTemplateSendmailSerializer,
        recipient_types=["internal_involved_entities"],
        message={"type": "communications-messages", "id": message.pk},
        instance={"id": message.topic.instance.pk, "type": "instances"},
    )


def _notify_applicants(message, context):
    notification_utils.send_mail(
        slug=settings.COMMUNICATIONS["NOTIFICATIONS"]["APPLICANT"]["template_slug"],
        context=context,
        serializer=PermissionlessNotificationTemplateSendmailSerializer,
        recipient_types=["applicant"],
        instance={"id": message.topic.instance.pk, "type": "instances"},
    )
