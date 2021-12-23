from datetime import timedelta

import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow import (
    api as workflow_api,
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from caluma.schema import schema
from django.utils import timezone


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Support", 3), ("Service", 1), ("TrustedService", 3), ("Applicant", 0)],
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
        case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
            form=caluma_form_models.Form.objects.get(pk="main-form"),
            user=caluma_admin_user,
        )
        instance.case = case
        instance.save()

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
        case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
            form=caluma_form_models.Form.objects.get(pk="main-form"),
            user=caluma_admin_user,
        )
        instance.case = case
        instance.save()

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
            user=caluma_admin_user,
        )
        instance.case = case
        instance.save()

        case.document.answers.create(question_id="is-paper", value="is-paper-no")

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
        case__instance__pk=visible_instance.pk
    )

    assert visible.count() == 4
    assert (
        set([str(_id) for _id in visible.values_list("id", flat=True)])
        == visible_workitems
    )

    # not so for not_visible_instance
    not_visible = caluma_workflow_models.WorkItem.objects.filter(
        case__instance__pk=not_visible_instance.pk
    )
    assert not_visible.count() == 4
    assert (
        set(
            [str(_id) for _id in not_visible.values_list("id", flat=True)]
        ).intersection(visible_workitems)
        == set()
    )


def test_public_visibility(
    db,
    rf,
):
    caluma_form_factories.QuestionFactory.create_batch(3)
    caluma_workflow_factories.CaseFactory.create_batch(3)

    questions_query = """
        query {
            allQuestions {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    questions_result = schema.execute(
        questions_query, context_value=rf.get("/graphql"), middleware=[]
    )

    assert len(questions_result.data["allQuestions"]["edges"]) == 3

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
    cases_request = rf.get("/graphql")
    cases_request.user = AnonymousUser()
    cases_result = schema.execute(
        cases_query, context_value=cases_request, middleware=[]
    )

    assert len(cases_result.data["allCases"]["edges"]) == 0


def test_public_document_visibility(
    db,
    rf,
    be_instance,
    application_settings,
    settings,
):
    application_settings["PUBLICATION_BACKEND"] = "caluma"

    publication_document = caluma_form_factories.DocumentFactory()
    caluma_form_factories.AnswerFactory(
        document=publication_document,
        question__slug="publikation-startdatum",
        date=timezone.now() - timedelta(days=1),
    )
    caluma_form_factories.AnswerFactory(
        document=publication_document,
        question__slug="publikation-ablaufdatum",
        date=timezone.now() + timedelta(days=12),
    )
    caluma_workflow_factories.WorkItemFactory(
        task_id="fill-publication",
        status="completed",
        document=publication_document,
        case=be_instance.case,
        closed_by_user="admin",
        meta={"is-published": True},
    )

    query = """
        query {
            allDocuments {
                edges {
                    node {
                        id
                        answers {
                            edges {
                                node {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    request = rf.get("/graphql")
    request.user = AnonymousUser()
    result = schema.execute(query, context_value=request, middleware=[])

    assert len(result.data["allDocuments"]["edges"]) == 2
    assert len(result.data["allDocuments"]["edges"][1]["node"]["answers"]["edges"]) == 2
