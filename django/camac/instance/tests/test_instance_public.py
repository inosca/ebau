from datetime import date, timedelta

import pytest
from caluma.caluma_form.factories import (
    AnswerFactory,
    DocumentFactory,
    DynamicOptionFactory,
)
from caluma.caluma_form.models import DynamicOption, Question
from caluma.caluma_workflow.factories import WorkItemFactory
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.document import permissions


@pytest.fixture
def create_caluma_publication(db, caluma_publication, publication_settings):
    publication_settings["BACKEND"] = "caluma"

    def wrapper(
        instance,
        start=timezone.now() - timedelta(days=1),
        end=timezone.now() + timedelta(days=12),
        published=True,
    ):
        publication_document = DocumentFactory()
        AnswerFactory(
            document=publication_document,
            question_id=publication_settings["RANGE_QUESTIONS"][0][0],
            date=start,
        )
        AnswerFactory(
            document=publication_document,
            question_id=publication_settings["RANGE_QUESTIONS"][0][1],
            date=end,
        )
        WorkItemFactory(
            task_id="fill-publication",
            status="completed",
            document=publication_document,
            case=instance.case,
            closed_by_user="admin",
            meta={"is-published": published},
        )

        return publication_document

    return wrapper


def test_public_caluma_instance_disabled(settings, admin_client):
    # "demo" is not configured in camac.user.permissions.PublicationPermission
    settings.APPLICATION_NAME = "demo"

    response = admin_client.get(
        reverse("public-caluma-instance"), HTTP_X_CAMAC_PUBLIC_ACCESS=True
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "is_authenticated,has_public_header,expected_status",
    [
        (False, False, status.HTTP_401_UNAUTHORIZED),
        (True, False, status.HTTP_403_FORBIDDEN),
        (False, True, status.HTTP_200_OK),
        (True, True, status.HTTP_200_OK),
    ],
)
def test_public_caluma_instance_enabled_empty_qs(
    db,
    client,
    admin_client,
    instance_factory,
    is_authenticated,
    has_public_header,
    expected_status,
):
    instance_factory.create_batch(5)

    used_client = admin_client if is_authenticated else client
    headers = {"HTTP_X_CAMAC_PUBLIC_ACCESS": True} if has_public_header else {}

    resp = used_client.get(reverse("public-caluma-instance"), **headers)

    assert resp.status_code == expected_status

    if resp.status_code == status.HTTP_200_OK:
        assert len(resp.json()["data"]) == 0


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "headers,num_queries,num_instances,form_type,expected",
    [
        ({}, 1, 0, "form-type-building-permit", "test"),
        (
            {"HTTP_X_CAMAC_PUBLIC_ACCESS": True},
            7,
            1,
            "form-type-commercial-permit",
            "Reklamegesuch",
        ),
        (
            {"HTTP_X_CAMAC_PUBLIC_ACCESS": True},
            7,
            1,
            "form-type-building-permit",
            "test",
        ),
        (
            {"HTTP_X_CAMAC_PUBLIC_ACCESS": True},
            7,
            1,
            "form-type-solar-announcement",
            "Solaranlage",
        ),
    ],
)
def test_public_caluma_instance_ur(
    db,
    publication_settings,
    admin_client,
    ur_instance,
    publication_entry_factory,
    django_assert_num_queries,
    headers,
    num_queries,
    num_instances,
    master_data_is_visible_mock,
    form_type,
    expected,
    settings,
):
    settings.APPLICATION_NAME = "kt_uri"
    publication_settings["BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        publication_end_date=timezone.now() + timedelta(days=30),
        instance=ur_instance,
        is_published=True,
    )

    ur_instance.case.meta["dossier-number"] = 123
    ur_instance.case.save()

    AnswerFactory(
        question_id="form-type",
        document=ur_instance.case.document,
        value=form_type,
    )

    AnswerFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        value="1",
    )
    AnswerFactory(
        question=Question.objects.create(
            slug="proposal-description", type=Question.TYPE_TEXT
        ),
        document=ur_instance.case.document,
        value="test",
    )

    DynamicOptionFactory(
        slug="1",
        label={"de": "Altdorf"},
        document=ur_instance.case.document,
        question_id="municipality",
    )

    url = reverse("public-caluma-instance")

    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, {"instance": ur_instance.pk}, **headers)

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_instances

    if num_instances > 0:
        assert result[0]["id"] == str(ur_instance.case.pk)
        assert result[0]["attributes"]["instance-id"] == ur_instance.pk
        assert result[0]["attributes"]["dossier-nr"] == 123
        assert result[0]["attributes"]["municipality"] == "Altdorf"
        assert result[0]["attributes"]["intent"] == expected


