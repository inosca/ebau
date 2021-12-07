import pprint
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from camac.dossier_import.models import DossierImport
from camac.dossier_import.validation import (
    validate_zip_archive_structure,
    verify_source_file,
)
from camac.user.models import Group

DOSSIER_IMPORT_LOADER_DEFAULT = "zip-archive-xlsx"


class Command(BaseCommand):

    help = "Validate archive for dossier_import"

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
        parser.add_argument(
            "path_to_source", type=str, nargs=1, help="Where to find th"
        )
        parser.add_argument(
            "--loader",
            type=str,
            nargs="?",
            default=DOSSIER_IMPORT_LOADER_DEFAULT,
            help=f"Specifies a loader class that provides the writer with Dossier dataclass instances. Available choices: {','.join(settings.DOSSIER_IMPORT_LOADER_CLASSES.keys())}. Defaults to {DOSSIER_IMPORT_LOADER_DEFAULT}",
        )
        parser.add_argument(
            "--override_application",
            type=str,
            nargs="?",
            default=settings.APPLICATION_NAME,
            help="Specify application name if you want to use another configuration than configured in the environment (e.g. when running tests).",
        )

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        group = Group.objects.get(pk=options["group_id"][0])

        source_file = verify_source_file(options["path_to_source"][0])

        f = open(source_file, "rb")
        file_content = File(f)

        dossier_import = DossierImport.objects.create(
            user_id=options["user_id"][0],
            location_id=options["location_id"][0],
            group=group,
            service=group.service,
            source_file=file_content,
        )
        if verbosity > 2:  # pragma: no cover
            self.stdout.write(f"Validation started: {datetime.now()}")
        dossier_import = validate_zip_archive_structure(str(dossier_import.pk))
        if verbosity > 2:  # pragma: no cover
            self.stdout.write(f"Validation finished: {datetime.now()}")
        self.stdout.write(f"(DossierImport ID: {dossier_import.pk})")
        self.stdout.write(
            pprint.pformat(
                dossier_import.messages["validation"]["summary"],
                indent=2,
                compact=True,
                depth=5,
                width=250,
            )
        )
