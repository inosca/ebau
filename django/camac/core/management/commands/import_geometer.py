from pathlib import Path

import pyexcel
from django.core.management.base import BaseCommand
from django.db.models import Q

from camac.user.models import (
    Group,
    GroupT,
    Role,
    Service,
    ServiceGroup,
    ServiceRelation,
)


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
        index_row = [val.strip() for val in index_row]  # just to be sure

        row_dicts = [
            dict(zip(index_row, [val.strip() for val in row])) for row in data_rows
        ]

        # The table is fully redundant, so each geometer may be
        # mentioned multiple times. We assume same name = same geometer.
        # The municipality is also by-name.

        for geometer in row_dicts:
            # This is not really efficient - we do update_or_create multiple
            # times per geometer. But it's an one-off script and not performance-
            # sensitive, so...
            self._build_geometer(geometer)

    def _build_geometer(self, geometer):
        zipcode, city = geometer["FirmaPlzOrt"].split(" ", 1)
        geometer_service_group = ServiceGroup.objects.get(name="geometer")
        geom_service, _ = Service.objects.update_or_create(
            # we set the name here in the untranslated object to be able
            # to find it again using update_or_create.
            name=geometer["Name eBAU"],
            defaults={
                "service_group": geometer_service_group,
                "address": geometer["FirmaStrasse"],
                "zip": zipcode,
                "phone": geometer["FirmaTelefon"],
                "email": geometer["FirmaEmail"],
                "notification": 1,  # yeah it's not a bool
            },
        )

        # TODO: shall we do FR translations too?
        geom_service.trans.update_or_create(
            language="de",
            defaults={
                "name": geometer["Name eBAU"],
                "city": city,
            },
        )
        geom_service.trans.update_or_create(
            language="fr",
            defaults={
                "name": geometer["Name eBAU"],
                "city": city,
            },
        )

        self._build_groups_for_service(geometer["Name eBAU"], geom_service)
        self._build_service_relations(geometer["Gemeinde"], geom_service)

    def _build_service_relations(self, municipality_name: str, geom_service: Service):
        municipality_service_group = ServiceGroup.objects.get(
            trans__name="Leitbehörde Gemeinde", trans__language="de"
        )
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
                f"Municipality {municipality_name} not found. Service '{geom_service.name}' created but not assigned"
            )
            return
        print(
            f"Leitbehörde found for {municipality_name}, updating/creating Geometer service"
        )

        # Overwrite if exists, otherwise create new
        ServiceRelation.objects.update_or_create(
            function=ServiceRelation.FUNCTION_GEOMETER,
            receiver=municipality_service,
            defaults={
                "provider": geom_service,
            },
        )

    def _build_groups_for_service(self, geometer_name: str, geom_service: Service):
        """Build the required groups and associate them with the corresponding roles.

        The geometer name should be the full name as it appears in the "Name eBAU"
        field (example: "Nachführungsgeometer Foo Bar").

        The geom_service is the service representing the Geometer company.
        """
        role_names = [
            "geometer-lead",
            "geometer-clerk",
            "geometer-readonly",
            "geometer-admin",
        ]
        roles = Role.objects.filter(name__in=role_names)
        assert len(roles) == 4, "Something's wrong with the Geometer roles"

        for role in roles:
            name_de = f"{role.get_trans_attr('group_prefix', 'de')} {geometer_name}"
            name_fr = f"{role.get_trans_attr('group_prefix', 'fr')} {geometer_name}"

            grp, _ = Group.objects.update_or_create(
                role=role, service=geom_service, defaults={"name": name_de}
            )
            GroupT.objects.update_or_create(
                group=grp, language="de", defaults={"name": name_de}
            )
            GroupT.objects.update_or_create(
                group=grp, language="fr", defaults={"name": name_fr}
            )
