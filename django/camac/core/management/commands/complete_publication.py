from caluma.caluma_form.models import Answer
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Complete the 'fill-publication' work-item if the start date has passed"

    def handle(self, *args, **options):
        work_items = (
            WorkItem.objects.filter(
                task_id="fill-publication",
                status=WorkItem.STATUS_READY,
                document__answers__question_id="publikation-startdatum",
                document__answers__date__lte=now().date(),
            )
            .annotate(
                has_end_date=Exists(
                    Answer.objects.filter(
                        document_id=OuterRef("document_id"),
                        question_id="publikation-ablaufdatum",
                        date__isnull=False,
                    )
                )
            )
            .filter(has_end_date=True)
        )

        for work_item in work_items:
            complete_work_item(work_item=work_item, user=AnonymousUser())

        self.stdout.write(f"Completed {work_items.count()} publication work items")
