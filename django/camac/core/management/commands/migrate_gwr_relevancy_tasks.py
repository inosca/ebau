import datetime
from datetime import timedelta

from caluma.caluma_form.models import Document
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
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
            2024, 1, 13, 0, 0, 0, 0, tzinfo=datetime.timezone.utc
        )

        instances = Instance.objects.filter(
            Q(creation_date__gte=due_date, case__document__form_id="building-permit")
            & ~Q(instance_state__name__in=["new", "arch", "old", "del", "rejected"])
        )

        check_gwr_relevancy_task = Task.objects.get(pk="check-gwr-relevancy")

        user = AnonymousUser()

        counter = 0
        for instance in instances:
            if instance.instance_state == "new":
                continue
            if instance.case.work_items.filter(
                task_id="complete-check", status="ready"
            ).exists():
                continue

            if instance.case.work_items.filter(
                task_id="complete-construction-monitoring",
                status__in=["completed", "skipped"],
            ).exists():
                continue

            gwr_relevancy_work_item = instance.case.work_items.filter(
                task_id="check-gwr-relevancy"
            ).first()

            complete_check_work_item = instance.case.work_items.filter(
                task_id="complete-check"
            ).first()

            if not gwr_relevancy_work_item:
                instance.case.work_items.create(
                    task=check_gwr_relevancy_task,
                    name=check_gwr_relevancy_task.name,
                    status=WorkItem.STATUS_READY,
                    addressed_groups=complete_check_work_item.addressed_groups,
                    controlling_groups=complete_check_work_item.addressed_groups,
                    created_at=now(),
                    created_by_user=user,
                    created_by_group=user.group,
                    previous_work_item=instance.case.work_items.filter(
                        task_id="complete-check"
                    ).first(),
                    document=Document.objects.create_document_for_task(
                        check_gwr_relevancy_task, user
                    ),
                    deadline=timezone.now() + timedelta(days=28),
                )
                self.stdout.write(
                    f"A work-item of type 'check-gwr-relevancy' was created for the instance {instance.pk}"
                )
                counter += 1
            else:
                self.stdout.write("No work-items were created")

        self.stdout.write(f"{counter} work-items were created")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
