from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Create a DB index that prevents duplicate dossier identifiers.

        If the index can't be created, run ./manage.py fix_duplicate_identifiers first.
        """
        connection.cursor().execute(
            """
            create unique index "unique_dossier_number" on caluma_workflow_case ((meta->>'dossier-number'));
            """
        )
