from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.core.utils import generate_sort_key
from camac.instance.domain_logic.create import CreateInstanceLogic


class Command(BaseCommand):
    help = "Migrates the dossier numbers for Kt. SO to the new format"

    def add_arguments(self, parser):
        parser.add_argument(
            "--summary",
            "-s",
            dest="summary",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--dry",
            "-d",
            dest="dry",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        cases = Case.objects.filter(**{"meta__dossier-number__isnull": False}).order_by(
            "meta__dossier-number-sort"
        )

        migrated = []

        for case in tqdm(cases):
            old_dossier_number = case.meta["dossier-number"]
            new_dossier_number = CreateInstanceLogic.generate_identifier_so(
                case.instance,
                int(old_dossier_number.split("-")[0]),  # extract year
            )

            case.meta["dossier-number"] = new_dossier_number
            case.meta["dossier-number-sort"] = generate_sort_key(new_dossier_number)
            case.save()

            migrated.append((old_dossier_number, new_dossier_number))

        if options["summary"]:
            numbers = "\n".join([f"\t- {old} => {new}" for old, new in migrated])
            self.stdout.write(f"Migrated dossier numbers:\n{numbers}")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
