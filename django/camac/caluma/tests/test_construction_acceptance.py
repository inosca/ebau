from camac.caluma.extensions.events.simple_workflow import (
    post_complete_construction_acceptance_gr,
)


def test_construction_acceptance_complete_instance_gr(
    db,
    gr_instance,
    caluma_work_item_factory,
    set_application_gr,
    mocker,
):
    permissions_mock = mocker.patch(
        "camac.caluma.extensions.events.simple_workflow.permissions_events.Trigger.instance_completed"
    )

    work_item = caluma_work_item_factory(
        case=gr_instance.case,
        task_id="construction-acceptance",
    )

    post_complete_construction_acceptance_gr(
        None,
        work_item=work_item,
        user=None,
        context={},
    )

    assert permissions_mock.call_count == 1
