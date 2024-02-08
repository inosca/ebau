from datetime import timedelta

import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import (
    cancel_work_item,
    complete_work_item,
    redo_work_item,
    resume_case,
    resume_work_item,
    skip_work_item,
    suspend_case,
)
from caluma.caluma_workflow.models import Case, WorkItem
from django.utils.timezone import now

from camac.constants import kt_bern as bern_constants


def _inquiry_factory(
    to_service,
    from_service,
    sent,
    user,
    distribution_child_case,
    distribution_settings,
):
    create_work_item = distribution_child_case.work_items.get(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups=[str(from_service.pk)],
        status=WorkItem.STATUS_READY,
    )

    complete_work_item(
        work_item=create_work_item,
        user=user,
        context={"addressed_groups": [str(to_service.pk)]},
    )

    create_work_item.refresh_from_db()

    work_item = create_work_item.succeeding_work_items.get(
        addressed_groups=[str(to_service.pk)],
        controlling_groups=[str(from_service.pk)],
        status=WorkItem.STATUS_SUSPENDED,
    )

    if sent:
        resume_work_item(work_item=work_item, user=user)
        work_item.refresh_from_db()

    return work_item


@pytest.fixture
def distribution_case_be(
    be_instance,
    caluma_admin_user,
    instance_state_factory,
    be_distribution_settings,
    notification_template_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="05-bericht-erstellt")
    notification_template_factory(slug="03-verfahrensablauf-fachstelle")
    notification_template_factory(slug="03-verfahrensablauf-gesuchsteller")
    notification_template_factory(slug="03-verfahren-vorzeitig-beendet")
    instance_state_factory(name="circulation")
    instance_state_factory(name="coordination")
    instance_state_factory(
        instance_state_id=bern_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS,
        name="correction",
    )

    case = be_instance.case

    for task in ["submit", "ebau-number"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_case_gr(
    gr_instance,
    caluma_admin_user,
    instance_state_factory,
    gr_distribution_settings,
    notification_template_factory,
):
    # this is needed so that simple workflow works
    notification_template_factory(slug="verfahrensablauf-fachstelle")
    notification_template_factory(slug="verfahrensablauf-uso")
    instance_state_factory(name="circulation")
    instance_state_factory(name="decision")
    instance_state_factory(
        instance_state_id=bern_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS,
        name="correction",
    )

    case = gr_instance.case

    for task in ["submit", "formal-exam"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_case_sz(
    sz_instance,
    caluma_admin_user,
    instance_state_factory,
    sz_distribution_settings,
    notification_template_factory,
):
    notification_template_factory(slug="einladung-zur-stellungnahme")

    instance_state_factory(name="circ")
    instance_state_factory(name="redac")

    case = sz_instance.case

    for task in ["submit", "complete-check"]:
        skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    return case


@pytest.fixture
def distribution_child_case_be(distribution_case_be, be_distribution_settings):
    return distribution_case_be.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def distribution_child_case_gr(distribution_case_gr, gr_distribution_settings):
    return distribution_case_gr.work_items.get(
        task_id=gr_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def distribution_child_case_sz(distribution_case_sz, sz_distribution_settings):
    return distribution_case_sz.work_items.get(
        task_id=sz_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def inquiry_factory_be(
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    service,
    service_factory,
):
    def factory(to_service=service_factory(), from_service=service, sent=False):
        return _inquiry_factory(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_be,
            distribution_settings=be_distribution_settings,
        )

    return factory


@pytest.fixture
def inquiry_factory_gr(
    caluma_admin_user,
    distribution_child_case_gr,
    gr_distribution_settings,
    service,
    service_factory,
):
    def factory(to_service=service_factory(), from_service=service, sent=False):
        return _inquiry_factory(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_gr,
            distribution_settings=gr_distribution_settings,
        )

    return factory


@pytest.fixture
def inquiry_factory_sz(
    caluma_admin_user,
    distribution_child_case_sz,
    sz_distribution_settings,
    service,
    service_factory,
):
    def factory(to_service=service_factory(), sent=False):
        return _inquiry_factory(
            to_service=to_service,
            from_service=service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_sz,
            distribution_settings=sz_distribution_settings,
        )

    return factory


@pytest.mark.freeze_time("2022-03-23")
def test_distribution_initial_state(
    db, distribution_child_case_be, be_distribution_settings, service
):
    create_inquiry = distribution_child_case_be.work_items.get(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"]
    )
    end_distribution = distribution_child_case_be.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_COMPLETE_TASK"]
    )
    init_distribution = distribution_child_case_be.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"]
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
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    service,
    service_factory,
):
    invited_service = service_factory()
    invited_subservice = service_factory(service_parent=service)

    service_inquiry = inquiry_factory_be(invited_service)
    subservice_inquiry = inquiry_factory_be(invited_subservice)

    for work_item in [service_inquiry, subservice_inquiry]:
        assert work_item.status == WorkItem.STATUS_SUSPENDED
        assert work_item.deadline.isoformat() == "2022-04-22T00:00:00+00:00"

    assert distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(invited_service.pk)],
    ).exists()
    assert distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    ).exists()

    # invited subservice should not have a create-inquiry work item
    assert not distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(invited_subservice.pk)],
    ).exists()


