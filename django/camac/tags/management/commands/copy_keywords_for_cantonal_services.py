from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.tags.models import Keyword
from camac.user.models import Service


class Command(BaseCommand):
    help = "Kt. AG: Copy relevant keywords from afb for cantonal services."

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Create data for real",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        new_keywords = []
        new_relations = []
        cantonal_services = Service.objects.filter(
            service_group__slug="service-cantonal"
        )

        through = Keyword.instances.through
        for keyword in Keyword.objects.filter(
            Q(service__slug="afb")
            & (Q(name__startswith="BVUAFB") | Q(name__startswith="EBPA"))
        ):
            for service in cantonal_services:
                new_kw = Keyword(name=keyword.name, service=service)
                new_keywords.append(new_kw)
                for instance in keyword.instances.all():
                    new_relations.append(through(keyword=new_kw, instance=instance))

        self.stdout.write(f"Prepared {len(new_keywords)} keywords to save.")
        Keyword.objects.bulk_create(new_keywords)

        self.stdout.write(
            f"Prepared {len(new_relations)} keyword-instance relations to save."
        )
        through.objects.bulk_create(new_relations)

        if options["commit"]:
            transaction.savepoint_commit(tid)
            self.stdout.write("saved to db.")
        else:
            transaction.savepoint_rollback(tid)
            self.stdout.write("nothing saved. Pass --commit to save.")
