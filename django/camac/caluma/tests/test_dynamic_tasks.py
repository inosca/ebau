from unittest.mock import Mock

import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import DynamicOption, Question
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from caluma.caluma_workflow.models import Case, WorkItem

from camac.caluma.extensions.dynamic_tasks import CustomDynamicTasks
from camac.caluma.tests.test_distribution_workflow import (  # noqa: F401
    distribution_case_be,
    distribution_child_case_be,
    inquiry_factory_be,
)
from camac.conftest import yes_no
from camac.instance import domain_logic
from camac.tests.form_utils import FormUtils


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


@pytest.mark.freeze_time("2025-11-06 15:15:15+02:00")
@pytest.mark.parametrize(
    "is_deactivated,should_continue_after_decision,involve_geometer,expected_tasks",
    [
        (
            False,
            True,
            True,
            ["sb1", "create-manual-workitems", "create-publication", "geometer"],
        ),
        (False, False, False, []),
        (True, True, True, []),
        (True, False, False, []),
    ],
)
def test_dynamic_task_after_decision_with_check_prevent_submit(
    db,
    mocker,
    application_settings,
    be_instance,
    be_decision_settings,
    decision_factory,
    instance_state_factory,
    instance_service_factory,
    instance_with_case,
    instance,
    service_factory,
    settings,
    is_deactivated,
    should_continue_after_decision,
    involve_geometer,
    expected_tasks,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    be_decision_settings["TASKS_AFTER_BUILDING_PERMIT_DECISION"] = [
        "sb1",
        "create-manual-workitems",
        "create-publication",
    ]

    instance_with_case(instance=instance, workflow="building-permit")

    service_municipality = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Burgdorf",
        meta={"deactivated-municipality-at": "2025-11-04T15:15:15+02:00"}
        if is_deactivated
        else {},
    )
    instance.instance_services.add(
        instance_service_factory(service=service_municipality)
    )

    decision = decision_factory(
        decision_geometer=(
            "decision-geometer-yes" if involve_geometer else "decision-geometer-no"
        ),
    )

    mocker.patch.object(
        domain_logic.DecisionLogic,
        "should_continue_after_decision",
        return_value=should_continue_after_decision,
    )

    custom_dynamic_task = CustomDynamicTasks()
    assert (
        custom_dynamic_task.resolve_after_decision(
            be_instance.case, None, decision, None
        )
        == expected_tasks
    )


@pytest.mark.parametrize(
    "construction_monitoring_enabled,positive_decision,form_id,expected_tasks",
    [
        (True, True, "baugesuch-v3", []),
        (True, True, "vorlaeufige-beurteilung-v3", []),
        (True, False, "baugesuch-v3", []),
        (True, False, "vorlaeufige-beurteilung-v3", []),
        (False, True, "baugesuch-v3", ["construction-acceptance"]),
        (False, True, "vorlaeufige-beurteilung-v3", []),
        (False, False, "baugesuch-v3", []),
        (False, False, "vorlaeufige-beurteilung-v3", []),
    ],
)
def test_after_decision_gr(
    mocker,
    db,
    set_application_gr,
    gr_construction_monitoring_settings,
    gr_instance,
    # parametrize
    construction_monitoring_enabled,
    positive_decision,
    form_id,
    expected_tasks,
    application_settings,
):
    application_settings["SHORT_NAME"] = "gr"
    gr_construction_monitoring_settings["ENABLED"] = construction_monitoring_enabled

    mocker.patch.object(
        domain_logic.DecisionLogic,
        "is_positive_decision",
        return_value=positive_decision,
    )
    gr_instance.case.document.form_id = form_id

    custom_dynamic_task = CustomDynamicTasks()
    assert (
        custom_dynamic_task.resolve_after_decision_gr(
            gr_instance.case, None, None, None
        )
        == expected_tasks
    )


