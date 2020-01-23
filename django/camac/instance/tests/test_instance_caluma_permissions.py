import json

import pytest
from caluma.caluma_form import factories as caluma_form_factories
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

FULL_PERMISSIONS = {
    "main": ["read", "write", "write-meta"],
    "sb1": ["read", "write", "write-meta"],
    "sb2": ["read", "write", "write-meta"],
    "nfd": ["read", "write", "write-meta"],
}


@pytest.fixture
def mock_nfd_permissions(requests_mock):
    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps({"data": {"allDocuments": {"edges": []}}}),
    )


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_permissions",
    [
        (
            "Applicant",
            "new",
            {
                "main": [
                    "read",
                    "write",
                    "write-meta",  # write-meta camac-instance-id, submit-date
                ],
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        ("Applicant", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        (
            "Applicant",
            "correction",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": []},
        ),
        (
            "Applicant",
            "rejected",
            {
                "main": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb1": [],
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb1",
            {
                "main": ["read"],
                "sb1": ["read", "write", "write-meta"],  # write-meta: submit-date
                "sb2": [],
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read", "write", "write-meta"],  # write-meta: submit-date
                "nfd": [],
            },
        ),
        (
            "Applicant",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        ("Service", "new", {"main": [], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "subm", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "correction", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "rejected", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb1", {"main": ["read"], "sb1": [], "sb2": [], "nfd": []}),
        ("Service", "sb2", {"main": ["read"], "sb1": ["read"], "sb2": [], "nfd": []}),
        (
            "Service",
            "conclusion",
            {"main": ["read"], "sb1": ["read"], "sb2": ["read"], "nfd": []},
        ),
        (
            "Municipality",
            "new",
            {"main": [], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "subm",
            {
                "main": ["read", "write-meta"],  # write-meta: ebau-number
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "correction",
            {
                "main": ["read", "write"],
                "sb1": [],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "rejected",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb1",
            {"main": ["read"], "sb1": [], "sb2": [], "nfd": ["write", "write-meta"]},
        ),
        (
            "Municipality",
            "sb2",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": [],
                "nfd": ["write", "write-meta"],
            },
        ),
        (
            "Municipality",
            "conclusion",
            {
                "main": ["read"],
                "sb1": ["read"],
                "sb2": ["read"],
                "nfd": ["write", "write-meta"],
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
    admin_client,
    activation,
    instance,
    expected_permissions,
    use_caluma_form,
    mock_nfd_permissions,
):
    url = reverse("instance-detail", args=[instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    permissions = response.json()["data"]["meta"]["permissions"]

    assert permissions == expected_permissions


@pytest.fixture
def nfd_form(nfd_table_question):

    form = caluma_form_factories.FormFactory(slug="nfd")
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
def no_document():
    return None


@pytest.fixture
def root_doc(nfd_form):
    doc = caluma_form_factories.DocumentFactory(form=nfd_form)
    return doc


@pytest.fixture
def empty_document(root_doc, instance):

    root_doc.meta = {"camac-instance-id": instance.pk}
    root_doc.save()

    return root_doc


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
    row_1 = caluma_form_factories.DocumentFactory(form=row_form, family=doc.pk)
    row_2 = caluma_form_factories.DocumentFactory(form=row_form, family=doc.pk)
    row_3 = caluma_form_factories.DocumentFactory(form=row_form, family=doc.pk)
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
    row_1 = caluma_form_factories.DocumentFactory(form=row_form, family=doc.pk)
    table_answer.documents.add(row_1)
    row_1.answers.create(
        question_id="nfd-tabelle-status", value="nfd-tabelle-status-erledigt"
    )

    return doc


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_nfd_permissions,caluma_doc",
    [
        ("Applicant", [], pytest.lazy_fixture("no_document")),
        ("Applicant", [], pytest.lazy_fixture("empty_document")),
        ("Applicant", [], pytest.lazy_fixture("document_with_row_but_wrong_status")),
        ("Applicant", ["read"], pytest.lazy_fixture("document_with_row_and_erledigt")),
        ("Applicant", ["read", "write"], pytest.lazy_fixture("document_with_all_rows")),
        ("Service", [], pytest.lazy_fixture("no_document")),
        ("Municipality", ["write", "write-meta"], pytest.lazy_fixture("no_document")),
        (
            "Support",
            ["read", "write", "write-meta"],
            pytest.lazy_fixture("no_document"),
        ),
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