@pytest.mark.freeze_time("2022-01-01")
@pytest.mark.parametrize(
    "passed_deadline,passed_remark,expected_deadline,expected_remark",
    [
        (None, None, "2022-01-31", None),
        ("2022-01-13", "Test", "2022-01-13", "Test"),
    ],
)
def test_inquiry_default_values(
    db,
    distribution_child_case_be,
    service_factory,
    caluma_admin_user,
    be_distribution_settings,
    service,
    passed_deadline,
    passed_remark,
    expected_deadline,
    expected_remark,
):
    to_service = service_factory()

    create_work_item = distribution_child_case_be.work_items.get(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    )

    context = {"addressed_groups": [str(to_service.pk)], "answers": {}}

    if passed_deadline:
        context["answers"][
            be_distribution_settings["QUESTIONS"]["DEADLINE"]
        ] = passed_deadline

    if passed_remark:
        context["answers"][
            be_distribution_settings["QUESTIONS"]["REMARK"]
        ] = passed_remark

    complete_work_item(
        work_item=create_work_item,
        user=caluma_admin_user,
        context=context,
    )

    create_work_item.refresh_from_db()

    inquiry = create_work_item.succeeding_work_items.get(
        addressed_groups=[str(to_service.pk)],
        controlling_groups=[str(service.pk)],
        status=WorkItem.STATUS_SUSPENDED,
    )

    assert inquiry

    assert (
        inquiry.document.answers.get(
            question_id=be_distribution_settings["QUESTIONS"]["DEADLINE"]
        ).date.isoformat()
        == expected_deadline
    )

    if expected_remark:
        assert (
            inquiry.document.answers.get(
                question_id=be_distribution_settings["QUESTIONS"]["REMARK"]
            ).value
            == expected_remark
        )


