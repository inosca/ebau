import time
from logging import getLogger
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from camac.gis_export.domain_logic import collect_so_exports
from camac.gis_export.formatters import build_sogis_transfer_xml
from camac.gis_export.models import SOGISExport

log = getLogger(__name__)


class Command(BaseCommand):
    help = """Command to run the SO GIS export locally.

    Writes the same XTF the API endpoint would return. Nothing is persisted
    unless --commit is passed.
    """

    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")
        parser.add_argument(
            "--mark-exported",
            action="store_true",
            help=(
                "Mark the exported dossiers as delivered - SO will NOT receive "
                "them again. Only for deliveries made out of band. Requires --commit."
            ),
        )
        parser.add_argument("--output", help="Write the XTF here instead of stdout")
        parser.add_argument(
            "--validate-only",
            action="store_true",
            help="Only report which dossiers cannot be exported",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["mark_exported"] and not options["commit"]:
            raise CommandError("--mark-exported requires --commit")

        savepoint = transaction.savepoint()

        start = time.time()
        transfer = build_sogis_transfer_xml(collect_so_exports())
        log.info(f"Execution time: {time.time() - start:.2f} seconds")

        for error in transfer.errors:
            self.stderr.write(str(error))

        self.stderr.write(
            f"{len(transfer.exported)} exportable, {len(transfer.errors)} invalid"
        )

        if transfer.exported and not options["validate_only"]:
            if options["output"]:
                Path(options["output"]).write_text(transfer.xml, encoding="utf-8")
                self.stderr.write(f"Wrote {options['output']}")
            else:
                self.stdout.write(transfer.xml)

            if options["mark_exported"]:
                # Only what actually made it into the document. The invalid
                # ones have to stay pending so they are retried.
                SOGISExport.objects.mark_exported(
                    [export.pk for export in transfer.exported]
                )
                self.stderr.write(
                    f"Marked {len(transfer.exported)} export(s) as delivered"
                )

        if options["commit"]:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)
