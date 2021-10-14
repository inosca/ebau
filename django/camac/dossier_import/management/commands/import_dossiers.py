from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string


class Command(BaseCommand):

    help = "Import instances and cases from zip package" "" ""

    def add_arguments(self, parser):
        parser.add_argument(
            "user_id",
            type=int,
            help="The ID of the user who should perform the import",
            nargs=1,
        )
        parser.add_argument(
            "group_id",
            type=int,
            nargs=1,
            help="The Service ID is required to assign the import to the original entity.",
        )
        parser.add_argument(
            "location_id",
            type=int,
            nargs=1,
            help="The location every imported instance is located to.",
        )
        parser.add_argument("path_to_archive", type=str, nargs=1)

    def handle(self, *args, **options):
        importer_cls = import_string(
            settings.APPLICATION["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls(user_id=options["user_id"][0])
        importer.initialize(
            options["group_id"][0],
            options["location_id"][0],
            options["path_to_archive"][0],
        )
        importer.import_dossiers()
        self.stdout.write(f"Dossier import finished Ref: {importer.import_case.pk}")
        self.stdout.write(f"{len(importer.import_case.messages)} instances imported.")
        for line in filter(lambda x: x["level"] > 1, importer.import_case.messages):
            self.stdout.write(str(line))
