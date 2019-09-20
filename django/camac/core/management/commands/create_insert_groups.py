from django.core.management.base import BaseCommand

from camac.user.models import Group


def get_missing_groups():
    groups = Group.objects.all()
    return groups.exclude(trans__language="fr")


def create_sql_file(sql_file):
    missing_groups = get_missing_groups()
    file = open(sql_file, "w+")
    for group in missing_groups:
        file.write(
            f"""INSERT INTO "GROUP_T" (
            "LANGUAGE",
            "NAME",
            "CITY",
            "GROUP_ID"
        ) VALUES (
            'fr',
            '{group.get_trans_attr("name")}',
            '{group.get_trans_attr("city")}',
            {group.get_trans_attr("group_id")}
        );
        \n"""
        )
    file.close()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "sql_file", nargs="?", default="camac/core/insert_groups.sql", type=str
        )

    def handle(self, *args, **option):
        create_sql_file(option["sql_file"])
