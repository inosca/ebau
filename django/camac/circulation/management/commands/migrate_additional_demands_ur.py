from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true", default=False)

    def reset(self):
        Case.objects.filter(**{"meta__migrated-additional-demand-case": True}).delete()
        WorkItem.objects.filter(
            task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
            **{"meta__migrated": True},
        ).delete()

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        create_inquiry_work_items = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
            status=WorkItem.STATUS_READY,
        )

        for inquiry_work_item in tqdm(
            create_inquiry_work_items, mininterval=1, maxinterval=2
        ):
            # Any service that has an open inquiry work item should also have a ready init-additional-demand work item
            init_additional_demand_work_item = WorkItem.objects.filter(
                task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                addressed_groups=inquiry_work_item.addressed_groups,
                status=WorkItem.STATUS_READY,
                case__family__instance__pk=inquiry_work_item.case.family.instance.pk,
            ).first()

            if not init_additional_demand_work_item:
                WorkItem.objects.create(
                    task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                    addressed_groups=inquiry_work_item.addressed_groups,
                    status=WorkItem.STATUS_READY,
                    meta={"migrated": True},
                    case=inquiry_work_item.case.family.work_items.get(
                        task_id=settings.DISTRIBUTION["DISTRIBUTION_TASK"]
                    ).child_case,
                )

                tqdm.write(
                    f"Migrated additional demand work item for #{inquiry_work_item.case.family.instance.pk}"
                )

        for instance in Instance.objects.filter(
            instance_state__name__in=["subm", "comm", "circ", "done"],
            case__status="running",
        ):
            if responsible_service := instance.responsible_service():
                # Any service that is responsible for an instance should also have a ready "init-additional-demand" work item
                init_additional_demand_work_item = WorkItem.objects.filter(
                    task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                    addressed_groups=[str(responsible_service.pk)],
                    status=WorkItem.STATUS_READY,
                )

                if not init_additional_demand_work_item:
                    WorkItem.objects.create(
                        task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                        addressed_groups=[str(responsible_service.pk)],
                        status=WorkItem.STATUS_READY,
                        meta={"migrated": True},
                        case=instance.case,
                    )

        tqdm.write("Completed migration")
