from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task

from camac.core.models import Circulation
from camac.instance.utils import should_continue_after_decision


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if case.workflow_id == "building-permit" and should_continue_after_decision(
            case.instance
        ):
            return ["sb1", "create-manual-workitems", "create-publication"]

        return []

    @register_dynamic_task("after-circulation")
    def resolve_after_circulation(self, case, user, prev_work_item, context):
        has_circulations = Circulation.objects.filter(
            instance=case.instance.pk
        ).exists()
        instance_state = case.instance.instance_state.name

        if not has_circulations:
            # last circulation was deleted
            if instance_state == "circulation_init":
                # circulation was not started before deleting
                return ["skip-circulation", "init-circulation"]
            elif instance_state == "circulation":
                # circulation was started before deleting
                return ["start-circulation", "start-decision"]

        return ["start-circulation", "check-activation", "start-decision"]
