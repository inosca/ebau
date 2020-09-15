from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task

from camac.constants.kt_bern import DECISIONS_BEWILLIGT
from camac.core.models import Circulation, DocxDecision


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if (
            case.workflow_id == "building-permit"
            and DocxDecision.objects.filter(
                instance=case.meta.get("camac-instance-id"),
                decision=DECISIONS_BEWILLIGT,
            ).exists()
        ):
            return ["sb1", "create-manual-workitems"]

        return []

    @register_dynamic_task("after-circulation")
    def resolve_after_circulation(self, case, user, prev_work_item, context):
        if not Circulation.objects.filter(
            instance=case.meta.get("camac-instance-id")
        ).exists():
            return ["init-circulation"]

        return ["start-circulation", "check-activation", "start-decision"]
