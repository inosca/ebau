from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

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

    def handle(self, *args, **options):
        cantonal_services = Service.objects.filter(
            service_group__slug="service-cantonal"
        )

        through = Keyword.instances.through
        for service in tqdm(cantonal_services):
            tqdm.write(f"Preparing {service.get_name()}")
            new_keywords = []
            new_relations = []
            existing = Keyword.objects.filter(
                Q(service=service)
                & (Q(name__startswith="BVUAFB") | Q(name__startswith="EBPA"))
            ).values_list("name", flat=True)
            keywords = (
                Keyword.objects.filter(
                    Q(service__slug="afb")
                    & (Q(name__startswith="BVUAFB") | Q(name__startswith="EBPA"))
                )
                .exclude(name__in=existing)
                .prefetch_related("instances")
            )
            for keyword in keywords:
                new_kw = Keyword(name=keyword.name, service=service)
                new_keywords.append(new_kw)
                for instance in keyword.instances.all():
                    new_relations.append(through(keyword=new_kw, instance=instance))

            tqdm.write(
                f"prepared {len(new_keywords)} keywords, {len(new_relations)} relations"
            )
            if options["commit"]:
                Keyword.objects.bulk_create(new_keywords)
                through.objects.bulk_create(new_relations)

        if not options["commit"]:
            tqdm.write("nothing saved. Pass --commit to save.")
