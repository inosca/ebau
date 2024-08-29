import json

import pytest
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from django.core import mail

from camac.caluma.extensions.events.construction_monitoring import (
    can_perform_construction_monitoring,
    can_perform_construction_monitoring_ur,
    post_complete_construction_control,
    post_create_construction_control,
)
from camac.caluma.extensions.visibilities import CustomVisibility
from camac.instance.models import InstanceState


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
    construction_monitoring_initialized_case_sz,
    construction_stage_factory_sz,
    caluma_admin_schema_executor,
    caluma_admin_user,
    service,
    distribution_settings,
    cancel,
    utils,
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
        utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
        utils.add_answer(
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
    utils,
    notification_template,
    mocker,
):
    ech_signal_mock = mocker.patch(
        "camac.ech0211.signals.construction_monitoring_started.send"
    )

    plan_stage = construction_monitoring_initialized_case_sz.work_items.first()
    utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
    utils.add_answer(
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


@pytest.mark.parametrize(
    "allow_forms_setting,allow_caluma_forms_setting,should_be_allowed",
    [
        (None, ["building-permit-caluma"], True),
        (["building-permit-camac"], None, True),
        (["no-building-permits-allowed-camac"], None, False),
        (None, ["no-building-permits-allowed-caluma"], False),
    ],
)
def test_can_perform_construction_monitoring_allow_forms(
    db,
    instance,
    construction_monitoring_settings,
    case_factory,
    document_factory,
    form_factory,
    # parametrize fixtures
    allow_forms_setting,
    allow_caluma_forms_setting,
    should_be_allowed,
):
    instance.form.family = form_factory(name="building-permit-camac")
    instance.save()
    case_factory(
        instance=instance,
        document=document_factory(form__slug="building-permit-caluma"),
    )

    construction_monitoring_settings["ALLOW_FORMS"] = allow_forms_setting
    construction_monitoring_settings["ALLOW_CALUMA_FORMS"] = allow_caluma_forms_setting

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
    case_factory,
    work_item_factory,
    document_factory,
    answer_factory,
    #
    expected_value,
    decision_answer,
):
    case_factory(instance=instance)
    complete_check_work_item = work_item_factory(
        case=instance.case, task__slug="complete-check", document=document_factory()
    )
    answer_factory(
        document=complete_check_work_item.document,
        question__slug="complete-check-baubewilligungspflichtig",
        value=decision_answer,
    )
    assert expected_value == can_perform_construction_monitoring_ur(instance)


def test_post_create_construction_control(
    db,
    instance_factory,
    case_factory,
    work_item_factory,
    document_factory,
    answer_factory,
    ur_construction_monitoring_settings,
):
    instance = instance_factory(case=case_factory())
    previous_construction_control_work_item = work_item_factory(
        case=instance.case,
        task__slug="construction-control",
        document=document_factory(),
        status=WorkItem.STATUS_COMPLETED,
    )
    answer_factory(
        document=previous_construction_control_work_item.document,
        question__slug="construction-control-date",
        date="2024-12-24",
    )
    construction_control_work_item = work_item_factory(
        case=instance.case, task_id="construction-control"
    )

    old_deadline = construction_control_work_item.deadline
    old_name = construction_control_work_item.name

    post_create_construction_control(
        None, user=None, work_item=construction_control_work_item, context={}
    )
    construction_control_work_item.refresh_from_db()

    assert (
        construction_control_work_item.name != old_name
    ), "the name should have been updated."
    assert (
        construction_control_work_item.deadline != old_deadline
    ), "the deadline should have been set accordingly."


def test_post_complete_construction_control(
    db,
    instance_factory,
    case_factory,
    work_item_factory,
    document_factory,
    answer_factory,
    construction_monitoring_settings,
    caluma_admin_user,
    instance_state_factory,
    ur_construction_monitoring_settings,
):
    instance = instance_factory(
        case=case_factory(),
        instance_state=instance_state_factory(name="some-instance-state"),
    )
    instance_state_factory(name="arch")

    construction_control_work_item = work_item_factory(
        case=instance.case,
        task__slug="construction-control",
        document=document_factory(),
    )
    answer_factory(
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
