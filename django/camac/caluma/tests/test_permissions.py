import datetime
import json
from unittest.mock import Mock

import pytest
import requests
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.utils.dateparse import parse_datetime
from inflection import underscore


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "involved_type,input,has_error",
    [
        (
            "creator",
            {
                "name": "Name change",
                "description": "Creator changes",
                "assignedUsers": ["3"],
                "deadline": "2022-11-16T00:00:00Z",
                "meta": json.dumps({"foo": "bar"}),
            },
            False,
        ),
        (
            "addressed",
            {
                "assignedUsers": ["3"],
                "meta": json.dumps({"foo": "bar"}),
            },
            False,
        ),
        ("addressed", {"name": "Bar"}, True),
        ("addressed", {"description": "Error"}, True),
        ("addressed", {"deadline": "2022-11-15T23:00:00Z"}, True),
        (
            "controller",
            {
                "description": "Controller changes",
                "deadline": "2022-11-15T00:00:00Z",
                "meta": json.dumps({"foo": "bar"}),
            },
            False,
        ),
        ("controller", {"name": "Bar"}, True),
        ("controller", {"assigned_users": ["1"]}, True),
    ],
)
def test_save_work_item_permission(
    caluma_admin_schema_executor,
    involved_type,
    input,
    has_error,
    snapshot,
    work_item_factory,
    service,
    be_instance,
    application_settings,
):
    work_item = work_item_factory(
        case=be_instance.case,
        name="Foo",
        description="Foo work item",
        created_by_group=str(service.pk) if involved_type == "creator" else None,
        addressed_groups=[str(service.pk)] if involved_type == "addressed" else [],
        controlling_groups=[str(service.pk)] if involved_type == "controller" else [],
        deadline=None,
    )

    if involved_type == "creator":
        application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"] = work_item.task_id

    mutation = """
        mutation($input: SaveWorkItemInput!) {
            saveWorkItem(input: $input) {
                clientMutationId
            }
        }
    """

    result = caluma_admin_schema_executor(
        mutation, variables={"input": {**input, "workItem": str(work_item.pk)}}
    )

    assert bool(result.errors) == has_error
    if not has_error:
        work_item.refresh_from_db()

        for key, value in input.items():
            if key == "deadline":
                value = parse_datetime(value)
            elif key == "meta":
                value = json.loads(value)

            assert getattr(work_item, underscore(key)) == value


@pytest.mark.parametrize(
    "role__name,mutation,task,status,is_permitted,expected_status",
    [
        (
            "municipality-lead",
            "completeWorkItem",
            "DISTRIBUTION_COMPLETE_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            True,
            "COMPLETED",
        ),
        (
            "municipality-clerk",
            "completeWorkItem",
            "DISTRIBUTION_COMPLETE_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            False,
            None,
        ),
        (
            "municipality-lead",
            "completeWorkItem",
            "INQUIRY_CHECK_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            True,
            "COMPLETED",
        ),
        (
            "municipality-clerk",
            "completeWorkItem",
            "INQUIRY_CHECK_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            False,
            None,
        ),
        (
            "municipality-lead",
            "cancelWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            True,
            "CANCELED",
        ),
        (
            "municipality-clerk",
            "cancelWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_READY,
            False,
            None,
        ),
        (
            "municipality-lead",
            "resumeWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
            True,
            "READY",
        ),
        (
            "municipality-clerk",
            "resumeWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
            False,
            None,
        ),
        (
            "municipality-lead",
            "redoWorkItem",
            "DISTRIBUTION_TASK",
            caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            True,
            "READY",
        ),
        (
            "municipality-clerk",
            "redoWorkItem",
            "DISTRIBUTION_TASK",
            caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            False,
            None,
        ),
        (
            "municipality-lead",
            "redoWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            True,
            "READY",
        ),
        (
            "municipality-clerk",
            "redoWorkItem",
            "INQUIRY_TASK",
            caluma_workflow_models.WorkItem.STATUS_COMPLETED,
            False,
            None,
        ),
    ],
)
def test_distribution_permission_for_task(
    db,
    active_inquiry_factory,
    be_distribution_settings,
    be_instance,
    caluma_admin_schema_executor,
    caluma_admin_user,
    expected_status,
    instance_state_factory,
    is_permitted,
    mocker,
    mutation,
    service,
    status,
    task,
    work_item_factory,
):
    work_item = active_inquiry_factory(
        be_instance,
        controlling_service=service,
        addressed_service=service,
        status=status,
    )

    if mutation == "redoWorkItem":
        if task == "DISTRIBUTION_TASK":
            work_item = be_instance.case.work_items.get(
                task_id=be_distribution_settings["DISTRIBUTION_TASK"]
            )
        elif task == "INQUIRY_TASK":
            work_item.status = caluma_workflow_models.WorkItem.STATUS_READY
            work_item.save()

            mocker.patch(
                "camac.caluma.extensions.events.distribution.send_inquiry_notification",
                return_value=None,
            )

        work_item.child_case.status = caluma_workflow_models.Case.STATUS_COMPLETED
        work_item.child_case.save()

        workflow_api.complete_work_item(work_item=work_item, user=caluma_admin_user)
    elif task != "INQUIRY_TASK":
        work_item = work_item_factory(
            case=work_item.case,
            child_case=None,
            addressed_groups=[service.pk],
            controlling_groups=[service.pk],
            task_id=be_distribution_settings[task],
            status=status,
        )

    # necessary for post_resume_work_item post_complete_work_item event handlers
    instance_state_factory(name="circulation")
    instance_state_factory(name="coordination")

    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    result = caluma_admin_schema_executor(
        """
        mutation {mutation} {{
            {mutation}(
            input: {{id: "{work_item}"}}
            ) {{
                clientMutationId
                workItem {{
                    id
                    status
                }}
            }}
        }}
        """.format(
            mutation=mutation, work_item=work_item.pk
        )
    )

    if not is_permitted:
        assert result.errors
        return

    assert not result.errors
    assert extract_global_id(result.data[mutation]["workItem"]["id"]) == str(
        work_item.pk
    )
    assert result.data[mutation]["workItem"]["status"] == expected_status


