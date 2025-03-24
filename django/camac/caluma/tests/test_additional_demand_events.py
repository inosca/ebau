import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events import additional_demand


def test_creating_an_additional_demand_sets_the_correct_instance_state(
    db,
    caluma_work_item_factory,
    caluma_workflow_factory,
    caluma_admin_user,
    ur_additional_demand_settings,
    ur_instance,
    instance_state_factory,
):
    work_item = caluma_work_item_factory(
        case=ur_instance.case, task_id=ur_additional_demand_settings["TASK"]
    )
    instance_state_factory(
        name=ur_additional_demand_settings["STATES"]["PENDING_ADDITIONAL_DEMANDS"]
    )
    additional_demand.post_create_additional_demand(
        sender=None, work_item=work_item, user=caluma_admin_user
    )

    ur_instance.refresh_from_db()

    assert (
        ur_instance.instance_state.name
        == ur_additional_demand_settings["STATES"]["PENDING_ADDITIONAL_DEMANDS"]
    )


def test_post_complete_check_additional_demand_ur(
    db,
    caluma_work_item_factory,
    caluma_workflow_factory,
    caluma_admin_user,
    ur_additional_demand_settings,
    ur_instance,
    instance_state_factory,
    admin_user,
    caluma_answer_factory,
    set_application_ur,
    ur_distribution_settings,
):
    ur_additional_demand_settings["NOTIFICATIONS"] = {}
    work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id=ur_additional_demand_settings["CHECK_TASK"],
        status=WorkItem.STATUS_COMPLETED,
    )
    distribution_init_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id=ur_distribution_settings["DISTRIBUTION_INIT_TASK"],
        status=WorkItem.STATUS_SUSPENDED,
    )
    caluma_answer_factory(
        document=work_item.document,
        question_id=ur_additional_demand_settings["QUESTIONS"]["DECISION"],
        value=ur_additional_demand_settings["ANSWERS"]["DECISION"]["ACCEPTED"],
    )
    instance_state_factory(
        name=ur_additional_demand_settings["STATES"]["PENDING_ADDITIONAL_DEMANDS"]
    )
    additional_demand.post_complete_check_additional_demand(
        sender=None, work_item=work_item, user=caluma_admin_user
    )

    ur_instance.refresh_from_db()

    assert ur_instance.instance_state.name == ur_instance.previous_instance_state.name
    distribution_init_work_item.refresh_from_db()
    assert distribution_init_work_item.status == WorkItem.STATUS_READY


@pytest.mark.parametrize("has_pending_additional_demands", [True, False])
def test_post_cancel_additional_demand_ur(
    db,
    ur_instance,
    set_application_ur,
    caluma_admin_user,
    caluma_work_item_factory,
    instance_state_factory,
    ur_additional_demand_settings,
    has_pending_additional_demands,
):
    ur_instance.instance_state.name = "nfd"
    ur_instance.instance_state.save()

    work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id=ur_additional_demand_settings["TASK"],
        status=WorkItem.STATUS_COMPLETED,
    )
    if has_pending_additional_demands:
        work_item = caluma_work_item_factory(
            case=ur_instance.case,
            task_id=ur_additional_demand_settings["TASK"],
            status=WorkItem.STATUS_READY,
        )

    additional_demand.post_cancel_additional_demand(
        sender=None, work_item=work_item, user=caluma_admin_user
    )

    ur_instance.refresh_from_db()

    if has_pending_additional_demands:
        assert ur_instance.instance_state.name == "nfd"
    else:
        assert (
            ur_instance.instance_state.name == ur_instance.previous_instance_state.name
        )
