from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task

from camac.constants.kt_bern import DECISIONS_BEWILLIGT
from camac.core.models import Circulation, DocxDecision
from camac.instance.models import Instance


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
        instance_id = case.meta.get("camac-instance-id")
        has_circulations = Circulation.objects.filter(instance=instance_id).exists()
        instance_state = Instance.objects.get(pk=instance_id).instance_state.name

        if not has_circulations:
            # last circulation was deleted
            if instance_state == "circulation_init":
                # circulation was not started before deleting
                return ["skip-circulation", "init-circulation"]
            elif instance_state == "circulation":
                # circulation was started before deleting
                return ["start-circulation", "start-decision"]

        return ["start-circulation", "check-activation", "start-decision"]
