import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import DynamicOption, Question
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from caluma.caluma_workflow.models import Case, WorkItem

from camac.caluma.tests.test_distribution_workflow import (  # noqa: F401
    distribution_case_be,
    distribution_child_case_be,
    inquiry_factory_be,
)
from camac.constants.kt_bern import (
    DECISION_TYPE_BAUBEWILLIGUNGSFREI,
    DECISION_TYPE_BUILDING_PERMIT,
    DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
    DECISION_TYPE_PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION,
    DECISIONS_ABGELEHNT,
    DECISIONS_ABGESCHRIEBEN,
    DECISIONS_BEWILLIGT,
    VORABKLAERUNG_DECISIONS_BEWILLIGT,
    VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT,
    VORABKLAERUNG_DECISIONS_NEGATIVE,
)


@pytest.mark.parametrize(
    "workflow_id,decision,decision_type,expected_case_status",
    [
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_BUILDING_PERMIT,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            DECISIONS_ABGESCHRIEBEN,
            DECISION_TYPE_BUILDING_PERMIT,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            Case.STATUS_RUNNING,
        ),
        (
            "preliminary-clarification",
            VORABKLAERUNG_DECISIONS_BEWILLIGT,
            None,
            Case.STATUS_COMPLETED,
        ),
        (
            "preliminary-clarification",
            VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT,
            None,
            Case.STATUS_COMPLETED,
        ),
        (
            "preliminary-clarification",
            VORABKLAERUNG_DECISIONS_NEGATIVE,
            None,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            DECISIONS_ABGESCHRIEBEN,
            DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BAUBEWILLIGUNGSFREI,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            DECISIONS_ABGESCHRIEBEN,
            DECISION_TYPE_PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION,
            Case.STATUS_RUNNING,
        ),
    ],
)
def test_dynamic_task_after_decision(
    db,
    caluma_admin_user,
    decision_factory,
    decision_type,
    decision,
    expected_case_status,
    instance_state_factory,
    instance_with_case,
    instance,
    service_factory,
    workflow_id,
):
    case = instance_with_case(instance=instance, workflow=workflow_id).case

    instance_state_factory(name="coordination")
    instance_state_factory(name="finished")
    instance_state_factory(name="sb1")
    instance_state_factory(name="evaluated")

    service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Burgdorf",
    )
    service = service_factory(
        service_group__name="construction-control",
        trans__name="Baukontrolle Burgdorf",
        trans__language="de",
    )
    dynamic_option = DynamicOption.objects.create(
        document=case.document,
        question_id="gemeinde",
        slug=str(service.pk),
        label="Musterdorf",
    )
    case.document.answers.create(question_id="gemeinde", value=dynamic_option.slug)

    for task_id, fn in [
        ("submit", complete_work_item),
        ("ebau-number", complete_work_item),
        ("distribution", skip_work_item),
        ("decision", complete_work_item),
    ]:
        if task_id == "decision":
            decision_factory(decision=decision, decision_type=decision_type)

        fn(case.work_items.get(task_id=task_id), caluma_admin_user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id="sb1").exists()
        assert case.instance.instance_state.name == "sb1"


@pytest.mark.parametrize(
    "is_lead_authority",
    [False, True],
)
def test_dynamic_task_after_inquiries_completed(
    db,
    caluma_admin_user,
    distribution_child_case_be,  # noqa: F811
    be_distribution_settings,  # noqa: F811
    inquiry_factory_be,  # noqa: F811
    service,
    service_factory,
    is_lead_authority,
):
    invited_service = service_factory()
    if is_lead_authority:
        inquiry1 = inquiry_factory_be(sent=True)
        inquiry2 = inquiry_factory_be(sent=True)
    else:
        inquiry_factory_be(to_service=invited_service, sent=True)
        inquiry1 = inquiry_factory_be(from_service=invited_service, sent=True)
        inquiry2 = inquiry_factory_be(from_service=invited_service, sent=True)

    def answer_inquiry(inquiry):
        save_answer(
            question=Question.objects.get(pk="inquiry-answer-status"),
            document=inquiry.child_case.document,
            value="inquiry-answer-status-negative",
            user=caluma_admin_user,
        )

        complete_work_item(
            work_item=inquiry.child_case.work_items.first(), user=caluma_admin_user
        )

    check_inquiries_work_items = distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["INQUIRY_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk if is_lead_authority else invited_service.pk)],
    )

    check_distribution_work_items = distribution_child_case_be.work_items.filter(
        task_id=be_distribution_settings["DISTRIBUTION_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk if is_lead_authority else invited_service.pk)],
    )

    answer_inquiry(inquiry1)

    # No check-distribution or check-inquiries work-item should be created
    # since there are pending controlling inquiries left.
    assert check_inquiries_work_items.count() == 0
    assert check_distribution_work_items.count() == 0

    answer_inquiry(inquiry2)

    # No pending controlling inquiries left, should create a
    # check-inquiries work-item and an check-distribution
    # (only for lead authority)
    assert check_inquiries_work_items.count() == 1
    assert check_distribution_work_items.count() == (1 if is_lead_authority else 0)

    inquiry3 = inquiry_factory_be(sent=True)

    # Check-distribution is canceled when new pending controlling
    # work-items appear
    assert check_inquiries_work_items.count() == 1
    assert check_distribution_work_items.count() == 0

    answer_inquiry(inquiry3)

    # Should create check-distribution work-item and not create another
    # check-inquiries work-item as there is already an existing one.
    assert check_inquiries_work_items.count() == 1
    assert check_distribution_work_items.count() == (1 if is_lead_authority else 0)
