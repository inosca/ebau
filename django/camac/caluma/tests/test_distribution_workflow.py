import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import (
    complete_work_item,
    redo_work_item,
    resume_work_item,
    skip_work_item,
)
from caluma.caluma_workflow.models import Case, WorkItem


@pytest.fixture
def distribution_case(be_instance, caluma_admin_user, instance_state_factory):
    instance_state_factory(name="circulation")
    instance_state_factory(name="coordination")

    case = be_instance.case

    skip_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )
    skip_work_item(
        work_item=case.work_items.get(task_id="ebau-number"), user=caluma_admin_user
    )

    return case


@pytest.fixture
def distribution_child_case(distribution_case, distribution_settings):
    return distribution_case.work_items.get(
        task_id=distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def inquiry_factory(
    caluma_admin_user,
    distribution_child_case,
    distribution_settings,
    service,
    service_factory,
    notification_template_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="03-verfahrensablauf-gesuchsteller")

    def factory(to_service=service_factory(), sent=False):
        complete_work_item(
            work_item=distribution_child_case.work_items.get(
                task_id=distribution_settings["INQUIRY_CREATE_TASK"],
                addressed_groups=[str(service.pk)],
                status=WorkItem.STATUS_READY,
            ),
            user=caluma_admin_user,
            context={"addressed_groups": [str(to_service.pk)]},
        )

        work_item = distribution_child_case.work_items.filter(
            addressed_groups=[str(to_service.pk)],
            controlling_groups=[str(service.pk)],
            status=WorkItem.STATUS_SUSPENDED,
        ).first()

        if sent:
            resume_work_item(
                work_item=work_item,
                user=caluma_admin_user,
            )
            work_item.refresh_from_db()

        return work_item

    return factory


@pytest.mark.freeze_time("2022-03-23")
def test_distribution_initial_state(
    db, distribution_child_case, distribution_settings, service
):
    create_inquiry = distribution_child_case.work_items.get(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"]
    )
    end_distribution = distribution_child_case.work_items.get(
        task_id=distribution_settings["DISTRIBUTION_COMPLETE_TASK"]
    )
    init_distribution = distribution_child_case.work_items.get(
        task_id=distribution_settings["DISTRIBUTION_INIT_TASK"]
    )

    for work_item in [create_inquiry, end_distribution, init_distribution]:
        assert work_item.status == WorkItem.STATUS_READY
        assert work_item.addressed_groups == [str(service.pk)]

    assert create_inquiry.deadline is None
    assert end_distribution.deadline is None
    assert init_distribution.controlling_groups == [str(service.pk)]
    assert init_distribution.deadline.isoformat() == "2022-04-02T00:00:00+00:00"


@pytest.mark.freeze_time("2022-03-23")
def test_create_inquiry(
    db,
    distribution_child_case,
    distribution_settings,
    inquiry_factory,
    service,
    service_factory,
):
    invited_service = service_factory()
    invited_subservice = service_factory(service_parent=service)

    service_inquiry = inquiry_factory(invited_service)
    subservice_inquiry = inquiry_factory(invited_subservice)

    for work_item in [service_inquiry, subservice_inquiry]:
        assert work_item.status == WorkItem.STATUS_SUSPENDED
        assert work_item.deadline is None

    assert distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(invited_service.pk)],
    ).exists()
    assert distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    ).exists()

    # invited subservice should not have a create-inquiry work item
    assert not distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(invited_subservice.pk)],
    ).exists()


@pytest.mark.freeze_time("2022-03-23")
@pytest.mark.parametrize("user__email", ["applicant@example.com"])
def test_send_inquiry(
    db,
    be_instance,
    distribution_child_case,
    distribution_settings,
    inquiry_factory,
    mailoutbox,
    notification_template_factory,
    service_factory,
):
    distribution_settings["NOTIFICATIONS"] = {
        "INQUIRY_SENT": {
            "template_slug": notification_template_factory().slug,
            "recipient_types": ["inquiry_addressed"],
        }
    }

    service = service_factory()
    inquiry = inquiry_factory(to_service=service, sent=True)

    assert inquiry.status == WorkItem.STATUS_READY
    assert inquiry.deadline.isoformat() == "2022-04-22T00:00:00+00:00"

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == "circulation"
    assert (
        distribution_child_case.work_items.get(
            task_id=distribution_settings["DISTRIBUTION_INIT_TASK"],
        ).status
        == WorkItem.STATUS_COMPLETED
    )

    assert len(mailoutbox) == 2
    assert mailoutbox[0].to[0] == "applicant@example.com"
    assert mailoutbox[1].to[0] == service.email


@pytest.mark.freeze_time("2022-03-23")
@pytest.mark.parametrize("service__email", ["service@example.com"])
def test_complete_inquiry(
    db,
    caluma_admin_user,
    distribution_child_case,
    distribution_settings,
    inquiry_factory,
    mailoutbox,
    notification_template_factory,
    service,
):
    distribution_settings["NOTIFICATIONS"] = {
        "INQUIRY_ANSWERED": {
            "template_slug": notification_template_factory().slug,
            "recipient_types": ["inquiry_controlling"],
        }
    }

    inquiry = inquiry_factory(sent=True)

    for question, value in [
        ("inquiry-answer-status", "inquiry-answer-status-positive"),
        ("inquiry-answer-statement", "Stellungnahme Test"),
        ("inquiry-answer-ancillary-clauses", "Nebenbestimmungen Test"),
    ]:
        save_answer(
            question=Question.objects.get(pk=question),
            document=inquiry.child_case.document,
            value=value,
            user=caluma_admin_user,
        )

    mailoutbox.clear()

    complete_work_item(
        work_item=inquiry.child_case.work_items.first(), user=caluma_admin_user
    )

    inquiry.refresh_from_db()

    assert distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    ).exists()

    assert inquiry.child_case.status == Case.STATUS_COMPLETED
    assert inquiry.status == WorkItem.STATUS_COMPLETED

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to[0] == "service@example.com"


