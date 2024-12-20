from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events import additional_demand


def test_creating_an_additional_demand_sets_the_correct_instance_state(
    db,
    work_item_factory,
    workflow_factory,
    caluma_admin_user,
    ur_additional_demand_settings,
    ur_instance,
    instance_state_factory,
):
    work_item = work_item_factory(
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
    work_item_factory,
    workflow_factory,
    caluma_admin_user,
    ur_additional_demand_settings,
    ur_instance,
    instance_state_factory,
    admin_user,
    answer_factory,
    set_application_ur,
    ur_distribution_settings,
):
    ur_additional_demand_settings["NOTIFICATIONS"] = {}
    work_item = work_item_factory(
        case=ur_instance.case,
        task_id=ur_additional_demand_settings["CHECK_TASK"],
        status=WorkItem.STATUS_COMPLETED,
    )
    distribution_init_work_item = work_item_factory(
        case=ur_instance.case,
        task_id=ur_distribution_settings["DISTRIBUTION_INIT_TASK"],
        status=WorkItem.STATUS_SUSPENDED,
    )
    answer_factory(
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
