from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        for i in Instance.objects.all():
            workflow_entry = i.workflowentry_set.filter(workflow_item_id=15).first()
            p = i.publication_entries.first()
            if (
                workflow_entry
                and p
                and workflow_entry.workflow_date != p.publication_date
            ):
                print(f"{i.pk}: {workflow_entry.workflow_date} -> {p.publication_date}")
                workflow_entry.workflow_date = p.publication_date
                workflow_entry.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
