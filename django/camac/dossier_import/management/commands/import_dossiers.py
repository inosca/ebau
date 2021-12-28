import json
import pprint
from dataclasses import asdict

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from camac.dossier_import.messages import get_message_max_level
from camac.dossier_import.models import DossierImport
from camac.dossier_import.validation import validate_zip_archive_structure
from camac.user.models import Group


class Command(BaseCommand):

    help = "Import instances and cases from zip package"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            default=False,
            help="If set, do not ask to abort import on validation failure.",
        )
        parser.add_argument(
            "--override_application",
            type=str,
            nargs="?",
            default=settings.APPLICATION_NAME,
            help="Specify application name if you want to use another configuration than configured in the environment (e.g. when running tests).",
        )
        source_subparsers = parser.add_subparsers(help="Specify the importing strategy")

        parser_from_archive = source_subparsers.add_parser(
            "from_archive", help="Specifiy an archive file that should be imported"
        )
        parser_from_archive.add_argument(
            "--user_id",
            type=int,
            help="The ID of the user who should perform the import",
            nargs=1,
        )
        parser_from_archive.add_argument(
            "--group_id",
            type=int,
            nargs=1,
            help="The Service ID is required to assign the import to the original entity.",
        )
        parser_from_archive.add_argument(
            "--location_id",
            type=int,
            nargs=1,
            help="The location every imported instance is located to.",
        )
        parser_from_archive.add_argument(
            "path_to_source",
            type=str,
            nargs=1,
            help="Where to find the archive",
        )

        parser_from_import_session = source_subparsers.add_parser(
            "from_session", help="Specifiy an import session's identifier (UUID)."
        )
        parser_from_import_session.add_argument(
            "dosser_import_id",
            type=str,
            nargs=1,
            help="UUID that identifies a session from a data upload.",
        )
        parser_from_import_session.add_argument(
            "--location_id",
            type=int,
            nargs=1,
            help="Set or override the location every imported instance is located to.",
        )

    def handle(self, *args, **options):
        location_id = None
        if options.get("location_id"):
            location_id = options["location_id"][0]

        if options.get("path_to_source"):
            f = open(options["path_to_source"][0], "rb")
            file_content = File(f)
            group = Group.objects.get(pk=options["group_id"][0])
            user_id = options["user_id"][0]
            dossier_import = DossierImport.objects.create(
                user_id=user_id,
                location_id=location_id,
                group=group,
                service=group.service,
                source_file=file_content,
            )

        if options.get("dosser_import_id"):
            dossier_import = DossierImport.objects.get(
                pk=options["dosser_import_id"][0]
            )
            if not dossier_import.source_file or not dossier_import.source_file.file:
                raise CommandError(
                    "No file found. File cannot be imported if validation was unsuccessful."
                )

        self.stdout.write(f"Starting import: {dossier_import.pk}")
        dossier_import = validate_zip_archive_structure(
            str(dossier_import.pk), clean_on_fail=False
        )
        self.stdout.write("Archive analysis result:")
        self.stdout.write(
            pprint.pformat(dossier_import.messages["validation"]["summary"])
        )
        if (
            dossier_import.status != DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL
            and not options.get("no_input")
        ):  # pragma: no cover
            if (
                input(
                    "The archive has errors. Do you still want to import (enter y) or abort and remove the file (enter n)"
                )
                != "y"
            ):
                return
        for message in dossier_import.perform_import(options["override_application"]):
            if get_message_max_level(message.details) > 1:
                self.stdout.write(json.dumps(asdict(message)), self.style.WARNING)

        self.stdout.write("========= Dossier import =========")
        if options["verbosity"] > 1:
            self.stdout.write(
                pprint.pformat(dossier_import.messages["import"]["details"]),
                self.style.NOTICE,
            )
        self.stdout.write(f"Dossier import finished Ref: {str(dossier_import.pk)}")
        self.stdout.write(
            f"{pprint.pformat(dossier_import.messages['import']['summary'])}"
        )
