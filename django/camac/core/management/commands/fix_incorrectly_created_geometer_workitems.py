from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose", dest="verbose", action="store_true", default=False
        )
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        geom_workitems = WorkItem.objects.filter(
            task="geometer",
            status=WorkItem.STATUS_READY,
        )

        affected_workitems = geom_workitems.filter(
            Exists(
                WorkItem.objects.filter(
                    task="decision",
                    document__answers__value="decision-geometer-no",
                    case_id=OuterRef("case_id"),
                    status__in=[
                        WorkItem.STATUS_COMPLETED,
                        WorkItem.STATUS_SKIPPED,
                    ],
                )
            )
        )
        count = affected_workitems.count()
        for wi in affected_workitems:
            wi.status = WorkItem.STATUS_CANCELED
            wi.meta["canceled-due-to-incorrect-geometer"] = True
            wi.save()
            dossier_nr = wi.case.instance.pk
            print(
                f"Dossier {dossier_nr}: cancelling 'geometer' workitem {wi.pk} due to bug"
            )

        if options["commit"]:
            print(f"Committing changes to database, {count} work items cancelled")
            transaction.savepoint_commit(sid)
        else:
            print(f"{count} work items would have been cancelled")
            print(
                "Not committing changes to database. Run again with --commit to actually apply changes"
            )
            transaction.savepoint_rollback(sid)
