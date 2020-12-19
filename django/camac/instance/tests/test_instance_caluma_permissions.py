import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

R = ["read"]
W = ["write"]
RW = R + W

FULL_PERMISSIONS = {
    "case-meta": RW,
    "main": RW,
    "sb1": RW,
    "sb2": RW,
    "nfd": RW,
    "dossierpruefung": RW,
}


def sort_permissions(permissions):
    return {key: sorted(value) for key, value in permissions.items()}


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
                "case-meta": R,
                "main": RW,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "subm",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "correction",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "rejected",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "sb1",
            {
                "case-meta": R,
                "main": R,
                "sb1": RW,
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "sb2",
            {
                "case-meta": R,
                "main": R,
                "sb1": R,
                "sb2": RW,
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Applicant",
            "conclusion",
            {
                "case-meta": R,
                "main": R,
                "sb1": R,
                "sb2": R,
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Service",
            "new",
            {
                "case-meta": R,
                "main": [],
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Service",
            "subm",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Service",
            "correction",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": [],
            },
        ),
        (
            "Service",
            "rejected",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": R,
            },
        ),
        (
            "Service",
            "sb1",
            {
                "case-meta": R,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": [],
                "dossierpruefung": R,
            },
        ),
        (
            "Service",
            "sb2",
            {
                "case-meta": R,
                "main": R,
                "sb1": R,
                "sb2": [],
                "nfd": [],
                "dossierpruefung": R,
            },
        ),
        (
            "Service",
            "conclusion",
            {
                "case-meta": R,
                "main": R,
                "sb1": R,
                "sb2": R,
                "nfd": [],
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "new",
            {
                "case-meta": R,
                "main": [],
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "subm",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "correction",
            {
                "case-meta": RW,
                "main": RW,
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "rejected",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "circulation_init",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": RW,
                "dossierpruefung": RW,
            },
        ),
        (
            "Municipality",
            "circulation",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": RW,
                "dossierpruefung": RW,
            },
        ),
        (
            "Municipality",
            "coordination",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": RW,
                "dossierpruefung": RW,
            },
        ),
        (
            "Municipality",
            "in_progress",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "in_progress_internal",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": RW,
                "dossierpruefung": RW,
            },
        ),
        (
            "Municipality",
            "sb1",
            {
                "case-meta": RW,
                "main": R,
                "sb1": [],
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "sb2",
            {
                "case-meta": RW,
                "main": R,
                "sb1": R,
                "sb2": [],
                "nfd": R,
                "dossierpruefung": R,
            },
        ),
        (
            "Municipality",
            "conclusion",
            {
                "case-meta": RW,
                "main": R,
                "sb1": R,
                "sb2": R,
                "nfd": R,
                "dossierpruefung": R,
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

    assert sort_permissions(permissions) == sort_permissions(expected_permissions)


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
def nfd_case(
    instance,
    caluma_workflow_config_be,
    nfd_form,
    caluma_admin_user,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(slug="building-permit"),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    return case


@pytest.fixture
def empty_document(nfd_case, caluma_admin_user):
    workflow_api.complete_work_item(
        work_item=nfd_case.work_items.get(task_id="submit"), user=caluma_admin_user
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
        ("Applicant", R, pytest.lazy_fixture("document_with_row_and_erledigt")),
        ("Applicant", RW, pytest.lazy_fixture("document_with_all_rows")),
        ("Service", [], pytest.lazy_fixture("empty_document")),
        ("Municipality", R, pytest.lazy_fixture("empty_document")),
        ("Support", RW, pytest.lazy_fixture("empty_document")),
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
    assert sorted(response.json()["data"]["meta"]["permissions"]["nfd"]) == sorted(
        expected_nfd_permissions
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "instance_state__name,group_name,form_slug,expected_permissions",
    [
        ("new", "municipality", "main", RW),
        ("new", "construction-control", "main", []),
        ("rejected", "municipality", "main", R),
        ("rejected", "construction-control", "main", R),
        ("sb1", "municipality", "sb1", []),
        ("sb1", "construction-control", "sb1", RW),
        ("sb2", "municipality", "sb2", []),
        ("sb2", "construction-control", "sb2", RW),
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
    assert sorted(response.json()["data"]["meta"]["permissions"][form_slug]) == sorted(
        expected_permissions
    )
