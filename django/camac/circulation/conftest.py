from typing import List

import pytest
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem

from camac.core.models import CirculationState


@pytest.fixture
def init_circulation_with_activations(
    instance_service,  # required to get permissions right for the `circulation-end` endpoint
    caluma_admin_user,
    circulation_factory,
    caluma_workflow_config_be,
    activation_factory,
):
    """
    Start a circulation belonging to the provided instance's case.

    The parameter `instance_with_case` is an instance with case and workitems where circulation can happen.
    Its workitem is ff'ed to `init-circulation`.

    The parameter `activations_answer` is an iterabale of booleans indicating how many activations belong
    to the circulation created and whether they are answered.

    The initialized circulation is returned.
    """

    def wrapper(camac_instance, service, activations_answer: List[CirculationState]):
        circulation = circulation_factory(instance=camac_instance, service=service)
        for task_id in ["submit", "ebau-number", "init-circulation"]:
            work_items = camac_instance.case.work_items.all()
            if work_items.filter(task_id=task_id).count() > 1:
                work_items = work_items.exclude(status=WorkItem.STATUS_READY)
            work_item = work_items.get(task_id=task_id)
            work_item.status = WorkItem.STATUS_READY
            work_item.meta.update(**{"circulation-id": circulation.pk})
            work_item.save()
            skip_work_item(
                work_item,
                caluma_admin_user,
                context={"circulation-id": circulation.pk},
            )
        for act in activations_answer:
            activation_factory(
                circulation=circulation,
                circulation_state=act,
            )
        circulation.save()
        return circulation

    return wrapper
