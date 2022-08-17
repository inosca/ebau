import json

import pytest


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_validate_create_inquiry_context(
    db,
    work_item_factory,
    service,
    be_instance,
    caluma_admin_schema_executor,
    distribution_settings,
):
    work_item = work_item_factory(case=be_instance.case, child_case=None)

    distribution_settings["INQUIRY_CREATE_TASK"] = work_item.task_id

    result = caluma_admin_schema_executor(
        """
        mutation($input: CompleteWorkItemInput!) {
            completeWorkItem(input: $input) {
                clientMutationId
            }
        }
        """,
        variables={
            "input": {
                "id": str(work_item.id),
                "context": json.dumps({"addressed_groups": [str(service.pk)]}),
            }
        },
    )

    assert result.errors
    assert "Services can't create inquiries for themselves!" in result.errors[0].message