@pytest.mark.parametrize(
    "afb_answered,afb_skipped,should_continue,expected_tasks",
    [
        (True, False, True, {"check-pa", "init-construction-monitoring"}),
        (False, True, True, {"check-pa", "init-construction-monitoring"}),
        (True, False, False, {"check-pa", "complete-instance"}),
        (False, False, True, {"init-construction-monitoring"}),
        (False, False, False, {"complete-instance"}),
    ],
)
def test_after_decision_ag(
    db,
    active_inquiry_factory,
    afb_answered,
    afb_skipped,
    ag_construction_monitoring_settings,
    ag_instance,
    expected_tasks,
    mocker,
    service_factory,
    should_continue,
):
    afb = service_factory(slug="afb")

    mocker.patch(
        "camac.instance.domain_logic.decision.DecisionLogic.should_continue_after_decision",
        return_value=should_continue,
    )

    if afb_answered or afb_skipped:
        active_inquiry_factory(
            ag_instance,
            afb,
            status=WorkItem.STATUS_COMPLETED
            if afb_answered
            else WorkItem.STATUS_SKIPPED,
        )

    assert (
        set(
            CustomDynamicTasks().resolve_after_decision_ag(
                ag_instance.case, None, None, None
            )
        )
        == expected_tasks
    )


@pytest.mark.parametrize("always_create_inquiry_check_work_item", [True, False])
@pytest.mark.parametrize(
    "is_lead_authority",
    [False, True],
)
def test_dynamic_task_after_inquiries_completed(
    db,
    caluma_admin_user,
    distribution_child_case_be,  # noqa: F811
    be_distribution_settings,
    inquiry_factory_be,  # noqa: F811
    service,
    service_factory,
    is_lead_authority,
    be_ech0211_settings,
    always_create_inquiry_check_work_item,
):
    be_distribution_settings["ALWAYS_CREATE_INQUIRY_CHECK_WORK_ITEM"] = (
        always_create_inquiry_check_work_item
    )

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
    if always_create_inquiry_check_work_item:
        assert check_inquiries_work_items.count() == 1
    else:
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
    caluma_case_factory,
):
    case = caluma_case_factory(meta={"is-appeal": True} if is_appeal else {})

    tasks = set(
        CustomDynamicTasks().resolve_after_ebau_number(
            case, caluma_admin_user, None, None
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "is_appeal,is_bab,form_slug,expected_tasks",
    [
        (
            False,
            False,
            "main-form",
            {"create-manual-workitems", "formal-exam", "init-additional-demand"},
        ),
        (
            False,
            True,
            "main-form",
            {
                "create-manual-workitems",
                "formal-exam",
                "init-additional-demand",
                "material-exam-bab",
            },
        ),
        (
            True,
            False,
            "main-form",
            {"create-manual-workitems", "appeal", "distribution"},
        ),
        (
            True,
            True,
            "main-form",
            {"create-manual-workitems", "appeal", "distribution", "material-exam-bab"},
        ),
        (
            False,
            False,
            "voranfrage",
            {"create-manual-workitems", "distribution"},
        ),
        (
            False,
            False,
            "meldung",
            {"create-manual-workitems", "distribution"},
        ),
        (
            False,
            False,
            "meldung-pv",
            {"create-manual-workitems", "formal-exam", "init-additional-demand"},
        ),
    ],
)
def test_dynamic_task_after_submit(
    db,
    caluma_admin_user,
    expected_tasks,
    is_appeal,
    is_bab,
    application_settings,
    form_slug,
    so_instance,
):
    application_settings["SHORT_NAME"] = "so"

    meta = {}

    if is_appeal:
        meta["is-appeal"] = True

    if is_bab:
        meta["is-bab"] = True

    so_instance.case.meta.update(meta)
    so_instance.case.save()
    so_instance.case.document.form_id = form_slug
    so_instance.case.document.save()

    tasks = set(
        CustomDynamicTasks().resolve_after_submit(
            so_instance.case, caluma_admin_user, None, None
        )
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
    caluma_answer_factory,
    decision,
    expected_tasks,
    caluma_work_item_factory,
):
    answer = caluma_answer_factory(
        question__slug=additional_demand_settings["QUESTIONS"]["DECISION"],
        value=additional_demand_settings["ANSWERS"]["DECISION"][decision],
    )

    work_item = caluma_work_item_factory(document=answer.document)

    tasks = set(
        CustomDynamicTasks().resolve_after_check_additional_demand(
            None, None, work_item, None
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "decision_slug,work_item_status",
    [
        ("foobar", WorkItem.STATUS_SUSPENDED),
        (
            "complete-check-vollstaendigkeitspruefung-incomplete-wait",
            WorkItem.STATUS_READY,
        ),
    ],
)
def test_dynamic_task_resume_check_gwr_relevancy_work_item(
    db,
    additional_demand_settings,
    decision_slug,
    work_item_status,
    caluma_answer_factory,
    ur_instance,
    set_application_ur,
    caluma_work_item_factory,
):
    answer = caluma_answer_factory(
        question__slug="complete-check-vollstaendigkeitspruefung",
        value=decision_slug,
    )

    complete_check_work_item = caluma_work_item_factory(
        document=answer.document, case=ur_instance.case, task_id="complete-check"
    )

    check_gwr_relevancy_work_item = caluma_work_item_factory(
        document=ur_instance.case.document,
        case=ur_instance.case,
        task_id="check-gwr-relevancy",
        status=WorkItem.STATUS_SUSPENDED,
    )
    CustomDynamicTasks().resolve_after_check_additional_demand(
        ur_instance.case, None, complete_check_work_item, None
    )

    check_gwr_relevancy_work_item.refresh_from_db()

    assert check_gwr_relevancy_work_item.status == work_item_status


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
    caluma_work_item_factory,
    gr_instance,
    passed_addressed_groups,
    groups_with_existing,
    create_additional_demand,
):
    for group in groups_with_existing:
        caluma_work_item_factory(
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
    "root_form,task_id,has_rejection_answer,geometer_required,expected_tasks",
    [
        ("main-form", "formal-exam", True, True, ["reject"]),
        ("main-form", "formal-exam", True, False, ["reject"]),
        ("main-form", "material-exam", True, False, ["reject"]),
        ("main-form", "formal-exam", False, False, ["material-exam"]),
        ("main-form", "formal-exam", False, True, ["material-exam", "geometer"]),
        (
            "main-form",
            "material-exam",
            False,
            False,
            ["distribution", "publication", "fill-publication", "objections"],
        ),
        ("meldung-pv", "formal-exam", False, False, ["material-exam"]),
        ("meldung-pv", "formal-exam", False, True, ["material-exam", "geometer"]),
        ("meldung-pv", "material-exam", False, False, ["distribution"]),
    ],
)
def test_dynamic_task_after_exam(
    db,
    caluma_answer_factory,
    expected_tasks,
    has_rejection_answer,
    geometer_required,
    root_form,
    so_instance,
    so_rejection_settings,
    task_id,
    caluma_work_item_factory,
    mocker,
):
    work_item = caluma_work_item_factory(task_id=task_id, case=so_instance.case)

    if has_rejection_answer:
        caluma_answer_factory(
            document=work_item.document,
            question__slug=so_rejection_settings["WORK_ITEM"]["ON_ANSWER"][task_id][0],
            value=so_rejection_settings["WORK_ITEM"]["ON_ANSWER"][task_id][1],
        )

    if geometer_required:
        master_data_mock = Mock()
        master_data_mock.geometer_required = True
        mocker.patch(
            "camac.instance.master_data.MasterData.from_case_id",
            return_value=master_data_mock,
        )

    work_item.case.document.form_id = root_form
    work_item.case.document.save()

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
    caluma_answer_factory,
    expected_tasks,
    perform_cadastral_survey,
    be_instance,
    caluma_work_item_factory,
    caluma_admin_user,
):
    geometer_work_item = caluma_work_item_factory(
        task_id="geometer", case=be_instance.case, child_case=None
    )
    caluma_answer_factory(
        document=geometer_work_item.document,
        question__slug="geometer-beurteilung-notwendigkeit-vermessung",
        value=(
            "geometer-beurteilung-notwendigkeit-vermessung-notwendig"
            if perform_cadastral_survey
            else "geometer-beurteilung-notwendigkeit-vermessung-nicht-notwendig"
        ),
    )

    complete_work_item(geometer_work_item, user=caluma_admin_user)
    work_item = caluma_work_item_factory(task_id="check-sb2", case=be_instance.case)

    assert (
        CustomDynamicTasks().resolve_after_check_sb2(
            be_instance.case, None, work_item, None
        )
        == expected_tasks
    )


@pytest.mark.parametrize(
    "decision_answer,gwr_answer,expected_tasks",
    [
        (
            "entscheid-beurteilung-bewilligt",
            "fuer-gwr-relevant-ja",
            ["update-gwr-status"],
        ),
        ("entscheid-beurteilung-bewilligt", "fuer-gwr-relevant-nein", []),
        (
            "entscheid-beurteilung-nicht-bewilligt",
            "fuer-gwr-relevant-ja",
            ["update-gwr-status-refused"],
        ),
        ("entscheid-beurteilung-nicht-bewilligt", "fuer-gwr-relevant-nein", []),
    ],
)
def test_dynamic_task_gwr_relevancy_after_decision_ur(
    db,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_question_factory,
    caluma_answer_factory,
    ur_instance,
    caluma_admin_user,
    expected_tasks,
    decision_answer,
    gwr_answer,
):
    work_item = caluma_work_item_factory(
        case=ur_instance.case, task_id="decision", document=caluma_document_factory()
    )
    caluma_answer_factory(
        document=work_item.document,
        question=caluma_question_factory(slug="decision-task-entscheid-beurteilung"),
        value=decision_answer,
    )

    gwr_relevancy_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id="check-gwr-relevancy",
    )
    caluma_answer_factory(
        document=gwr_relevancy_work_item.document,
        question=caluma_question_factory(slug="fuer-gwr-relevant"),
        value=gwr_answer,
    )

    result = CustomDynamicTasks().resolve_after_decision_ur(
        ur_instance.case, caluma_admin_user, work_item, None
    )

    assert result == expected_tasks


@pytest.mark.parametrize(
    "answer,expected_tasks",
    [
        (
            "decision-task-nachfuehrungsgeometer-ja",
            ["geometer"],
        ),
        (
            "decision-task-nachfuehrungsgeometer-nein",
            [],
        ),
    ],
)
def test_dynamic_task_geometer_after_decision_ur(
    db,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    ur_instance,
    caluma_admin_user,
    expected_tasks,
    answer,
):
    work_item = caluma_work_item_factory(
        case=ur_instance.case, task_id="decision", document=caluma_document_factory()
    )

    if answer == "decision-task-nachfuehrungsgeometer-ja":
        caluma_answer_factory(
            document=work_item.document,
            question__slug="decision-task-nachfuehrungsgeometer",
            value=answer,
        )

        result = CustomDynamicTasks().resolve_after_decision_ur(
            ur_instance.case, caluma_admin_user, work_item, None
        )
        assert result == expected_tasks


@pytest.mark.parametrize(
    "involve_geometer,involve_gebaeudeschaetzung,expected_tasks",
    [
        (
            "decision-task-nachfuehrungsgeometer-ja",
            "decision-task-gebaudeschaetzung-ja",
            ["geometer-final-measurement", "gebaeudeschaetzung"],
        ),
        (
            "decision-task-nachfuehrungsgeometer-nein",
            "decision-task-gebaudeschaetzung-nein",
            [],
        ),
    ],
)
def test_after_complete_construction_monitoring_ur(
    db,
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    #
    involve_geometer,
    involve_gebaeudeschaetzung,
    expected_tasks,
):
    decision_work_item = caluma_work_item_factory(
        task__slug="decision",
        document=caluma_document_factory(),
        case=caluma_case_factory(),
    )
    caluma_answer_factory(
        question__slug="decision-task-nachfuehrungsgeometer",
        value=involve_geometer,
        document=decision_work_item.document,
    )
    caluma_answer_factory(
        document=decision_work_item.document,
        question__slug="decision-task-gebaudeschaetzung",
        value=involve_gebaeudeschaetzung,
    )

    result = CustomDynamicTasks().resolve_after_complete_construction_monitoring_ur(
        decision_work_item.case, None, caluma_work_item_factory(), None
    )

    for task in expected_tasks:
        assert task in result


