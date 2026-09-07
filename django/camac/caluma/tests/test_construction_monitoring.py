import json
from datetime import date

import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core import mail
from pytest_lazy_fixtures import lf

from camac.caluma.extensions.dynamic_tasks import CustomDynamicTasks
from camac.caluma.extensions.events.construction_monitoring import (
    clear_init_construction_monitoring_deadline,
    post_complete_construction_control,
    post_complete_construction_monitoring,
    post_complete_init_construction_monitoring,
    post_create_complete_construction_monitoring,
    post_create_construction_control,
    post_create_dynamic_addressed_work_item,
    post_create_plan_construction_stage_ur,
    set_construction_monitoring_deadlines_after_decision,
)
from camac.caluma.extensions.visibilities import CustomVisibility
from camac.instance.domain_logic.construction_monitoring import (
    can_perform_construction_monitoring,
    maybe_start_construction_monitoring_after_construction_step,
    maybe_start_construction_monitoring_after_decision,
)
from camac.instance.models import InstanceState
from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL
from camac.tests.form_utils import FormUtils
from camac.user.models import ServiceRelation


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("address_groups", "expected_events"),
    [
        (["geometer"], ["geometer"]),
        (["geometer_schnurgeruestabnahme"], ["geometer"]),
        (["geometer-ur"], ["geometer"]),
        (["gebaudeversicherung"], ["gvg"]),
        (["geometer", "gebaudeversicherung"], ["geometer", "gvg"]),
        (["municipality"], []),
        (None, []),
    ],
)
def test_post_create_dynamic_addressed_work_item_trigger(
    caluma_work_item_factory,
    mocker,
    service_factory,
    set_application_gr,
    address_groups,
    expected_events,
):
    addressed_service = service_factory()
    work_item = caluma_work_item_factory(
        addressed_groups=[str(addressed_service.pk)],
        task__address_groups=address_groups,
    )
    events = {
        "geometer": mocker.patch(
            "camac.caluma.extensions.events.construction_monitoring."
            "Trigger.geometer_work_item_created"
        ),
        "gvg": mocker.patch(
            "camac.caluma.extensions.events.construction_monitoring."
            "Trigger.gvg_work_item_created"
        ),
    }

    post_create_dynamic_addressed_work_item(None, work_item, None, None)

    for name, event in events.items():
        if name in expected_events:
            event.assert_called_once_with(None, work_item)
        else:
            event.assert_not_called()


@pytest.mark.parametrize(
    ("construction_settings", "instance_state__name", "should_start"),
    [
        (lf("disable_construction_monitoring_settings"), "decided", False),
        (lf("gr_construction_monitoring_settings"), "other", False),
        (lf("gr_construction_monitoring_settings"), "decided", True),
    ],
)
@pytest.mark.django_db
def test_maybe_start_construction_monitoring_after_construction_step(
    admin_user,
    caluma_admin_user,
    gr_instance,
    mocker,
    request,
    set_application_gr,
    construction_settings,
    should_start,
):
    start = mocker.patch(
        "camac.instance.domain_logic.construction_monitoring.start_construction_monitoring"
    )

    maybe_start_construction_monitoring_after_construction_step(
        gr_instance, caluma_admin_user, admin_user
    )

    if should_start:
        start.assert_called_once_with(
            gr_instance,
            caluma_admin_user,
            admin_user,
            sender="post_complete_construction_step_work_item",
        )
    else:
        start.assert_not_called()


