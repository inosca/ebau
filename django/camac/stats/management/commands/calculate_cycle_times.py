from django.core.management.base import BaseCommand

from camac.instance.models import Instance
from camac.stats.cycle_time import compute_cycle_time


class Command(BaseCommand):
    """Calculate cycle times and safe result to case meta."""

    def handle(self, **options):
        instances = Instance.objects.exclude(
            decision__isnull=True,
            case__meta__has_key="total_cycle_time",  # do not recompute
            **{
                "case__meta__submit-date": None,
            },
        )
        success = 0
        failure = 0
        self.stdout.write(
            f"Starting update of instances' cycle time. {instances.count()} to process...\n"
        )
        for instance in instances.iterator():
            try:
                cycle_time_dict = compute_cycle_time(instance)
            except Exception as e:
                self.stderr.write(
                    f"Failed to update cycle time for instance {instance.pk} with error: {e}"
                )
                failure += 1
                continue
            instance.case.meta.update(cycle_time_dict)
            instance.case.save()
            success += 1
        self.stdout.write(
            f"Updated instances cycle times. Success: {success}. Fails: {failure}."
        )
