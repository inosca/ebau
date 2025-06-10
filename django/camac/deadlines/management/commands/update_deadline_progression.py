from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from tqdm import tqdm

from camac.deadlines import models as deadlines_models


class Command(BaseCommand):
    help = """
    Update deadline progression while suspensions are open.
    """

    @transaction.atomic
    def handle(self, *args, **options):
        deadlines = self.query_open_deadlines()

        for deadline in tqdm(deadlines, desc="Updating deadlines"):
            try:
                deadline.update_progression()

                self.stdout.write(
                    f"Updated deadline for instance {deadline.instance.pk} and service {deadline.service.pk}: {deadline.total_days_of_suspension} days, end date {deadline.process_deadline_date.strftime('%Y-%m-%d') if deadline.process_deadline_date else 'None'} with lead time {deadline.deadline_type.lead_time if deadline.deadline_type else 'None'}"
                )
            except Exception as e:  # pragma: no cover
                self.stderr.write(
                    f"Error updating deadline for instance {deadline.instance.pk}: {e}"
                )
                continue

    def query_open_deadlines(self):
        """Query deadlines related to services/instances with open suspensions."""
        return deadlines_models.InstanceDeadline.objects.annotate(
            has_open_suspension=Exists(
                deadlines_models.Suspension.objects.filter(
                    deadline=OuterRef("pk"),
                    end_date__isnull=True,
                )
            )
        ).filter(has_open_suspension=True)
