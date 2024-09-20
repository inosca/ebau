from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    help = """
    Re-open the decision work item for instances which are recent and the responsible municipality might want to perform the decision/construction monitoring.
    """

    @transaction.atomic
    def handle(self, *args, **options):
        instances_in_control_after_2023 = Instance.objects.filter(
            instance_state__name="control", case__created_at__gt=datetime(2023, 1, 1)
        )

        for instance in instances_in_control_after_2023:
            if (
                instance.case.work_items.filter(
                    task_id="decision", status="completed"
                ).exists()
                and not instance.case.work_items.filter(
                    task_id="init-construction-monitoring"
                ).exists()
            ):
                decision_work_item = instance.case.work_items.get(
                    task_id="decision", status="completed"
                )
                print(
                    f"Instance: {instance.pk} (#{instance.responsible_service().name}) has a completed decision work item and no construction monitoring work item"
                )
                decision_work_item.status = "ready"
                decision_work_item.save()
