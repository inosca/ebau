from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task

from camac.constants.kt_bern import DECISIONS_ABGELEHNT, DECISIONS_ABGESCHRIEBEN
from camac.core.models import DocxDecision


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if DocxDecision.objects.filter(
            instance=case.meta.get("camac-instance-id"),
            decision__in=[DECISIONS_ABGELEHNT, DECISIONS_ABGESCHRIEBEN],
        ).exists():
            return []

        return ["sb1", "create-manual-workitems"]
