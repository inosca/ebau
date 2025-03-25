import pprint

from django.conf import settings
from django.core.management.base import BaseCommand

from camac.dossier_import.domain_logic import perform_import
from camac.dossier_import.models import DossierImport
from camac.user.models import Group, User


class Command(BaseCommand):
    help = "Import a form from an data integration"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dossier",
            type=str,
            help="The path or file glob of the dossier(s) from that the form data will be imported",
            nargs=1,
        )

    def handle(self, *args, **options):
        user_id = User.objects.get(username=settings.DOSSIER_IMPORT["USER"]).pk
        # todo switch to group name
        group_id = Group.objects.get(group_id=settings.DOSSIER_IMPORT["GROUP"]).pk

        if options.get("dossier"):
            dossier_path = options.get("dossier")[0]
            self.stdout.write(f"Importing from '{dossier_path}'")
            dossier_import = DossierImport.objects.create(
                user_id=user_id,
                group_id=group_id,
                dossier_loader_type="Kanton Aargau SAP",
                source_file=dossier_path,
            )
        else:
            self.stdout.write("Importing all")
            dossier_import = DossierImport.objects.create(
                user_id=user_id,
                group_id=group_id,
                dossier_loader_type="Kanton Aargau SAP",
                source_file=f"{settings.DOSSIER_IMPORT['SAP_ACCESS']['json_target_dir']}/**/*.json",
            )

        self.stdout.write(f"Starting import: {dossier_import.pk}")

        perform_import(dossier_import)

        self.stdout.write(f"Dossier import finished Ref: {str(dossier_import.pk)}")
        self.stdout.write(
            f"{pprint.pformat(dossier_import.messages['import']['summary'])}"
        )