@pytest.mark.freeze_time("2022-03-23")
@pytest.mark.parametrize("user__email", ["applicant@example.com"])
def test_send_inquiry(
    db,
    be_instance,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    mailoutbox,
    service_factory,
    work_item_factory,
    service,
):
    addressed_service = service_factory()
    work_item_factory(
        task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        case=distribution_child_case_be,
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    inquiry = inquiry_factory_be(to_service=addressed_service, sent=True)

    assert inquiry.status == WorkItem.STATUS_READY
    assert inquiry.deadline.isoformat() == "2022-04-22T00:00:00+00:00"

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == "circulation"
    assert (
        distribution_child_case_be.work_items.get(
            task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"],
        ).status
        == WorkItem.STATUS_COMPLETED
    )
    assert (
        distribution_child_case_be.work_items.get(
            task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        ).status
        == WorkItem.STATUS_CANCELED
    )

    assert len(mailoutbox) == 2
    # mail to applicant, configured in simple workflow
    assert mailoutbox[0].to[0] == "applicant@example.com"
    assert mailoutbox[1].to[0] == addressed_service.email


@pytest.mark.freeze_time("2022-03-23")
def test_send_inquiry_gr(
    db,
    gr_instance,
    distribution_child_case_gr,
    inquiry_factory_gr,
    mailoutbox,
    service_factory,
    group_factory,
    work_item_factory,
    service,
    settings,
):
    settings.APPLICATION_NAME = "kt_gr"
    addressed_service = service_factory(service_group__name="uso")
    work_item_factory(
        task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
        case=distribution_child_case_gr,
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    inquiry_factory_gr(to_service=addressed_service, sent=True)

    gr_instance.refresh_from_db()

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to[0] == addressed_service.email


@pytest.mark.freeze_time("2022-03-23")
@pytest.mark.parametrize("user__email", ["applicant@example.com"])
def test_do_not_send_inquiry_in_correction(
    db,
    caluma_admin_user,
    be_instance,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    mailoutbox,
    mocker,
    service_factory,
    instance_state_factory,
    service,
    settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    instance_state_correction = instance_state_factory(name="correction")
    mocker.patch(
        "camac.constants.kt_bern.INSTANCE_STATE_CORRECTION_IN_PROGRESS",
        instance_state_correction.pk,
    )

    addressed_service1 = service_factory()
    addressed_service2 = service_factory()

    inquiry1 = inquiry_factory_be(
        to_service=addressed_service1, from_service=service, sent=True
    )
    inquiry2 = inquiry_factory_be(
        to_service=addressed_service2, from_service=addressed_service1, sent=True
    )
    inquiry3 = inquiry_factory_be(
        to_service=addressed_service2, from_service=addressed_service1, sent=False
    )

    assert inquiry1.status == WorkItem.STATUS_READY
    assert inquiry2.status == WorkItem.STATUS_READY
    assert inquiry3.status == WorkItem.STATUS_SUSPENDED
    assert len(mailoutbox) == 3
    mailoutbox.clear()

    # dossier correction
    suspend_case(be_instance.case, caluma_admin_user)

    be_instance.instance_state = instance_state_correction
    be_instance.save()

    be_instance.refresh_from_db()
    inquiry1.refresh_from_db()
    inquiry2.refresh_from_db()
    inquiry3.refresh_from_db()

    assert inquiry1.status == WorkItem.STATUS_SUSPENDED
    assert inquiry2.status == WorkItem.STATUS_SUSPENDED
    assert inquiry3.status == WorkItem.STATUS_SUSPENDED
    assert len(mailoutbox) == 0

    # finish dossier correction
    resume_case(be_instance.case, caluma_admin_user)

    be_instance.refresh_from_db()
    inquiry1.refresh_from_db()
    inquiry2.refresh_from_db()
    inquiry3.refresh_from_db()

    assert inquiry1.status == WorkItem.STATUS_READY
    assert inquiry2.status == WorkItem.STATUS_READY
    assert inquiry3.status == WorkItem.STATUS_SUSPENDED
    assert len(mailoutbox) == 0


@pytest.mark.freeze_time("2022-03-23")
@pytest.mark.parametrize("service__email", ["service@example.com"])
@pytest.mark.parametrize(
    "has_multiple_inquiries",
    [True, False],
)
@pytest.mark.parametrize(
    "is_lead_authority",
    [True, False],
)
def test_complete_inquiry(
    db,
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    mailoutbox,
    service,
    has_multiple_inquiries,
    work_item_factory,
    service_factory,
    is_lead_authority,
):
    service1 = service_factory()
    to_service = service if is_lead_authority else service1
    from_service = service1 if is_lead_authority else service

    if is_lead_authority:
        inquiry_factory_be(sent=True, to_service=service1)

    inquiry1 = inquiry_factory_be(
        sent=True, from_service=from_service, to_service=to_service
    )

    inquiry2 = (
        inquiry_factory_be(sent=True, from_service=from_service, to_service=to_service)
        if has_multiple_inquiries
        else None
    )

    addressed_check_work_item = work_item_factory(
        task_id=be_distribution_settings["INQUIRY_CHECK_TASK"],
        case=inquiry1.case,
        status=WorkItem.STATUS_READY,
        addressed_groups=inquiry1.addressed_groups,
        deadline=now(),
        child_case=None,
    )

    addressed_redo_work_item = work_item_factory(
        task_id=be_distribution_settings["INQUIRY_REDO_TASK"],
        case=inquiry1.case,
        status=WorkItem.STATUS_READY,
        addressed_groups=inquiry1.addressed_groups,
        child_case=None,
    )

    addressed_create_work_item = inquiry1.case.work_items.get(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=inquiry1.addressed_groups,
    )

    for question, value in [
        ("inquiry-answer-status", "inquiry-answer-status-positive"),
        ("inquiry-answer-statement", "Stellungnahme Test"),
        ("inquiry-answer-ancillary-clauses", "Nebenbestimmungen Test"),
    ]:
        save_answer(
            question=Question.objects.get(pk=question),
            document=inquiry1.child_case.document,
            value=value,
            user=caluma_admin_user,
        )

    mailoutbox.clear()

    complete_work_item(
        work_item=inquiry1.child_case.work_items.first(), user=caluma_admin_user
    )

    addressed_check_work_item.refresh_from_db()
    addressed_redo_work_item.refresh_from_db()
    addressed_create_work_item.refresh_from_db()

    assert addressed_check_work_item.status == WorkItem.STATUS_COMPLETED

    if has_multiple_inquiries or is_lead_authority:
        assert addressed_redo_work_item.status == WorkItem.STATUS_READY
        assert addressed_create_work_item.status == WorkItem.STATUS_READY
    else:
        assert addressed_redo_work_item.status == WorkItem.STATUS_CANCELED
        assert addressed_create_work_item.status == WorkItem.STATUS_CANCELED

    inquiry1.refresh_from_db()

    check_inquiries_work_items = distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )

    check_distribution_work_items = distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )

    if not is_lead_authority:
        assert check_inquiries_work_items.exists() != has_multiple_inquiries
        assert check_distribution_work_items.exists() != has_multiple_inquiries

    assert inquiry1.child_case.status == Case.STATUS_COMPLETED
    assert inquiry1.status == WorkItem.STATUS_COMPLETED

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to[0] == (
        service1.email if is_lead_authority else service.email
    )

    if has_multiple_inquiries:
        save_answer(
            question=Question.objects.get(pk="inquiry-answer-status"),
            document=inquiry2.child_case.document,
            value="inquiry-answer-status-negative",
            user=caluma_admin_user,
        )

        complete_work_item(
            work_item=inquiry2.child_case.work_items.first(), user=caluma_admin_user
        )

        if not is_lead_authority:
            assert check_inquiries_work_items.exists()
            assert check_distribution_work_items.exists()

        addressed_redo_work_item.refresh_from_db()
        addressed_create_work_item.refresh_from_db()

        if not is_lead_authority:
            assert addressed_redo_work_item.status == WorkItem.STATUS_CANCELED
            assert addressed_create_work_item.status == WorkItem.STATUS_CANCELED
        else:
            assert addressed_redo_work_item.status == WorkItem.STATUS_READY
            assert addressed_create_work_item.status == WorkItem.STATUS_READY


def test_complete_distribution(
    db,
    be_instance,
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    mailoutbox,
    service_factory,
    work_item_factory,
):
    service = service_factory()

    draft_inquiry = inquiry_factory_be()  # draft - will be canceled
    sent_inquiry = inquiry_factory_be(
        to_service=service, sent=True
    )  # sent - will be skipped

    check_distribution = work_item_factory(
        task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        case=distribution_child_case_be,
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
        child_case=None,
    )

    assert (
        distribution_child_case_be.work_items.filter(
            status=WorkItem.STATUS_READY
        ).count()
        == 6  # 1x complete-distribution, 3x create-inquiry, 1x inquiry, 1x check-distribution
    )
    assert (
        distribution_child_case_be.work_items.filter(
            status=WorkItem.STATUS_SUSPENDED
        ).count()
        == 1  # 1x inquiry
    )

    mailoutbox.clear()

    complete_work_item(
        work_item=distribution_child_case_be.work_items.get(
            task_id=be_distribution_settings["DISTRIBUTION_COMPLETE_TASK"],
            status=WorkItem.STATUS_READY,
        ),
        user=caluma_admin_user,
    )

    draft_inquiry.refresh_from_db()
    sent_inquiry.refresh_from_db()
    check_distribution.refresh_from_db()

    assert draft_inquiry.status == WorkItem.STATUS_CANCELED
    assert sent_inquiry.status == WorkItem.STATUS_SKIPPED
    assert check_distribution.status == WorkItem.STATUS_COMPLETED

    assert (
        distribution_child_case_be.work_items.filter(
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED]
        ).count()
        == 0
    )

    distribution_child_case_be.refresh_from_db()

    assert distribution_child_case_be.status == Case.STATUS_COMPLETED
    assert (
        distribution_child_case_be.parent_work_item.status == WorkItem.STATUS_COMPLETED
    )

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == "coordination"

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to[0] == service.email