@pytest.mark.parametrize("role__name", ["Oereb Api"])
@pytest.mark.parametrize(
    "is_oereb_form,instance_state__name,num_queries,is_visible",
    [
        (True, "comm", 8, True),
        (False, "comm", 1, False),
        (True, "new", 2, False),
        (True, "new_portal", 2, False),
    ],
)
def test_public_caluma_instance_oereb_ur(
    db,
    application_settings,
    admin_client,
    ur_instance,
    django_assert_num_queries,
    num_queries,
    is_visible,
    form_factory,
    user_group_factory,
    group_factory,
    role,
    is_oereb_form,
    master_data_is_visible_mock,
):
    settings.APPLICATION_NAME = "kt_uri"
    application_settings["INSTANCE_HIDDEN_STATES"] = settings.APPLICATIONS["kt_uri"][
        "INSTANCE_HIDDEN_STATES"
    ]
    application_settings["USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT"] = True

    oereb_form = form_factory()
    if is_oereb_form:
        application_settings["OEREB_FORMS"] = [oereb_form.pk]

    ur_instance.form = oereb_form
    ur_instance.case.meta = {"dossier-number": "1201-20-001"}
    ur_instance.case.save()
    ur_instance.save()

    admin_client.user.groups.clear()

    oereb_group = group_factory(role=role)
    user_group_factory(user=admin_client.user, group=oereb_group)

    dynamic_option = DynamicOption.objects.create(
        document=ur_instance.case.document,
        question_id="leitbehoerde",
        slug="1",
        label="Leitbehörde Altdorf",
    )
    ur_instance.case.document.answers.create(
        question_id="leitbehoerde", value=dynamic_option.slug
    )

    AnswerFactory(
        question=Question.objects.create(
            slug="oereb-thema", type=Question.TYPE_MULTIPLE_CHOICE
        ),
        document=ur_instance.case.document,
        value=["oereb-thema-kpz"],
    )
    AnswerFactory(
        question=Question.objects.create(
            slug="typ-des-verfahrens", type=Question.TYPE_MULTIPLE_CHOICE
        ),
        document=ur_instance.case.document,
        value="typ-des-verfahrens-meldung",
    )

    url = reverse("public-caluma-instance")

    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url, {"instance": ur_instance.pk}, HTTP_X_CAMAC_GROUP=oereb_group.pk
        )

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == (1 if is_visible else 0)
    if is_visible:
        assert result[0]["id"] == str(ur_instance.case.pk)
        assert result[0]["attributes"]["oereb-topic"] == ["oereb-thema-kpz"]
        assert result[0]["attributes"]["legal-state"] == "typ-des-verfahrens-meldung"
        assert result[0]["attributes"]["dossier-nr"] == "1201-20-001"
        assert result[0]["attributes"]["authority"] == "Leitbehörde Altdorf"


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "headers,is_applicant,num_documents",
    [
        ({}, True, 2),
        ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, True, 1),
        ({}, False, 0),
        ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, False, 1),
    ],
)
def test_public_caluma_documents_ur(
    db,
    publication_settings,
    admin_client,
    admin_user,
    ur_instance,
    publication_entry_factory,
    attachment_section_factory,
    attachment_attachment_section_factory,
    applicant_factory,
    headers,
    is_applicant,
    num_documents,
    mocker,
):
    if is_applicant:
        applicant_factory(invitee=admin_user, instance=ur_instance)

    publication_settings["BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        publication_end_date=timezone.now() + timedelta(days=30),
        instance=ur_instance,
        is_published=True,
    )
    section = attachment_section_factory()
    attachment_attachment_section_factory(
        attachmentsection=section,
        attachment__context={"isPublished": True},
        attachment__instance=ur_instance,
    )
    attachment_attachment_section_factory(
        attachmentsection=section, attachment__instance=ur_instance
    )

    # fix attachment permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {"applicant": {permissions.AdminPermission: [section.pk]}}},
    )

    response = admin_client.get(reverse("attachment-list"), **headers)
    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_documents


