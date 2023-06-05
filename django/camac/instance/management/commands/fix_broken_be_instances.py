from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef, Q

from camac.caluma.utils import work_item_by_addressed_service_condition
from camac.user.models import Service


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.ebaubeops380()
        self.ebaubeops381()

    @transaction.atomic
    def ebaubeops380(self):
        pending_inquiries = (
            WorkItem.objects.filter(
                task_id="inquiry",
                status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED],
            )
            .filter(
                work_item_by_addressed_service_condition(Q(service_parent__isnull=True))
            )
            .exclude(
                Exists(
                    WorkItem.objects.filter(
                        task_id="create-inquiry",
                        addressed_groups=OuterRef("addressed_groups"),
                        case=OuterRef("case"),
                    )
                )
            )
        ).order_by("addressed_groups")

        task = Task.objects.get(pk="create-inquiry")

        for i in pending_inquiries:
            WorkItem.objects.create(
                task=task,
                name=task.name,
                addressed_groups=i.addressed_groups,
                status=i.status,
                case=i.case,
            )

            svc = Service.objects.get(pk=i.addressed_groups[0])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created missing create-inquiry work item for {svc.get_name()} on instance {i.case.family.instance.pk}"
                )
            )

    @transaction.atomic
    def ebaubeops381(self):
        broken_case = Case.objects.get(instance__pk=111677)

        if broken_case.work_items.filter(task_id="decision").exists():
            return

        distribution = broken_case.work_items.get(task_id="distribution")
        distribution.status = WorkItem.STATUS_READY
        distribution.save()

        closed_at = distribution.closed_at
        user = BaseUser(
            username=distribution.closed_by_user, group=distribution.closed_by_group
        )

        skip_work_item(work_item=distribution, user=user, context={})

        distribution.status = WorkItem.STATUS_COMPLETED
        distribution.closed_at = closed_at
        distribution.save()

        self.stdout.write(self.style.SUCCESS("Fixed decision for instance 111677"))
