import pytest
from caluma.caluma_form.models import DynamicOption, Form
from caluma.caluma_workflow.api import complete_work_item, skip_work_item, start_case
from caluma.caluma_workflow.models import Case, Workflow, WorkItem

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
    caluma_publication,
    docx_decision_factory,
    instance,
    workflow_id,
    decision,
    decision_type,
    circulation,
    expected_case_status,
    instance_state_factory,
    service_factory,
):
    docx_decision_factory(
        decision=decision, decision_type=decision_type, instance=instance
    )

    case = start_case(
        workflow=Workflow.objects.get(pk=workflow_id),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    instance_state_factory(name="coordination")
    instance_state_factory(name="finished")
    instance_state_factory(name="sb1")
    instance_state_factory(name="evaluated")

    dynamic_option = DynamicOption.objects.create(
        document=case.document, question_id="gemeinde", slug="1", label="Musterdorf"
    )
    case.document.answers.create(question_id="gemeinde", value=dynamic_option.slug)
    service_factory(pk=1, service_group__name="construction-control")

    for task_id in [
        "submit",
        "ebau-number",
        "skip-circulation",
        "decision",
    ]:
        complete_work_item(case.work_items.get(task_id=task_id), caluma_admin_user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id="sb1").exists()
        assert case.instance.instance_state.name == "sb1"


@pytest.mark.parametrize(
    "has_circulation,instance_state__name,expected_tasks",
    [
        (False, "circulation_init", ["skip-circulation", "init-circulation"]),
        (False, "circulation", ["start-circulation", "start-decision"]),
        (
            True,
            "circulation",
            ["start-circulation", "check-activation", "start-decision"],
        ),
    ],
)
def test_dynamic_task_after_circulation(
    db,
    caluma_admin_user,
    caluma_publication,
    instance,
    instance_state,
    circulation_factory,
    has_circulation,
    expected_tasks,
):
    if has_circulation:
        circulation_factory(instance=instance)

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    for task_id in ["submit", "ebau-number", "init-circulation", "circulation"]:
        skip_work_item(case.work_items.get(task_id=task_id), caluma_admin_user)

    for task in expected_tasks:
        assert case.work_items.filter(
            task_id=task, status=WorkItem.STATUS_READY
        ).exists()
