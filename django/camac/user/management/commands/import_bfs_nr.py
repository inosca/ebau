import pyexcel
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service


class Command(BaseCommand):
    help = "Import BfS numbers for municipalities in SO"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            "-s",
            type=str,
            help="Path to excel file",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        for row in pyexcel.get_array(file_name=options["source"]):
            name = row[0].replace("(SO)", "").strip()
            full_name = f"Gemeinde {name}"

            service = Service.objects.filter(
                service_group__name="municipality", trans__name=full_name
            ).first()

            if not service:
                self.stdout.write(
                    self.style.ERROR(
                        f"No municipality with name {full_name} found -- skipping"
                    )
                )
                continue

            service.external_identifier = row[1]
            service.save()

        services_without = Service.objects.filter(
            service_group__name="municipality", external_identifier__isnull=True
        )

        if services_without.exists():
            names = ", ".join([s.get_name() for s in services_without])
            self.stdout.write(
                self.style.SUCCESS(
                    f"There are municipalities without a BfS number: {names}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("All municipalities have a BfS number")
            )
