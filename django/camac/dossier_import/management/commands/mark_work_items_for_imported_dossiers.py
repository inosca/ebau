from datetime import datetime, timedelta

from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db.models import Q, QuerySet

from camac.instance.models import Instance


class Command(BaseCommand):
    help = "Mark all work items generated from dossier import as imported."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            dest="commit",
            default=False,
            help="Do not pretend, commit changes to DB",
            required=False,
        )
        parser.add_argument(
            "--buffer",
            type=int,
            nargs=1,
            help="Time buffer in minutes on which work items should be marked as imported based on instance creation date.",
        )

    def handle(self, *args, **options):
        instances: QuerySet[Instance] = Instance.objects.filter(
            case__document__form_id="migriertes-dossier"
        )
        for instance in instances:
            instance_creation_date: datetime = instance.creation_date
            work_items: QuerySet[WorkItem] = instance.case.work_items.filter(
                Q(meta__imported__isnull=True) | Q(meta__imported=False)
            )
            if not work_items.count():
                print(f"No work items to migrate for instance {instance.pk}.")
                continue

            for work_item in work_items:
                try:
                    buffer: timedelta = timedelta(minutes=options["buffer"][0])
                except TypeError:
                    buffer: timedelta = timedelta(minutes=5)

                if (
                    work_item.created_at >= instance_creation_date - buffer
                    and work_item.created_at <= instance_creation_date + buffer
                ):
                    work_item.meta["imported"] = True
                    print(
                        f"{work_item.pk}: {work_item.created_at} marked as imported as it's {buffer} minute/s within instance creation date {instance_creation_date} ({instance.pk})."
                    )
                    if options["commit"]:
                        work_item.save()