@pytest.mark.parametrize("is_permitted", [True, False])
@pytest.mark.parametrize(
    "role__name,mutation,distribution_form,question,value",
    [
        (
            "municipality-lead",
            "saveDocumentDateAnswer",
            "INQUIRY_FORM",
            "DEADLINE",
            datetime.date.today(),
        ),
        (
            "service-lead",
            "saveDocumentStringAnswer",
            "INQUIRY_FORM",
            "REMARK",
            "Test",
        ),
        (
            "subservice",
            "saveDocumentDateAnswer",
            "INQUIRY_FORM",
            "DEADLINE",
            datetime.date.today(),
        ),
        (
            "municipality-lead",
            "saveDocumentStringAnswer",
            "INQUIRY_ANSWER_FORM",
            "STATUS",
            "CLAIM",
        ),
        (
            "service-lead",
            "saveDocumentStringAnswer",
            "INQUIRY_ANSWER_FORM",
            "STATEMENT",
            "Test",
        ),
        (
            "subservice",
            "saveDocumentStringAnswer",
            "INQUIRY_ANSWER_FORM",
            "ANCILLARY_CLAUSES",
            "Test",
        ),
    ],
)
def test_distribution_permission_for_answer(
    db,
    role,
    service,
    be_instance,
    active_inquiry_factory,
    service_factory,
    caluma_admin_schema_executor,
    caluma_admin_user,
    work_item_factory,
    be_distribution_settings,
    mocker,
    mutation,
    distribution_form,
    question,
    value,
    is_permitted,
):
    response = Mock(spec=requests.models.Response)
    response.status_code = 200
    response.json.return_value = {
        "data": {
            "meta": {
                "permissions": {
                    "inquiry": {"read", "write"},
                    "inquiry-answer": {"read", "write"},
                }
            }
        }
    }
    mocker.patch.object(requests, "get", return_value=response)

    # Services need to have an invitation to have the instance visibility
    if distribution_form == "INQUIRY_FORM" and "service" in role.name:
        active_inquiry_factory(
            be_instance,
            addressed_service=service,
            status=caluma_workflow_models.WorkItem.STATUS_READY,
        )

    inquiry = active_inquiry_factory(
        be_instance,
        controlling_service=service
        if distribution_form == "INQUIRY_FORM" and is_permitted
        else service_factory(),
        addressed_service=service
        if distribution_form == "INQUIRY_ANSWER_FORM" and is_permitted
        else service_factory(),
        status=caluma_workflow_models.WorkItem.STATUS_SUSPENDED
        if distribution_form == "INQUIRY_FORM" and is_permitted
        else caluma_workflow_models.WorkItem.STATUS_READY,
    )

    document = (
        inquiry.document
        if distribution_form == "INQUIRY_FORM"
        else inquiry.child_case.document
    )

    question_slug = be_distribution_settings["QUESTIONS"][question]
    value = be_distribution_settings["ANSWERS"].get(question, {}).get(value) or value

    result = caluma_admin_schema_executor(
        """
        mutation {mutation} {{
            {mutation}(
            input: {{document: "{document}", question: "{question}", value: "{value}"}}
            ) {{
                clientMutationId
                answer {{
                    id
                }}
            }}
        }}
        """.format(
            mutation=mutation,
            document=document.pk,
            question=question_slug,
            value=value,
        )
    )

    if not is_permitted:
        assert result.errors
        return

    assert not result.errors
    answer = result.data[mutation]["answer"]
    assert extract_global_id(answer["id"]) == str(
        document.answers.filter(question=question_slug)
        .values_list("pk", flat=True)
        .first()
    )

    answer = document.answers.filter(question=question_slug)
    assert (
        answer.values_list(
            "value" if mutation == "saveDocumentStringAnswer" else "date", flat=True
        ).first()
        == value
    )
