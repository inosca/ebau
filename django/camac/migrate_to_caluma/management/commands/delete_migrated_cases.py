from logging import getLogger

from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from django.core.management.base import BaseCommand

log = getLogger(__name__)


class Command(BaseCommand):
    """Delete migrated cases and associated documents."""

    help = "Delete migrated cases and associated documents"

    def handle(self, *args, **options):
        migrated_cases = workflow_models.Case.objects.filter(
            meta__migrated_from_old_camac=True
        )

        # need a list as the QS result will be gone after deleting cases

        for case in migrated_cases:
            print(
                f"cases to go: {migrated_cases._clone().count()}, case#{case.pk}, inst={case.meta['camac-instance-id']}"
            )
            documents = list(
                str(pk["pk"])
                for pk in form_models.Document.objects.filter(case=case).values("pk")
            )
            case.delete()
            form_models.Document.objects.filter(family__in=documents).delete()
