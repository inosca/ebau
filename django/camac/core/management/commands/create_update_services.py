from django.core.management.base import BaseCommand

from camac.user.models import Service


def set_uppercase(word):
    return f"{word[0].upper()}{word[1:]}"


def create_sql_file(sql_file):
    german = [
        "Sachbearbeiter",
        "Einsichtsberechtigte",
        "Leitung",
        "Leitbehörde",
        "Baukontrolle",
    ]
    services = Service.objects.filter(trans__language="fr")
    file = open(sql_file, "w+")
    for service in services:
        if any(item in service.get_trans_attr("name") for item in german):
            file.write(
                f"""UPDATE "SERVICE_T"
            SET "NAME" = '{set_uppercase(service.get_trans_attr("name").replace(
                    "Sachbearbeiter", "collaborateur"
                ).replace(
                    "Einsichtsberechtigte", "personne autorisée à consulter"
                ).replace (
                    "Leitung", "responsable"
                ).replace (
                    "Leitbehörde", "autorité directrice"
                ).replace (
                    "Baukontrolle", "contrôle construction"
                ).replace (
                    "'", "''"
                ))}'
            WHERE "NAME" = '{service.get_trans_attr("name").replace("'", "''")}'
            AND "LANGUAGE" = 'fr';
            \n"""
            )
    file.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file", nargs="?", default="camac/core/update_services.sql", type=str
        )

    def handle(self, *args, **option):
        create_sql_file(option["sql_file"])