@pytest.mark.parametrize(
    (
        "construction_settings",
        "instance_state__name",
        "init_status",
        "should_start",
    ),
    [
        (lf("disable_construction_monitoring_settings"), "decided", None, False),
        (lf("construction_monitoring_settings"), "decided", None, False),
        (lf("gr_construction_monitoring_settings"), "other", None, False),
        (
            lf("gr_construction_monitoring_settings"),
            "decided",
            WorkItem.STATUS_READY,
            False,
        ),
        (
            lf("gr_construction_monitoring_settings"),
            "decided",
            WorkItem.STATUS_COMPLETED,
            True,
        ),
    ],
)
@pytest.mark.django_db
def test_maybe_start_construction_monitoring_after_decision(
    admin_user,
    caluma_admin_user,
    caluma_work_item_factory,
    gr_instance,
    init_status,
    mocker,
    request,
    set_application_gr,
    construction_settings,
    should_start,
):
    if init_status:
        caluma_work_item_factory(
            case=gr_instance.case,
            task_id=construction_settings["INIT_CONSTRUCTION_MONITORING_TASK"],
            status=init_status,
        )
    start = mocker.patch(
        "camac.instance.domain_logic.construction_monitoring.start_construction_monitoring"
    )

    maybe_start_construction_monitoring_after_decision(
        gr_instance, caluma_admin_user, admin_user
    )

    if should_start:
        start.assert_called_once_with(
            gr_instance,
            caluma_admin_user,
            admin_user,
            sender="post_complete_decision",
        )
    else:
        start.assert_not_called()


@pytest.mark.django_db
def test_construction_monitoring_dynamic_step_items(
    caluma_work_item_factory, caluma_case_factory, caluma_task_factory, mocker
):
    case = caluma_case_factory()
    tasks = [
        caluma_task_factory(
            pk=f"construction-step-{i}",
            meta={
                "construction-step": {"next": [], "index": i, "total": 3},
                "construction-step-id": "construction-step-test",
            },
        )
        for i in range(3)
    ]
    dynamic_tasks = CustomDynamicTasks()

    resolve_step = mocker.patch.object(
        dynamic_tasks, "resolve_after_construction_step", return_value=[]
    )
    can_continue = mocker.patch(
        "camac.caluma.extensions.dynamic_tasks.can_continue_construction_step",
        return_value=True,
    )

    def create_task_work_item(task):
        return caluma_work_item_factory(case=case, task=task, meta=task.meta)

    # resolve step 0, should return step 1
    step0 = create_task_work_item(tasks[0])
    assert dynamic_tasks.resolve_after_construction_step_item(
        case=case, prev_work_item=step0, user=None, context={}
    ) == [str(tasks[1].pk)]

    # resolve step 1, should return step 2
    step1 = create_task_work_item(tasks[1])
    assert dynamic_tasks.resolve_after_construction_step_item(
        case=case, prev_work_item=step1, user=None, context={}
    ) == [str(tasks[2].pk)]

    # when step 1 is not approved, should go back to step 0
    can_continue.return_value = False
    assert dynamic_tasks.resolve_after_construction_step_item(
        case=case, prev_work_item=step1, user=None, context={}
    ) == [str(tasks[0].pk)]

    # no more steps after step 2, should call resolve_after_construction_step
    assert resolve_step.call_count == 0
    can_continue.return_value = True
    step2 = create_task_work_item(tasks[2])
    assert (
        dynamic_tasks.resolve_after_construction_step_item(
            case=case, prev_work_item=step2, user=None, context={}
        )
        == []
    )
    assert resolve_step.call_count == 1


