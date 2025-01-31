import pyexcel
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service


class Command(BaseCommand):
    help = """
    Import BfS numbers for municipalities.


    Bfs number and municipality name in source excel of format:
      3637 | Rothenbrunnen
      3834 | Roveredo (GR)

    There are municipalies that have a canton identifier appended to the municipality  name
    in the format "Municipality Name (CANTON IDENTIFIER)".

    Examples:
    Kt. Solothurn:
        2425 | Holderbank (SO)
    Kt. Bern:
        310  | Rapperswil (BE)
    Kt. Graubünden:
        3834 | Roveredo (GR)

    The way the name of these municipalities is saved in the camac db differs per canton.

    For some cantons (for example kt. Bern and kt. Graubünden), we save the name of the municipality
    with the canton identifier appended:
        "Gemeinde Rapperswil (BE)", "Gemeinde Roveredo (GR)"

    For other cantons (for example kt. Solothurn), we do NOT save this canton identifier appended to the municipality name:
        "Gemeinde Holderbank"

    For cantons with the latter approach, we can strip the canton identifier from the excel source
    by passing for example: `--canton "(SO)"` argument to the command.
    This is necessary for the service query filtering by municipality full translated name.

    Full command example:

    python manage.py import_bfs_nr --source SO_BFS_NR_SOURCE.xlsx --canton "(SO)"

    So, to generalize the `--canton` argument usage:
        `--canton "(CANTON IDENTIFIER)"` => use canton short name in brackets and quotes (!!!).
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            "-s",
            type=str,
            help="Path to excel file",
        )
        parser.add_argument(
            "--canton",
            "-c",
            type=str,
            default="",
            help="Optional canton identifier from excel file, to be specified when canton identifier is not saved in our db for municipality names",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        canton = options["canton"]
        for row in pyexcel.get_array(file_name=options["source"]):
            name = row[1].replace(canton, "").strip()
            if not name:
                break

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

            service.external_identifier = row[0]
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
