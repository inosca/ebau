from datetime import datetime, timedelta

import pytz
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from tqdm import tqdm


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true", default=False)

    def reset(self):
        WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
        ).update(name=dict(de="Stellungnahme verfassen", fr=None))

        migrated_work_items = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_COMPLETED],
        )

        migrated_work_items.update(deadline=None)
        migrated_work_items.update(controlling_groups=[])
        migrated_work_items.update(meta={})

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        tqdm.write("Renaming inquiry task")

        WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
        ).update(name=dict(de="Stellungnahme zustellen", fr=None))

        tqdm.write("Updating fill-inquiry work-items")

        sync_to_answer_tasks = settings.DISTRIBUTION.get(
            "SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS", {}
        )

        work_items_to_migrate = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_COMPLETED],
        )

        for work_item in tqdm(work_items_to_migrate, mininterval=1, maxinterval=2):
            try:
                deadline = work_item.case.parent_work_item.document.answers.get(
                    question_id=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
                ).date

                work_item.deadline = pytz.utc.localize(
                    datetime.combine(
                        deadline
                        + sync_to_answer_tasks[
                            settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"]
                        ].get("TIME_DELTA", timedelta()),
                        datetime.min.time(),
                    )
                )

                work_item.controlling_groups = work_item.addressed_groups
                work_item.meta = {
                    "not-viewed": True,
                    "notify-completed": False,
                    "notify-deadline": True,
                }
                # Calling save() individually on each work-item seems to
                # perform better than calling bulk_update() on all
                work_item.save()

            except Exception as e:  # noqa: B902
                raise CommandError(
                    f"Exception ocurred during migration of instance {work_item.case.family.instance.pk}: {str(e)}"
                )

        tqdm.write("Migration completed")
