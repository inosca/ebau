import re

from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.domain_logic import CreateInstanceLogic


class Command(BaseCommand):
    help = """Migrate the dossier numbers which have no zero before the abbreviated year."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        all_cases = Case.objects.filter(**{"meta__dossier-number__isnull": False})

        cases_with_wrong_dossier_number = [
            case
            for case in all_cases
            if case.meta["dossier-number"] is not None
            and len(case.meta["dossier-number"]) == 10
        ]

        for case in cases_with_wrong_dossier_number:
            old_dossier_number = case.meta["dossier-number"]

            year = re.search("\-(.*?)\-", case.meta["dossier-number"]).group(1)

            new_dossier_number = CreateInstanceLogic.generate_identifier(
                case.instance, year=int(year)
            )

            case.meta["dossier-number"] = new_dossier_number
            case.save()

            self.stdout.write(
                f"Dossier number was migrated from {old_dossier_number} to {new_dossier_number}"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
