import datetime

from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from camac.instance.models import Instance


class Command(BaseCommand):
    help = """Create work-items of task 'check-gwr-relevancy' for every instance created after ..."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        due_date = datetime.datetime(
            2025, 1, 13, 0, 0, 0, 0, tzinfo=datetime.timezone.utc
        )

        instances = Instance.objects.filter(creation_date__gte=due_date)

        check_gwr_relevancy_task = Task.objects.get(pk="check-gwr-relevancy")

        user = AnonymousUser()

        for instance in instances:
            gwr_relevancy_work_item = instance.case.work_items.filter(
                task_id="check-gwr-relevancy"
            ).first()

            if not gwr_relevancy_work_item:
                instance.case.work_items.create(
                    task=check_gwr_relevancy_task,
                    name=check_gwr_relevancy_task.name,
                    status=WorkItem.STATUS_READY,
                    addressed_groups=[],
                    controlling_groups=[],
                    created_at=now(),
                    created_by_user=user,
                    created_by_group=user.group,
                    previous_work_item=instance.case.work_items.filter(
                        task_id="complete-check"
                    ).first(),
                    document=instance.case.document,
                )
                self.stdout.write(
                    f"A work-item of type 'check-gwr-relevancy' was created for the instance {instance.pk}"
                )
            else:
                self.stdout.write("No work-items were created")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
