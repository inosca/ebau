from camac.core.dataimport import (
    ImportCommand,
    create_or_update_group,
    create_or_update_service,
)
from camac.core.models import Role, ServiceGroup

ROLE_LEITUNG_LEITBEHOERDE = 3
ROLE_LEITUNG_FACHSTELLE = 4
ROLE_SACHBEARBEITER_FACHSTELLE = 20001
ROLE_READONLY_FACHSTELLE = 20002
ROLE_UNTERFACHSTELLE = 20000

SERVICE_GROUP_FACHSTELLE = ServiceGroup.objects.get(pk=1)


class Command(ImportCommand):
    help = """
    (Bern): Import services from csv file. For every entry, the following
    database entries are created/updated:

    * Groups "Leitung {name}", "Sachbearbeiter {name}" and
      "Einsichtsberechtigte {name}"
    * Service (Organisation) "{name}"
    """

    def import_data(self, reader):
        _import_data(reader)


def _import_data(reader):
    service_group = None
    service = None
    for row in reader:
        if row.get("Unterfachstelle"):
            subservice = create_or_update_service(
                row,
                "Unterfachstelle",
                defaults={"service_group": service_group, "service_parent": service},
            )
            create_or_update_group(
                row,
                "Unterfachstelle",
                defaults={
                    "role": Role.objects.get(pk=ROLE_UNTERFACHSTELLE),
                    "service": subservice,
                },
            )
        else:
            service_group = SERVICE_GROUP_FACHSTELLE
            service = create_or_update_service(
                row, "", defaults={"service_group": service_group}
            )
            create_or_update_group(
                row,
                "Leitung",
                defaults={
                    "role": Role.objects.get(pk=ROLE_LEITUNG_FACHSTELLE),
                    "service": service,
                },
            )
            create_or_update_group(
                row,
                "Sachbearbeiter",
                defaults={
                    "role": Role.objects.get(pk=ROLE_SACHBEARBEITER_FACHSTELLE),
                    "service": service,
                },
            )
            create_or_update_group(
                row,
                "Einsichtsberechtigte",
                defaults={
                    "role": Role.objects.get(pk=ROLE_READONLY_FACHSTELLE),
                    "service": service,
                },
            )
