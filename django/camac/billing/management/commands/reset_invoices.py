from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.billing.models import Invoice, LineItem

log = getLogger(__name__)


class Command(BaseCommand):
    help = "Reset invoices"

    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options) -> None:  # pragma: no cover
        savepoint = transaction.savepoint()
        do_commit = options.get("commit")
        count_i, _ = Invoice.objects.all().delete()
        count_l, _ = LineItem.objects.all().delete()
        log.info(f"Deleting {count_i} Invoices and {count_l} LineItems")
        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)
