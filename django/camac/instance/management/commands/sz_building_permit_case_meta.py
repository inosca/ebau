from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.utils import generate_sort_key
from camac.instance.models import Instance


class Command(BaseCommand):
    help = "Set missing meta attributes on building permits cases"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Modify data for real",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        building_permits = (
            Instance.objects.filter(case__workflow__slug="building-permit")
            .exclude(instance_state__name="new")
            .select_related("case")
        )

        tid = transaction.savepoint()
        for instance in building_permits:
            instance.case.meta["form-backend"] = "camac-ng"
            instance.case.meta["dossier-number"] = instance.identifier
            instance.case.meta["dossier-number-sort"] = generate_sort_key(
                instance.identifier
            )
            instance.case.save(update_fields=["meta"])
            self.stdout.write(f"{instance.case.meta}")
        if options["commit"]:
            transaction.savepoint_commit(tid)
        else:
            transaction.savepoint_rollback(tid)