@pytest.mark.parametrize("has_inquiries", [True, False])
def test_distribution_complete_history(
    db,
    be_instance,
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    has_inquiries,
    mocker,
):
    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    be_distribution_settings["HISTORY"] = {
        "COMPLETE_DISTRIBUTION": "complete",
        "SKIP_DISTRIBUTION": "skip",
    }

    # draft will be canceled, therefore it will be excluded
    inquiry_factory_be()

    if has_inquiries:
        inquiry_factory_be(sent=True)

    complete_work_item(
        work_item=distribution_child_case_be.work_items.get(
            task_id=be_distribution_settings["DISTRIBUTION_COMPLETE_TASK"],
            status=WorkItem.STATUS_READY,
        ),
        user=caluma_admin_user,
    )

    if has_inquiries:
        assert be_instance.history.last().get_trans_attr("title") == "complete"
    else:
        assert be_instance.history.last().get_trans_attr("title") == "skip"


def test_reopen_distribution(
    db,
    be_instance,
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    service_factory,
    service,
    instance_state_factory,
    task_factory,
):
    instance_state_distribution = instance_state_factory()

    be_distribution_settings["INSTANCE_STATE_DISTRIBUTION"] = (
        instance_state_distribution.name
    )
    be_distribution_settings["HISTORY"] = {"REDO_DISTRIBUTION": "reopen"}
    be_distribution_settings["REDO_DISTRIBUTION"] = {
        "CREATE_TASKS": [task_factory().slug]
    }

    service_with_sent_inquiry = service_factory()
    service_with_unsent_inquiry = service_factory()
    subservice_with_sent_inquiry = service_factory(
        service_parent=service_with_sent_inquiry
    )

    inquiry_factory_be(to_service=service_with_sent_inquiry, sent=True)
    inquiry_factory_be(to_service=service_with_unsent_inquiry)
    inquiry_factory_be(to_service=subservice_with_sent_inquiry, sent=True)

    complete_distribution = distribution_child_case_be.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_COMPLETE_TASK"]
    )

    # complete distribution to create proper workflow status for reopening the
    # distribution again
    complete_work_item(work_item=complete_distribution, user=caluma_admin_user)

    distribution_child_case_be.refresh_from_db()
    be_instance.refresh_from_db()

    distribution = be_instance.case.work_items.get(
        task_id=be_distribution_settings["DISTRIBUTION_TASK"]
    )
    decision = be_instance.case.work_items.get(task_id="decision")

    assert distribution_child_case_be.status == Case.STATUS_COMPLETED
    assert distribution.status == WorkItem.STATUS_COMPLETED
    assert decision.status == WorkItem.STATUS_READY
    assert be_instance.instance_state.name == "coordination"

    # redo distribution
    redo_work_item(work_item=distribution, user=caluma_admin_user)

    distribution_child_case_be.refresh_from_db()
    distribution.refresh_from_db()
    complete_distribution.refresh_from_db()
    decision.refresh_from_db()
    be_instance.refresh_from_db()

    assert distribution_child_case_be.status == Case.STATUS_RUNNING
    assert distribution.status == WorkItem.STATUS_READY
    assert complete_distribution.status == WorkItem.STATUS_READY
    assert decision.status == WorkItem.STATUS_REDO
    assert be_instance.instance_state == instance_state_distribution

    # the service that reopened the distribution should have a work item to
    # create a new inquiry
    assert distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the service that had an inquiry in the previous distribution run should
    # have a work item to create a new inquiry
    assert distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service_with_sent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the service that had an inquiry that was unsent in the previous
    # distribution run should **not** have a work item to create a new inquiry
    # since the previous inquiry was canceled on completion of the distribution
    assert not distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(service_with_unsent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # the subservice that had a sent inquiry should **not** have a work item to
    # create a new inquiry
    assert not distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups__contains=[str(subservice_with_sent_inquiry.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # A check-distribution work-item should have been recreated or redone
    # for the services that reopened the distribution
    assert distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        addressed_groups__contains=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    ).exists()

    # Any configured, necessary work-items in the distribution case should
    # be re-created
    assert distribution_child_case_be.family.work_items.filter(
        task_id=be_distribution_settings["REDO_DISTRIBUTION"]["CREATE_TASKS"][0],
        addressed_groups__contains=[str(distribution.addressed_groups[0])],
        status=WorkItem.STATUS_READY,
        previous_work_item=distribution.previous_work_item,
    ).exists()

    assert be_instance.history.last().get_trans_attr("title") == "reopen"


def test_reopen_inquiry(
    db,
    caluma_admin_user,
    sz_distribution_settings,
    inquiry_factory_sz,
):
    inquiry = inquiry_factory_sz(sent=True)

    skip_work_item(
        work_item=inquiry.child_case.work_items.get(
            task_id=sz_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
        ),
        user=caluma_admin_user,
    )
    complete_work_item(
        work_item=inquiry.child_case.work_items.get(
            task_id=sz_distribution_settings["INQUIRY_ANSWER_CHECK_TASK"]
        ),
        user=caluma_admin_user,
    )

    inquiry.refresh_from_db()

    assert inquiry.status == WorkItem.STATUS_COMPLETED

    # redo inquiry
    redo_work_item(work_item=inquiry, user=caluma_admin_user)

    inquiry.refresh_from_db()

    assert inquiry.status == WorkItem.STATUS_READY

    assert (
        inquiry.child_case.work_items.get(
            task_id=sz_distribution_settings["INQUIRY_ANSWER_CHECK_TASK"]
        ).status
        == WorkItem.STATUS_CANCELED
    )

    assert (
        inquiry.child_case.work_items.get(
            task_id=sz_distribution_settings["INQUIRY_ANSWER_REVISE_TASK"]
        ).status
        == WorkItem.STATUS_COMPLETED
    )

    assert (
        inquiry.child_case.work_items.get(
            task_id=sz_distribution_settings["INQUIRY_ANSWER_ALTER_TASK"]
        ).status
        == WorkItem.STATUS_READY
    )


@pytest.mark.parametrize(
    "is_subservice,inquiry_count,has_multiple_create_work_items",
    [
        # Service has only one inquiry, create-inquiry should be canceled
        # immediately.
        (False, 1, False),
        # Service has two inquiries, create-inquiry should be canceled after the
        # last inquiry is canceled.
        (False, 2, False),
        # Subservice has only one inquiry, no create-inquiry work item should
        # exist since those don't get created for subservices.
        (True, 1, False),
        # Service has only one inquiry but more than one create-inquiry work
        # items. This should raise an error since this should technically not
        # happen.
        (False, 1, True),
    ],
)
def test_cancel_inquiry(
    db,
    caluma_admin_user,
    distribution_child_case_be,
    be_distribution_settings,
    inquiry_factory_be,
    service_factory,
    work_item_factory,
    is_subservice,
    inquiry_count,
    has_multiple_create_work_items,
):
    service = service_factory(
        service_parent=service_factory() if is_subservice else None
    )

    inquiries = [inquiry_factory_be(to_service=service) for x in range(inquiry_count)]

    create_inquiry_work_items = distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        addressed_groups=[str(service.pk)],
    )

    if is_subservice:
        assert not create_inquiry_work_items.exists()
    else:
        assert create_inquiry_work_items.filter(status=WorkItem.STATUS_READY).exists()

    # provoke error
    if has_multiple_create_work_items:
        work_item_factory(
            case=distribution_child_case_be,
            addressed_groups=[str(service.pk)],
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
        )

    for i, inquiry in enumerate(inquiries, start=1):
        if has_multiple_create_work_items:
            with pytest.raises(RuntimeError):
                cancel_work_item(work_item=inquiry, user=caluma_admin_user)
        else:
            cancel_work_item(work_item=inquiry, user=caluma_admin_user)

            if is_subservice:
                assert not create_inquiry_work_items.exists()
            else:
                assert create_inquiry_work_items.filter(
                    status=(
                        WorkItem.STATUS_CANCELED
                        if i == len(inquiries)
                        else WorkItem.STATUS_READY
                    )
                ).exists()


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("deadline,success", [("2022-10-24", True), (None, False)])
def test_sync_inquiry_deadline(
    db,
    be_distribution_settings,
    caluma_admin_schema_executor,
    deadline,
    inquiry_factory_be,
    mocker,
    success,
):
    mocker.patch(
        "camac.caluma.extensions.permissions.CustomPermission.has_camac_edit_permission",
        return_value=True,
    )
    be_distribution_settings["SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS"] = {
        f'{be_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]}': {
            "TIME_DELTA": timedelta(days=-5)
        }
    }

    inquiry = inquiry_factory_be(sent=True)

    variables = {
        "input": {
            "document": str(inquiry.document.pk),
            "question": be_distribution_settings["QUESTIONS"]["DEADLINE"],
            "value": deadline,
        }
    }

    if not deadline:
        del variables["input"]["value"]

    result = caluma_admin_schema_executor(
        """
        mutation($input: SaveDocumentDateAnswerInput!) {
            saveDocumentDateAnswer(input: $input) {
                clientMutationId
            }
        }
        """,
        variables=variables,
    )

    if not success:
        assert result.errors
        assert "Deadline is required" in result.errors[0].message
    else:
        assert not result.errors

        inquiry.refresh_from_db()

        assert inquiry.deadline.isoformat() == "2022-10-24T00:00:00+00:00"
        assert (
            inquiry.document.answers.get(
                question_id=be_distribution_settings["QUESTIONS"]["DEADLINE"]
            ).date.isoformat()
            == "2022-10-24"
        )

        assert (
            inquiry.child_case.work_items.filter(
                task_id=be_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
            )
            .first()
            .deadline.isoformat()
            == "2022-10-19T00:00:00+00:00"
        )
