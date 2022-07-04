from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        for i in Instance.objects.filter(group__service__service_group=68):
            if i.location and i.location not in i.group.locations.all():
                prev_group = i.group.name
                i.group = i.location.group_set.filter(service__service_group=68).first()
                i.save()
                print(
                    f"{i.pk} ({i.location.name}): {prev_group} -> {i.group.name} ({i.group.pk})"
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
