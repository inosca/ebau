from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string


class Command(BaseCommand):
    help = "Import instances and cases from zip package"

    def add_arguments(self, parser):
        parser.add_argument(
            "service_id",
            type=int,
            help="This identifies the 'Gemeinde' responsible"
            " for the dossiers about to be imported.",
        )
        parser.add_argument("path_to_archive", type=str)

    def handle(self, *args, **options):
        importer_cls = import_string(
            settings.APPLICATION["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls()
        importer.initialize(options["service_id"], options["path_to_archive"])
        importer.import_dossiers()
