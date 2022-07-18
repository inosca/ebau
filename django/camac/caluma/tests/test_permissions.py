import datetime
from unittest.mock import Mock

import pytest
import requests
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_save_work_item_permission(
    db,
    role,
    be_instance,
    service,
    service_factory,
    caluma_admin_schema_executor,
    caluma_admin_user,
):
    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="submit"),
        user=caluma_admin_user,
    )

    not_creator_work_item = caluma_workflow_models.WorkItem.objects.get(
        task_id="create-manual-workitems"
    )
    not_creator_work_item.created_by_group = service_factory().pk
    not_creator_work_item.save()

    assigned_work_item = caluma_workflow_models.WorkItem.objects.get(
        task_id="ebau-number"
    )

    result = caluma_admin_schema_executor(
        """
        mutation saveWorkItem {{
            saveWorkItem(
                input: {{workItem: "{work_item}", description: "Lorem ipsum"}}
            ) {{
                clientMutationId
                workItem {{
                    id
                    description
                }}
            }}
        }}
        """.format(
            work_item=assigned_work_item.pk
        )
    )

    if not role.name == "Municipality":
        assert result.errors
        return

    assert not result.errors
    assert result.data["saveWorkItem"]["workItem"]["description"] == "Lorem ipsum"

    result = caluma_admin_schema_executor(
        """
        mutation saveWorkItem {{
            saveWorkItem(
                input: {{workItem: "{work_item}", name: "{name}"}}
            ) {{
                clientMutationId
                workItem {{
                    id
                    name
                }}
            }}
        }}
        """.format(
            work_item=not_creator_work_item.pk, name="Good Name"
        )
    )

    assert result.errors

    result = caluma_admin_schema_executor(
        """
        mutation saveWorkItem {{
            saveWorkItem(
                input: {{workItem: "{work_item}", name: "{name}"}}
            ) {{
                clientMutationId
                workItem {{
                    id
                    name
                }}
            }}
        }}
        """.format(
            work_item=assigned_work_item.pk, name="Good Name"
        )
    )

    assigned_work_item.refresh_from_db()
    assert assigned_work_item.name == "Good Name"


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
            "suspended",
            False,
            None,
        ),
    ],
)
def test_distribution_permission_for_task(
    db,
    role,
    service,
    be_instance,
    caluma_admin_schema_executor,
    caluma_admin_user,
    active_inquiry_factory,
    instance_state_factory,
    work_item_factory,
    be_distribution_settings,
    mocker,
    application_settings,
    mutation,
    task,
    status,
    is_permitted,
    expected_status,
):

    work_item = active_inquiry_factory(
        be_instance,
        controlling_service=service,
        addressed_service=service,
        status=status,
    )
    if task != "INQUIRY_TASK":
        work_item = work_item_factory(
            case=work_item.case,
            child_case=None,
            addressed_groups=[service.pk],
            controlling_groups=[service.pk],
            task=caluma_workflow_models.Task.objects.get(
                pk=be_distribution_settings[task]
            ),
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
        if distribution_form == "INQUIRY_FORM"
        else service_factory(),
        addressed_service=service
        if distribution_form == "INQUIRY_ANSWER_FORM" and is_permitted
        else service_factory(),
        status=caluma_workflow_models.WorkItem.STATUS_SUSPENDED
        if distribution_form == "INQUIRY_FORM"
        else caluma_workflow_models.WorkItem.STATUS_READY,
    )

    document = (
        inquiry.document
        if distribution_form == "INQUIRY_FORM"
        else inquiry.child_case.document
    )

    if distribution_form == "INQUIRY_FORM" and is_permitted:
        work_item_factory(
            case=inquiry.case,
            child_case=None,
            addressed_groups=[service.pk],
            task=caluma_workflow_models.Task.objects.get(
                slug=be_distribution_settings["INQUIRY_CREATE_TASK"]
            ),
            status=caluma_workflow_models.WorkItem.STATUS_READY,
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
