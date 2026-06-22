import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import post_complete_case, post_create_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem

from camac.instance.models import HistoryActionConfig


@pytest.mark.django_db
def test_additonal_demand(
    additional_demand_settings,
    instance,
    caluma_admin_user,
    caluma_work_item_factory,
    caluma_workflow_factory,
):
    workflow = caluma_workflow_factory(slug=additional_demand_settings["WORKFLOW"])
    work_item = caluma_work_item_factory(
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
@pytest.mark.django_db
def test_additonal_demand_check_notification(
    gr_additional_demand_settings,
    caluma_answer_factory,
    caluma_case_factory,
    caluma_admin_user,
    decision,
    gr_instance,
    mailoutbox,
    notification_template_factory,
    caluma_work_item_factory,
    mocker,
):
    # disable the file_subsequently signal for this test
    mocker.patch("camac.ech0211.signals.file_subsequently.send")

    accepted_notification = notification_template_factory()
    rejected_notification = notification_template_factory()

    gr_additional_demand_settings["NOTIFICATIONS"] = {
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
    gr_additional_demand_settings["HISTORY_ENTRIES"] = {
        "ACCEPTED": "Test accepted",
        "REJECTED": "Test rejected",
    }

    answer = caluma_answer_factory(
        question=Question.objects.get(
            slug=gr_additional_demand_settings["QUESTIONS"]["DECISION"]
        ),
        value=gr_additional_demand_settings["ANSWERS"]["DECISION"][decision],
    )

    work_item = caluma_work_item_factory(
        task=Task.objects.get(slug=gr_additional_demand_settings["CHECK_TASK"]),
        document=answer.document,
        child_case=None,
        case=caluma_case_factory(family=gr_instance.case.family),
    )
    caluma_work_item_factory(
        task_id=gr_additional_demand_settings["TASK"],
        child_case=work_item.case,
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


@pytest.mark.django_db
def test_additional_demand_fill_notification_be(
    be_additional_demand_settings,
    application_settings,
    caluma_admin_user,
    be_instance,
    mailoutbox,
    notification_template_factory,
    caluma_work_item_factory,
    mocker,
):
    mock_file_subsequently = mocker.patch(
        "camac.ech0211.signals.file_subsequently.send"
    )
    caluma_fill_notification = notification_template_factory()

    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["fill-additional-demand"][
        "notification"
    ]["template_slug"] = caluma_fill_notification.slug

    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["fill-additional-demand"][
        "history_text"
    ] = "Test additional demand was answered"
    work_item = caluma_work_item_factory(
        task=Task.objects.get(slug=be_additional_demand_settings["FILL_TASK"]),
        child_case=None,
        case=be_instance.case,
    )
    caluma_work_item_factory(
        task_id=be_additional_demand_settings["TASK"],
        child_case=work_item.case,
    )

    complete_work_item(work_item=work_item, user=caluma_admin_user, context={})

    history_entry = (
        be_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
    )

    assert len(mailoutbox) == 1
    assert caluma_fill_notification.subject in mailoutbox[0].subject
    assert history_entry == "Test additional demand was answered"
    assert mock_file_subsequently.call_count == 1
