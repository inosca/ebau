from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task
from django.conf import settings

from camac.instance.utils import should_continue_after_decision


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-decision")
    def resolve_after_decision(self, case, user, prev_work_item, context):
        if case.workflow_id == "building-permit" and should_continue_after_decision(
            case.instance, prev_work_item
        ):
            return [
                "sb1",
                settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
                "create-publication",
            ]

        return []
