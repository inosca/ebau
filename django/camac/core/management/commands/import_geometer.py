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

        parser.add_argument(
            "--clear-relations",
            action="store_true",
            help="Clear all service relations before importing",
        )
        parser.add_argument(
            "--clear-geometers",
            action="store_true",
            help="Clear all geometer services before importing",
        )

    def handle(self, *args, **options):
        path = options["path"].resolve()

        if options.get("clear_geometers"):
            geometer_services = Service.objects.filter(service_group__name="geometer")
            geometer_groups = Group.objects.filter(
                role__name__in=[
                    "geometer-lead",
                    "geometer-clerk",
                    "geometer-readonly",
                    "geometer-admin",
                ],
                service__in=geometer_services,
            )
            geometer_groups.delete()
            geometer_services.delete()

        if options.get("clear_relations"):
            geometer_relations = ServiceRelation.objects.filter(
                function=ServiceRelation.FUNCTION_GEOMETER
            )
            geometer_relations.delete()

        # we just open the default book
        book = pyexcel.get_book(file_name=str(path))
        sheet: pyexcel.Sheet = book.sheet_by_index(0)

        index_row, *data_rows = sheet.rows()
        index_row = [str(val).strip() for val in index_row]  # just to be sure

        row_dicts = [
            dict(zip(index_row, [str(val).strip() for val in row])) for row in data_rows
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

        # We use "name, company" as an "identifier", so it remains unique.
        # The "Name eBau" can't be used as it would duplicate services when
        # the same geometer is referenced both from FR and DE municipalities
        name = ", ".join(
            [
                geometer["Geometer"],
                geometer["FirmaName"],
            ]
        )
        validated_email = self._email_or_none(geometer["FirmaEmail"])
        if not validated_email:  # pragma: no cover
            print(f"Geometer {name} has an invalid email: {geometer['FirmaEmail']}")

        geom_service, _ = Service.objects.update_or_create(
            # we set the name here in the untranslated object to be able
            # to find it again using update_or_create.
            name=name,
            defaults={
                "service_group": geometer_service_group,
                "address": geometer["FirmaStrasse"],
                "zip": zipcode,
                "phone": geometer["FirmaTelefon"],
                "email": validated_email,
                "notification": 1,  # yeah it's not a bool
            },
        )

        # Same logic as in the Excel sheet.
        prefix_fr = "géomètre conservateur"
        prefix_de = "Nachführungsgeometer"
        display_name = geometer["Geometer"]

        geom_service.trans.update_or_create(
            language="de",
            defaults={
                "name": f"{prefix_de} {display_name}",
                "city": city,
            },
        )
        geom_service.trans.update_or_create(
            language="fr",
            defaults={
                "name": f"{prefix_fr} {display_name}",
                "city": city,
            },
        )

        self._build_groups_for_service(geom_service)
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
            & Q(service_group=municipality_service_group)
            # need to find the "root" service, not a subservice that may match
            # by name, as the name matching sadly needs to ba a bit fuzzy
            & Q(service_parent__isnull=True)
        ).first()

        if not municipality_service:
            print(
                f"Municipality service for '{municipality_name}' not found. "
                f"Service '{geom_service.get_trans_attr('name')}' "
                "created but not assigned"
            )
            return

        print(
            f"Leitbehörde '{municipality_service.get_trans_attr('name')}' "
            f"found for '{municipality_name}', assigning "
            f"Geometer service: {geom_service.get_trans_attr('name')}"
        )

        # Overwrite if exists, otherwise create new
        ServiceRelation.objects.update_or_create(
            function=ServiceRelation.FUNCTION_GEOMETER,
            receiver=municipality_service,
            defaults={
                "provider": geom_service,
            },
        )

    def _build_groups_for_service(self, geom_service: Service):
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
            geom_name_de = geom_service.get_trans_attr("name", "de")
            geom_name_fr = geom_service.get_trans_attr("name", "fr")
            prefix_de = role.get_trans_attr("group_prefix", "de")
            prefix_fr = role.get_trans_attr("group_prefix", "fr")
            name_de = f"{prefix_de} {geom_name_de}"
            name_fr = f"{prefix_fr} {geom_name_fr}"

            grp, _ = Group.objects.update_or_create(
                role=role, service=geom_service, defaults={"name": name_de}
            )
            GroupT.objects.update_or_create(
                group=grp, language="de", defaults={"name": name_de}
            )
            GroupT.objects.update_or_create(
                group=grp, language="fr", defaults={"name": name_fr}
            )

    def _email_or_none(self, email: str):
        email = str(email)  # just in case it's coming in as None already.

        if any(
            [
                " " in email,
                "/" in email,
                not email,
                "@" not in email,
            ]
        ):
            # Invalid email - drop it
            return None
        return email
