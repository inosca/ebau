from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.events import post_create_work_item


def test_additonal_demand_child_case(
    db,
    settings,
    additional_demand_settings,
    instance,
    caluma_admin_user,
    work_item_factory,
    workflow_factory,
    task_factory,
):
    workflow_factory(slug="additional-demand")
    work_item = work_item_factory(
        task=task_factory(slug="additional-demand"), child_case=None
    )

    case = work_item.case
    instance.case = case
    instance.save()

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    work_item.refresh_from_db()

    assert work_item.child_case_id
