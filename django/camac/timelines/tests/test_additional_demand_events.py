from datetime import datetime, timedelta

import pytest
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow.models import WorkItem

from camac.tests.form_utils import FormUtils
from camac.timelines import events
from camac.timelines.models import FormTimeline


@pytest.mark.parametrize("test_case", ["applicant_reply", "cancel_additional_demand"])
def test_additional_demand_event_formtimelines(
    db,
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
    caluma_form_question_factory(
        form=fill_form,
        question=caluma_question_factory(
            slug="additional-demand-formtimeline",
            type=Question.TYPE_TEXT,
        ),
    )
    send_form = Form.objects.get(slug="send-additional-demand")
    allow_question = caluma_question_factory(
        slug="additional-demand-allow-changes",
        type=Question.TYPE_MULTIPLE_CHOICE,
    )
    caluma_form_question_factory(
        form=send_form,
        question=allow_question,
    )
    caluma_question_option_factory(
        question=allow_question,
        option=caluma_option_factory(slug="additional-demand-allow-changes"),
    )

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
    events.post_complete_send_additional_demand_allow_changes(
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
