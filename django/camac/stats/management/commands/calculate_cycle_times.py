from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.instance.models import Instance
from camac.stats.cycle_time import compute_cycle_time


class Command(BaseCommand):
    """Calculate cycle times and save result to case meta."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-recompute",
            action="store_true",
            dest="no_recompute",
            help="Skip case if total-cycle-time exists in case.meta",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
        )
        parser.add_argument("instance", nargs="*", type=int)

    def handle(self, *args, **options):
        instances = Instance.objects.all()

        if options.get("instance"):
            instances = instances.filter(pk__in=options["instance"])
        instances = instances.exclude(
            Q(decision__isnull=True) | Q(**{"case__meta__submit-date": None})
        )
        if options.get("no_recompute"):
            instances = instances.exclude(case__meta__has_key="total-cycle-time")

        success = 0
        self.stdout.write(
            f"Starting update of instances' cycle time. {instances.count()} to process...\n"
        )
        for num, instance in enumerate(instances.iterator(), start=1):
            cycle_time_dict = compute_cycle_time(instance)
            instance.case.meta.update(cycle_time_dict)
            if not options.get("dry_run"):
                instance.case.save()
            success += 1
            if num % 100 == 0:
                self.stdout.write(f"[{num}/{instances.count()}]")
        self.stdout.write(f"Updated {success} instances' cycle times. Done.")
