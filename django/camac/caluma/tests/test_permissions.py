import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.utils import timezone

from camac.utils import is_lead_role


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
            "ready",
            True,
            "COMPLETED",
        ),
        (
            "municipality-clerk",
            "completeWorkItem",
            "DISTRIBUTION_COMPLETE_TASK",
            "ready",
            False,
            None,
        ),
        (
            "municipality-lead",
            "cancelWorkItem",
            "INQUIRY_TASK",
            "ready",
            True,
            "CANCELED",
        ),
        ("municipality-clerk", "cancelWorkItem", "INQUIRY_TASK", "ready", False, None),
        (
            "municipality-lead",
            "resumeWorkItem",
            "INQUIRY_TASK",
            "suspended",
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
def test_distribution_permission_for(
    db,
    role,
    group,
    instance,
    case_factory,
    task_factory,
    caluma_admin_schema_executor,
    caluma_admin_user,
    work_item_factory,
    distribution_settings,
    application_settings,
    mutation,
    task,
    status,
    is_permitted,
    expected_status,
):

    instance.case = case_factory()
    instance.save()
    work_item = work_item_factory(
        case=instance.case,
        child_case=None,
        addressed_groups=[group.service_id],
        controlling_groups=[group.service_id],
        task=task_factory(slug=distribution_settings[task]),
        status=status,
    )

    # necessary for post_resume_work_item event handler
    if mutation == "resumeWorkItem":
        question = caluma_form_models.Question.objects.create(
            slug=distribution_settings["QUESTIONS"]["DEADLINE"]
        )
        caluma_form_models.Answer.objects.create(
            question=question, document=work_item.document, date=timezone.now()
        )
        caluma_form_models.Form.objects.create(
            slug=distribution_settings["INQUIRY_ANSWER_FORM"]
        )
        caluma_workflow_models.Workflow.objects.create(
            slug=distribution_settings["INQUIRY_WORKFLOW"], allow_all_forms=True
        )

    application_settings["INTER_SERVICE_GROUP_VISIBILITIES"] = {}
    mutation_name = mutation[0].capitalize() + mutation[1:]
    distribution_settings["PERMISSIONS"] = {
        f"{mutation_name}": {
            f"{task}": lambda role: is_lead_role(role),
        },
    }

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
