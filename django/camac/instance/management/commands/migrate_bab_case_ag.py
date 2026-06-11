from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from tqdm import tqdm

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.verbosity = options.get("verbosity", 1)
        sid = transaction.savepoint()

        bab_instances = Instance.objects.annotate(
            has_bauzone=Exists(
                Answer.objects.filter(
                    document=OuterRef("case__document"),
                ).filter(
                    Q(question_id="ausserhalb-bauzone", value="ausserhalb-bauzone-ja")
                    | Q(
                        question_id="bauzonen-auswahl-migration",
                        value="bauzonen-auswahl-migration-ausserhalb-rechtskraeftiger-bauzone",
                    )
                )
            )
        ).filter(has_bauzone=True)
        count = bab_instances.count()

        for instance in tqdm(
            bab_instances, total=count, desc="Processing BAB instances"
        ):
            instance.case.meta["is-bab"] = True
            instance.case.save()

            if self.verbosity >= 2:
                tqdm.write(
                    f"Dossier {instance.pk}: setting 'is-bab' flag for case {instance.case.pk}"
                )

        if options["commit"]:
            print(f"Committing changes to database, {count} instances cancelled")
            transaction.savepoint_commit(sid)
        else:
            print(f"{count} instances would have been changed")
            print(
                "Not committing changes to database. Run again with --commit to actually apply changes"
            )
            transaction.savepoint_rollback(sid)
