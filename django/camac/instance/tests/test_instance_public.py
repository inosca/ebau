from datetime import timedelta

import pytest
from caluma.caluma_form.factories import (
    AnswerFactory,
    DocumentFactory,
    DynamicOptionFactory,
)
from caluma.caluma_workflow.factories import WorkItemFactory
from django.conf import settings
from django.urls import clear_url_caches, reverse
from django.urls.exceptions import NoReverseMatch
from django.utils import timezone
from rest_framework import status

from camac.document import permissions
from camac.instance import urls


@pytest.fixture
def enable_public_urls(application_settings):
    application_settings["ENABLE_PUBLIC_ENDPOINTS"] = True
    urls.enable_public_caluma_instances()
    clear_url_caches()
    yield
    urls.urlpatterns.pop()
    clear_url_caches()


@pytest.fixture
def running_caluma_publication(db, caluma_publication, application_settings):
    application_settings["PUBLICATION_BACKEND"] = "caluma"

    def wrapper(instance):
        publication_document = DocumentFactory()
        AnswerFactory(
            document=publication_document,
            question_id="publikation-startdatum",
            date=timezone.now() - timedelta(days=1),
        )
        AnswerFactory(
            document=publication_document,
            question_id="publikation-ablaufdatum",
            date=timezone.now() + timedelta(days=12),
        )
        WorkItemFactory(
            task_id="fill-publication",
            status="completed",
            document=publication_document,
            case=instance.case,
            closed_by_user="admin",
        )

        return publication_document

    return wrapper


def test_public_caluma_instance_disabled():
    with pytest.raises(NoReverseMatch):
        reverse("public-caluma-instance")


@pytest.mark.parametrize("with_client", ["public", "admin"])
def test_public_caluma_instance_enabled_empty_qs(
    db,
    client,
    admin_client,
    instance_factory,
    with_client,
    enable_public_urls,
):
    instance_factory.create_batch(5)
    url = reverse("public-caluma-instance")

    if with_client == "public":
        resp = client.get(url)
    else:
        resp = admin_client.get(url, HTTP_X_CAMAC_PUBLIC_ACCESS=True)

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()["data"]) == 0


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "headers,num_queries,num_instances",
    [({}, 1, 0), ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, 3, 1)],
)
def test_public_caluma_instance_ur(
    db,
    application_settings,
    admin_client,
    ur_instance,
    enable_public_urls,
    publication_entry_factory,
    django_assert_num_queries,
    headers,
    num_queries,
    num_instances,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_uri"]["MASTER_DATA"]
    application_settings["PUBLICATION_DURATION"] = timedelta(days=30)
    application_settings["PUBLICATION_BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        instance=ur_instance,
        is_published=True,
    )

    ur_instance.case.meta["dossier-number"] = 123
    ur_instance.case.save()

    DynamicOptionFactory(
        slug=1,
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
        assert result[0]["attributes"]["dossier-nr"] == "123"
        assert result[0]["attributes"]["municipality"] == "Altdorf"


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
    application_settings,
    admin_client,
    admin_user,
    ur_instance,
    enable_public_urls,
    publication_entry_factory,
    django_assert_num_queries,
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

    application_settings["PUBLICATION_DURATION"] = timedelta(days=30)
    application_settings["PUBLICATION_BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
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
        {"demo": {"applicant": {permissions.AdminPermission: [section.pk]}}},
    )

    response = admin_client.get(reverse("attachment-list"), **headers)
    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_documents


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize(
    "headers,num_queries,num_instances",
    [({}, 2, 0), ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, 5, 1)],
)
def test_public_instance_sz(
    db,
    application_settings,
    admin_client,
    instance,
    publication_entry_factory,
    django_assert_num_queries,
    headers,
    num_queries,
    num_instances,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_schwyz"][
        "MASTER_DATA"
    ]
    application_settings["PUBLICATION_DURATION"] = timedelta(days=30)
    application_settings["PUBLICATION_BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
        instance=instance,
        is_published=True,
    )

    url = reverse("instance-list")

    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, {"instance": instance.pk}, **headers)

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_instances

    if num_instances > 0:
        assert result[0]["id"] == str(instance.pk)
        assert set(result[0]["meta"]["editable"]) == set()
        assert result[0]["meta"]["access-type"] == "public"


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
    admin_client,
    admin_user,
    instance,
    publication_entry_factory,
    django_assert_num_queries,
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

    application_settings["PUBLICATION_DURATION"] = timedelta(days=30)
    application_settings["PUBLICATION_BACKEND"] = "camac-ng"

    publication_entry_factory(
        publication_date=timezone.now() - timedelta(days=1),
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
            "demo": {
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
@pytest.mark.parametrize(
    "headers,num_queries,num_instances",
    [({}, 1, 0), ({"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, 3, 1)],
)
def test_public_caluma_instance_be(
    db,
    application_settings,
    admin_client,
    be_instance,
    enable_public_urls,
    django_assert_num_queries,
    running_caluma_publication,
    applicant_factory,
    headers,
    num_queries,
    num_instances,
):
    be_instance.involved_applicants.first().delete()

    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    running_caluma_publication(be_instance)

    be_instance.case.meta["ebau-number"] = "2021-55"
    be_instance.case.save()

    DynamicOptionFactory(
        slug=1,
        label={"de": "Bern", "fr": "Berne"},
        document=be_instance.case.document,
        question_id="gemeinde",
    )

    url = reverse("public-caluma-instance")

    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, {"instance": be_instance.pk}, **headers)

    assert response.status_code == status.HTTP_200_OK

    result = response.json()["data"]

    assert len(result) == num_instances

    if num_instances > 0:
        assert result[0]["id"] == str(be_instance.case.pk)
        assert result[0]["attributes"]["instance-id"] == be_instance.pk
        assert result[0]["attributes"]["dossier-nr"] == "2021-55"
        assert result[0]["attributes"]["municipality"] == "Bern"


def test_public_caluma_instance_municipality_filter(
    db,
    application_settings,
    admin_client,
    instance_factory,
    instance_with_case,
    enable_public_urls,
    caluma_workflow_config_be,
    running_caluma_publication,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    instances = [
        instance_with_case(instance) for instance in instance_factory.create_batch(5)
    ]

    for instance in instances:
        running_caluma_publication(instance)

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
