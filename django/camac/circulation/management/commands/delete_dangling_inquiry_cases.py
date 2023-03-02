from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        cases = Case.objects.filter(
            workflow_id="inquiry", parent_work_item__isnull=True
        )
        self.stdout.write(
            self.style.SUCCESS(f"Delete {cases.count()} dangling inquiry cases")
        )
        cases.delete()
