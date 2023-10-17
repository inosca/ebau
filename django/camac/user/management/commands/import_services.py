import pyexcel
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Group, GroupT, Role, Service, ServiceGroup, ServiceT


def get_type_map(canton):
    if canton == "kt_gr":
        return {
            "SERVICE_GROUP": {
                1: ServiceGroup.objects.get(pk=2),  # Sachbearbeitung Gemeinde
                2: ServiceGroup.objects.get(pk=1),  # Fachstelle
                3: ServiceGroup.objects.get(pk=3),  # ARE
            },
            "ROLE": {
                1: {
                    "lead": Role.objects.get(pk=3),  # Sachbearbeitung Leitbehörde
                    "admin": Role.objects.get(pk=5),  # Administration Leitbehörde
                },
                2: {
                    "lead": Role.objects.get(pk=4),  # Sachbearbeitung Fachstelle
                    "admin": Role.objects.get(pk=6),  # Administration Fachstelle
                },
                # ARE also gets "Fachstelle" role
                3: {
                    "lead": Role.objects.get(pk=4),  # Sachbearbeitung Fachstelle
                    "admin": Role.objects.get(pk=6),  # Administration Fachstelle
                },
            },
            "PREFIX": {
                1: "Leitbehörde",
                2: None,
                3: None,
            },
        }
    elif canton == "kt_so":
        return {
            "SERVICE_GROUP": {
                1: ServiceGroup.objects.get(pk=1),  # Gemeinde
                2: ServiceGroup.objects.get(pk=2),  # Kantonale Fachstelle
                3: ServiceGroup.objects.get(pk=3),  # Ausserkantonale Fachstelle
            },
            "ROLE": {
                1: {
                    "admin": Role.objects.get(pk=4),  # Administration Leitbehörde
                    "lead": Role.objects.get(pk=5),  # Leitung Leitbehörde
                    "clerk": Role.objects.get(pk=6),  # Sachbearbeitung Leitbehörde
                    "construction-monitoring": Role.objects.get(
                        pk=7
                    ),  # Baubegleitung Leitbehörde
                    "read": Role.objects.get(pk=8),  # Einsichtsberechtigte Leitbehörde
                },
                2: {
                    "admin": Role.objects.get(pk=9),  # Administration Fachstelle
                    "lead": Role.objects.get(pk=10),  # Leitung Fachstelle
                    "clerk": Role.objects.get(pk=11),  # Sachbearbeitung Fachstelle
                },
                3: {
                    "admin": Role.objects.get(pk=9),  # Administration Fachstelle
                    "lead": Role.objects.get(pk=10),  # Leitung Fachstelle
                    "clerk": Role.objects.get(pk=11),  # Sachbearbeitung Fachstelle
                },
            },
            "PREFIX": {
                1: "Gemeinde",
                2: None,
                3: None,
            },
        }

    return {}


def get_group_types(canton):
    if canton == "kt_gr":
        return {"lead": "Sachbearbeitung", "admin": "Administration"}
    elif canton == "kt_so":
        return {
            "lead": "Leitung",
            "admin": "Administration",
            "clerk": "Sachbearbeitung",
            "read": "Einsichtsberechtigte",
            "construction-monitoring": "Baubegleitung",
        }

    return {}


TYPE_MAP = get_type_map(settings.APPLICATION_NAME)
GROUP_TYPES = get_group_types(settings.APPLICATION_NAME)


def scrub(value, default=None):
    if settings.ENV == "development":
        return default

    return value.strip()


class Command(BaseCommand):
    help = "Import services from excel file for GR and SO"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            "-s",
            type=str,
            help="Path to excel file",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        rows = pyexcel.get_array(file_name=options["source"])

        services = []
        skipped_services = []
        service_ts = []
        groups = []
        group_ts = []

        for row in rows[1:]:
            if not row[0]:
                continue
            service_group = TYPE_MAP["SERVICE_GROUP"][row[0]]
            roles = TYPE_MAP["ROLE"][row[0]]
            prefix = TYPE_MAP["PREFIX"][row[0]]

            raw_name = row[1].strip()
            name = f"{prefix} {raw_name}" if prefix else raw_name

            if Service.objects.filter(trans__name=name).exists():
                skipped_services.append(name)
                continue

            # Create service
            service = Service(
                service_parent=None,
                service_group=service_group,
                name=None,
                description=None,
                email=scrub(row[2], "email@example.ch"),
                zip=scrub(str(row[3])),
                city=None,
                address=scrub(row[5]),
                phone=scrub(row[6]),
                website=scrub(row[7]),
                notification=1,
                responsibility_construction_control=0,
                disabled=int(row[8]),
            )
            service_t = ServiceT(
                language="de",
                service=service,
                name=name,
                description=name,
                city=scrub(row[4]),
            )

            services.append(service)
            service_ts.append(service_t)

            # Create groups
            for group_type, group_type_name in GROUP_TYPES.items():
                if not roles.get(group_type):
                    continue

                group = Group(
                    service=service,
                    role=roles[group_type],
                    name=None,
                    email=None,
                    zip=None,
                    city=None,
                    address=None,
                    phone=None,
                    website=None,
                    disabled=int(row[8]),
                )
                group_t = GroupT(
                    language="de",
                    group=group,
                    name=f"{group_type_name} {name}",
                    city=scrub(row[4]),
                )
                groups.append(group)
                group_ts.append(group_t)

        created_services = Service.objects.bulk_create(services)
        created_service_ts = ServiceT.objects.bulk_create(service_ts)
        created_groups = Group.objects.bulk_create(groups)
        created_group_ts = GroupT.objects.bulk_create(group_ts)

        print("Import finished.")
        if skipped_services:
            print(
                f"Skipped {len(skipped_services)} Services because they already exist:"
            )
            for service in skipped_services[:10]:
                print(f"- {service}")
            if len(skipped_services) > 10:
                print(f"- ... and {len(skipped_services) - 10} more")

        print("Number of created objects:")
        print(f"- {len(created_services)} Services")
        print(f"- {len(created_service_ts)} Service Translations")
        print(f"- {len(created_groups)} Groups")
        print(f"- {len(created_group_ts)} Group Translations")
