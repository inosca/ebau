import pprint

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from camac.instance.models import Instance


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
        parser.add_argument(
            "override_application",
            type=str,
            nargs="?",
            default=settings.APPLICATION_NAME,
            help="Specify application name if you want to use another configuration than configured in the environment (e.g. when running tests).",
        )

    def handle(self, *args, **options):

        configured_writer_cls = import_string(
            settings.APPLICATIONS[options["override_application"]]["DOSSIER_IMPORT"][
                "ZIP_ARCHIVE_IMPORT_DOSSIER_WRITER_CLASS"
            ]
        )

        configured_loader_cls = import_string(
            settings.APPLICATIONS[options["override_application"]]["DOSSIER_IMPORT"][
                "ZIP_ARCHIVE_IMPORT_DOSSIER_LOADER_CLASS"
            ]
        )

        loader = configured_loader_cls()
        writer = configured_writer_cls(
            user_id=options["user_id"][0],
            group_id=options["group_id"][0],
            location_id=options["location_id"][0],
            path_to_archive=options["path_to_archive"][0],
            import_settings=settings.APPLICATIONS[options["override_application"]][
                "DOSSIER_IMPORT"
            ],
        )
        for dossier in loader.load_dossiers(writer.dossiers_xlsx):
            message = writer.import_dossier(dossier)
            if options["verbosity"] > 1:
                self.stdout.write(pprint.pformat(message), self.style.NOTICE)
        self.stdout.write("========= Dossier import =========")
        for line in filter(lambda x: x["level"] > 1, writer.import_session.messages):
            self.stdout.write(str(line))
        self.stdout.write(f"Dossier import finished Ref: {writer.import_session.pk}")
        imported_count = Instance.objects.filter(
            **{"case__meta__import-id": str(writer.import_session.pk)}
        ).count()
        self.stdout.write(f"{imported_count} instances imported.")
