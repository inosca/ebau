from camac.core.dataimport import (ImportCommand, create_or_update_group,
                                   create_or_update_service)
from camac.core.models import Role, ServiceGroup

ROLE_LEITUNG_LEITBEHOERDE = 3
ROLE_SACHBEARBEITER_LEITBEHOERDE = 20004
ROLE_READONLY_LEITBEHOERDE = 20003

SERVICE_GROUP_LEITBEHOERDE_RSTA = ServiceGroup.objects.get(pk=20000)


class Command(ImportCommand):
    help = """
    (Bern): Import RSTAs from csv file. For every entry, the following
    database entries are created/updated:

    * Groups "Leitung {name}", "Sachbearbeiter {name}" and
      "Einsichtsberechtigte {name}"
    * Service (Organisation) "{name}"
    """

    def import_data(self, reader):
        _import_data(reader)


def _import_data(reader):
    for row in reader:
        service_group = SERVICE_GROUP_LEITBEHOERDE_RSTA
        service = create_or_update_service(
            row, "", defaults={"service_group": service_group}
        )
        create_or_update_group(
            row,
            "Leitung",
            defaults={
                "role": Role.objects.get(pk=ROLE_LEITUNG_LEITBEHOERDE),
                "service": service,
            },
        )
        create_or_update_group(
            row,
            "Sachbearbeiter",
            defaults={
                "role": Role.objects.get(pk=ROLE_SACHBEARBEITER_LEITBEHOERDE),
                "service": service,
            },
        )
        create_or_update_group(
            row,
            "Einsichtsberechtigte",
            defaults={
                "role": Role.objects.get(pk=ROLE_READONLY_LEITBEHOERDE),
                "service": service,
            },
        )
