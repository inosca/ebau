from datetime import datetime

from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Issue

status_map = {"open": "ready", "delayed": "suspended", "done": "completed"}


class Command(BaseCommand):
    help = "Migrate all issues in the existing database to caluma workitems"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Migrating all Issues to WorkItems")
        task = Task.objects.get(slug="create-manual-workitems")
        for issue in Issue.objects.all():
            case = Case.objects.get(
                meta__contains={"camac-instance-id": issue.instance.pk}
            )
            deadline = datetime(
                issue.deadline_date.year,
                issue.deadline_date.month,
                issue.deadline_date.day,
            )

            WorkItem.objects.create(
                name=issue.text[:20],
                description=issue.text,
                deadline=deadline,
                status=status_map[issue.state],
                addressed_groups=[issue.service.pk],
                controlling_groups=[issue.service.pk],
                assigned_users=[issue.user.pk],
                task=task,
                case=case,
                created_at=datetime.now(),
                modified_at=datetime.now(),
            )

        self.stdout.write("Created all WorkItems from Issues with no problems")
