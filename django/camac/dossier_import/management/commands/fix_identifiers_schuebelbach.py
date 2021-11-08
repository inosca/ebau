from django.core.management import BaseCommand
from django.db.models import Count
from django.db.models.functions import ExtractYear

from camac.core.models import WorkflowEntry
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.master_data import MasterData
from camac.instance.models import Instance


class Command(BaseCommand):  # pragma: no cover

    help = """Fix bad identifiers (ebau numbers) for Schübelbach."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            type=bool,
            help="Commit changes to db",
        )

    def handle(self, *args, **options):
        Instance.objects.filter(
            **{"case__meta__import-id": "04891f6d-aed4-44fb-88fe-58ad76660bb2"}
        ).count()

        instances_before_2021 = Instance.objects.filter(
            **{"case__meta__import-id": "04891f6d-aed4-44fb-88fe-58ad76660bb2"}
        ).filter(
            workflowentry__workflow_date__year__lt=2021,
            workflowentry__workflow_item_id=10,
        )

        print(f"Total before 2021: {instances_before_2021.count()}")
        print(
            f"duplicate identifiers: {Instance.objects.all().values('identifier').annotate(Count('pk')).order_by().filter(pk__count__gt=1)}"
        )

        years = (
            WorkflowEntry.objects.filter(
                **{
                    "instance__case__meta__import-id": "04891f6d-aed4-44fb-88fe-58ad76660bb2"
                },
                workflow_item_id=10,
            )
            .annotate(year=ExtractYear("workflow_date__year"))
            .values("year")
            .annotate(Count("year"))
            .values_list("year", flat=True)
        )

        print("=== before ===")
        cnt = 0
        for year in years:
            yr = f"{year % 100:02}"
            count = Instance.objects.filter(
                identifier__startswith=f"IM-46-{yr}-"
            ).count()
            print(f"IM-46-{yr}: {count}")
            cnt += count

        print(f"Total: {cnt}")

        for instance in instances_before_2021.iterator():
            instance.case.meta = {"ident-save": instance.identifier}
            instance.identifier = None
            md = MasterData(instance.case)
            instance.identifier = CreateInstanceLogic.generate_identifier(
                instance, year=md.submit_date.year, prefix="IM", seq_zero_padding=4
            )
            if options.get("commit"):
                instance.save()

        print("=== after ===")
        print(f"Total before 2021: {instances_before_2021.count()}")
        print(
            f"duplicate identifiers: {Instance.objects.all().values('identifier').annotate(Count('pk')).order_by().filter(pk__count__gt=1)}"
        )

        years = (
            WorkflowEntry.objects.filter(
                **{
                    "instance__case__meta__import-id": "04891f6d-aed4-44fb-88fe-58ad76660bb2"
                },
                workflow_item_id=10,
            )
            .annotate(year=ExtractYear("workflow_date__year"))
            .values("year")
            .annotate(Count("year"))
            .values_list("year", flat=True)
        )

        cnt = 0
        for year in years:
            yr = f"{year % 100:02}"
            count = Instance.objects.filter(
                identifier__startswith=f"IM-46-{yr}-"
            ).count()
            print(f"IM-46-{yr}: {count}")
            cnt += count

        print(f"Total: {cnt}")
