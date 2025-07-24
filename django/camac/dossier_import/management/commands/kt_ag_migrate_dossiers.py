from datetime import datetime

from django.core.management.base import BaseCommand

from camac.dossier_import.config.kt_ag.kt_ag_migrator import KtAargauMigrator


class Command(BaseCommand):
    help = "Migrate dossier data from Kanton Aargau SAP"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dossier",
            type=str,
            help="The path or file glob of the dossier(s) json files from that the data will be imported, without segmentation",
            nargs=1,
        )
        parser.add_argument(
            "--source-path",
            type=str,
            help="The directory or .zip file (without toplevel directory) from that the segmented data will be imported.",
            nargs="*",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Dossiers that already exist are not attempted to be updated",
        )
        parser.add_argument(
            "--rm",
            action="store_true",
            help="Dossier files that are successfully imported are deleted.",
        )

    def handle(self, *args, **options):
        skip_existing = options.get("skip_existing")
        rm_file = options.get("rm")
        source_paths = options.get("source_path") or [None]
        dossier = (options.get("dossier") or [None])[0]
        start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        for source_path in source_paths:
            KtAargauMigrator(
                source_path, start_time, dossier, skip_existing, rm_file
            ).migrate()
