import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import post_complete_case, post_create_work_item
from caluma.caluma_workflow.models import Case, WorkItem

from camac.instance.models import HistoryActionConfig


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


@pytest.mark.parametrize("decision", ["REJECTED", "ACCEPTED"])
def test_additonal_demand_check_notification(
    db,
    additional_demand_settings,
    answer_factory,
    caluma_admin_user,
    decision,
    gr_instance,
    mailoutbox,
    notification_template_factory,
    work_item_factory,
):
    accepted_notification = notification_template_factory()
    rejected_notification = notification_template_factory()

    additional_demand_settings["NOTIFICATIONS"] = {
        "ACCEPTED": [
            {
                "template_slug": accepted_notification.slug,
                "recipient_types": ["applicant"],
            }
        ],
        "REJECTED": [
            {
                "template_slug": rejected_notification.slug,
                "recipient_types": ["applicant"],
            }
        ],
    }
    additional_demand_settings["HISTORY_ENTRIES"] = {
        "ACCEPTED": "Test accepted",
        "REJECTED": "Test rejected",
    }

    answer = answer_factory(
        question__slug=additional_demand_settings["QUESTIONS"]["DECISION"],
        value=additional_demand_settings["ANSWERS"]["DECISION"][decision],
    )

    work_item = work_item_factory(
        task__slug=additional_demand_settings["CHECK_TASK"],
        document=answer.document,
        child_case=None,
        case=gr_instance.case,
    )

    complete_work_item(work_item=work_item, user=caluma_admin_user, context={})

    history_entry = (
        gr_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
    )

    assert len(mailoutbox) == 1
    if decision == "ACCEPTED":
        assert accepted_notification.subject in mailoutbox[0].subject
        assert history_entry == "Test accepted"
    elif decision == "REJECTED":
        assert rejected_notification.subject in mailoutbox[0].subject
        assert history_entry == "Test rejected"
