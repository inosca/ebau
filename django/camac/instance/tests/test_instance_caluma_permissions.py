import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

FULL_PERMISSIONS = {
    "case-meta": ["read", "write"],
    "main": ["read", "write"],
    "sb1": ["read", "write"],
    "sb2": ["read", "write"],
    "nfd": ["read", "write"],
}


@pytest.mark.parametrize(
    "instance__user,service_group__name",
    [(LazyFixture("admin_user"), "construction-control")],
)
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_permissions",
    [
        (
            "Applicant",
            "new",
            {
                "case-meta": ["read"],
                "main": ["read", "write"],
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "subm",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "correction",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "rejected",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "sb1",
            {
                "case-meta": ["read"],
                "main": ["read"],
                "sb1": ["read", "write"],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb2",
            {
                "case-meta": ["read"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read", "write"],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "conclusion",
            {
                "case-meta": ["read"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": [],
            },
        ),
        (
            "Service",
            "new",
            {"case-meta": ["read"], "main": [], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Service",
            "subm",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Service",
            "correction",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Service",
            "rejected",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Service",
            "sb1",
            {"case-meta": ["read"], "main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Service",
            "sb2",
            {
                "case-meta": ["read"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Service",
            "conclusion",
            {
                "case-meta": ["read"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": [],
            },
        ),
        (
            "Municipality",
            "new",
            {"case-meta": ["read"], "main": [], "sb1": [], "sb2": [], "nfd": ["write"]},
        ),
        (
            "Municipality",
            "subm",
            {
                "case-meta": ["read", "write"],
                "main": ["read"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write"],
            },
        ),
        (
            "Municipality",
            "correction",
            {
                "case-meta": ["read", "write"],
                "main": ["read", "write"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write"],
            },
        ),
        (
            "Municipality",
            "rejected",
            {
                "case-meta": ["read", "write"],
                "main": ["read"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write"],
            },
        ),
        (
            "Municipality",
            "sb1",
            {
                "case-meta": ["read", "write"],
                "main": ["read"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write"],
            },
        ),
        (
            "Municipality",
            "sb2",
            {
                "case-meta": ["read", "write"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": [],
                "nfd": ["write"],
            },
        ),
        (
            "Municipality",
            "conclusion",
            {
                "case-meta": ["read", "write"],
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": ["write"],
            },
        ),
        ("Support", "new", FULL_PERMISSIONS),
        ("Support", "subm", FULL_PERMISSIONS),
        ("Support", "correction", FULL_PERMISSIONS),
        ("Support", "rejected", FULL_PERMISSIONS),
        ("Support", "sb1", FULL_PERMISSIONS),
        ("Support", "sb2", FULL_PERMISSIONS),
        ("Support", "conclusion", FULL_PERMISSIONS),
    ],
)
def test_instance_permissions(
    admin_client, activation, instance, expected_permissions, use_caluma_form
):
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    permissions = response.json()["data"]["meta"]["permissions"]

    assert permissions == expected_permissions


@pytest.fixture
def nfd_form(nfd_table_question):
    form = caluma_form_models.Form.objects.get(slug="nfd")
    caluma_form_factories.FormQuestionFactory(form=form, question=nfd_table_question)
    return form


@pytest.fixture
def nfd_status_question():
    return caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-status",
        # not entirely correct: it's actually an option,
        # but it's easier to mock this way
        type="text",
    )


@pytest.fixture
def row_form(nfd_status_question):
    form = caluma_form_factories.FormFactory()
    caluma_form_factories.FormQuestionFactory(form=form, question=nfd_status_question)
    return form


@pytest.fixture
def nfd_table_question(row_form):
    table_question = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-table", type="table", row_form=row_form
    )
    return table_question


@pytest.fixture
def nfd_case(instance, caluma_workflow, nfd_form):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(slug="building-permit"),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=BaseUser(),
    )

    return case


@pytest.fixture
def empty_document(nfd_case):
    workflow_api.complete_work_item(
        work_item=nfd_case.work_items.get(task_id="submit"), user=BaseUser()
    )

    return nfd_case.work_items.get(task_id="nfd").document


@pytest.fixture
def document_with_row_but_wrong_status(empty_document, instance, nfd_table_question):
    doc = empty_document
    doc.answers.create(question=nfd_table_question)

    return doc


@pytest.fixture
def document_with_all_rows(empty_document, row_form, nfd_table_question):
    doc = empty_document
    table_answer = doc.answers.create(question=nfd_table_question)
    # row 1
    row_1 = caluma_form_factories.DocumentFactory(form=row_form, family=doc)
    row_2 = caluma_form_factories.DocumentFactory(form=row_form, family=doc)
    row_3 = caluma_form_factories.DocumentFactory(form=row_form, family=doc)
    table_answer.documents.add(row_1)
    table_answer.documents.add(row_2)
    table_answer.documents.add(row_3)
    row_1.answers.create(
        question_id="nfd-tabelle-status", value="nfd-tabelle-status-entwurf"
    )
    row_2.answers.create(
        question_id="nfd-tabelle-status", value="nfd-tabelle-status-in-bearbeitung"
    )
    row_3.answers.create(
        question_id="nfd-tabelle-status", value="nfd-tabelle-status-erledigt"
    )

    return doc


@pytest.fixture
def document_with_row_and_erledigt(empty_document, row_form, nfd_table_question):
    doc = empty_document
    table_answer = doc.answers.create(question=nfd_table_question)
    row_1 = caluma_form_factories.DocumentFactory(form=row_form, family=doc)
    table_answer.documents.add(row_1)
    row_1.answers.create(
        question_id="nfd-tabelle-status", value="nfd-tabelle-status-erledigt"
    )

    return doc


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_nfd_permissions,caluma_doc",
    [
        ("Applicant", [], pytest.lazy_fixture("empty_document")),
        ("Applicant", [], pytest.lazy_fixture("document_with_row_but_wrong_status")),
        ("Applicant", ["read"], pytest.lazy_fixture("document_with_row_and_erledigt")),
        ("Applicant", ["read", "write"], pytest.lazy_fixture("document_with_all_rows")),
        ("Service", [], pytest.lazy_fixture("empty_document")),
        ("Municipality", ["write"], pytest.lazy_fixture("empty_document")),
        ("Support", ["read", "write"], pytest.lazy_fixture("empty_document")),
    ],
)
def test_instance_nfd_permissions(
    admin_client,
    activation,
    instance,
    expected_nfd_permissions,
    use_caluma_form,
    requests_mock,
    caluma_doc,
):
    url = reverse("instance-detail", args=[instance.pk])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["meta"]["permissions"]["nfd"]
        == expected_nfd_permissions
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "instance_state__name,group_name,form_slug,expected_permissions",
    [
        ("new", "municipality", "main", ["read", "write"]),
        ("new", "construction-control", "main", []),
        ("rejected", "municipality", "main", ["read"]),
        ("rejected", "construction-control", "main", ["read"]),
        ("sb1", "municipality", "sb1", []),
        ("sb1", "construction-control", "sb1", ["read", "write"]),
        ("sb2", "municipality", "sb2", []),
        ("sb2", "construction-control", "sb2", ["read", "write"]),
    ],
)
def test_instance_paper_permissions(
    admin_client,
    admin_user,
    role,
    instance,
    instance_state,
    group_name,
    form_slug,
    expected_permissions,
    use_caluma_form,
    mocker,
    group_factory,
    service_factory,
    user_group_factory,
    application_settings,
    instance_service_factory,
):
    mocker.patch("camac.caluma.api.CalumaApi.is_paper", lambda s, i: True)

    groups = {
        "municipality": group_factory(role=role),
        "construction-control": group_factory(role=role),
    }

    municipality_group = groups["municipality"]
    construction_control_group = groups["construction-control"]

    for name, group in groups.items():
        user_group_factory(group=group, user=admin_user)
        instance_service_factory(instance=instance, service=group.service)

    application_settings["PAPER"] = {
        "ALLOWED_ROLES": {
            "SB1": [construction_control_group.role.pk],
            "SB2": [construction_control_group.role.pk],
            "DEFAULT": [municipality_group.role.pk],
        },
        "ALLOWED_SERVICE_GROUPS": {
            "SB1": [construction_control_group.service.service_group.pk],
            "SB2": [construction_control_group.service.service_group.pk],
            "DEFAULT": [municipality_group.service.service_group.pk],
        },
    }

    response = admin_client.get(
        reverse("instance-detail", args=[instance.pk]),
        data={"group": groups.get(group_name).pk},
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["meta"]["permissions"][form_slug]
        == expected_permissions
    )
