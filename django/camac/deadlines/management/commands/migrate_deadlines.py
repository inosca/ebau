from itertools import chain
from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.caluma.models import Inquiry
from camac.deadlines import models as deadlines_models
from camac.instance.models import Instance, Service

log = getLogger(__name__)


class Command(BaseCommand):
    help = """
    Management command to migrate instance deadlines records.

    Each instance will create a deadline if needed for the involved services.
    Start- end end dates will be set automatically.
    """

    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        verbosity = int(options["verbosity"])
        do_commit = options.get("commit")
        savepoint = transaction.savepoint()

        instances = Instance.objects.all().order_by("pk")
        for instance in tqdm(instances.iterator(), desc="Processing instances"):
            if verbosity >= 1:
                log.info(f"> Processing instance {instance.pk} for deadline migration.")

            responsible_service = instance.responsible_service()
            addressed_groups = list(
                chain(
                    *Inquiry.objects.for_instance(instance)
                    .exclude_withdrawn()
                    .values_list("addressed_groups", flat=True)
                )
            )
            involved_services = [
                responsible_service,
                *Service.objects.filter(pk__in=addressed_groups),
            ]

            for service in involved_services:
                deadline = (
                    deadlines_models.InstanceDeadline.objects.for_instance(instance)
                    .for_service(service)
                    .first()
                )

                if deadline:
                    continue

                deadline = deadlines_models.InstanceDeadline.objects.create_deadline(
                    instance=instance,
                    service=service,
                )

                if not deadline:
                    continue

                deadline.recalculate_progression()
                if verbosity >= 1:
                    start_date = self._format_date(deadline.start_date)
                    end_date = self._format_date(deadline.process_deadline_date)
                    lead_time = self._format_days(
                        deadline.deadline_type.lead_time
                        if deadline.deadline_type
                        else 0
                    )

                    log.info(
                        f"  > Created deadline for instance {deadline.instance.pk} and service "
                        f"{deadline.service.pk} ({deadline.service.get_name()}): "
                        f"from {start_date} - to {end_date} with lead time "
                        f"{lead_time}"
                    )
        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)

    def _format_date(self, date):
        """Format date to string if set, otherwise return 'n.a.'."""
        return date.strftime("%Y-%m-%d") if date else "n.a."

    def _format_days(self, days):
        """Format number of days if set, otherwise return 'n.a.'."""
        return f"{days} days" if days is not None else "n.a."
