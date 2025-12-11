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


def get_context(user_or_username: User | str, group: Group | int):
    if not user_or_username or not group:
        return {}

    if isinstance(user_or_username, User):
        user = user_or_username
    else:
        user = User.objects.get(username=user_or_username)

    if not isinstance(group, Group):
        group = Group.objects.get(pk=group)

    return {"request": Request(user=user, group=group, query_params=[])}


def send_mail_without_request(
    slug, user_or_username: User | str = None, group: Group | int = None, **kwargs
):
    """Send notification email if you don't have a HTTP request.

    Note: You can leave out username and group_id. In that case, the emails
    will be sent from the system / support account.
    """

    return send_mail(
        slug,
        get_context(user_or_username, group),
        serializer=PermissionlessNotificationTemplateSendmailSerializer,
        **kwargs,
    )


def send_mail(
    slug: str,
    context: dict,
    serializer=NotificationTemplateSendmailSerializer,
    **kwargs,
):
    """Call a SendmailSerializer based on a NotificationTemplate Slug.

    Only use this when there is no previous business logic that already validated
    instance access. For most cases where you want to send notifications from
    python code, call `send_mail_without_request`.
    """
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
