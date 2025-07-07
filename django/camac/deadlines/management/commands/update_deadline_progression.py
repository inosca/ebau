from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.deadlines import models as deadlines_models


class Command(BaseCommand):
    help = """
    Management command to update deadlines progression.

    All deadlines that have any non-closed suspensions will be updated.
    """

    @transaction.atomic
    def handle(self, *args, **options):
        verbosity = int(options["verbosity"])

        updates = deadlines_models.InstanceDeadline.objects.recalculate_deadlines()
        if verbosity >= 2:
            log = getLogger(__name__)
            for deadline in updates:
                end_date = (
                    deadline.process_deadline_date.strftime("%Y-%m-%d")
                    if deadline.process_deadline_date
                    else "None"
                )
                lead_time = (
                    deadline.deadline_type.lead_time
                    if deadline.deadline_type
                    else "None"
                )
                log.info(
                    f"Updated deadline for instance {deadline.instance.pk} and service "
                    f"{deadline.service.pk}: {deadline.total_days_of_suspension} days, "
                    f"end date {end_date} with lead time "
                    f"{lead_time}"
                )
