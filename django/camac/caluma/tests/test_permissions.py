import pytest
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
    activation_factory,
    circulation_state_factory,
):
    activation_factory(
        circulation__instance=be_instance,
        service=service,
        circulation_state=circulation_state_factory(),
    )

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
