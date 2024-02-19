from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        for i in Instance.objects.filter(
            pk__in=[
                47333,
                47354,
                47357,
                47364,
                47394,
                47396,
                47368,
                47343,
                47391,
                47387,
                47326,
                47267,
                47266,
                47249,
                42768,
                46271,
                47029,
                47245,
            ]
        ):
            workflow_entry = i.workflowentry_set.filter(workflow_item_id=65).first()
            new_date = workflow_entry.workflow_date - timedelta(days=20)
            print(f"{i.pk}: {workflow_entry.workflow_date} --> {new_date}")
            workflow_entry.workflow_date = new_date
            workflow_entry.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
