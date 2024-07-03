import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.factories import FormFactory
from caluma.caluma_form.models import DynamicOption, Question
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from caluma.caluma_workflow.models import Case, WorkItem

from camac.caluma.extensions.dynamic_tasks import CustomDynamicTasks
from camac.caluma.tests.test_distribution_workflow import (  # noqa: F401
    distribution_case_be,
    distribution_child_case_be,
    inquiry_factory_be,
)


@pytest.mark.parametrize(
    "workflow_id,decision,decision_type,involve_geometer,expected_case_status",
    [
        (
            "building-permit",
            "REJECTED",
            "BUILDING_PERMIT",
            True,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            "DEPRECIATED",
            "BUILDING_PERMIT",
            True,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            "APPROVED",
            "BUILDING_PERMIT",
            True,
            Case.STATUS_RUNNING,
        ),
        (
            "preliminary-clarification",
            "POSITIVE",
            None,
            True,
            Case.STATUS_COMPLETED,
        ),
        (
            "preliminary-clarification",
            "POSITIVE_WITH_RESERVATION",
            None,
            False,
            Case.STATUS_COMPLETED,
        ),
        (
            "preliminary-clarification",
            "NEGATIVE",
            None,
            True,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            "REJECTED",
            "CONSTRUCTION_TEE_WITH_RESTORATION",
            False,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            "DEPRECIATED",
            "CONSTRUCTION_TEE_WITH_RESTORATION",
            True,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            "APPROVED",
            "BUILDING_PERMIT_FREE",
            True,
            Case.STATUS_COMPLETED,
        ),
        (
            "building-permit",
            "REJECTED",
            "PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION",
            False,
            Case.STATUS_RUNNING,
        ),
        (
            "building-permit",
            "DEPRECIATED",
            "PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION",
            True,
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
    involve_geometer,
    expected_case_status,
    instance_state_factory,
    instance_with_case,
    instance,
    service_factory,
    workflow_id,
    settings,
    application_settings,
    be_decision_settings,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
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
            decision = decision_factory(
                decision=be_decision_settings["ANSWERS"]["DECISION"][decision],
                decision_type=(
                    be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][decision_type]
                    if decision_type
                    else None
                ),
                decision_geometer=(
                    "decision-geometer-yes"
                    if involve_geometer
                    else "decision-geometer-no"
                ),
            )

        fn(case.work_items.get(task_id=task_id), caluma_admin_user)

    case.refresh_from_db()

    assert case.status == expected_case_status

    if case.status == Case.STATUS_RUNNING:
        assert case.work_items.filter(task_id="sb1").exists()
        assert case.instance.instance_state.name == "sb1"

    geometer_work_item_exists = case.work_items.filter(task_id="geometer").exists()
    assert (
        geometer_work_item_exists
        if involve_geometer and case.status == Case.STATUS_RUNNING
        else not geometer_work_item_exists
    )


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
    be_ech0211_settings,
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


@pytest.mark.parametrize(
    "is_appeal,expected_tasks",
    [
        (
            False,
            {
                "distribution",
                "audit",
                "publication",
                "fill-publication",
                "information-of-neighbors",
                "legal-submission",
            },
        ),
        (
            True,
            {
                "distribution",
                "audit",
                "publication",
                "fill-publication",
                "information-of-neighbors",
                "legal-submission",
                "appeal",
            },
        ),
    ],
)
def test_dynamic_task_after_ebau_number(
    db,
    caluma_admin_user,
    expected_tasks,
    is_appeal,
    case_factory,
):
    case = case_factory(meta={"is-appeal": True} if is_appeal else {})

    tasks = set(
        CustomDynamicTasks().resolve_after_ebau_number(
            case, caluma_admin_user, None, None
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "is_appeal,form_slug,expected_tasks",
    [
        (
            False,
            "main-form",
            {"create-manual-workitems", "formal-exam", "init-additional-demand"},
        ),
        (
            True,
            "main-form",
            {"create-manual-workitems", "appeal", "decision"},
        ),
        (
            False,
            "voranfrage",
            {"create-manual-workitems", "distribution"},
        ),
        (
            False,
            "meldung",
            {"create-manual-workitems", "decision"},
        ),
    ],
)
def test_dynamic_task_after_submit(
    db,
    caluma_admin_user,
    expected_tasks,
    is_appeal,
    case_factory,
    form_slug,
):
    case = case_factory(
        meta={"is-appeal": True} if is_appeal else {},
        document__form=FormFactory(slug=form_slug),
    )

    tasks = set(
        CustomDynamicTasks().resolve_after_submit(case, caluma_admin_user, None, None)
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "decision,expected_tasks",
    [
        ("ACCEPTED", set()),
        ("REJECTED", {"fill-additional-demand"}),
    ],
)
def test_dynamic_task_after_check_additional_demand(
    db,
    additional_demand_settings,
    answer_factory,
    decision,
    expected_tasks,
    work_item_factory,
):
    answer = answer_factory(
        question__slug=additional_demand_settings["QUESTIONS"]["DECISION"],
        value=additional_demand_settings["ANSWERS"]["DECISION"][decision],
    )

    work_item = work_item_factory(document=answer.document)

    tasks = set(
        CustomDynamicTasks().resolve_after_check_additional_demand(
            None, None, work_item, None
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "passed_addressed_groups,groups_with_existing,create_additional_demand",
    [
        (["1"], ["1"], False),
        (["1", "2"], ["1", "2"], False),
        (["1", "2"], ["1", "1"], True),  # this case shouldn't happen but it may
        (["1", "2"], ["1"], True),
    ],
)
def test_dynamic_task_after_create_inquiry(
    db,
    additional_demand_settings,
    distribution_settings,
    work_item_factory,
    gr_instance,
    passed_addressed_groups,
    groups_with_existing,
    create_additional_demand,
):
    for group in groups_with_existing:
        work_item_factory(
            case=gr_instance.case,
            addressed_groups=[group],
            task_id=additional_demand_settings["CREATE_TASK"],
        )

    tasks = set(
        CustomDynamicTasks().resolve_after_create_inquiry(
            gr_instance.case, None, None, {"addressed_groups": passed_addressed_groups}
        )
    )

    expected_tasks = set(
        [
            distribution_settings["INQUIRY_CREATE_TASK"],
            distribution_settings["INQUIRY_TASK"],
        ]
    )

    if create_additional_demand:
        expected_tasks.add(additional_demand_settings["CREATE_TASK"])

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "task_id,has_rejection_answer,is_bab,expected_tasks",
    [
        ("formal-exam", True, False, ["reject"]),
        ("material-exam", True, False, ["reject"]),
        ("formal-exam", False, False, ["material-exam"]),
        (
            "material-exam",
            False,
            False,
            ["distribution", "publication", "fill-publication", "objections"],
        ),
        (
            "material-exam",
            False,
            True,
            [
                "distribution",
                "publication",
                "fill-publication",
                "objections",
                "material-exam-bab",
            ],
        ),
    ],
)
def test_dynamic_task_after_exam(
    db,
    answer_factory,
    expected_tasks,
    has_rejection_answer,
    is_bab,
    so_instance,
    so_rejection_settings,
    task_id,
    work_item_factory,
):
    work_item = work_item_factory(task_id=task_id, case=so_instance.case)

    if has_rejection_answer:
        answer_factory(
            document=work_item.document,
            question__slug=so_rejection_settings["WORK_ITEM"]["ON_ANSWER"][task_id][0],
            value=so_rejection_settings["WORK_ITEM"]["ON_ANSWER"][task_id][1],
        )

    if is_bab:
        work_item.case.meta.update({"is-bab": True})
        work_item.case.save()

    assert (
        CustomDynamicTasks().resolve_after_exam(so_instance.case, None, work_item, None)
        == expected_tasks
    )


@pytest.mark.parametrize(
    "perform_cadastral_survey,expected_tasks",
    [
        (True, ["cadastral-survey"]),
        (False, []),
    ],
)
def test_dynamic_task_after_check_sb2(
    db,
    answer_factory,
    expected_tasks,
    perform_cadastral_survey,
    be_instance,
    work_item_factory,
    caluma_admin_user,
):
    geometer_work_item = work_item_factory(
        task_id="geometer", case=be_instance.case, child_case=None
    )
    answer_factory(
        document=geometer_work_item.document,
        question__slug="geometer-beurteilung-notwendigkeit-vermessung",
        value=(
            "geometer-beurteilung-notwendigkeit-vermessung-notwendig"
            if perform_cadastral_survey
            else "geometer-beurteilung-notwendigkeit-vermessung-nicht-notwendig"
        ),
    )

    complete_work_item(geometer_work_item, user=caluma_admin_user)
    work_item = work_item_factory(task_id="check-sb2", case=be_instance.case)

    assert (
        CustomDynamicTasks().resolve_after_check_sb2(
            be_instance.case, None, work_item, None
        )
        == expected_tasks
    )


@pytest.mark.parametrize(
    "answer1,answer2,expected_tasks",
    [
        (
            "decision-task-nachfuehrungsgeometer-ja",
            "decision-task-gebaudeschaetzung-ja",
            ["geometer", "gebaeudeschaetzung"],
        ),
        (
            "decision-task-nachfuehrungsgeometer-nein",
            "decision-task-gebaudeschaetzung-nein",
            [],
        ),
    ],
)
def test_dynamic_task_after_decision_ur(
    db,
    work_item_factory,
    document_factory,
    question_factory,
    answer_factory,
    ur_instance,
    caluma_admin_user,
    expected_tasks,
    answer1,
    answer2,
):
    work_item = work_item_factory(
        case=ur_instance.case,
        task_id="decision",
    )
    work_item.document = document_factory()
    work_item.save()

    answer_factory(
        document=work_item.document,
        question=question_factory(slug="decision-task-nachfuehrungsgeometer"),
        value=answer1,
    )
    answer_factory(
        document=work_item.document,
        question=question_factory(slug="decision-task-gebaudeschaetzung"),
        value=answer2,
    )

    result = CustomDynamicTasks().resolve_after_decision_ur(
        ur_instance.case, caluma_admin_user, work_item, None
    )

    assert result == expected_tasks


@pytest.mark.parametrize(
    "answer,expected_tasks",
    [
        (
            "complete-check-vollstaendigkeitspruefung-incomplete",
            ["init-additional-demand"],
        ),
        ("complete-check-vollstaendigkeitspruefung-complete", []),
    ],
)
def test_dynamic_task_after_complete_check_ur(
    db,
    work_item_factory,
    document_factory,
    question_factory,
    answer_factory,
    ur_instance,
    caluma_admin_user,
    answer,
    expected_tasks,
):
    work_item = work_item_factory(
        case=ur_instance.case,
        task_id="decision",
    )
    work_item.document = document_factory()
    work_item.save()

    answer_factory(
        document=work_item.document,
        question=question_factory(slug="complete-check-vollstaendigkeitspruefung"),
        value=answer,
    )

    result = CustomDynamicTasks().resolve_after_complete_check_ur(
        ur_instance.case, caluma_admin_user, work_item, None
    )

    assert result == expected_tasks


@pytest.mark.parametrize(
    "needs_approval,is_approved,previous_task,selected_steps,expected_tasks",
    [
        (
            True,
            True,
            "construction-step-baufreigabe",
            [
                "construction-step-baufreigabe",
                "construction-step-kanalisationsabnahme",
                "construction-step-schnurgeruestabnahme",
            ],
            {
                "construction-step-kanalisationsabnahme-melden",
                "construction-step-schnurgeruestabnahme-melden",
            },
        ),
        (
            True,
            False,
            "construction-step-schnurgeruest-kontrollieren",
            [
                "construction-step-schnurgeruestabnahme",
            ],
            {
                "construction-step-schnurgeruestabnahme-melden",
            },
        ),
        (
            False,
            False,
            "construction-step-baubeginn-melden",
            [
                "construction-step-baubeginn",
                "construction-step-rohbauabnahme",
            ],
            {
                "construction-step-rohbauabnahme-melden",
            },
        ),
        (
            True,
            True,
            "construction-step-baufreigabe",
            [
                "construction-step-baufreigabe",
                "construction-step-schlussabnahme-gebaeude",
                "construction-step-schlussabnahme-projekt",
            ],
            {
                "construction-step-schlussabnahme-gebaeude-melden",
            },
        ),
        (
            True,
            True,
            "construction-step-baufreigabe",
            [
                "construction-step-baufreigabe",
            ],
            set(),
        ),
    ],
)
def test_dynamic_task_after_construction_step(
    db,
    caluma_admin_user,
    previous_task,
    expected_tasks,
    selected_steps,
    needs_approval,
    is_approved,
    sz_construction_monitoring_settings,
    construction_monitoring_initialized_case_sz,
    sz_instance,
    utils,
):
    plan_stage = construction_monitoring_initialized_case_sz.work_items.first()
    utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
    utils.add_answer(plan_stage.document, "construction-steps", selected_steps)
    complete_work_item(work_item=plan_stage, user=caluma_admin_user)

    previous_work_items = construction_monitoring_initialized_case_sz.work_items.filter(
        status=WorkItem.STATUS_READY
    )
    previous_work_item = previous_work_items.first()
    while previous_work_item.task_id != previous_task:
        previous_work_item.document.form.questions.update(is_required="False")
        complete_work_item(work_item=previous_work_item, user=caluma_admin_user)
        previous_work_item = previous_work_items.first()

    if needs_approval:
        question = previous_work_item.meta["construction-step"]["needs-approval"]
        answer = f"{question}-yes" if is_approved else f"{question}-no"
        utils.add_answer(previous_work_item.document, question, answer)

    tasks = set(
        CustomDynamicTasks().resolve_after_construction_step(
            construction_monitoring_initialized_case_sz,
            caluma_admin_user,
            previous_work_item,
            None,
        )
    )

    assert tasks == expected_tasks
