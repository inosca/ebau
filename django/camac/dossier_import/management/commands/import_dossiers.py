import pprint

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from camac.document.models import Attachment
from camac.dossier_import.messages import Summary, update_summary
from camac.dossier_import.models import DossierImport
from camac.instance.models import Instance
from camac.user.models import Group

DOSSIER_IMPORT_LOADER_DEFAULT = "zip-archive-xlsx"


class Command(BaseCommand):

    help = "Import instances and cases from zip package"

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
        group = Group.objects.get(pk=options["group_id"][0])
        f = open(options["path_to_source"][0], "rb")
        file_content = File(f)
        configured_writer_cls = import_string(
            settings.APPLICATIONS[options["override_application"]]["DOSSIER_IMPORT"][
                "WRITER_CLASS"
            ]
        )

        configured_loader_cls = import_string(
            settings.DOSSIER_IMPORT_LOADER_CLASSES.get(
                options["loader"][0],
                settings.DOSSIER_IMPORT_LOADER_CLASSES[DOSSIER_IMPORT_LOADER_DEFAULT],
            )
        )

        loader = configured_loader_cls()

        dossier_import = DossierImport.objects.create(
            user_id=options["user_id"][0],
            location_id=options["location_id"][0],
            group=group,
            service=group.service,
            source_file=file_content,
        )

        writer = configured_writer_cls(
            user_id=dossier_import.user.pk,
            group_id=dossier_import.group.pk,
            location_id=dossier_import.location.pk,
            import_settings=settings.APPLICATIONS[options["override_application"]][
                "DOSSIER_IMPORT"
            ],
        )
        dossier_import.messages["import"] = {"details": []}
        for dossier in loader.load_dossiers(options["path_to_source"][0]):
            message = writer.import_dossier(dossier, str(dossier_import.id))
            dossier_import.messages["import"]["details"].append(message.to_dict())
            dossier_import.save()
        update_summary(dossier_import)
        dossier_import.messages["import"]["summary"] = Summary(
            dossiers_written=Instance.objects.filter(
                **{"case__meta__import-id": str(dossier_import.pk)}
            ).count(),
            num_documents=Attachment.objects.filter(
                **{"instance__case__meta__import-id": str(dossier_import.pk)}
            ).count(),
        ).to_dict()
        dossier_import.save()
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