def test_complete_distribution(
    db,
    be_instance,
    caluma_admin_user,
    distribution_child_case,
    distribution_settings,
    inquiry_factory,
    mailoutbox,
    notification_template_factory,
    service_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="03-verfahren-vorzeitig-beendet")

    service = service_factory()

    draft_inquiry = inquiry_factory()  # draft - will be canceled
    sent_inquiry = inquiry_factory(
        to_service=service, sent=True
    )  # sent - will be skipped

    assert (
        distribution_child_case.work_items.filter(status=WorkItem.STATUS_READY).count()
        == 5  # 1x complete-distribution, 3x create-inquiry, 1x inquiry
    )
    assert (
        distribution_child_case.work_items.filter(
            status=WorkItem.STATUS_SUSPENDED
        ).count()
        == 1  # 1x inquiry
    )

    mailoutbox.clear()

    complete_work_item(
        work_item=distribution_child_case.work_items.get(
            task_id=distribution_settings["DISTRIBUTION_COMPLETE_TASK"],
            status=WorkItem.STATUS_READY,
        ),
        user=caluma_admin_user,
    )

    draft_inquiry.refresh_from_db()
    sent_inquiry.refresh_from_db()

    assert draft_inquiry.status == WorkItem.STATUS_CANCELED
    assert sent_inquiry.status == WorkItem.STATUS_SKIPPED

    assert (
        distribution_child_case.work_items.filter(
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED]
        ).count()
        == 0
    )

    distribution_child_case.refresh_from_db()

    assert distribution_child_case.status == Case.STATUS_COMPLETED
    assert distribution_child_case.parent_work_item.status == WorkItem.STATUS_COMPLETED

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == "coordination"

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to[0] == service.email


def test_reopen_distribution(
    db,
    be_instance,
    caluma_admin_user,
    distribution_child_case,
    distribution_settings,
    inquiry_factory,
    notification_template_factory,
    service_factory,
    service,
    instance_state_factory,
):
    instance_state_distribution = instance_state_factory()

    distribution_settings[
        "INSTANCE_STATE_DISTRIBUTION"
    ] = instance_state_distribution.name

    # this is needed so that simple workflow works
    notification_template_factory(slug="03-verfahren-vorzeitig-beendet")

    service_with_sent_inquiry = service_factory()
    service_with_unsent_inquiry = service_factory()
    subservice_with_sent_inquiry = service_factory(
        service_parent=service_with_sent_inquiry
    )

    inquiry_factory(to_service=service_with_sent_inquiry, sent=True)
    inquiry_factory(to_service=service_with_unsent_inquiry)
    inquiry_factory(to_service=subservice_with_sent_inquiry, sent=True)

    complete_distribution = distribution_child_case.work_items.get(
        task_id=distribution_settings["DISTRIBUTION_COMPLETE_TASK"]
    )

    # complete distribution to create proper workflow status for reopening the
    # distribution again
    complete_work_item(work_item=complete_distribution, user=caluma_admin_user)

    distribution_child_case.refresh_from_db()
    be_instance.refresh_from_db()

    distribution = be_instance.case.work_items.get(
        task_id=distribution_settings["DISTRIBUTION_TASK"]
    )
    decision = be_instance.case.work_items.get(task_id="decision")

    assert distribution_child_case.status == Case.STATUS_COMPLETED
    assert distribution.status == WorkItem.STATUS_COMPLETED
    assert decision.status == WorkItem.STATUS_READY
    assert be_instance.instance_state.name == "coordination"

    # redo distribution
    redo_work_item(work_item=distribution, user=caluma_admin_user)

    distribution_child_case.refresh_from_db()
    distribution.refresh_from_db()
    complete_distribution.refresh_from_db()
    decision.refresh_from_db()
    be_instance.refresh_from_db()

    assert distribution_child_case.status == Case.STATUS_RUNNING
    assert distribution.status == WorkItem.STATUS_READY
    assert complete_distribution.status == WorkItem.STATUS_READY
    assert decision.status == WorkItem.STATUS_REDO
    assert be_instance.instance_state == instance_state_distribution

    # the service that reopened the distribution should have a work item to
    # create a new inquiry
    assert distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the service that had an inquiry in the previous distribution run should
    # have a work item to create a new inquiry
    assert distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service_with_sent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the service that had an inquiry that was unsent in the previous
    # distribution run should **not** have a work item to create a new inquiry
    # since the previous inquiry was canceled on completion of the distribution
    assert not distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service_with_unsent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the subservice that had a sent inquiry should **not** have a work item to
    # create a new inquiry
    assert not distribution_child_case.work_items.filter(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(subservice_with_sent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()