@pytest.mark.freeze_time("2023-09-04")
@pytest.mark.django_db
def test_construction_monitoring_initial_state(
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
@pytest.mark.django_db
def test_init_construction_monitoring(
    sz_instance,
    sz_construction_monitoring_settings,
    application_settings,
    construction_monitoring_case_sz,
    caluma_admin_schema_executor,
    service,
    skip,
):
    case = sz_instance.case

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
        assert construction_stage.child_case.status == Case.STATUS_RUNNING
        assert (
            construction_stage.child_case.workflow_id
            == sz_construction_monitoring_settings["CONSTRUCTION_STAGE_WORKFLOW"]
        )


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db
def test_create_construction_stage(
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
@pytest.mark.django_db
def test_complete_construction_stage(
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
@pytest.mark.django_db
def test_complete_construction_monitoring(
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


@pytest.mark.django_db
def test_complete_construction_monitoring_schedules_ag_smartservice_done(
    ag_construction_monitoring_settings,
    ag_instance,
    caluma_admin_user,
    caluma_work_item_factory,
    mocker,
):
    construction_stage = caluma_work_item_factory(
        case=ag_instance.case,
        task_id=ag_construction_monitoring_settings["CONSTRUCTION_STAGE_TASK"],
        status=WorkItem.STATUS_READY,
    )
    complete_construction_monitoring = caluma_work_item_factory(
        case=ag_instance.case,
        task_id=ag_construction_monitoring_settings[
            "COMPLETE_CONSTRUCTION_MONITORING_TASK"
        ],
        status=WorkItem.STATUS_COMPLETED,
    )
    complete = mocker.patch("camac.agsmartservice.api.complete")

    post_complete_construction_monitoring(
        None,
        work_item=complete_construction_monitoring,
        user=caluma_admin_user,
        context={},
    )

    construction_stage.refresh_from_db()
    assert construction_stage.status == WorkItem.STATUS_SKIPPED
    complete.assert_called_once_with(ag_instance)


@pytest.mark.django_db
def test_skip_construction_monitoring_schedules_ag_smartservice_done(
    ag_construction_monitoring_settings,
    ag_instance,
    caluma_admin_user,
    caluma_work_item_factory,
    mocker,
):
    work_item = caluma_work_item_factory(
        case=ag_instance.case,
        task_id=ag_construction_monitoring_settings[
            "INIT_CONSTRUCTION_MONITORING_TASK"
        ],
        status=WorkItem.STATUS_COMPLETED,
    )
    complete = mocker.patch("camac.agsmartservice.api.complete")

    post_complete_init_construction_monitoring(
        None, work_item=work_item, user=caluma_admin_user, context={"skip": True}
    )

    complete.assert_called_once_with(ag_instance)


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("state_matches", [True, False])
@pytest.mark.django_db
def test_complete_construction_step_work_item(
    sz_instance,
    sz_construction_monitoring_settings,
    construction_monitoring_initialized_case_sz,
    caluma_admin_schema_executor,
    service,
    form_utils: FormUtils,
    notification_template,
    mocker,
    state_matches,
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
        name=sz_construction_monitoring_settings[
            "PREVIOUS_INSTANCE_STATE"
            if state_matches
            else "CONSTRUCTION_MONITORING_INSTANCE_STATE"
        ]
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
    if state_matches:
        ech_signal_mock.assert_called_once()
    else:
        ech_signal_mock.assert_not_called()


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
    ("construction_task", "service_slug", "is_addressed", "expected_visible"),
    [
        (False, "other-service", True, True),
        (False, "other-service", False, True),
        (False, "gvg", True, True),
        (False, "gvg", False, True),
        (True, "other-service", True, False),
        (True, "other-service", False, False),
        (True, "gvg", False, False),
        # gvg service can see construction monitoring when addressed.
        (True, "gvg", True, True),
    ],
)
@pytest.mark.django_db
def test_construction_monitoring_work_item_visibility_service_gvg_gr(
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
    workitems_id = {
        extract_global_id(edge["node"]["id"])
        for edge in result.data["allWorkItems"]["edges"]
    }

    if expected_visible:
        assert str(wi.pk) in workitems_id
    else:
        assert str(wi.pk) not in workitems_id


@pytest.mark.parametrize(
    ("module_settings", "allow_forms_setting", "should_be_allowed"),
    [
        (lf("disable_construction_monitoring_settings"), None, False),
        (lf("construction_monitoring_settings"), None, True),
        (lf("construction_monitoring_settings"), ["building-permit-camac"], True),
        (
            lf("construction_monitoring_settings"),
            ["no-building-permits-allowed-camac"],
            False,
        ),
    ],
)
@pytest.mark.django_db
def test_can_perform_construction_monitoring_allow_forms(
    instance,
    caluma_case_factory,
    caluma_document_factory,
    form_factory,
    # parametrize fixtures
    allow_forms_setting,
    module_settings,
    should_be_allowed,
    application_settings,
):
    application_settings["FORM_BACKEND"] = "camac-ng"
    instance.form.family = form_factory(name="building-permit-camac")
    instance.form.save()

    instance.case = caluma_case_factory(
        document=caluma_document_factory(form__slug="building-permit-caluma"),
    )
    instance.save()

    module_settings["ALLOW_FORMS"] = allow_forms_setting

    assert can_perform_construction_monitoring(instance) == should_be_allowed


@pytest.mark.parametrize(
    ("expected_value", "decision_answer"),
    [
        (True, "complete-check-baubewilligungspflichtig-baubewilligungspflichtig"),
        (
            False,
            "complete-check-baubewilligungspflichtig-nicht-baubewilligungspflichtig",
        ),
    ],
)
@pytest.mark.django_db
def test_can_perform_construction_monitoring_ur(
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
    application_settings,
):
    application_settings["FORM_BACKEND"] = "camac-ng"

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


@pytest.mark.django_db
def test_post_create_construction_control(
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


@pytest.mark.django_db
def test_post_complete_construction_control(
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


@pytest.mark.django_db
def test_post_create_plan_construction_stage_ur(
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("address_group", "target_service", "expected_access_level"),
    [
        ("geometer", "geometer", "geometer"),
        ("geometer_schnurgeruestabnahme", "geometer", "geometer"),
        ("geometer_schnurgeruestabnahme", None, None),
        ("gebaudeversicherung", "gvg", "distribution-service"),
    ],
)
@pytest.mark.parametrize("has_read_acl", [False, True])
def test_post_create_dynamic_addressed_work_item_gr(
    gr_instance,
    instance_service_factory,
    service_factory,
    caluma_task_factory,
    access_level_factory,
    gr_permissions_settings,
    set_application_gr,
    address_group,
    target_service,
    expected_access_level,
    has_read_acl,
):
    read_access_level = access_level_factory(pk="read")
    if expected_access_level:
        access_level_factory(pk=expected_access_level)

    task = caluma_task_factory(address_groups=[address_group])
    municipality = service_factory(service_group__name="municipality")
    instance_service_factory(
        instance=gr_instance,
        service=municipality,
        active=1,
    )
    addressed_services = [municipality]

    specialist = None
    if target_service == "geometer":
        specialist = service_factory()
        ServiceRelation.objects.create(
            receiver=municipality,
            provider=specialist,
            function=ServiceRelation.FUNCTION_GEOMETER,
        )
    elif target_service == "gvg":
        specialist = service_factory(slug="gvg")

    if specialist:
        addressed_services.append(specialist)

    case = gr_instance.case

    permission_manager = permissions_api.PermissionManager.for_anonymous()
    municipality_read_acl = permission_manager.grant(
        gr_instance,
        grant_type="SERVICE",
        access_level=read_access_level,
        service=municipality,
    )

    specialist_read_acl = None
    if has_read_acl and specialist:
        specialist_read_acl = permission_manager.grant(
            gr_instance,
            grant_type="SERVICE",
            access_level=read_access_level,
            service=specialist,
        )

    work_item = WorkItem.objects.create(
        case=case,
        task_id=task.pk,
        name="Resolve after submit GR",
        addressed_groups=[str(service.pk) for service in addressed_services],
    )

    post_create_dynamic_addressed_work_item(None, work_item, None, None)
    post_create_dynamic_addressed_work_item(None, work_item, None, None)

    specialist_access_levels = (
        list(
            InstanceACL.currently_active()
            .filter(instance=case.family.instance, service=specialist)
            .values_list("access_level_id", flat=True)
        )
        if specialist
        else []
    )

    expected_access_levels = []
    if has_read_acl and specialist:
        expected_access_levels.append("read")
    if expected_access_level:
        expected_access_levels.append(expected_access_level)
    assert sorted(specialist_access_levels) == sorted(
        expected_access_levels,
    )

    if specialist_read_acl:
        specialist_read_acl.refresh_from_db()
        assert specialist_read_acl.end_time is None
        assert specialist_read_acl.revoked_by_event is None

    municipality_read_acl.refresh_from_db()
    assert municipality_read_acl.end_time is None
    assert municipality_read_acl.revoked_by_event is None


@pytest.mark.freeze_time("2026-01-01")
@pytest.mark.django_db
def test_start_after_submit_init_construction_monitoring_deadline(
    caluma_admin_user,
    caluma_case_factory,
    caluma_task_factory,
    caluma_work_item_factory,
    construction_monitoring_settings,
    decision_settings,
    service,
    freezer,
):
    """Tests deadlines of init work items when started after submit.

    If the construction monitoring process is already started after the
    submission of the instance, we need to handle the deadline of the
    `init-construction-monitoring` work item differently: It should only ever
    have a deadline if the instance is already decided. On decision, the work
    item (if still ready) should get a recalculated deadline.
    """

    construction_monitoring_settings["START_AFTER_SUBMIT"] = True

    init_task = caluma_task_factory(
        pk=construction_monitoring_settings["INIT_CONSTRUCTION_MONITORING_TASK"],
        lead_time=30 * 24 * 3600,  # 30d
    )

    case = caluma_case_factory()
    init_work_item = caluma_work_item_factory(
        case=case,
        task=init_task,
        addressed_groups=[str(service.pk)],
        deadline=init_task.calculate_deadline(),
        status=WorkItem.STATUS_READY,
    )
    decision_work_item = caluma_work_item_factory(
        case=case,
        task__pk=decision_settings["TASK"],
        status=WorkItem.STATUS_READY,
    )

    # No event fired yet, we should have a normally calculated deadline
    assert init_work_item.deadline.date() == date(2026, 1, 31)

    # After we call the event that would've been triggered after creation, we
    # shouldn't have a deadline anymore
    clear_init_construction_monitoring_deadline(
        None, work_item=init_work_item, user=None, context={}
    )
    init_work_item.refresh_from_db()
    assert init_work_item.deadline is None

    # If the decision work item is completed, the deadline will be freshly
    # calculated depending on the current date (now +30d)
    freezer.move_to("2026-03-12")
    set_construction_monitoring_deadlines_after_decision(
        None, work_item=decision_work_item, user=None, context={}
    )
    init_work_item.refresh_from_db()
    assert init_work_item.deadline.date() == date(2026, 4, 11)


@pytest.mark.freeze_time("2026-01-01")
@pytest.mark.django_db
def test_start_after_submit_complete_construction_monitoring_deadline(
    caluma_admin_user,
    caluma_case_factory,
    caluma_task_factory,
    caluma_work_item_factory,
    construction_monitoring_settings,
    decision_settings,
    service,
    freezer,
):
    """Tests deadlines of complete work items when started after submit.

    If the construction monitoring process is already started after the
    submission of the instance, we need to handle the deadline of the
    `complete-construction-monitoring` work item differently: It should only
    ever have a deadline if the instance is already decided. On decision, the
    work item (if still ready) should get a recalculated deadline. In addition
    to that, the work item deadline must be recalculated each time a stage is
    created, completed or canceled (same as when `START_AFTER_SUBMIT` is
    `False`, which is why we don't test this explicitly here).
    """

    construction_monitoring_settings["START_AFTER_SUBMIT"] = True

    complete_task = caluma_task_factory(
        pk=construction_monitoring_settings["COMPLETE_CONSTRUCTION_MONITORING_TASK"],
        lead_time=10 * 24 * 3600,  # 10d
    )

    case = caluma_case_factory()
    complete_work_item = caluma_work_item_factory(
        case=case,
        task=complete_task,
        addressed_groups=[str(service.pk)],
        deadline=complete_task.calculate_deadline(),
        status=WorkItem.STATUS_READY,
    )
    decision_work_item = caluma_work_item_factory(
        case=case,
        task__pk=decision_settings["TASK"],
        status=WorkItem.STATUS_READY,
    )

    # No event fired yet, we should have a normally calculated deadline
    assert complete_work_item.deadline.date() == date(2026, 1, 11)

    # After we call the event that would've been triggered after creation, we
    # shouldn't have a deadline anymore as the decision work item is not
    # completed yet
    post_create_complete_construction_monitoring(
        None, work_item=complete_work_item, user=None, context={}
    )
    complete_work_item.refresh_from_db()
    assert complete_work_item.deadline is None

    # If the decision work item is completed, the deadline will be freshly
    # calculated depending on the current date (now +10d)
    freezer.move_to("2026-03-12")
    decision_work_item.status = WorkItem.STATUS_COMPLETED
    decision_work_item.save(update_fields=["status"])
    set_construction_monitoring_deadlines_after_decision(
        None, work_item=decision_work_item, user=None, context={}
    )
    complete_work_item.refresh_from_db()
    assert complete_work_item.deadline.date() == date(2026, 3, 22)


@pytest.mark.parametrize(
    ("should_continue_after_decision", "current_status", "expected_status"),
    [
        (True, WorkItem.STATUS_READY, WorkItem.STATUS_READY),
        (True, WorkItem.STATUS_COMPLETED, WorkItem.STATUS_COMPLETED),
        (False, WorkItem.STATUS_READY, WorkItem.STATUS_COMPLETED),
        (False, WorkItem.STATUS_COMPLETED, WorkItem.STATUS_COMPLETED),
    ],
)
@pytest.mark.django_db
def test_skip_construction_monitoring_after_decision(
    caluma_admin_user,
    caluma_work_item_factory,
    construction_monitoring_settings,
    current_status,
    decision_settings,
    disable_ech0211_settings,  # Don't fire eCH-0211 events
    expected_status,
    mocker,
    sg_instance,
    should_continue_after_decision,
):
    """Tests that construction monitoring is skipped on a final decision.

    When construction monitoring is started after submit, the
    `init-construction-monitoring` work item is created before the decision is
    made. If the decision does not continue the case (e.g. a negative decision),
    the construction monitoring is obsolete and its still ready init work item
    should be completed on decision. If the case does continue, the init work
    item must stay ready.

    If the init work item is already completed (the municipality has already
    started the monitoring process), it is left untouched regardless of the
    decision.
    """

    construction_monitoring_settings["START_AFTER_SUBMIT"] = True
    construction_monitoring_settings["PREVIOUS_INSTANCE_STATE"] = (
        sg_instance.instance_state.name
    )
    construction_monitoring_settings["CONSTRUCTION_MONITORING_INSTANCE_STATE"] = (
        "construction-monitoring"
    )

    mocker.patch("camac.instance.models.Instance.set_instance_state")
    mocker.patch(
        "camac.instance.domain_logic.decision.DecisionLogic.should_continue_after_decision",
        return_value=should_continue_after_decision,
    )

    init_work_item = caluma_work_item_factory(
        case=sg_instance.case,
        task_id=construction_monitoring_settings["INIT_CONSTRUCTION_MONITORING_TASK"],
        status=current_status,
        child_case=None,
    )
    decision_work_item = caluma_work_item_factory(
        case=sg_instance.case,
        task_id=decision_settings["TASK"],
        status=WorkItem.STATUS_READY,
        child_case=None,
    )

    complete_work_item(decision_work_item, caluma_admin_user)

    init_work_item.refresh_from_db()

    assert init_work_item.status == expected_status
