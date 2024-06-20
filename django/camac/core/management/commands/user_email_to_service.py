from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models.functions import Collate

from camac.user.models import Service, UserGroup


class Command(BaseCommand):
    help = "Copy user's email to their primary group's service"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **option):
        service_emails = defaultdict(list)

        # only update where user has an email, and only do it for the default groups
        # PostgreSQL does not allow LIKE queries with nondeterministic collations
        # therefore annotate a deterministic collation for this query
        # und-x-icu: general purpose, language-agnostic Unicode collation
        for ug in UserGroup.objects.annotate(
            email_deterministic=Collate("user__email", "und-x-icu")
        ).filter(default_group=1, email_deterministic__contains="@"):
            service_emails[ug.group.service_id].append(ug.user.email)

        for service_id, mails in service_emails.items():
            Service.objects.filter(pk=service_id).update(email=",".join(mails))
