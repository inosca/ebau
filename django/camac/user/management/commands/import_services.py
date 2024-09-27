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
                1: "Gemeinde",
                2: None,
                3: None,
            },
        }
    elif canton == "kt_so":
        return {
            "SERVICE_GROUP": {
                1: ServiceGroup.objects.get(name="municipality"),
                2: ServiceGroup.objects.get(name="service-cantonal"),
                3: ServiceGroup.objects.get(name="service-extra-cantonal"),
                4: ServiceGroup.objects.get(name="service-bab"),
                5: ServiceGroup.objects.get(name="canton"),
            },
            "ROLE": {
                1: {
                    "admin": Role.objects.get(name="municipality-admin"),
                    "lead": Role.objects.get(name="municipality-lead"),
                    "read": Role.objects.get(name="municipality-read"),
                },
                2: {
                    "admin": Role.objects.get(name="service-admin"),
                    "lead": Role.objects.get(name="service-lead"),
                },
                3: {
                    "admin": Role.objects.get(name="service-admin"),
                    "lead": Role.objects.get(name="service-lead"),
                },
                4: {
                    "admin": Role.objects.get(name="service-admin"),
                    "lead": Role.objects.get(name="service-lead"),
                },
                5: {
                    "admin": Role.objects.get(name="municipality-admin"),
                    "lead": Role.objects.get(name="municipality-lead"),
                    "read": Role.objects.get(name="municipality-read"),
                },
            },
            "PREFIX": {
                1: "Gemeinde",
                2: None,
                3: None,
                4: None,
                5: None,
            },
        }

    return {}


def get_group_types(canton):
    if canton == "kt_gr":
        return {"lead": "Sachbearbeitung", "admin": "Administration"}
    elif canton == "kt_so":
        return {
            "lead": "Sachbearbeitung",
            "admin": "Administration",
            "read": "Einsichtsberechtigte",
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

        for row in rows[1:]:
            if not row[0]:
                continue
            service_group = TYPE_MAP["SERVICE_GROUP"][row[0]]
            roles = TYPE_MAP["ROLE"][row[0]]
            prefix = TYPE_MAP["PREFIX"][row[0]]

            raw_name = row[1].strip()
            name = f"{prefix} {raw_name}" if prefix else raw_name

            service_data = dict(
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
                disabled=int(row[8] or 0),
                external_identifier=row[9] or None,
            )

            existing = Service.objects.filter(trans__name=name).first()

            if existing:
                self.stdout.write(self.style.WARNING(f"Updating service {name}"))
                Service.objects.filter(pk=existing.pk).update(**service_data)
                service = existing
            else:
                self.stdout.write(self.style.SUCCESS(f"Creating service {name}"))
                service = Service.objects.create(**service_data)

            service_t_data = dict(
                language="de",
                service=service,
                name=name,
                description=name,
                city=scrub(row[4]),
            )

            if existing:
                ServiceT.objects.filter(service_id=existing.pk).update(**service_t_data)
            else:
                ServiceT.objects.create(**service_t_data)

            for group_type, group_type_name in GROUP_TYPES.items():
                if not roles.get(group_type):
                    continue

                group_name = f"{group_type_name} {name}"

                group_data = dict(
                    service=service,
                    role=roles[group_type],
                    name=None,
                    email=None,
                    zip=None,
                    city=None,
                    address=None,
                    phone=None,
                    website=None,
                    disabled=int(row[8] or 0),
                )

                existing = Group.objects.filter(trans__name=group_name).first()

                if existing:
                    Group.objects.filter(pk=existing.pk).update(**group_data)
                    group = existing
                else:
                    group = Group.objects.create(**group_data)

                group_t_data = dict(
                    language="de",
                    group=group,
                    name=group_name,
                    city=scrub(row[4]),
                )

                if existing:
                    GroupT.objects.filter(group_id=existing.pk).update(**group_t_data)
                else:
                    GroupT.objects.create(**group_t_data)
