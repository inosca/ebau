import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import api as workflow_api
from django.conf import settings
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


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "instance_state__name",
    [
        "new",
        "subm",
        "rejected",
        "circulation_init",
        "circulation",
        "coordination",
        "correction",
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        # preliminary clarification
        "evaluated",
        # migrated
        "in_progress",
        # internal
        "in_progress_internal",
        "finished_internal",
    ],
)
@pytest.mark.parametrize(
    "role__name,service_group__name",
    [
        ("applicant", None),
        ("municipality-lead", "municipality"),
        ("municipality-lead", "district"),
        ("municipality-readonly", "municipality"),
        ("municipality-readonly", "district"),
        ("construction-control", "construction-control"),
        ("construction-control-readonly", "construction-control"),
        ("service-lead", "service"),
        ("service-readonly", "service"),
        ("support", None),
    ],
)
def test_instance_permissions_be(
    admin_client,
    activation,
    be_instance,
    instance_state,
    use_caluma_form,
    snapshot,
    application_settings,
):
    application_settings["ROLE_PERMISSIONS"] = settings.APPLICATIONS["kt_bern"][
        "ROLE_PERMISSIONS"
    ]
    application_settings["CALUMA"]["FORM_PERMISSIONS"] = settings.APPLICATIONS[
        "kt_bern"
    ]["CALUMA"]["FORM_PERMISSIONS"]
    application_settings["INSTANCE_PERMISSIONS"] = settings.APPLICATIONS["kt_bern"][
        "INSTANCE_PERMISSIONS"
    ]

    response = admin_client.get(reverse("instance-detail", args=[be_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(
        sort_permissions(response.json()["data"]["meta"]["permissions"])
    )


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize("role__name", ["Coordination", "Support"])
@pytest.mark.parametrize("instance_state__name", ["ext", "circ", "redac"])
def test_instance_permissions_ur(
    admin_client,
    activation,
    ur_instance,
    instance_state,
    use_caluma_form,
    snapshot,
    application_settings,
):
    application_settings["CALUMA"]["FORM_PERMISSIONS"] = settings.APPLICATIONS[
        "kt_uri"
    ]["CALUMA"]["FORM_PERMISSIONS"]

    response = admin_client.get(reverse("instance-detail", args=[ur_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(
        sort_permissions(response.json()["data"]["meta"]["permissions"])
    )


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
    be_instance,
    nfd_form,
    caluma_admin_user,
):
    return be_instance.case


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
    be_instance,
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
        instance_service_factory(instance=be_instance, service=group.service)

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
        reverse("instance-detail", args=[be_instance.pk]),
        data={"group": groups.get(group_name).pk},
    )

    assert response.status_code == status.HTTP_200_OK
    assert sorted(response.json()["data"]["meta"]["permissions"][form_slug]) == sorted(
        expected_permissions
    )
