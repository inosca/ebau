from logging import getLogger

from django.core.management.base import BaseCommand

from camac.deadlines import models as deadlines_models


class Command(BaseCommand):
    help = """
    Management command to update deadlines progression.

    All deadlines where there are open suspensions, no end-date is set,
    or the end-date is in the future will be recalculated.
    If the --all option is given, all deadlines will be recalculated.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Update all deadlines, not only those that are active.",
        )

    def handle(self, *args, **options):
        verbosity = int(options["verbosity"])
        all = int(options["all"])

        updates = deadlines_models.InstanceDeadline.objects.recalculate_deadlines(
            process_all=all
        )
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
                    f"Updated deadline for instance {deadline.instance.pk}"
                    f"[state-{deadline.instance.instance_state.name}] "
                    f"and service {deadline.service.pk}[{deadline.service.get_name()}]: "
                    f"{deadline.total_days_of_suspension} days suspended, "
                    f"processed days: {deadline.process_deadline_days}, "
                    f"end date {end_date} with lead time "
                    f"{lead_time} days."
                    f" Completed: {deadline.completed}"
                )
