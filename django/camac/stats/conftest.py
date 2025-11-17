import datetime
from typing import Callable, List, Union

import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.instance.models import Instance, InstanceState
from camac.instance.serializers import SUBMIT_DATE_FORMAT


@pytest.fixture
def additional_demand_work_item(caluma_case_factory) -> Callable:
    def wrapper(
        instance,
        status,
        task_id=None,
        service_id=None,
        date_request=None,
        date_response=None,
    ):
        caluma_case = caluma_case_factory(family=instance.case)
        work_item = WorkItem.objects.create(
            task_id=task_id or "fill-additional-demand",
            case=caluma_case,
            created_by_group=service_id,
            closed_at=date_response,
            status=status,
        )
        if date_request:
            work_item.created_at = date_request
            work_item.save()
            work_item.refresh_from_db()

        return work_item

    return wrapper


@pytest.fixture
def rejected_application_factory(
    instance_factory, instance_with_case, history_entry_t_factory, freezer
):
    def wrapper(parent_application: Instance, duration: int = 5) -> Instance:
        """
        Create one rejected application predating a parent application.

        @param parent_application: Application instance succeeding rejected instance
        @param duration: num of days until rejection
        @return: instance of rejected application: Instance
        """
        instance_state_finished, created = InstanceState.objects.get_or_create(
            name="finished"
        )
        instance_state_rejected, created = InstanceState.objects.get_or_create(
            name="rejected"
        )
        freezer.move_to(
            parent_application.creation_date - datetime.timedelta(days=duration)
        )
        rejected_application = instance_with_case(
            instance_factory(
                instance_state=instance_state_finished,
                previous_instance_state=instance_state_rejected,
            )
        )
        freezer.move_to(parent_application.creation_date)
        history_entry_t_factory(
            history_entry__instance=rejected_application,
            language="de",
            title="Dossier zurückgewiesen",
        )
        rejected_application.case.meta.update(
            {
                "submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
                "paper-submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            }
        )
        rejected_application.case.save()

        parent_application.case.document.source = rejected_application.case.document
        parent_application.case.document.save()
        return rejected_application

    return wrapper


@pytest.fixture
def nest_rejected_applications(rejected_application_factory):
    def wrapper(parent: Instance, recursions: List[int]) -> Union[Instance, Callable]:
        """
        Recursively nest rejected instances.

        Every item in the recursion parameter defines a number of days
         the parent instance predates the current instance.

        The recursions sum up to the total number of days to add to the cases cycle time.
        """
        if not recursions:
            return parent
        new_parent = rejected_application_factory(parent, recursions[0])
        return wrapper(new_parent, recursions[1:])

    return wrapper
