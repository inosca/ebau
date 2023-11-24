from pathlib import Path

import pyexcel
from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.user.models import Service, ServiceGroup, ServiceRelation


class Command(BaseCommand):
    help = """Import initial Geometer data for Kt. Bern"""

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            metavar="PATH",
            type=Path,
            help="Path to directory or XLSX file",
        )

    def handle(self, *args, **options):
        path = options["path"].resolve()

        # we just open the default book
        book = pyexcel.get_book(file_name=str(path))
        sheet: pyexcel.Sheet = book.sheet_by_index(0)

        index_row, *data_rows = sheet.rows()

        row_dicts = [dict(zip(index_row, row)) for row in data_rows]

        # The table is fully redundant, so each geometer may be
        # mentioned multiple times. We assume same name = same geometer.
        # The municipality is also by-name.

        # Build up import structure.
        geometer_service_group = ServiceGroup.objects.get(name="Nachführungsgeometer")

        geometers_by_municipality = {}
        for geometer in row_dicts:
            municipality = geometer["Gemeinde"]

            zipcode, city = geometer["FirmaPlzOrt"].split(" ", 1)
            # This is not really efficient - we do update_or_create multiple
            # times per geometer. But it's an one-off script and not performance-
            # sensitive, so...
            service, _ = Service.objects.update_or_create(
                name=geometer["Name eBAU"],
                defaults={
                    "service_group": geometer_service_group,
                    "address": geometer["FirmaStrasse"],
                    "zip": zipcode,
                    "city": city,
                    "phone": geometer["FirmaTelefon"],
                    "email": geometer["FirmaEmail"],
                },
            )
            geometer["geometer_service"] = service

            geometers_by_municipality[municipality] = service

        municipality_service_group = ServiceGroup.objects.get(
            trans__name="Leitbehörde Gemeinde", trans__language="de"
        )

        for municipality_name, geometer in geometers_by_municipality.items():
            municipality_service = Service.objects.filter(
                (
                    # City name match is ok
                    Q(trans__city__iexact=municipality_name)
                    # Exact service name match is best match
                    | Q(trans__name__iexact=f"Leitbehörde {municipality_name}")
                    # Startswith, but with trailing space, so we can match
                    # "Gsteig" to "Gsteig bei gstaad" but not "Gsteigwiler"
                    | Q(trans__city__istartswith=f"{municipality_name} ")
                )
                & Q(service_group=municipality_service_group),
            ).first()

            if not municipality_service:
                print(
                    f"Could not find municipality {municipality_name}, skipping Geometer import"
                )
                continue
            print(
                f"Leitbehörde found for {municipality_name}, updating/creating Geometer service"
            )

            # Overwrite if exists, otherwise create new
            ServiceRelation.objects.update_or_create(
                function=ServiceRelation.FUNCTION_GEOMETER,
                receiver=municipality_service,
                defaults={
                    "provider": geometer,
                },
            )
