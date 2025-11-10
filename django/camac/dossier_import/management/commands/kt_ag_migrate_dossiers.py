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
            help="Do not update existing dossiers, only create new ones. Default: false.",
        )
        parser.add_argument(
            "--rm",
            action="store_true",
            help="Dossier files that are successfully imported are deleted. Default: false.",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            help="Send notification emails when creating inquiries. Default: false.",
        )
        parser.add_argument(
            "--skip-dossier-import",
            action="store_true",
            help="Do not import any form data of the dossiers. Default: false.",
        )
        parser.add_argument(
            "--skip-document-import",
            action="store_true",
            help="Do not import any document form S3 to Alexandria. Default: false.",
        )
        parser.add_argument(
            "--skip-document-export",
            action="store_true",
            help="Do not export documents form SAP to S3. Default: false.",
        )
        parser.add_argument(
            "--only-municipalities",
            type=str,
            help="Only migrate municipalites from this blank separated list. Default: all municipalities from the source are migrated.",
            nargs="*",
        )
        parser.add_argument(
            "--only-dossiers",
            type=str,
            help="Only migrate dossier with ids from this blank separated list. Default: all dossiers from the source are migrated.",
            nargs="*",
        )

    def handle(self, *args, **options):
        skip_existing = options.get("skip_existing")
        rm_file = options.get("rm")
        notify = options.get("notify")
        source_paths = options.get("source_path") or [None]
        dossier = (options.get("dossier") or [None])[0]
        start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        skip_dossier_import = options.get("skip_dossier_import")
        skip_document_import = options.get("skip_document_import")
        skip_document_export = options.get("skip_document_export")
        only_municipalities = options.get("only_municipalities") or None
        only_dossiers = options.get("only_dossiers") or None

        for source_path in source_paths:
            KtAargauMigrator(
                source_path,
                start_time,
                dossier,
                skip_existing,
                rm_file,
                not notify,
                skip_dossier_import,
                skip_document_import,
                skip_document_export,
                only_municipalities,
                only_dossiers,
            ).migrate()
