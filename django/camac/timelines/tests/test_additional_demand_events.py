from datetime import datetime, timedelta

import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events import additional_demand
from camac.tests.form_utils import FormUtils
from camac.timelines import events
from camac.timelines.models import FormTimeline
from camac.timelines.utils import is_additional_demand_with_changes


@pytest.mark.parametrize("test_case", ["applicant_reply", "cancel_additional_demand"])
@pytest.mark.django_db
def test_additional_demand_event_formtimelines(
    caluma_work_item_factory,
    caluma_case_factory,
    caluma_document_factory,
    caluma_question_factory,
    caluma_form_question_factory,
    caluma_question_option_factory,
    caluma_answer_factory,
    caluma_option_factory,
    caluma_admin_user,
    gr_additional_demand_settings,
    gr_instance,
    form_utils: FormUtils,
    test_case,
    timelines_settings,
    mocker,
):
    timelines_settings.enabled = True
    # mock the follow up signal file_subsequently for this test,
    # as this instance does not have all required answers to produce a valid xml
    mocker.patch("camac.ech0211.signals.file_subsequently.send")

    # disable notification sending for this test
    mocker.patch("camac.notification.utils.send_mail")

    assert FormTimeline.objects.count() == 0
    additional_demand_case = caluma_case_factory(family=gr_instance.case.family)

    # add extra questions and options to additional demand forms.
    fill_form = Form.objects.get(slug="fill-additional-demand")
    send_form = Form.objects.get(slug="send-additional-demand")

    # prepare additional demand work items.
    work_item_send = caluma_work_item_factory(
        case=additional_demand_case,
        child_case=None,
        document=caluma_document_factory(form=send_form),
        task_id=gr_additional_demand_settings["SEND_TASK"],
        status=WorkItem.STATUS_READY,
    )
    work_item_fill = caluma_work_item_factory(
        case=additional_demand_case,
        child_case=None,
        document=caluma_document_factory(form=fill_form),
        task_id=gr_additional_demand_settings["FILL_TASK"],
        status=WorkItem.STATUS_READY,
    )
    work_item_parent = caluma_work_item_factory(
        case=gr_instance.case.family,
        child_case=additional_demand_case,
        task_id=gr_additional_demand_settings["TASK"],
        meta={"allow-form-changes": True},
        status=WorkItem.STATUS_READY,
    )

    # fill required answers for the send additional demand work item
    caluma_answer_factory(
        document=work_item_send.document,
        question_id="additional-demand-allow-changes",
        value=["additional-demand-allow-changes"],
    )
    caluma_answer_factory(
        document=work_item_send.document,
        question_id="additional-demand-comment",
        value="test",
    )
    caluma_answer_factory(
        document=work_item_send.document,
        question_id="additional-demand-deadline",
        date=datetime.today() + timedelta(days=7),
    )

    # completing the send workitem will create a timeline.
    assert FormTimeline.objects.count() == 0
    events.post_complete_send_check_additional_demand_allow_changes(
        sender=None, work_item=work_item_send, user=caluma_admin_user
    )
    assert FormTimeline.objects.count() == 1

    events.post_create_fill_additional_demand_formtimeline(
        sender=None, work_item=work_item_fill, user=caluma_admin_user
    )
    assert work_item_fill.document.answers.filter(
        question_id="additional-demand-formtimeline"
    ).exists()

    timeline = FormTimeline.objects.first()
    assert timeline.end_date is None

    # on completing or canceling the additional demand, the timeline
    # should be closed by setting an end date.
    if test_case == "cancel_additional_demand":
        events.post_cancel_additional_demand_allow_changes(
            sender=None, work_item=work_item_parent, user=caluma_admin_user
        )
    else:
        events.post_complete_fill_additional_demand_form_timelines(
            sender=None, work_item=work_item_fill, user=caluma_admin_user
        )

    assert FormTimeline.objects.count() == 1
    timeline.refresh_from_db()
    assert timeline.end_date is not None


@pytest.mark.parametrize("allow_changes", [True, False])
@pytest.mark.parametrize("decision_is_positive", [True, False])
@pytest.mark.django_db
def test_post_complete_check_additional_demand_with_changes_gr(
    caluma_work_item_factory,
    caluma_admin_user,
    gr_additional_demand_settings,
    gr_instance,
    caluma_answer_factory,
    notification_template_factory,
    active_inquiry_factory,
    service_factory,
    mailoutbox,
    form_utils: FormUtils,
    allow_changes,
    decision_is_positive,
    application_settings,
    set_application_gr,
):
    service_a = service_factory()
    service_b = service_factory()

    active_inquiry_factory(controlling_service=service_a, addressed_service=service_b)
    tpl_accept_changes = notification_template_factory()
    tpl_accept = notification_template_factory()
    tpl_rejected = notification_template_factory()

    gr_additional_demand_settings["NOTIFICATIONS"] = {
        "ACCEPTED": [
            {
                "recipient_types": ["work_item_controlling"],
                "template_slug": tpl_accept.slug,
                "condition": lambda work_item: (
                    not is_additional_demand_with_changes(work_item)
                ),
            },
            {
                "recipient_types": ["work_item_controlling"],
                "template_slug": tpl_accept_changes.slug,
                "condition": lambda work_item: is_additional_demand_with_changes(
                    work_item
                ),
            },
        ],
        "REJECTED": [
            {
                "recipient_types": ["applicant"],
                "template_slug": tpl_rejected.slug,
            }
        ],
    }
    application_settings["CALUMA_WORKFLOW_NOTIFICATIONS"] = {}

    work_item_send = caluma_work_item_factory(
        case=gr_instance.case,
        task_id=gr_additional_demand_settings["SEND_TASK"],
        status=WorkItem.STATUS_COMPLETED,
        controlling_groups=[str(service_a.pk)],
    )
    if allow_changes:
        form_utils.add_answer(
            work_item_send.document,
            "additional-demand-allow-changes",
            ["additional-demand-allow-changes"],
        )
    work_item = caluma_work_item_factory(
        case=gr_instance.case,
        child_case=gr_instance.case,
        task_id=gr_additional_demand_settings["CHECK_TASK"],
        status=WorkItem.STATUS_COMPLETED,
        controlling_groups=[str(service_a.pk)],
    )
    caluma_answer_factory(
        document=work_item.document,
        question_id=gr_additional_demand_settings["QUESTIONS"]["DECISION"],
        value=gr_additional_demand_settings["ANSWERS"]["DECISION"]["ACCEPTED"]
        if decision_is_positive
        else gr_additional_demand_settings["ANSWERS"]["DECISION"]["REJECTED"],
    )
    additional_demand.post_complete_check_additional_demand(
        sender=None, work_item=work_item, user=caluma_admin_user
    )

    assert len(mailoutbox) == 1
    if decision_is_positive:
        assert mailoutbox[0].recipients() == [service_a.email]

        if not allow_changes:
            assert tpl_accept.subject in mailoutbox[0].subject
        else:
            assert tpl_accept_changes.subject in mailoutbox[0].subject
    else:
        assert mailoutbox[0].recipients() == [
            applicant.invitee.email
            for applicant in gr_instance.involved_applicants.all()
            if applicant.invitee
        ]
        assert tpl_rejected.subject in mailoutbox[0].subject
