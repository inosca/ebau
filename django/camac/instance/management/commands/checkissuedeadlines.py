from datetime import date

import jinja2
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand, CommandError

from camac.instance.models import Issue
from camac.notification.models import NotificationTemplate
from camac.notification.serializers import IssueMergeSerializer


class Command(BaseCommand):
    help = (
        "Marks all issues with due deadline as "
        "delayed and sends notification to service and user"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--template",
            type=int,
            help="Template to send notification to service and user",
        )

    def _merge(self, value, issue):
        try:
            value_template = jinja2.Template(value)
            data = IssueMergeSerializer(issue).data
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise CommandError(str(e))

    def handle(self, *args, **options):
        issues = Issue.objects.filter(
            state=Issue.STATE_OPEN, deadline_date__lt=date.today()
        )
        notification_template = NotificationTemplate.objects.get(pk=options["template"])

        messages = []
        for issue in issues:
            subject = self._merge(notification_template.subject, issue)
            body = self._merge(notification_template.body, issue)
            to = [issue.service.email]
            if issue.user:
                to.append(issue.user.email)
            messages.append(EmailMessage(subject=subject, body=body, to=to))

        if messages:
            connection = get_connection()
            connection.send_messages(messages)
        issues.update(state=Issue.STATE_DELAYED)
