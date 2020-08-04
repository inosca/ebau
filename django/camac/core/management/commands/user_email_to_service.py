from collections import defaultdict

from django.core.management.base import BaseCommand

from camac.user.models import Service, UserGroup


class Command(BaseCommand):
    help = "Copy user's email to their primary group's service"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **option):
        service_emails = defaultdict(list)

        # only update where user has an email, and only do it for the default groups
        for ug in UserGroup.objects.filter(default_group=1, user__email__contains="@"):
            service_emails[ug.group.service_id].append(ug.user.email)

        for service_id, mails in service_emails.items():
            Service.objects.filter(pk=service_id).update(email=",".join(mails))
