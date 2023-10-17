from django.core.management.base import BaseCommand
from django.db.models import F, Value
from django.db.models.functions import Replace

from camac.user.models import GroupT, ServiceT


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--before",
            "-b",
            dest="before",
            type=str,
            default="Leitbehörde",
        )
        parser.add_argument(
            "--after",
            "-a",
            dest="after",
            type=str,
            default="Gemeinde",
        )

    def handle(self, *args, **options):
        before = options["before"]
        after = options["after"]

        # Update service names
        ServiceT.objects.filter(name__contains=before).update(
            name=Replace(
                "name",
                Value(before),
                Value(after),
            )
        )
        ServiceT.objects.update(description=F("name"))

        # Update group names
        GroupT.objects.filter(name__contains=before).update(
            name=Replace(
                "name",
                Value(before),
                Value(after),
            )
        )
