from django.core.management.base import BaseCommand

from camac.user.models import Group, Role, Service, User

ADMIN_ROLE_MAPPING = {
    # service group: admin role
    1: 20008,  # Fachstelle
    2: 20007,  # Leitbehörde Gemeinde
    3: 20009,  # Baukontrolle
    20000: 20007,  # Leitbehörde RSTA
}

LEAD_ROLE_MAPPING = {
    # service group: lead role
    1: 4,  # Fachstelle
    2: 3,  # Leitbehörde Gemeinde
    3: 5,  # Baukontrolle
    20000: 3,  # Leitbehörde RSTA
}


def escape(string):
    return string.replace("'", "''")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file",
            nargs="?",
            default="camac/core/insert_admin_groups.sql",
            type=str,
        )

    def handle(self, *args, **option):
        with open(option["sql_file"], "w+") as f:
            for service in Service.objects.filter(service_parent__isnull=True):
                role = Role.objects.get(pk=ADMIN_ROLE_MAPPING[service.service_group.pk])

                de = service.trans.filter(language="de").first()
                fr = service.trans.filter(language="fr").first()

                id = "SELECT CURRVAL(pg_get_serial_sequence('\"GROUP\"','GROUP_ID'))"

                f.write(
                    f"-- {service.get_name()}\n"
                    # create a new group
                    f'INSERT INTO "GROUP" ("ROLE_ID", "SERVICE_ID") VALUES ({role.pk}, {service.pk});\n'
                    # create translations for the new group
                    f'INSERT INTO "GROUP_T" ("GROUP_ID", "LANGUAGE", "CITY", "NAME") VALUES (({id}), \'de\', \'{escape(de.city)}\', \'Administration {escape(de.name)}\');\n'
                    f'INSERT INTO "GROUP_T" ("GROUP_ID", "LANGUAGE", "CITY", "NAME") VALUES (({id}), \'fr\', \'{escape(fr.city)}\', \'Administration: {escape(fr.name)}\');\n'
                    "\n"
                )

                # find all users which are member of the "lead" group of the service
                for user in User.objects.filter(
                    groups__in=Group.objects.filter(
                        service=service,
                        role=Role.objects.get(
                            pk=LEAD_ROLE_MAPPING[service.service_group.pk]
                        ),
                    )
                ):
                    # add those users to the new admin group
                    f.write(
                        f'INSERT INTO "USER_GROUP" ("GROUP_ID", "DEFAULT_GROUP", "USER_ID") VALUES (({id}), 0, {user.pk});\n'
                    )

                f.write("\n\n")

            f.close()
