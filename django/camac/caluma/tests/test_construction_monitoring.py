import json

import pytest
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from django.core import mail

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
        assert work_item.task.pk ==  sz_construction_monitoring_settings["CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK"]
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
):

    plan_stage = construction_monitoring_initialized_case_sz.work_items.first()
    utils.add_answer(plan_stage.document, "construction-stage-name", "Test")
    utils.add_answer(
    plan_stage.document, "construction-steps", ["construction-step-baubeginn"])
    sz_construction_monitoring_settings["NOTIFICATIONS"] = {
        plan_stage.task.pk: [{
            "template_slug": notification_template.slug,
            "recipient_types": ["leitbehoerde"],
        }]
    }

    sz_instance.instance_state = InstanceState.objects.get(name=sz_construction_monitoring_settings["PREVIOUS_INSTANCE_STATE"])
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

    assert sz_instance.instance_state.name == sz_construction_monitoring_settings["CONSTRUCTION_MONITORING_INSTANCE_STATE"]
    assert len(mail.outbox) == 1
    assert sz_instance.group.service.email in mail.outbox[0].recipients()
