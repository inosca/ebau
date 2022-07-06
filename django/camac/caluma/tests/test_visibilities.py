from datetime import timedelta

import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_form import factories as caluma_form_factories
from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_workflow import (
    api as workflow_api,
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.api import skip_work_item
from caluma.schema import schema
from django.db.models import Q
from django.utils import timezone

from camac.caluma.extensions.visibilities import CustomVisibility, CustomVisibilitySZ


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Support", 3), ("Service", 1), ("TrustedService", 3), ("Applicant", 0)],
)
def test_document_visibility(
    db,
    active_inquiry_factory,
    admin_user,
    caluma_admin_schema_executor,
    caluma_workflow_config_be,
    expected_count,
    instance_factory,
    instance_with_case,
    role,
):
    group = admin_user.groups.first()

    instance = instance_with_case(instance_factory(group=group))
    instance_with_case(instance_factory(group=group))
    instance_with_case(instance_factory())

    active_inquiry_factory(instance, group.service)

    result = caluma_admin_schema_executor(
        """
        query {
            allDocuments(filter: [{ form: "main-form" }]) {
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
    active_inquiry_factory,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance_factory,
    instance_with_case,
    rf,
    role,
):
    group = admin_user.groups.first()

    instance1 = instance_with_case(instance_factory(group=group))
    active_inquiry_factory(
        instance1,
        group.service,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
    )

    instance2 = instance_with_case(instance_factory(group=group))
    active_inquiry_factory(
        instance2,
        group.service,
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
    )

    request = rf.get(
        "/graphql",
        **{"HTTP_X_CAMAC_FILTERS": "inquiry_state=pending"},
    )
    request.user = caluma_admin_user
    query = """
        query {
            allDocuments(filter: [{ form: "main-form" }]) {
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
def test_work_item_visibility_sz(
    db,
    admin_user,
    caluma_admin_schema_executor,
    caluma_admin_user,
    caluma_workflow_config_sz,
    distribution_settings,
    application_settings,
    instance_with_case,
    active_inquiry_factory,
    group_factory,
    instance_factory,
    role,
    mocker,
):

    mocker.patch(
        "caluma.caluma_core.types.Node.visibility_classes", [CustomVisibilitySZ]
    )

    group = admin_user.groups.first()
    instance = instance_with_case(instance_factory(group=group))

    controlling_group = group
    addressed_group = group_factory()
    other_group = group_factory()
    another_group = group_factory()

    application_settings["INTER_SERVICE_GROUP_VISIBILITIES"] = {
        controlling_group.service.service_group.pk: [
            other_group.service.service_group.pk
        ],
    }

    visible_workitems = [
        # visible: the corresponding instance is visible and task != inquiry
        caluma_workflow_factories.WorkItemFactory(
            task_id="complete-check", case=instance.case, status="completed"
        ).pk,
        # visible: service is in controlling_groups
        active_inquiry_factory(
            instance,
            addressed_service=addressed_group.service,
            controlling_service=controlling_group.service,
        ).pk,
        # visible: service is in addressed_groups
        active_inquiry_factory(
            instance,
            addressed_service=controlling_group.service,
            controlling_service=other_group.service,
        ).pk,
        # visible: service_group of other_group visible to controlling_group
        active_inquiry_factory(
            instance,
            addressed_service=other_group.service,
            controlling_service=addressed_group.service,
        ).pk,
    ] + list(
        # submit
        caluma_workflow_models.WorkItem.objects.filter(
            Q(case__family__instance__pk=instance.pk)
            & ~Q(task__pk=distribution_settings["INQUIRY_TASK"])
        ).values_list("id", flat=True)
    )

    # not visible: the corresponding instance is not visible
    caluma_workflow_factories.WorkItemFactory(
        task_id="complete-check",
        case=instance_with_case(instance_factory()).case,
        status="completed",
    )
    # not visible: service_group of another_group not visible to controlling_group
    active_inquiry_factory(
        instance,
        addressed_service=another_group.service,
        controlling_service=addressed_group.service,
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
    retrieved_workitems = set(
        [
            extract_global_id(edge["node"]["id"])
            for edge in result.data["allWorkItems"]["edges"]
        ]
    )

    assert len(retrieved_workitems) == 5

    assert retrieved_workitems == set(
        [str(work_item) for work_item in visible_workitems]
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_work_item_visibility(
    db,
    active_inquiry_factory,
    admin_user,
    caluma_admin_schema_executor,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance_factory,
    instance_with_case,
    role,
    mocker,
):
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])

    group = admin_user.groups.first()
    visible_instance = instance_with_case(instance_factory(group=group))
    not_visible_instance = instance_with_case(instance_factory())
    active_inquiry_factory(visible_instance, group.service)

    for instance in [visible_instance, not_visible_instance]:
        instance.case.document.answers.create(
            question_id="is-paper", value="is-paper-no"
        )

        # complete submit work item, there should now be 4 work items
        workflow_api.complete_work_item(
            work_item=instance.case.work_items.get(task_id="submit"),
            user=caluma_admin_user,
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
    assert (
        len(visible_workitems) == 5
    )  # submit, nfd, create-manual-workitem, ebau-number, inquiry

    # should be same as from graphql query
    visible = caluma_workflow_models.WorkItem.objects.filter(
        case__instance__pk=visible_instance.pk
    )
    assert visible.count() == 5
    assert (
        set([str(_id) for _id in visible.values_list("id", flat=True)])
        == visible_workitems
    )

    # not so for not_visible_instance
    not_visible = caluma_workflow_models.WorkItem.objects.filter(
        case__instance__pk=not_visible_instance.pk
    )
    assert not_visible.count() == 4  # submit, nfd, create-manual-workitem, ebau-number
    assert (
        set(
            [str(_id) for _id in not_visible.values_list("id", flat=True)]
        ).intersection(visible_workitems)
        == set()
    )


def test_public_visibility(
    db,
    rf,
    mocker,
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
    # public visibility used in Kt. SZ
    mocker.patch(
        "caluma.caluma_core.types.Node.visibility_classes", [CustomVisibilitySZ]
    )
    questions_result = schema.execute(
        questions_query, context_value=rf.get("/graphql"), middleware=[]
    )

    assert len(questions_result.data["allQuestions"]["edges"]) == 3

    # public visibility used in Kt. BE and Kt. UR
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])
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


@pytest.mark.parametrize(
    "role__name,service__name,expected_form_count_public,expected_form_count_sz",
    [
        # Kt. SZ specific roles
        ("Admin", "Service 0", 6, 4),
        ("Guest", "Service 0", 6, 2),
        ("Gemeinde", "Service 0", 6, 4),
        ("Portal", "Service 0", 6, 1),
        ("Fachstelle", "Service 0", 6, 2),
        ("Kanton", "Service 1", 6, 3),
        ("Fachstelle Sachbearbeiter", "Service 2", 6, 3),
        ("Gemeinde Sachbearbeiter", "Service 3", 6, 3),
        ("Publikation", "Service 0", 6, 1),
        ("Lesezugriff", "Service 0", 6, 2),
        ("Fachstelle Leitbehörde", "Service 0", 6, 3),
        ("Support", "Service 4", 6, 3),
    ],
)
def test_form_visibility_sz(
    db,
    rf,
    role,
    service,
    expected_form_count_public,
    expected_form_count_sz,
    group,
    token,
    user,
    settings,
    application_settings,
    role_factory,
    user_group_factory,
    group_factory,
    service_factory,
    mocker,
):
    """Visibility test configuration.

    The 6 test forms are configured with the following visibilites:

        Form 1: No visibility configured.
        Form 2: Public visibility.
        Form 3: Internal visibility.
        Form 4: Specific visibility for roles 'Admin' and 'Gemeinde' or
                for services 'Service 1', 'Service 2' and 'Service 3'.
        Form 5: Specific visibility for roles 'Admin', 'Gemeinde' and
                'Fachstelle Leitbehörde'.
        Form 6: Specific visibility for service 'Service 4'.

    In the CustomVisibility class all the forms are visible (expected_form_count_public).
    In the CustomVisibilitySZ class, the number of forms that are visible to
    the request user depends on their role and service (expected_form_count_sz).
    """
    # Kt. SZ specific public roles configuration
    application_settings["PUBLIC_ROLES"] = settings.APPLICATIONS["kt_schwyz"][
        "PUBLIC_ROLES"
    ]

    role_names = [
        "Publikation",
        "Portal",
        "Admin",
        "Gemeinde",
        "Fachstelle Leitbehörde",
    ]
    roles = {
        role_name: role_factory(name=role_name)
        for role_name in role_names
        if role_name != role.name
    }
    roles[role.name] = role

    service_names = [
        "Service 0",
        "Service 1",
        "Service 2",
        "Service 3",
        "Service 4",
    ]
    services = {
        service_name: service_factory(name=service_name)
        for service_name in service_names
        if service_name != service.name
    }
    services[service.name] = service

    group = group_factory(role=role, service=service)
    user_group_factory(group=group, user=user, default_group=1)

    oidc_user = OIDCUser(
        token=token,
        userinfo={
            settings.OIDC_USERNAME_CLAIM: user.username,
            settings.OIDC_GROUPS_CLAIM: [group.service_id],
            "sub": user.username,
        },
    )

    caluma_form_factories.FormFactory()
    caluma_form_factories.FormFactory(meta={"visibility": {"type": "public"}})
    caluma_form_factories.FormFactory(meta={"visibility": {"type": "internal"}})
    caluma_form_factories.FormFactory(
        meta={
            "visibility": {
                "type": "specific",
                "visibleFor": {
                    "roles": [roles["Admin"].pk, roles["Gemeinde"].pk],
                    "services": [
                        services["Service 1"].pk,
                        services["Service 2"].pk,
                        services["Service 3"].pk,
                    ],
                },
            }
        }
    )
    caluma_form_factories.FormFactory(
        meta={
            "visibility": {
                "type": "specific",
                "visibleFor": {
                    "roles": [
                        roles["Admin"].pk,
                        roles["Gemeinde"].pk,
                        roles["Fachstelle Leitbehörde"].pk,
                    ]
                },
            }
        }
    )
    caluma_form_factories.FormFactory(
        meta={
            "visibility": {
                "type": "specific",
                "visibleFor": {"services": [services["Service 4"].pk]},
            }
        }
    ),

    query = """
        query {
            allForms {
                edges {
                    node {
                        slug
                    }
                }
            }
        }
    """

    request = rf.get("/graphql")
    request.user = oidc_user

    # public form visibility used in Kt. BE and Kt. UR
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])
    result = schema.execute(query, context_value=request, middleware=[])
    assert len(result.data["allForms"]["edges"]) == expected_form_count_public

    # configurable form visibility used in Kt. SZ
    mocker.patch(
        "caluma.caluma_core.types.Node.visibility_classes", [CustomVisibilitySZ]
    )
    result = schema.execute(query, context_value=request, middleware=[])
    assert len(result.data["allForms"]["edges"]) == expected_form_count_sz


@pytest.mark.parametrize(
    "role__name,exclude_child_case,expected_count",
    [
        ("Support", "true", 1),
        ("Support", "false", 2),
        ("Service", "true", 1),
        ("Service", "false", 2),
        ("Municipality", "true", 1),
        ("Municipality", "false", 2),
        ("Applicant", "true", 0),
        ("Applicant", "false", 0),
    ],
)
def test_case_visibility_sz(
    rf,
    expected_count,
    caluma_admin_user,
    sz_instance,
    caluma_workflow_config_sz,
    exclude_child_case,
    distribution_settings,
    mocker,
):
    mocker.patch(
        "caluma.caluma_core.types.Node.visibility_classes", [CustomVisibilitySZ]
    )

    case = sz_instance.case

    skip_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )
    skip_work_item(
        work_item=case.work_items.get(task_id="complete-check"), user=caluma_admin_user
    )

    request = rf.get(
        "/graphql",
        **{"HTTP_X_CAMAC_FILTERS": f"exclude_child_cases={exclude_child_case}"},
    )
    request.user = caluma_admin_user

    query = """
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

    result = schema.execute(query, context_value=request, middleware=[])
    assert not result.errors
    assert len(result.data["allCases"]["edges"]) == expected_count
