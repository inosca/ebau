from collections import namedtuple

from camac.notification.models import NotificationTemplate
from camac.notification.serializers import (
    NotificationTemplateSendmailSerializer,
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.user.models import Group, User


def send_mail_without_request(slug, username, group_id, **kwargs):
    Request = namedtuple("Request", ["user", "group", "query_params"])

    context = {
        "request": Request(
            user=User.objects.get(username=username),
            group=Group.objects.get(pk=group_id),
            query_params=[],
        )
    }

    return send_mail(
        slug,
        context,
        serializer=PermissionlessNotificationTemplateSendmailSerializer,
        **kwargs,
    )


def send_mail(
    slug,
    context,
    serializer=NotificationTemplateSendmailSerializer,
    **kwargs,
):
    """Call a SendmailSerializer based on a NotificationTemplate Slug."""
    notification_template = NotificationTemplate.objects.get(slug=slug)

    data = {
        "notification_template": {
            "type": "notification-templates",
            "id": notification_template.pk,
        },
        **kwargs,
    }

    serializer = serializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer
