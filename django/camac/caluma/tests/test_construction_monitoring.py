import json

import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core import mail

from camac.caluma.extensions.events.construction_monitoring import (
    can_perform_construction_monitoring,
    post_complete_construction_control,
    post_complete_decision_start_init_monitoring_gr,
    post_create_construction_control,
    post_create_gvg_work_item,
    post_create_plan_construction_stage_ur,
)
from camac.caluma.extensions.visibilities import CustomVisibility
from camac.instance.models import InstanceState
from camac.permissions.models import InstanceACL
from camac.tests.form_utils import FormUtils


@pytest.mark.freeze_time("2023-09-04")
def test_construction_monitoring_initial_state(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    construction_monitoring_case_sz,
    service,
):
    case = sz_instance.case

    init_construction_monitoring = case.work_items.get(
        task_id=sz_construction_monitoring_settings[
            "INIT_CONSTRUCTION_MONITORING_TASK"
        ],
    )

    assert init_construction_monitoring.status == WorkItem.STATUS_READY
    assert (
        init_construction_monitoring.addressed_groups
        == case.work_items.get(task_id="make-decision").addressed_groups
    )
    assert init_construction_monitoring.addressed_groups == [str(service.pk)]
    assert (
        init_construction_monitoring.deadline.isoformat() == "2023-10-04T00:00:00+00:00"
    )


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("skip", [True, False])
@pytest.mark.freeze_time("2023-09-04")
def test_init_construction_monitoring(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    application_settings,
    construction_monitoring_case_sz,
    caluma_admin_schema_executor,
    service,
    skip,
):
    case = sz_instance.case

    # Prevent creation of construction monitoring work item to fail because of
    # missing notification templates in the test:
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"] = {}

    init_construction_monitoring = case.work_items.get(
        task_id=sz_construction_monitoring_settings[
            "INIT_CONSTRUCTION_MONITORING_TASK"
        ],
        status=WorkItem.STATUS_READY,
    )

    variables = {
        "input": {
            "id": str(init_construction_monitoring.pk),
            "context": json.dumps({"skip": True} if skip else {}),
        }
    }

    result = caluma_admin_schema_executor(
        """
        mutation CompleteWorkItem($input: CompleteWorkItemInput!) {
            completeWorkItem(input: $input) {
                clientMutationId
            }
        }
        """,
        variables=variables,
    )

    assert not result.errors

    construction_stage = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["CONSTRUCTION_STAGE_TASK"]
    ).first()

    complete_construction_monitoring = case.work_items.filter(
        task_id=sz_construction_monitoring_settings[
            "COMPLETE_CONSTRUCTION_MONITORING_TASK"
        ]
    ).first()

    complete_instance = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["COMPLETE_INSTANCE_TASK"]
    ).first()

    created = (
        [complete_instance]
        if skip
        else [construction_stage, complete_construction_monitoring]
    )
    for work_item in [
        construction_stage,
        complete_construction_monitoring,
        complete_instance,
    ]:
        if work_item in created:
            assert work_item.status == WorkItem.STATUS_READY
            assert work_item.addressed_groups == [str(service.pk)]
        else:
            assert not work_item

    if not skip:
        construction_stage.child_case.status == Case.STATUS_RUNNING
        construction_stage.child_case.workflow == sz_construction_monitoring_settings[
            "CONSTRUCTION_STAGE_WORKFLOW"
        ]


@pytest.mark.parametrize("role__name", ["municipality-lead"])
def test_create_construction_stage(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    construction_monitoring_initialized_case_sz,
    caluma_admin_schema_executor,
    service,
):
    case = sz_instance.case

    construction_stages = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["CONSTRUCTION_STAGE_TASK"]
    )

    assert construction_stages.count() == 1

    variables = {
        "input": {
            "case": str(case.pk),
            "multipleInstanceTask": sz_construction_monitoring_settings[
                "CONSTRUCTION_STAGE_TASK"
            ],
        }
    }

    result = caluma_admin_schema_executor(
        """
        mutation createWorkItem($input: CreateWorkItemInput!) {
            createWorkItem(input: $input) {
                clientMutationId
            }
        }
        """,
        variables=variables,
    )

    assert not result.errors
    assert construction_stages.count() == 2

    for stage in construction_stages:
        assert stage.status == WorkItem.STATUS_READY
        assert stage.addressed_groups == [str(service.pk)]
        assert stage.child_case.status == Case.STATUS_RUNNING
        assert (
            stage.child_case.workflow.pk
            == sz_construction_monitoring_settings["CONSTRUCTION_STAGE_WORKFLOW"]
        )

        assert stage.child_case.work_items.count() == 1
        work_item = stage.child_case.work_items.first()
        assert (
            work_item.task.pk
            == sz_construction_monitoring_settings[
                "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK"
            ]
        )
        assert work_item.status == WorkItem.STATUS_READY
        assert work_item.addressed_groups == [str(service.pk)]
        assert (
            work_item.meta["construction-step-id"]
            == "construction-step-plan-construction-stage"
        )


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("cancel", [True, False])
@pytest.mark.freeze_time("2023-09-04")
def test_complete_construction_stage(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    notification_template,
    construction_monitoring_initialized_case_sz,
    construction_stage_factory_sz,
    caluma_admin_schema_executor,
    caluma_admin_user,
    service,
    distribution_settings,
    cancel,
    form_utils: FormUtils,
):
    sz_construction_monitoring_settings["NOTIFICATIONS"][
        sz_construction_monitoring_settings["CONSTRUCTION_STAGE_WORKFLOW"]
    ] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["leitbehoerde"],
        },
    ]

    case = sz_instance.case
    construction_stage = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["CONSTRUCTION_STAGE_TASK"]
    ).first()

    complete_construction_monitoring = case.work_items.filter(
        task_id=sz_construction_monitoring_settings[
            "COMPLETE_CONSTRUCTION_MONITORING_TASK"
        ]
    ).first()

    assert complete_construction_monitoring.deadline is None

    if cancel:
        variables = {
            "input": {
                "id": str(construction_stage.child_case.pk),
            }
        }
        query = """
            mutation CancelCase($input: CancelCaseInput!) {
                cancelCase(
                    input: $input
                ) {
                    clientMutationId
                }
            }
            """
    else:
        # Complete last work-item of case
        plan_stage = construction_stage.child_case.work_items.first()
        form_utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
        form_utils.add_answer(
            plan_stage.document, "construction-steps", ["construction-step-baubeginn"]
        )

        complete_work_item(work_item=plan_stage, user=caluma_admin_user)
        baubeginn = construction_stage.child_case.work_items.filter(
            status=WorkItem.STATUS_READY
        ).first()
        baubeginn.document.form.questions.update(is_required=False)

        variables = {
            "id": str(baubeginn.pk),
        }
        query = """
            mutation CompleteWorkItem($id: ID!) {
                completeWorkItem(input: { id: $id }) {
                    clientMutationId
                }
            }
            """

    result = caluma_admin_schema_executor(
        query,
        variables=variables,
    )

    assert not result.errors
    construction_stage.refresh_from_db()

    assert construction_stage.status == WorkItem.STATUS_READY
    assert construction_stage.child_case.status == (
        Case.STATUS_CANCELED if cancel else Case.STATUS_COMPLETED
    )

    complete_construction_monitoring.refresh_from_db()
    assert (
        complete_construction_monitoring.deadline.isoformat()
        == "2023-09-14T00:00:00+00:00"
    )

    construction_stage_factory_sz(case)
    complete_construction_monitoring.refresh_from_db()
    assert complete_construction_monitoring.deadline is None

    assert len(mail.outbox) == (0 if cancel else 1)


@pytest.mark.parametrize("role__name", ["municipality-lead"])
def test_complete_construction_monitoring(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    construction_monitoring_initialized_case_sz,
    caluma_admin_schema_executor,
    service,
):
    case = sz_instance.case

    construction_stage = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["CONSTRUCTION_STAGE_TASK"]
    ).first()

    complete_construction_monitoring = case.work_items.filter(
        task_id=sz_construction_monitoring_settings[
            "COMPLETE_CONSTRUCTION_MONITORING_TASK"
        ]
    ).first()

    variables = {
        "id": str(complete_construction_monitoring.pk),
    }

    result = caluma_admin_schema_executor(
        """
        mutation CompleteWorkItem($id: ID!) {
            completeWorkItem(input: { id: $id }) {
                clientMutationId
            }
        }
        """,
        variables=variables,
    )

    assert not result.errors
    complete_construction_monitoring.refresh_from_db()
    construction_stage.refresh_from_db()

    assert complete_construction_monitoring.status == WorkItem.STATUS_COMPLETED
    assert construction_stage.status == WorkItem.STATUS_SKIPPED
    assert construction_stage.child_case.status == WorkItem.STATUS_CANCELED

    complete_instance = case.work_items.filter(
        task_id=sz_construction_monitoring_settings["COMPLETE_INSTANCE_TASK"]
    ).first()
    assert complete_instance.status == WorkItem.STATUS_READY
    assert complete_instance.addressed_groups == [str(service.pk)]


@pytest.mark.parametrize("role__name", ["municipality-lead"])
def test_complete_construction_step_work_item(
    db,
    sz_instance,
    sz_construction_monitoring_settings,
    construction_monitoring_initialized_case_sz,
    caluma_admin_schema_executor,
    service,
    form_utils: FormUtils,
    notification_template,
    mocker,
):
    ech_signal_mock = mocker.patch(
        "camac.ech0211.signals.construction_monitoring_started.send"
    )

    plan_stage = construction_monitoring_initialized_case_sz.work_items.first()
    form_utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
    form_utils.add_answer(
        plan_stage.document, "construction-steps", ["construction-step-baubeginn"]
    )
    sz_construction_monitoring_settings["NOTIFICATIONS"] = {
        plan_stage.task.pk: [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["leitbehoerde"],
            }
        ]
    }

    sz_instance.instance_state = InstanceState.objects.get(
        name=sz_construction_monitoring_settings["PREVIOUS_INSTANCE_STATE"]
    )
    sz_instance.save()

    variables = {
        "id": str(plan_stage.pk),
    }

    result = caluma_admin_schema_executor(
        """
        mutation CompleteWorkItem($id: ID!) {
            completeWorkItem(input: { id: $id }) {
                clientMutationId
            }
        }
        """,
        variables=variables,
    )

    assert not result.errors
    plan_stage.refresh_from_db()
    sz_instance.refresh_from_db()

    assert (
        sz_instance.instance_state.name
        == sz_construction_monitoring_settings["CONSTRUCTION_MONITORING_INSTANCE_STATE"]
    )
    assert len(mail.outbox) == 1
    assert sz_instance.group.service.email in mail.outbox[0].recipients()
    ech_signal_mock.assert_called_once()


def test_construction_monitoring_work_item_visibility_coordination(mocker):
    custom_visibility = CustomVisibility()
    mocker.patch.object(
        custom_visibility,
        "visible_construction_step_work_items_expression_for_municipality",
    )

    custom_visibility.visible_construction_step_work_items_expression_for_coordination(
        None
    )

    assert custom_visibility.visible_construction_step_work_items_expression_for_municipality.called


@pytest.mark.parametrize("role__name", ["service-lead"])
@pytest.mark.parametrize(
    "construction_task,service_slug,is_addressed,expected_visible",
    [
        [False, "other-service", True, True],
        [False, "other-service", False, True],
        [False, "gvg", True, True],
        [False, "gvg", False, True],
        [True, "other-service", True, False],
        [True, "other-service", False, False],
        [True, "gvg", False, False],
        # gvg service can see construction monitoring when addressed.
        [True, "gvg", True, True],
    ],
)
def test_construction_monitoring_work_item_visibility_service_gvg_gr(
    db,
    role,
    group,
    service,
    caluma_work_item_factory,
    caluma_task_factory,
    caluma_admin_request,
    service_factory,
    gr_instance,
    construction_task,
    is_addressed,
    service_slug,
    expected_visible,
    admin_user,
    caluma_admin_schema_executor,
    construction_monitoring_settings,
    gr_permissions_settings,
    set_application_gr,
    mocker,
):
    """Test workitem visibility for kt. GR for construction monitoring."""
    construction_monitoring_settings["ENABLED"] = True

    group = admin_user.groups.first()
    group.service.slug = service_slug
    group.service.save()

    # reload the request to apply the new service slug for the group
    request = caluma_admin_request()

    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[gr_instance.pk],
    )

    # decide the task to use in the test.
    task = (
        Task.objects.get(
            pk=construction_monitoring_settings["INIT_CONSTRUCTION_MONITORING_TASK"]
        )
        if construction_task
        else caluma_task_factory()
    )

    wi = caluma_work_item_factory(
        case=gr_instance.case,
        addressed_groups=(
            [str(service.pk)] if is_addressed else [str(service_factory().pk)]
        ),
        task=task,
    )

    result = caluma_admin_schema_executor(
        """
        query {
            allWorkItems {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """,
        context_value=request,
    )

    assert not result.errors
    workitems_id = set(
        [
            extract_global_id(edge["node"]["id"])
            for edge in result.data["allWorkItems"]["edges"]
        ]
    )

    if expected_visible:
        assert str(wi.pk) in workitems_id
    else:
        assert str(wi.pk) not in workitems_id


@pytest.mark.parametrize(
    "allow_forms_setting,should_be_allowed",
    [
        (None, True),
        (["building-permit-camac"], True),
        (["no-building-permits-allowed-camac"], False),
    ],
)
def test_can_perform_construction_monitoring_allow_forms(
    db,
    instance,
    construction_monitoring_settings,
    caluma_case_factory,
    caluma_document_factory,
    form_factory,
    # parametrize fixtures
    allow_forms_setting,
    should_be_allowed,
):
    instance.form.family = form_factory(name="building-permit-camac")
    instance.form.save()

    instance.case = caluma_case_factory(
        document=caluma_document_factory(form__slug="building-permit-caluma"),
    )
    instance.save()

    construction_monitoring_settings["ALLOW_FORMS"] = allow_forms_setting

    assert can_perform_construction_monitoring(instance) == should_be_allowed


@pytest.mark.parametrize(
    "expected_value,decision_answer",
    [
        (True, "complete-check-baubewilligungspflichtig-baubewilligungspflichtig"),
        (
            False,
            "complete-check-baubewilligungspflichtig-nicht-baubewilligungspflichtig",
        ),
    ],
)
def test_can_perform_construction_monitoring_ur(
    db,
    instance,
    set_application_ur,
    construction_monitoring_settings,
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    #
    expected_value,
    decision_answer,
):
    instance.case = caluma_case_factory()
    instance.save()
    complete_check_work_item = caluma_work_item_factory(
        case=instance.case,
        task__slug="complete-check",
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        document=complete_check_work_item.document,
        question__slug="complete-check-baubewilligungspflichtig",
        value=decision_answer,
    )
    assert expected_value == can_perform_construction_monitoring(instance)


def test_post_create_construction_control(
    db,
    instance_factory,
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    ur_construction_monitoring_settings,
):
    instance = instance_factory(case=caluma_case_factory())
    previous_construction_control_work_item = caluma_work_item_factory(
        case=instance.case,
        task__slug="construction-control",
        document=caluma_document_factory(),
        status=WorkItem.STATUS_COMPLETED,
    )
    caluma_answer_factory(
        document=previous_construction_control_work_item.document,
        question__slug="construction-control-date",
        date="2024-12-24",
    )
    construction_control_work_item = caluma_work_item_factory(
        case=instance.case, task_id="construction-control"
    )

    old_deadline = construction_control_work_item.deadline
    old_name = construction_control_work_item.name

    post_create_construction_control(
        None, user=None, work_item=construction_control_work_item, context={}
    )
    construction_control_work_item.refresh_from_db()

    assert construction_control_work_item.name != old_name, (
        "the name should have been updated."
    )
    assert construction_control_work_item.deadline != old_deadline, (
        "the deadline should have been set accordingly."
    )


def test_post_complete_construction_control(
    db,
    instance_factory,
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    construction_monitoring_settings,
    caluma_admin_user,
    instance_state_factory,
    ur_construction_monitoring_settings,
):
    instance = instance_factory(
        case=caluma_case_factory(),
        instance_state=instance_state_factory(name="some-instance-state"),
    )
    instance_state_factory(name="arch")

    construction_control_work_item = caluma_work_item_factory(
        case=instance.case,
        task__slug="construction-control",
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        document=construction_control_work_item.document,
        question__slug="construction-control-control",
        value="construction-control-control-control-performed-no-more-controls",
    )

    post_complete_construction_control(
        None,
        user=caluma_admin_user,
        work_item=construction_control_work_item,
        context={},
    )

    instance.refresh_from_db()

    assert instance.instance_state.name == "arch"


def test_post_create_plan_construction_stage_ur(
    db,
    set_application_ur,
    ur_construction_monitoring_settings,
    ur_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
):
    check_gwr_relevancy_work_item = caluma_work_item_factory(
        document=ur_instance.case.document,
        case=ur_instance.case,
        task_id="check-gwr-relevancy",
        status="completed",
    )
    caluma_answer_factory(
        document=check_gwr_relevancy_work_item.document,
        question__slug="fuer-gwr-relevant",
        value="fuer-gwr-relevant-ja",
    )

    plan_stage_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id="construction-step-plan-construction-stage",
        document=caluma_document_factory(
            form_id="construction-step-plan-construction-stage"
        ),
    )
    post_create_plan_construction_stage_ur(
        None, user=None, work_item=plan_stage_work_item, context={}
    )
    assert (
        "construction-step-baubeginn"
        in plan_stage_work_item.document.answers.get(
            question_id="construction-steps"
        ).value
    )
    assert (
        "construction-step-schlussabnahme-gebaeude"
        in plan_stage_work_item.document.answers.get(
            question_id="construction-steps"
        ).value
    )


def test_construction_monitoring_task_gvg_gr(
    db,
    gr_instance,
    construction_monitoring_settings,
    service_factory,
    caluma_task_factory,
    access_level_factory,
    gr_permissions_settings,
    set_application_gr,
):
    """In kt. GR the gvg should be granted when a workitem is addressed."""
    construction_monitoring_settings["ENABLED"] = True
    access_level = access_level_factory(pk="distribution-service")
    task = caluma_task_factory(address_groups=["gebaudeversicherung"])
    gvg_service = service_factory(slug="gvg")
    case = gr_instance.case

    assert not (
        InstanceACL.objects.filter(
            instance=case.family.instance,
            service=gvg_service,
            access_level=access_level,
        ).exists()
    )

    work_item = WorkItem.objects.create(
        case=case,
        task_id=task.pk,
        name="Resolve after submit GR",
        addressed_groups=[str(gvg_service.pk)],
    )

    post_create_gvg_work_item(None, work_item, None, None)

    assert InstanceACL.objects.filter(
        instance=case.family.instance,
        service=gvg_service,
        access_level=access_level,
    ).exists()


@pytest.mark.freeze_time("2026-01-01")
def test_init_construction_monitoring_deadline_gr(
    db,
    caluma_work_item_factory,
    caluma_case_factory,
    caluma_task_factory,
    service,
    gr_decision_settings,
    gr_construction_monitoring_settings,
    set_application_gr,
):
    case = caluma_case_factory()
    init_work_item = caluma_work_item_factory(
        case=case,
        task=caluma_task_factory(
            pk=gr_construction_monitoring_settings["INIT_CONSTRUCTION_MONITORING_TASK"],
            meta={"lead-time-after-decision": 30 * 24 * 3600},  # 30 days
        ),
        addressed_groups=[str(service.pk)],
        deadline=None,  # deadline is not set initially
    )
    decision_work_item = caluma_work_item_factory(
        case=case,
        task=caluma_task_factory(pk=gr_decision_settings["TASK"]),
    )

    assert init_work_item.deadline is None

    post_complete_decision_start_init_monitoring_gr(
        None, work_item=decision_work_item, user=None, context={}
    )
    init_work_item.refresh_from_db()
    assert init_work_item.deadline.isoformat() == "2026-01-31T00:00:00+00:00"
