import pytest
from alexandria.core.factories import DocumentFactory, FileFactory, TagFactory
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework.status import HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,instance__user,expected_count",
    [
        ("Applicant", LazyFixture("user"), 3),
        ("Municipality", LazyFixture("user"), 2),
        ("Service", LazyFixture("user"), 1),
    ],
)
def test_document_visibility(
    db,
    role,
    caluma_admin_user,
    admin_client,
    instance,
    category_factory,
    instance_alexandria_document_factory,
    expected_count,
):
    # directly readble
    applicant_category = category_factory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = category_factory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = category_factory(metainfo={"access": {"service": "Internal"}})

    DocumentFactory.create_batch(2, category=applicant_category)
    DocumentFactory.create_batch(2, category=municipality_category)

    # readable from service
    DocumentFactory(category=service_category, created_by_group=caluma_admin_user.group)

    # readable as invitee
    document = DocumentFactory(category=applicant_category)
    instance_alexandria_document_factory(instance=instance, document=document)

    url = reverse("document-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("Applicant", 3),
        ("Municipality", 2),
        ("Service", 1),
    ],
)
def test_file_visibility(
    db, caluma_admin_user, admin_client, category_factory, role, expected_count
):
    applicant_category = category_factory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = category_factory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = category_factory(metainfo={"access": {"service": "Internal"}})
    applicant_document = DocumentFactory(category=applicant_category)
    municipality_document = DocumentFactory(category=municipality_category)
    service_document = DocumentFactory(
        category=service_category, created_by_group=caluma_admin_user.group
    )
    FileFactory.create_batch(3, document=applicant_document)
    FileFactory.create_batch(2, document=municipality_document)
    FileFactory.create_batch(1, document=service_document)

    url = reverse("file-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("Applicant", 1),
        ("Municipality", 3),
        ("Service", 2),
    ],
)
def test_category_visibility(
    db, admin_client, role, expected_count, category_factory, snapshot
):
    category_factory(
        metainfo={
            "access": {"applicant": "Admin", "municipality": "Read", "service": "Read"}
        }
    )
    category_factory(metainfo={"access": {"municipality": "Read"}})
    category_factory(
        metainfo={"access": {"service": "Internal", "municipality": "Read"}}
    )

    url = reverse("category-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
    snapshot.assert_match(json["data"][0]["attributes"]["metainfo"])


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("Applicant", 1),
        ("Municipality", 2),
        ("Service", 2),
    ],
)
def test_tag_visibility(
    db,
    caluma_admin_user,
    application_settings,
    admin_client,
    role,
    expected_count,
):
    TagFactory(created_by_group=caluma_admin_user.group)
    public_tag = TagFactory()
    application_settings["ALEXANDRIA"]["PUBLIC_TAGS"] = [public_tag.pk]
    if role.name == "Applicant":
        application_settings["PORTAL_GROUP"] = caluma_admin_user.camac_group

    url = reverse("tag-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