@pytest.mark.parametrize("role__name", ["Applicant"])
def test_public_caluma_instance_sz(
    db,
    application_settings,
    publication_settings,
    admin_client,
    sz_instance,
    django_assert_num_queries,
    publication_entry_factory,
    form_field_factory,
    master_data_is_visible_mock,
):
    settings.APPLICATION_NAME = "kt_schwyz"
    publication_settings["BACKEND"] = "camac-ng"

    sz_instance.involved_applicants.first().delete()

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        publication_end_date=timezone.now() + timedelta(days=30),
        instance=sz_instance,
        is_published=True,
    )

    form_field_factory(
        instance=sz_instance,
        name="ortsbezeichnung-des-vorhabens",
        value="Teststrasse 6",
    )
    form_field_factory(
        instance=sz_instance, name="standort-spezialbezeichnung", value="Box"
    )
    form_field_factory(instance=sz_instance, name="standort-ort", value="Schübelbach")
    form_field_factory(
        instance=sz_instance, name="bezeichnung", value="This is a SZ test intent"
    )

    url = reverse("public-caluma-instance")

    with django_assert_num_queries(4):
        response = admin_client.get(
            url, {"instance": sz_instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
        )

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == 1

    assert result[0]["id"] == str(sz_instance.case.pk)
    assert result[0]["attributes"]["instance-id"] == sz_instance.pk
    assert result[0]["attributes"]["dossier-nr"] == sz_instance.identifier
    assert result[0]["attributes"]["municipality"] == sz_instance.location.name
    assert result[0]["attributes"]["form-description"] == sz_instance.form.description
    assert result[0]["attributes"]["intent"] == "This is a SZ test intent"
    assert result[0]["attributes"]["street"] == "Teststrasse 6, Box, Schübelbach"


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "headers,is_applicant,num_documents",
    [
        ({}, True, 2),
        ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, True, 1),
        ({}, False, 0),
        ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, False, 1),
    ],
)
def test_public_documents_sz(
    db,
    application_settings,
    publication_settings,
    admin_client,
    admin_user,
    instance,
    publication_entry_factory,
    attachment_section_factory,
    attachment_attachment_section_factory,
    applicant_factory,
    headers,
    is_applicant,
    num_documents,
    mocker,
):
    if is_applicant:
        applicant_factory(invitee=admin_user, instance=instance)

    publication_settings["BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        publication_end_date=timezone.now() + timedelta(days=30),
        instance=instance,
        is_published=True,
    )
    section = attachment_section_factory()
    section_public = attachment_section_factory()
    attachment_attachment_section_factory(
        attachmentsection=section_public,
        attachment__instance=instance,
    )
    attachment_attachment_section_factory(
        attachmentsection=section, attachment__instance=instance
    )

    application_settings["PUBLICATION_ATTACHMENT_SECTION"] = [section_public.pk]

    # fix attachment permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "test": {
                "applicant": {
                    permissions.AdminPermission: [section_public.pk, section.pk]
                }
            }
        },
    )

    response = admin_client.get(reverse("attachment-list"), **headers)
    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_documents


