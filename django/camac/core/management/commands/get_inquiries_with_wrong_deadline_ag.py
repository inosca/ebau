from datetime import timedelta

from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service

ADDRESSED_SERVICE_LEAD_TIME_MAPPING = {
    "afb": 60,
    "amb": 30,
    "agv-bs": 30,
    "agv-esp": 30,
    "bks-dp": 14,
    "bks-ka": 14,
    "dvi-awa-iga": 14,
    "aew": 14,
    "axpo": 14,
    "dgs-avs-vet": 14,
    "dgs-avs-lmi": 14,
}


class Command(BaseCommand):
    help = """Show all inquiry work-items with a wrong deadline"""

    @transaction.atomic
    def handle(self, *args, **options):
        work_items_with_wrong_deadline = []

        work_items = WorkItem.objects.filter(
            task_id="inquiry",
        ).select_related("document")

        for work_item in work_items:
            work_item_deadline = work_item.deadline.date()

            answer_obj = work_item.document.answers.filter(
                question_id="inquiry-deadline"
            ).first()
            caluma_deadline_answer = answer_obj.date if answer_obj else None

            addressed_services = Service.objects.filter(
                pk__in=work_item.addressed_groups
            )

            child_case = work_item.child_case

            if not child_case:
                continue

            fill_inquiry_work_item = child_case.work_items.filter(
                task_id="fill-inquiry"
            ).first()

            for service in addressed_services:
                lead_time_days = ADDRESSED_SERVICE_LEAD_TIME_MAPPING.get(service.slug)
                if lead_time_days is None:
                    continue

                expected_deadline = (
                    fill_inquiry_work_item.created_at.date()
                    + timedelta(days=lead_time_days)
                )

                if (
                    expected_deadline != work_item_deadline
                    or expected_deadline != caluma_deadline_answer
                ):
                    work_items_with_wrong_deadline.append(
                        {
                            "instance_id": work_item.case.family.instance.pk,
                            "id": work_item.id,
                            "service": service.slug,
                            "expected_deadline": expected_deadline,
                            "actual_deadline": work_item_deadline,
                            "caluma_answer": caluma_deadline_answer,
                            "difference": (expected_deadline - work_item_deadline).days,
                        }
                    )
                    break

        for item in work_items_with_wrong_deadline:
            self.stdout.write(
                f"Instance ID: {item['instance_id']} | "
                f"WorkItem ID: {item['id']} | "
                f"Service: {item['service']} | "
                f"Expected: {item['expected_deadline']} | "
                f"Actual: {item['actual_deadline']} | "
                f"Difference in days: {item['difference']} | "
                f"Caluma: {item['caluma_answer']}"
            )

        self.stdout.write(
            f"Found {len(work_items_with_wrong_deadline)} items with wrong deadlines."
        )
