import csv
from collections import namedtuple
from sys import exit

from django.core.management.base import BaseCommand

from camac.user.models import User

Row = namedtuple("Row", ["username", "email", "disabled"])


def is_disabled(row):
    return not row[6].lower().strip() == "x"


def load_csv(csv_file):
    rows = []
    with open(csv_file) as csv_file:
        for row in csv.reader(csv_file):
            row = Row(username=row[2], email=row[5], disabled=is_disabled(row))
            rows.append(row)
    return rows


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **option):
        csv_file = option["csv_file"]
        rows = load_csv(csv_file)

        users = []
        missing = []
        for row in rows:
            try:
                user = User.objects.get(username=row.username)
                users.append(user)
            except User.DoesNotExist:
                missing.append(row.username)

        if missing:
            print("The users with the following usernames do not exist:")
            for username in missing:
                print(f"  {username}")
            print("Please fix your CSV first.")
            exit(1)

        for user, row in zip(users, rows):
            if row.email:
                user.email = row.email
                if row.disabled:
                    user.email = "disabled-" + row.email
            user.disabled = row.disabled
            user.save()
            print(row.username)
