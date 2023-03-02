from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            default=False,
            dest="dry",
            action="store_true",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        decisions = (
            WorkItem.objects.filter(
                task_id="decision",
                document__isnull=True,
                status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
            )
            .exclude(case__workflow_id="migrated")
            .order_by("case__instance__pk")
        )

        for decision in tqdm(decisions):
            decision_with_document = (
                decision.case.work_items.filter(
                    task_id="decision", document__isnull=False
                )
                .exclude(pk=decision.pk)
                .order_by("-created_at")
            ).get()

            document = decision_with_document.document

            if (
                decision_with_document.status == WorkItem.STATUS_COMPLETED
                and decision.closed_at > decision_with_document.closed_at
            ):
                decision_with_document.delete()
                decision_with_document = None
                tqdm.write(
                    self.style.WARNING(
                        f"Deleted duplicate completed decision work item for instance {decision.case.instance.pk}"
                    )
                )

            if decision_with_document:
                decision_with_document.document = None
                decision_with_document.save()

            decision.document = document
            decision.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Fixed missing decision documents for {len(decisions)} instances"
            )
        )

        assert not decisions.all().exists()

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
