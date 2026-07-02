import time
from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.gis_export.utils import export_agis

log = getLogger(__name__)


class Command(BaseCommand):
    help = """Command to run AG AGIS export."""

    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        do_commit = options.get("commit")
        savepoint = transaction.savepoint()

        start = time.time()
        export_agis()
        end = time.time()
        log.info(f"Execution time: {end - start:.2f} seconds")

        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)
