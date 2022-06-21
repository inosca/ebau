from django.core.management.base import BaseCommand

from camac.user.models import Group


class Command(BaseCommand):
    help = "Disable obsolete groups for SZ."

    def handle(self, *args, **options):
        Group.objects.filter(
            role_id__in=[
                6,  # Kanton
                9,  # Publikation
            ]
        ).update(disabled=1)
