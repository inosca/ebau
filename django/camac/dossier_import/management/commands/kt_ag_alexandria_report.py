from django.core.management.base import BaseCommand

from camac.dossier_import.config.kt_ag.kt_ag_alexandria_report_generator import (
    KtAargauAlexandriaReportGenerator,
)


class Command(BaseCommand):  # pragma: no cover
    help = (
        "Create a report for migrated documents from SAP to Alexandria based on export reports "
        "from the export REST endpoint."
        "For each .csv file found in the source-path, a report file with the same name is created in the "
        "source-path/alexandria subdirectory."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--source-path",
            dest="source_path",
            type=str,
            help="The directory that contains export-reports.",
            nargs="*",
        )

    def handle(self, *args, **options):
        source_paths = options.get("source_path") or [None]

        for source_path in source_paths:
            KtAargauAlexandriaReportGenerator(source_path).generate()
