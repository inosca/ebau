from datetime import date, timedelta

import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import (
    complete_work_item,
)
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events import additional_demand
from camac.tests.form_utils import FormUtils


@pytest.mark.django_db
def test_creating_an_additional_demand_sets_the_correct_instance_state(
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


@pytest.mark.django_db
def test_post_complete_check_additional_demand_ur(
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
@pytest.mark.django_db
def test_post_cancel_additional_demand_ur(
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


@pytest.mark.parametrize("ech_enabled", [True, False])
@pytest.mark.django_db
def test_post_complete_fill_additional_demand_file_subsequently(
    set_application_gr,
    caluma_work_item_factory,
    caluma_admin_user,
    gr_additional_demand_settings,
    gr_ech0211_settings,
    gr_instance,
    mocker,
    ech_enabled,
):
    gr_ech0211_settings["API_LEVEL"] = "full" if ech_enabled else "none"
    ech_signal_mock = mocker.patch("camac.ech0211.signals.file_subsequently.send")
    work_item = caluma_work_item_factory(
        case=gr_instance.case, task_id=gr_additional_demand_settings["FILL_TASK"]
    )
    additional_demand.post_complete_fill_additional_demand_file_subsequently(
        sender=None, work_item=work_item, user=caluma_admin_user
    )
    if ech_enabled:
        ech_signal_mock.assert_called_once()
    else:
        ech_signal_mock.assert_not_called()


@pytest.mark.parametrize(
    "test_case",
    [
        "decision_unknown_not_set",
        "ech_not_enabled",
        "ech_claim_not_enabled",
        "no_ech_meta",
        "ok",
    ],
)
@pytest.mark.django_db
def test_post_create_check_additional_demand(
    set_application_gr,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_admin_user,
    gr_additional_demand_settings,
    gr_ech0211_settings,
    gr_instance,
    mocker,
    form_utils: FormUtils,
    test_case,
):
    # mock the follow up signal file_subsequently for this test,
    # as this instance does not have all required answers to produce a valid xml
    mocker.patch("camac.ech0211.signals.file_subsequently.send")

    # disable notification sending for this test
    mocker.patch("camac.notification.utils.send_mail")

    # unset UNKNOWN decision setting for decision_unknown_not_set
    gr_additional_demand_settings["ANSWERS"]["DECISION"]["UNKNOWN"] = (
        None
        if test_case == "decision_unknown_not_set"
        else "additional-demand-decision-unknown"
    )

    # disable eCH0211 settings for ech_not_enabled
    gr_ech0211_settings["API_LEVEL"] = (
        "none" if test_case == "ech_not_enabled" else "full"
    )

    # disable claim settings for ech_claim_not_enabled
    gr_ech0211_settings["CLAIM"]["ENABLED"] = (
        False if test_case == "ech_claim_not_enabled" else True
    )

    work_item_init = caluma_work_item_factory(
        case=gr_instance.case.family,
        task_id=gr_additional_demand_settings["CREATE_TASK"],
    )

    # set the eCH0211 meta data on work items if not no_ech_meta
    meta = (
        {"ech-init-workitem": str(work_item_init.pk)}
        if test_case != "no_ech_meta"
        else {}
    )
    if test_case != "no_ech_meta":
        work_item_init.meta["ech-init-workitem"] = str(work_item_init.pk)
        work_item_init.save()

    # prepare the check task work item
    work_item_check = caluma_work_item_factory(
        case=gr_instance.case.family,
        document=caluma_document_factory(
            form=Form.objects.get(slug="check-additional-demand")
        ),
        task_id=gr_additional_demand_settings["CHECK_TASK"],
        child_case=None,
        meta=meta,
        status=WorkItem.STATUS_READY,
    )

    # check exception raised for decision_unknown_not_set
    if test_case == "decision_unknown_not_set":
        with pytest.raises(Exception):
            additional_demand.post_create_check_additional_demand(
                sender=None, work_item=work_item_check, user=caluma_admin_user
            )
        return

    # prepare the fill task work item and add only the required answers
    work_item_fill = caluma_work_item_factory(
        case=gr_instance.case.family,
        document=caluma_document_factory(
            form=Form.objects.get(slug="fill-additional-demand")
        ),
        task_id=gr_additional_demand_settings["FILL_TASK"],
        status=WorkItem.STATUS_READY,
        meta=meta,
        child_case=None,
    )
    form_utils.add_answer(
        work_item_fill.document,
        gr_additional_demand_settings["QUESTIONS"]["DEADLINE"],
        date.today() + timedelta(days=30),
    )

    complete_work_item(
        work_item=work_item_fill,
        user=caluma_admin_user,
    )
    assert work_item_fill.status == WorkItem.STATUS_COMPLETED

    # trigger the event manually
    additional_demand.post_create_check_additional_demand(
        sender=None, work_item=work_item_check, user=caluma_admin_user
    )

    ech_answer = work_item_check.document.answers.filter(
        question_id="additional-demand-ech0211"
    ).first()

    # only when all conditions have been fulfilled, work item should be
    # immediately completed
    if test_case == "ok":
        assert work_item_check.status == WorkItem.STATUS_COMPLETED
        assert ech_answer and ech_answer.value == "true", (
            "additional demand work item ech answer should be created"
        )
    elif test_case == "no_ech_meta":
        assert work_item_check.status == WorkItem.STATUS_READY
        assert ech_answer is None, (
            "additional demand work item ech answer should not be created"
        )
    else:
        assert work_item_check.status == WorkItem.STATUS_READY


@pytest.mark.django_db
def test_post_cancel_additional_demand_notification(
    caluma_work_item_factory,
    notification_template_factory,
    caluma_task_factory,
    caluma_admin_user,
    caluma_case_factory,
    instance,
    mailoutbox,
    additional_demand_settings,
):
    case = caluma_case_factory()
    instance.case = case
    instance.save()

    work_item = caluma_work_item_factory(
        case=instance.case,
        task=caluma_task_factory(pk=additional_demand_settings["TASK"]),
    )

    # by default no notifications are configured for cancel.
    additional_demand.post_cancel_additional_demand_notification(
        sender=None, work_item=work_item, user=caluma_admin_user
    )
    assert len(mailoutbox) == 0

    # test with a cancel notification configured.
    test_template = notification_template_factory()
    additional_demand_settings["NOTIFICATIONS"]["CANCELLED"] = [
        {
            "template_slug": test_template.slug,
            "recipient_types": ["applicant"],
        }
    ]
    additional_demand.post_cancel_additional_demand_notification(
        sender=None, work_item=work_item, user=caluma_admin_user
    )
    assert len(mailoutbox) == 1
    assert test_template.subject in mailoutbox[0].subject
