from django.core.management.base import BaseCommand
from django.db import connection

from camac.user.models import Group, Role, Service, User

ADMIN_ROLE_MAPPING = {
    "Fachstelle": "Administration Fachstelle",
    "Leitbehörde Gemeinde": "Administration Leitbehörde",
    "Baukontrolle": "Administration Baukontrolle",
    "Leitbehörde RSTA": "Administration Leitbehörde",
}

LEAD_ROLE_MAPPING = {
    "Fachstelle": "Leitung Fachstelle",
    "Leitbehörde Gemeinde": "Leitung Leitbehörde",
    "Baukontrolle": "Leitung Baukontrolle",
    "Leitbehörde RSTA": "Leitung Leitbehörde",
}


def escape(string):
    return string.replace("'", "''") if string else None


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-e",
            "--execute",
            default=False,
            dest="exec",
            action="store_true",
            help="Directly execute the query instead of just printing it",
        )
        parser.add_argument(
            "--no-transaction",
            default=True,
            dest="use_transaction",
            action="store_false",
            help="Suppress transaction usage in generated SQL output (needed for tests)",
        )

    def handle(self, *args, **options):
        queries = []

        for service in Service.objects.filter(service_parent__isnull=True):
            role = Role.objects.get(
                trans__language="de",
                trans__name=ADMIN_ROLE_MAPPING[
                    service.service_group.trans.filter(language="de").first().name
                ],
            )

            if service.groups.filter(role=role).exists():  # pragma: no cover
                continue

            de = service.trans.filter(language="de").first()
            fr = service.trans.filter(language="fr").first()

            id = "SELECT CURRVAL(pg_get_serial_sequence('\"GROUP\"', 'GROUP_ID'))"

            queries.append(f"-- {service.get_name()}")
            # create a new group
            queries.append(
                f'INSERT INTO "GROUP" ("ROLE_ID", "SERVICE_ID") VALUES ({role.pk}, {service.pk});'
            )
            # create translations for the new group
            if de:
                queries.append(
                    f'INSERT INTO "GROUP_T" ("GROUP_ID", "LANGUAGE", "CITY", "NAME") VALUES (({id}), \'de\', \'{escape(de.city)}\', \'Administration {escape(de.name)}\');'
                )
            if fr:  # pragma: no cover
                queries.append(
                    f'INSERT INTO "GROUP_T" ("GROUP_ID", "LANGUAGE", "CITY", "NAME") VALUES (({id}), \'fr\', \'{escape(fr.city)}\', \'Administration: {escape(fr.name)}\');'
                )

            queries.append("\n")

            # find all users which are member of the "lead" group of the service
            for user in User.objects.filter(
                groups__in=Group.objects.filter(
                    service=service,
                    role=Role.objects.get(
                        trans__language="de",
                        trans__name=LEAD_ROLE_MAPPING[
                            service.service_group.trans.filter(language="de")
                            .first()
                            .name
                        ],
                    ),
                )
            ).distinct():
                # add those users to the new admin group
                queries.append(
                    f'INSERT INTO "USER_GROUP" ("GROUP_ID", "DEFAULT_GROUP", "USER_ID") VALUES (({id}), 0, {user.pk});'
                )

        if len(queries) and options["use_transaction"]:  # pragma: no cover
            queries = ["BEGIN;", *queries, "COMMIT;"]

        script = "\n".join(queries)

        self.stdout.write(script)

        if options["exec"]:
            with connection.cursor() as cursor:
                cursor.execute(script)
