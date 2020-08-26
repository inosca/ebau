import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.schema import schema


@pytest.mark.parametrize(
    "role__name,expected_count", [("Support", 3), ("Service", 1), ("Applicant", 0)]
)
def test_document_visibility(
    db,
    role,
    expected_count,
    instance_factory,
    activation_factory,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    caluma_admin_schema_executor,
):
    group = admin_user.groups.first()

    instance = instance_factory(group=group)
    activation_factory(circulation__instance=instance, service=group.service)

    for instance in [instance, instance_factory(group=group), instance_factory()]:
        workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
            form=caluma_form_models.Form.objects.get(pk="main-form"),
            meta={"camac-instance-id": instance.pk},
            user=caluma_admin_user,
        )

    result = caluma_admin_schema_executor(
        """
        query {
            allDocuments {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    )

    assert not result.errors
    assert len(result.data["allDocuments"]["edges"]) == expected_count

    cases_result = caluma_admin_schema_executor(
        """
        query {
            allCases {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    )

    assert not cases_result.errors
    assert len(cases_result.data["allCases"]["edges"]) == expected_count


@pytest.mark.parametrize("role__name", ["Support"])
def test_document_visibility_filter(
    db,
    rf,
    role,
    instance_factory,
    activation_factory,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    circulation_state,
    circulation_state_factory,
):
    group = admin_user.groups.first()

    instance1 = instance_factory(group=group)
    activation_factory(
        circulation__instance=instance1,
        service=group.service,
        circulation_state=circulation_state,
    )

    instance2 = instance_factory(group=group)
    activation_factory(
        circulation__instance=instance2,
        service=group.service,
        circulation_state=circulation_state_factory(),
    )

    for instance in [instance1, instance2]:
        workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
            form=caluma_form_models.Form.objects.get(pk="main-form"),
            meta={"camac-instance-id": instance.pk},
            user=caluma_admin_user,
        )

    request = rf.get(
        "/graphql",
        **{"HTTP_X_CAMAC_FILTERS": f"circulation_state={circulation_state.pk}"},
    )
    request.user = caluma_admin_user
    query = """
        query {
            allDocuments {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    result = schema.execute(query, context_value=request, middleware=[])

    assert not result.errors
    assert len(result.data["allDocuments"]["edges"]) == 1

    cases_query = """
        query {
            allCases {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    cases_result = schema.execute(cases_query, context_value=request, middleware=[])

    assert not cases_result.errors
    assert len(cases_result.data["allCases"]["edges"]) == 1


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_work_item_visibility(
    db,
    role,
    instance_factory,
    admin_user,
    caluma_admin_schema_executor,
    caluma_admin_user,
    caluma_workflow_config_be,
    activation_factory,
    circulation_state_factory,
):
    group = admin_user.groups.first()
    visible_instance = instance_factory(group=group)
    not_visible_instance = instance_factory()
    activation_factory(
        circulation__instance=visible_instance,
        service=group.service,
        circulation_state=circulation_state_factory(),
    )

    for instance in [visible_instance, not_visible_instance]:
        case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
            form=caluma_form_models.Form.objects.get(pk="main-form"),
            meta={"camac-instance-id": instance.pk},
            user=caluma_admin_user,
        )

        case.document.answers.create(
            question_id="papierdossier", value="papierdossier-nein"
        )

        # complete submit work item, there should now be 4 work items
        workflow_api.complete_work_item(
            work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
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
    """
    )

    assert not result.errors

    visible_workitems = set(
        [
            extract_global_id(edge["node"]["id"])
            for edge in result.data["allWorkItems"]["edges"]
        ]
    )
    assert len(visible_workitems) == 4

    # should be same as from graphql query
    visible = caluma_workflow_models.WorkItem.objects.filter(
        **{"case__meta__camac-instance-id": visible_instance.pk}
    )

    assert visible.count() == 4
    assert (
        set([str(_id) for _id in visible.values_list("id", flat=True)])
        == visible_workitems
    )

    # not so for not_visible_instance
    not_visible = caluma_workflow_models.WorkItem.objects.filter(
        **{"case__meta__camac-instance-id": not_visible_instance.pk}
    )
    assert not_visible.count() == 4
    assert (
        set(
            [str(_id) for _id in not_visible.values_list("id", flat=True)]
        ).intersection(visible_workitems)
        == set()
    )
