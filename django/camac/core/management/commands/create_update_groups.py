from django.core.management.base import BaseCommand

from camac.user.models import GroupT


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
    groups = GroupT.objects.filter(language="fr")
    file = open(sql_file, "w+")
    for group in groups:
        if any(item in group.name for item in german):
            file.write(
                f"""UPDATE "GROUP_T"
            SET "NAME" = '{set_uppercase(group.name.replace(
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
            WHERE id = {group.pk};"""
            )
    file.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file", nargs="?", default="camac/core/update_groups.sql", type=str
        )

    def handle(self, *args, **option):
        create_sql_file(option["sql_file"])