@pytest.mark.parametrize(
    "main_form_slug,complete_check_answer,should_generate_additional_demand_task,should_generate_reject_task,should_generate_bk_task, should_generate_rpg_task",
    [
        (
            "building-permit",
            "complete-check-vollstaendigkeitspruefung-incomplete",
            True,
            False,
            True,
            False,
        ),
        (
            "building-permit",
            "complete-check-vollstaendigkeitspruefung-complete",
            False,
            False,
            True,
            False,
        ),
        (
            "building-permit",
            "complete-check-vollstaendigkeitspruefung-reject",
            False,
            True,
            False,
            False,
        ),
        (
            "cantonal-territory-usage",
            "complete-check-vollstaendigkeitspruefung-complete",
            False,
            False,
            False,
            False,
        ),
        (
            "oereb-verfahren-gemeinde",
            "complete-check-vollstaendigkeitspruefung-complete",
            False,
            False,
            False,
            True,
        ),
    ],
)
def test_dynamic_task_after_complete_check_ur(
    db,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_question_factory,
    caluma_answer_factory,
    caluma_admin_user,
    complete_check_answer,
    main_form_slug,
    should_generate_additional_demand_task,
    caluma_case_factory,
    should_generate_bk_task,
    should_generate_reject_task,
    should_generate_rpg_task,
):
    caluma_case = caluma_case_factory(document__form__slug=main_form_slug)
    work_item = caluma_work_item_factory(
        case=caluma_case,
        task__slug="complete-check",
        document=caluma_document_factory(),
    )

    caluma_answer_factory(
        document=work_item.document,
        question=caluma_question_factory(
            slug="complete-check-vollstaendigkeitspruefung"
        ),
        value=complete_check_answer,
    )

    caluma_answer_factory(
        document=caluma_case.document,
        question=caluma_question_factory(slug="oereb-thema"),
        value="oereb-thema-gnp" if should_generate_rpg_task else "oereb-thema-kpz",
    )

    result = CustomDynamicTasks().resolve_after_complete_check_ur(
        caluma_case, caluma_admin_user, work_item, None
    )

    if should_generate_additional_demand_task:
        assert "additional-demand" in result
    else:
        assert "additional-demand" not in result

    if should_generate_bk_task:
        assert "release-for-bk" in result
    else:
        assert "release-for-bk" not in result

    if should_generate_reject_task:
        assert "reject" in result
    else:
        assert "reject" not in result

    if should_generate_rpg_task:
        assert "rpg" in result
    else:
        assert "rpg" not in result


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
    form_utils: FormUtils,
):
    plan_stage = construction_monitoring_initialized_case_sz.work_items.first()
    form_utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
    form_utils.add_answer(plan_stage.document, "construction-steps", selected_steps)
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
        form_utils.add_answer(previous_work_item.document, question, answer)

    tasks = set(
        CustomDynamicTasks().resolve_after_construction_step(
            construction_monitoring_initialized_case_sz,
            caluma_admin_user,
            previous_work_item,
            None,
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize("construction_monitoring_enabled", [True, False])
@pytest.mark.parametrize(
    "form_slug,expected_tasks",
    [
        ("bauanzeige", ["distribution"]),
        ("solaranlage", ["distribution"]),
        ("vorlaeufige-beurteilung", ["distribution"]),
        ("baugesuch", ["distribution", "fill-publication", "publication"]),
    ],
)
def test_dynamic_task_after_formal_exam(
    db,
    caluma_work_item_factory,
    gr_instance,
    gr_publication_settings,
    gr_distribution_settings,
    gr_address_assignment_settings,
    gr_construction_monitoring_settings,
    construction_monitoring_enabled,
    caluma_admin_user,
    form_slug,
    expected_tasks,
):
    gr_construction_monitoring_settings["ENABLED"] = construction_monitoring_enabled
    gr_address_assignment_settings["ENABLED"] = construction_monitoring_enabled

    gr_instance.case.document.form.slug = form_slug
    gr_instance.case.document.form.save()

    work_item = caluma_work_item_factory(
        case=gr_instance.case,
        task_id="formal-exam",
    )

    result = CustomDynamicTasks().resolve_after_formal_exam(
        gr_instance.case, caluma_admin_user, work_item, None
    )

    if len(result) > 1:
        result.sort()

    assert all([task in result for task in expected_tasks])


@pytest.mark.parametrize(
    "expected_value,answer",
    [
        (
            ["construction-control"],
            "complete-instance-ac-verfahren-abgeschlossen-auflagenkontrolle-notwendig",
        ),
        ([], "some-other-answer"),
    ],
)
def test_after_complete_instance(
    db,
    caluma_admin_user,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    #
    expected_value,
    answer,
):
    work_item = caluma_work_item_factory(document=caluma_document_factory())
    caluma_answer_factory(
        document=work_item.document, question__slug="complete-instance-ac", value=answer
    )
    result = CustomDynamicTasks().after_complete_instance(
        None, caluma_admin_user, work_item, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "expected_value,answer",
    [
        (
            ["construction-control"],
            "construction-control-control-control-performed-further-control",
        ),
        ([], "some-other-answer"),
    ],
)
def test_construction_control(
    db,
    caluma_admin_user,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    #
    expected_value,
    answer,
):
    work_item = caluma_work_item_factory(document=caluma_document_factory())
    caluma_answer_factory(
        document=work_item.document,
        question__slug="construction-control-control",
        value=answer,
    )
    result = CustomDynamicTasks().after_construction_control(
        None, caluma_admin_user, work_item, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "expected_value,massnahmen_answer,schutzraum_answer",
    [
        (
            ["zs-ersatzbeitrag-pruefen"],
            "schutzraumrelevante-massnahmen-ja",
            "schutzraum-antrag",
        ),
        ([], "schutzraumrelevante-massnahmen-ja", "wrong_answer"),
        ([], "wrong_answer", "schutzraum-antrag"),
        ([], "some-other-answer", "yet-another-one"),
    ],
)
def test_after_schnurgeruestabnahme_kontrollieren_uri(
    db,
    caluma_admin_user,
    ur_instance,
    notification_template,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    expected_value,
    massnahmen_answer,
    schutzraum_answer,
):
    notification_template.slug = "6-411-schnurgeruestabnahme-erfolgt"
    notification_template.save()

    work_item = caluma_work_item_factory(document=caluma_document_factory())
    caluma_answer_factory(
        document=ur_instance.case.document,
        question__slug="schutzraumrelevante-massnahmen",
        value=massnahmen_answer,
    )
    caluma_answer_factory(
        document=ur_instance.case.document,
        question__slug="schutzraum",
        value=schutzraum_answer,
    )
    result = CustomDynamicTasks().resolve_after_schnurgeruestabnahme_kontrollieren(
        ur_instance.case, caluma_admin_user, work_item, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "work_item_exists,gwr_answer,expected_value",
    [
        (True, "fuer-gwr-relevant-ja", ["construction-step-gwr-state-demolition"]),
        (True, "fuer-gwr-relevant-nein", []),
        (False, "not-necessary", ["construction-step-gwr-state-demolition"]),
    ],
)
def test_after_gebaeudeabbruch_melden(
    db,
    caluma_admin_user,
    work_item_exists,
    gwr_answer,
    expected_value,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    instance_factory,
    caluma_case_factory,
    caluma_task_factory,
):
    instance = instance_factory(case=caluma_case_factory())

    if work_item_exists:
        work_item = caluma_work_item_factory(
            case=instance.case,
            task=caluma_task_factory(slug="check-gwr-relevancy"),
            document=caluma_document_factory(),
            status="completed",
        )
        caluma_answer_factory(
            document=work_item.document,
            question__slug="fuer-gwr-relevant",
            value=gwr_answer,
        )

    result = CustomDynamicTasks().resolve_after_gebaeudeabbruch_melden(
        instance.case, caluma_admin_user, work_item if work_item_exists else None, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "work_item_exists,gwr_answer,expected_value",
    [
        (
            True,
            "fuer-gwr-relevant-ja",
            ["construction-step-gwr-state-construction-start"],
        ),
        (True, "fuer-gwr-relevant-nein", []),
        (False, "not-necessary", ["construction-step-gwr-state-construction-start"]),
    ],
)
def test_after_baubeginn_melden(
    db,
    caluma_admin_user,
    work_item_exists,
    gwr_answer,
    expected_value,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    instance_factory,
    caluma_case_factory,
    caluma_task_factory,
):
    instance = instance_factory(case=caluma_case_factory())

    if work_item_exists:
        work_item = caluma_work_item_factory(
            case=instance.case,
            task=caluma_task_factory(slug="check-gwr-relevancy"),
            document=caluma_document_factory(),
            status="completed",
        )
        caluma_answer_factory(
            document=work_item.document,
            question__slug="fuer-gwr-relevant",
            value=gwr_answer,
        )

    result = CustomDynamicTasks().resolve_after_baubeginn_melden(
        instance.case, caluma_admin_user, work_item if work_item_exists else None, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "work_item_exists,gwr_answer,expected_value",
    [
        (True, "fuer-gwr-relevant-ja", ["construction-step-gwr-state-building"]),
        (True, "fuer-gwr-relevant-nein", []),
        (False, "not-necessary", ["construction-step-gwr-state-building"]),
    ],
)
def test_after_schlussabnahme_gebaeude(
    db,
    caluma_admin_user,
    work_item_exists,
    gwr_answer,
    expected_value,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    instance_factory,
    caluma_case_factory,
    caluma_task_factory,
):
    instance = instance_factory(case=caluma_case_factory())

    if work_item_exists:
        work_item = caluma_work_item_factory(
            case=instance.case,
            task=caluma_task_factory(slug="check-gwr-relevancy"),
            document=caluma_document_factory(),
            status="completed",
        )
        caluma_answer_factory(
            document=work_item.document,
            question__slug="fuer-gwr-relevant",
            value=gwr_answer,
        )

    result = CustomDynamicTasks().resolve_after_schlussabnahme_gebaeude(
        instance.case, caluma_admin_user, work_item if work_item_exists else None, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "work_item_exists,gwr_answer,expected_value",
    [
        (True, "fuer-gwr-relevant-ja", ["open-gwr-construction-project"]),
        (True, "fuer-gwr-relevant-nein", []),
        (False, "not-necessary", ["open-gwr-construction-project"]),
    ],
)
def test_after_check_gwr_relevancy(
    db,
    caluma_admin_user,
    work_item_exists,
    gwr_answer,
    expected_value,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    instance_factory,
    caluma_case_factory,
    caluma_task_factory,
):
    instance = instance_factory(case=caluma_case_factory())

    if work_item_exists:
        work_item = caluma_work_item_factory(
            case=instance.case,
            task=caluma_task_factory(slug="check-gwr-relevancy"),
            document=caluma_document_factory(),
            status="completed",
        )
        caluma_answer_factory(
            document=work_item.document,
            question__slug="fuer-gwr-relevant",
            value=gwr_answer,
        )

    result = CustomDynamicTasks().resolve_after_check_gwr_relevancy(
        instance.case, caluma_admin_user, work_item if work_item_exists else None, None
    )
    assert result == expected_value


@pytest.mark.parametrize(
    "publication_required,information_of_neighbors_required,expected_tasks",
    [
        (False, False, []),
        (True, False, ["publication", "fill-publication"]),
        (False, True, ["information-of-neighbors", "fill-information-of-neighbors"]),
        (
            True,
            True,
            [
                "publication",
                "fill-publication",
                "information-of-neighbors",
                "fill-information-of-neighbors",
            ],
        ),
    ],
)
def test_dynamic_task_maybe_publication(
    db,
    ag_instance,
    ag_master_data_settings,
    caluma_admin_user,
    caluma_work_item_factory,
    expected_tasks,
    information_of_neighbors_required,
    master_data_is_visible_mock,
    publication_required,
    form_utils: FormUtils,
):
    formal_exam = caluma_work_item_factory(
        case=ag_instance.case,
        task_id="formal-exam",
    )

    form_utils.add_answer(
        formal_exam.document,
        "vorlaeufige-pruefung-publikation",
        f"vorlaeufige-pruefung-publikation-{yes_no(publication_required, 'de')}",
    )
    form_utils.add_answer(
        formal_exam.document,
        "vorlaeufige-pruefung-auswaertige-anstoesser",
        f"vorlaeufige-pruefung-auswaertige-anstoesser-{yes_no(information_of_neighbors_required, 'de')}",
    )

    tasks = CustomDynamicTasks().resolve_maybe_publication(
        ag_instance.case, caluma_admin_user, formal_exam, None
    )

    assert set(tasks) == set(expected_tasks)


@pytest.mark.parametrize(
    "form_slug,expected_tasks",
    [
        (
            "main-form",
            {
                "create-manual-workitems",
                "formal-exam",
                "init-additional-demand",
                "withdrawal-request",
            },
        ),
        (
            "plangenehmigungsverfahren-bund",
            {
                "create-manual-workitems",
                "distribution",
                "cantonal-exam",
                "objections",
                "withdrawal-request",
            },
        ),
        (
            "plangenehmigungsverfahren-gas",
            {
                "create-manual-workitems",
                "distribution",
                "cantonal-exam",
                "objections",
                "init-additional-demand",
                "withdrawal-request",
            },
        ),
    ],
)
def test_dynamic_task_after_submit_ag(
    db, ag_instance, application_settings, caluma_admin_user, expected_tasks, form_slug
):
    application_settings["SHORT_NAME"] = "ag"

    ag_instance.case.document.form_id = form_slug
    ag_instance.case.document.save()

    tasks = set(
        CustomDynamicTasks().resolve_after_submit(
            ag_instance.case, caluma_admin_user, None, None
        )
    )

    assert tasks == expected_tasks


@pytest.mark.parametrize(
    "inquiry_answer, afb_in_addressed_groups, existing_work_item, should_create_work_item",
    [
        ("inquiry-answer-status-not-involved", True, False, False),
        ("inquiry-answer-status-positive", True, False, True),
        ("inquiry-answer-status-positive", True, True, False),
        ("inquiry-answer-status-positive", False, False, False),
    ],
)
def test_resolve_maybe_trigger_billing(
    db,
    ag_instance,
    service_factory,
    caluma_work_item_factory,
    caluma_answer_factory,
    caluma_admin_user,
    inquiry_answer,
    afb_in_addressed_groups,
    existing_work_item,
    should_create_work_item,
    mocker,
):
    afb = service_factory(slug="afb")
    addressed_groups = [str(afb.pk)] if afb_in_addressed_groups else []

    parent_work_item = caluma_work_item_factory(
        case=ag_instance.case,
        addressed_groups=addressed_groups,
    )

    caluma_answer_factory(
        document=parent_work_item.document,
        question_id="inquiry-answer-status",
        value=inquiry_answer,
    )

    if existing_work_item:
        caluma_work_item_factory(
            case=ag_instance.case.family,
            task_id="trigger-billing",
            status="ready",
            addressed_groups=addressed_groups,
        )

    mock_send_event = mocker.patch("camac.caluma.extensions.dynamic_tasks.send_event")

    result = CustomDynamicTasks().resolve_maybe_trigger_billing(
        ag_instance.case, caluma_admin_user, parent_work_item, None
    )

    assert result == []

    trigger_billing_items = ag_instance.case.family.work_items.filter(
        task_id="trigger-billing",
        status="ready",
        addressed_groups=addressed_groups,
    )

    if should_create_work_item:
        assert trigger_billing_items.exists()
        assert mock_send_event.called
    else:
        if existing_work_item:
            assert trigger_billing_items.exists()
        else:
            assert not trigger_billing_items.exists()
