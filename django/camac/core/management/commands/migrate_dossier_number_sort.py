from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.core.utils import generate_sort_key


class Command(BaseCommand):
    help = """Set the numerical sort key for the passed meta key."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )
        parser.add_argument(
            "--key",
            default="ebau-number",
            action="store",
            nargs="?",
            help="Meta key which stores the dossier-number/ebau-number",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(f"Migrating to create {options['key']}-sort")
        sid = transaction.savepoint()

        chunk = []
        # smaller chunk to be memory friendly
        chunk_size = 5000

        cases = Case.objects.filter(meta__has_key=options["key"]).only("meta")
        for i, case_old in enumerate(
            tqdm(
                cases.iterator(chunk_size=chunk_size),
                total=cases.count(),
            )
        ):
            # expected format 2020-12345, extracting 2020, 12345
            case_old.meta[options["key"] + "-sort"] = generate_sort_key(
                case_old.meta[options["key"]]
            )
            chunk.append(case_old)

            if i % chunk_size == 0 and chunk:
                Case.objects.bulk_update(chunk, ["meta"])
                chunk = []

        # update the remaining cases
        Case.objects.bulk_update(chunk, ["meta"])

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

        self.stdout.write("Finished migration")