@pytest.mark.parametrize("role__name", ["Applicant"])
def test_public_caluma_instance_be(
    db,
    admin_client,
    be_instance,
    django_assert_num_queries,
    create_caluma_publication,
    master_data_is_visible_mock,
):
    settings.APPLICATION_NAME = "kt_bern"
    be_instance.involved_applicants.first().delete()

    create_caluma_publication(be_instance)

    be_instance.case.meta["ebau-number"] = "2021-55"
    be_instance.case.save()

    AnswerFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        value="1",
    )
    DynamicOptionFactory(
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
        document=be_instance.case.document,
        question_id="gemeinde",
    )

    url = reverse("public-caluma-instance")

    with django_assert_num_queries(9):
        response = admin_client.get(
            url, {"instance": be_instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
        )

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == 1

    assert result[0]["id"] == str(be_instance.case.pk)
    assert result[0]["attributes"]["instance-id"] == be_instance.pk
    assert result[0]["attributes"]["dossier-nr"] == "2021-55"
    assert result[0]["attributes"]["municipality"] == "Bern"


def test_public_caluma_instance_municipality_filter(
    db,
    admin_client,
    instance_factory,
    instance_with_case,
    caluma_workflow_config_be,
    create_caluma_publication,
    settings,
):
    settings.APPLICATION_NAME = "kt_bern"

    instances = [
        instance_with_case(instance) for instance in instance_factory.create_batch(5)
    ]

    for instance in instances:
        create_caluma_publication(instance)

    for instance in instances[:3]:
        AnswerFactory(
            question_id="gemeinde", value="1", document=instance.case.document
        )

    for instance in instances[3:]:
        AnswerFactory(
            question_id="gemeinde", value="2", document=instance.case.document
        )

    url = reverse("public-caluma-instance")

    response = admin_client.get(
        url,
        {"municipality": 1, "fields[public-caluma-instances]": "id"},
        HTTP_X_CAMAC_PUBLIC_ACCESS=True,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 3


def test_public_caluma_instance_form_type_filter(
    db,
    publication_settings,
    admin_client,
    instance_factory,
    instance_with_case,
    caluma_workflow_config_ur,
    publication_entry_factory,
):
    publication_settings["BACKEND"] = "camac-ng"

    instances = [
        instance_with_case(instance) for instance in instance_factory.create_batch(5)
    ]

    for instance in instances[:3]:
        AnswerFactory(
            question_id="form-type",
            value="form-type-baubewilligungsverfahren",
            document=instance.case.document,
        )

        publication_entry_factory(
            publication_date=timezone.now() - timedelta(days=1),
            publication_end_date=timezone.now() + timedelta(days=10),
            is_published=True,
            instance_id=instance.pk,
        )

    for instance in instances[3:]:
        AnswerFactory(
            question_id="form-type",
            value="does-not-exist",
            document=instance.case.document,
        )

    url = reverse("public-caluma-instance")

    response = admin_client.get(
        url,
        {
            "form_type": "form-type-baubewilligungsverfahren",
        },
        HTTP_X_CAMAC_PUBLIC_ACCESS=True,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 3


def test_information_of_neighbors_instance_be(
    db,
    publication_settings,
    client,
    be_instance,
):
    publication_settings["BACKEND"] = "caluma"

    be_instance.case.meta["ebau-number"] = "2021-55"
    be_instance.case.save()

    AnswerFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        value="1",
    )
    DynamicOptionFactory(
        slug=1,
        label={"de": "Bern", "fr": "Berne"},
        document=be_instance.case.document,
        question_id="gemeinde",
    )

    document = DocumentFactory()
    AnswerFactory(
        document=document,
        question__slug="information-of-neighbors-start-date",
        date=timezone.now().date() - timedelta(days=1),
    )
    AnswerFactory(
        document=document,
        question__slug="information-of-neighbors-end-date",
        date=timezone.now().date() + timedelta(days=1),
    )
    WorkItemFactory(
        task_id="information-of-neighbors",
        status="completed",
        document=document,
        case=be_instance.case,
        meta={"is-published": True},
    )

    url = reverse("public-caluma-instance")

    response = client.get(
        url,
        {"instance": be_instance.pk},
        HTTP_X_CAMAC_PUBLIC_ACCESS=True,
        HTTP_X_CAMAC_PUBLIC_ACCESS_KEY=str(document.pk)[:7],
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"])


@pytest.mark.freeze_time("2023-09-13")
@pytest.mark.parametrize(
    "publish_answer_slug,start_date_municipality,start_date_canton,end_date_municipality,end_date_canton,expected_instances",
    [
        (
            # start date municipality until end date municipality
            ["oeffentliche-auflage-ja"],
            date(2023, 9, 11),
            timezone.now().date(),
            date(2023, 9, 15),
            timezone.now().date(),
            1,
        ),
        (
            # start date canton until end date canton
            ["oeffentliche-auflage-ja"],
            timezone.now().date(),
            date(2023, 9, 11),
            timezone.now().date(),
            date(2023, 9, 15),
            1,
        ),
        (
            # start date municipality until end date canton
            ["oeffentliche-auflage-ja"],
            date(2023, 9, 11),
            timezone.now().date(),
            timezone.now().date(),
            date(2023, 9, 15),
            1,
        ),
        (
            # start date canton until end date municipality
            ["oeffentliche-auflage-ja"],
            timezone.now().date(),
            date(2023, 9, 11),
            date(2023, 9, 15),
            timezone.now().date(),
            1,
        ),
        (
            # current date inbetween both publications
            ["oeffentliche-auflage-ja"],
            date(2023, 9, 11),
            date(2023, 9, 14),
            date(2023, 9, 12),
            date(2023, 9, 15),
            0,
        ),
        (
            # no public instances
            ["oeffentliche-auflage-nein"],
            date(2023, 9, 11),
            timezone.now().date(),
            timezone.now().date(),
            date(2023, 9, 15),
            0,
        ),
        (
            # timeframe doesn't match
            ["oeffentliche-auflage-ja"],
            date(2023, 9, 9),
            date(2023, 9, 9),
            date(2023, 9, 11),
            date(2023, 9, 11),
            0,
        ),
    ],
)
def test_public_caluma_instance_gr(
    db,
    gr_publication_settings,
    client,
    gr_instance,
    publish_answer_slug,
    expected_instances,
    start_date_municipality,
    start_date_canton,
    end_date_municipality,
    end_date_canton,
):
    document = DocumentFactory()
    AnswerFactory(
        document=document,
        question__slug="oeffentliche-auflage",
        value=publish_answer_slug,
    )
    AnswerFactory(
        document=document,
        question__slug="beginn-publikationsorgan-gemeinde",
        date=start_date_municipality,
    )
    AnswerFactory(
        document=document,
        question__slug="beginn-publikation-kantonsamtsblatt",
        date=start_date_canton,
    )
    AnswerFactory(
        document=document,
        question__slug="ende-publikationsorgan-gemeinde",
        date=end_date_municipality,
    )
    AnswerFactory(
        document=document,
        question__slug="ende-publikation-kantonsamtsblatt",
        date=end_date_canton,
    )
    WorkItemFactory(
        task_id="fill-publication",
        status="completed",
        document=document,
        case=gr_instance.case,
        meta={"is-published": True},
    )

    url = reverse("public-caluma-instance")

    response = client.get(
        url, {"instance": gr_instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["data"]) == expected_instances


@pytest.mark.freeze_time("2022-04-12")
def test_disabled_publication(
    db,
    admin_client,
    be_instance,
    caluma_workflow_config_be,
    create_caluma_publication,
    settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    # active date range but disabled
    create_caluma_publication(
        instance=be_instance,
        start=date(2022, 4, 10),
        end=date(2022, 4, 20),
        published=False,
    )
    # inactive date range but published
    create_caluma_publication(
        instance=be_instance,
        start=date(2022, 4, 14),
        end=date(2022, 4, 24),
        published=True,
    )

    response = admin_client.get(
        reverse("public-caluma-instance"),
        HTTP_X_CAMAC_PUBLIC_ACCESS=True,
    )

    assert len(response.json()["data"]) == 0
