from camac.core.dataimport import ImportCommand
from camac.user.models import Role, ServiceGroup

ROLE_LEITUNG_LEITBEHOERDE = 3
ROLE_SACHBEARBEITER_LEITBEHOERDE = 20004
ROLE_READONLY_LEITBEHOERDE = 20003

ROLE_LEITUNG_BAUKONTROLLE = 5
ROLE_SACHBEARBEITER_BAUKONTROLLE = 20005
ROLE_READONLY_BAUKONTROLLE = 20006

ROLE_LEITUNG_FACHSTELLE = 4
ROLE_UNTERFACHSTELLE = 20000

# service_group: (id, prefix)
SERVICE_GROUP_LEITBEHOERDE_GEMEINDE = {
    "service_group": ServiceGroup.objects.get(pk=2),
    "name": "Leitbehörde",
    "groups": [
        ("Leitung", ROLE_LEITUNG_LEITBEHOERDE),
        ("Sachbearbeiter", ROLE_SACHBEARBEITER_LEITBEHOERDE),
        ("Einsichtsberechtigte", ROLE_READONLY_LEITBEHOERDE),
    ],
}
SERVICE_GROUP_BAUKONTROLLE = {
    "service_group": ServiceGroup.objects.get(pk=3),
    "name": "Baukontrolle",
    "groups": [
        ("Leitung", ROLE_LEITUNG_BAUKONTROLLE),
        ("Sachbearbeiter", ROLE_SACHBEARBEITER_BAUKONTROLLE),
        ("Einsichtsberechtigte", ROLE_READONLY_BAUKONTROLLE),
    ],
}


class Command(ImportCommand):
    help = """
    (Bern): Import municipalities from csv file. For every entry, the following
    database entries are created/updated:

    * Groups "Leitung {name}", "Sachbearbeiter {name}" and
      "Einsichtsberechtigte {name}"
    * Service (Organisation) "{name}"
    """

    def import_data(self, reader):
        service = None
        for row in reader:
            for sg in [SERVICE_GROUP_BAUKONTROLLE, SERVICE_GROUP_LEITBEHOERDE_GEMEINDE]:
                service = self.create_or_update_service(
                    row,
                    sg["name"],
                    defaults={"service_group": sg["service_group"], "disabled": True},
                )
                for role in sg["groups"]:
                    self.create_or_update_group(
                        row,
                        "{0} {1}".format(role[0], sg["name"]),
                        defaults={
                            "role": Role.objects.get(pk=role[1]),
                            "service": service,
                        },
                    )
