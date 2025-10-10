from collections import namedtuple

import jinja2
from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from camac.notification.models import NotificationTemplate
from camac.notification.serializers import (
    NotificationTemplateSendmailSerializer,
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.user.models import Group, User

Request = namedtuple("Request", ["user", "group", "query_params"])


def send_mail_without_request(slug, username=None, group_id=None, **kwargs):
    """Send notification email if you don't have a HTTP request.

    Note: You can leave out username and group_id. In that case, the emails
    will be sent from the system / support account.
    """
    if not username or not group_id:
        context = {}
    else:
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
    slug: str,
    context: dict,
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


def send_mail_without_instance(
    notification_template_slug: str,
    recipients: list[str],
    additional_placeholders: dict = {},
):
    notification_template = NotificationTemplate.objects.get(
        slug=notification_template_slug
    )
    placeholder_data = (
        _get_placeholder_data_without_instance() | additional_placeholders
    )

    subject = notification_template.get_trans_attr("subject")
    body = notification_template.get_trans_attr("body")
    subject = _merge(subject, placeholder_data)
    body = _merge(body, placeholder_data)

    django_send_mail(
        subject,
        body,
        from_email=None,
        recipient_list=recipients,
    )


def _merge(value, data):
    value_template = jinja2.Template(value)

    return value_template.render(data)


def _get_placeholder_data_without_instance():
    return {"INTERNAL_BASE_URL": settings.INTERNAL_BASE_URL}
