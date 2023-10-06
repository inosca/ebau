from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.events import post_complete_case, post_create_work_item
from caluma.caluma_workflow.models import Case, WorkItem


def test_additonal_demand(
    db,
    additional_demand_settings,
    instance,
    caluma_admin_user,
    work_item_factory,
    workflow_factory,
):
    workflow = workflow_factory(slug=additional_demand_settings["WORKFLOW"])
    work_item = work_item_factory(
        task__slug=additional_demand_settings["TASK"], child_case=None
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

    assert work_item.child_case.status == Case.STATUS_RUNNING
    assert work_item.child_case.workflow == workflow

    work_item.child_case.status = Case.STATUS_COMPLETED
    work_item.child_case.save()
    send_event(
        post_complete_case,
        sender="post_complete_case",
        case=work_item.child_case,
        user=caluma_admin_user,
        context={},
    )

    work_item.refresh_from_db()

    assert work_item.status == WorkItem.STATUS_COMPLETED
