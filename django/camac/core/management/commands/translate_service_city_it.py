from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service


class Command(BaseCommand):
    help = """Translate the city attribute for all services in italian"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        services = Service.objects.filter(trans__name__startswith="Gemeinde")
        for service in services:
            city_de = service.trans.get(language="de").city
            service_t_it = service.trans.get(language="it")
            if city_de:
                service_t_it.city = "Coira" if city_de == "Chur" else city_de
                print(f"The city {city_de} was translated into {service_t_it.city}")

            name_it = service.trans.get(language="it").name
            if name_it:
                service_t_it.description = name_it
                print(f"The name {name_it} was added to the description")
            service_t_it.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
