from django.core.management.base import BaseCommand

from camac.user.models import Service


def get_missing_services():
    services = Service.objects.all()
    return services.exclude(trans__language="fr")


def insert_missing_services(sql_file):
    missing_services = get_missing_services()
    file = open(sql_file, "w+")
    for service in missing_services:
        file.write(
            f"""INSERT INTO "SERVICE_T" (
            "LANGUAGE",
            "NAME",
            "DESCRIPTION",
            "CITY",
            "SERVICE_ID"
        ) VALUES (
            'fr',
            '{service.get_trans_attr("name")}',
            '{service.get_trans_attr("description")}',
            '{service.get_trans_attr("city")}',
            {service.get_trans_attr("service_id")}
        );
        \n"""
        )
    file.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file", nargs="?", default="camac/core/insert_services.sql", type=str
        )

    def handle(self, *args, **option):
        insert_missing_services(option["sql_file"])
