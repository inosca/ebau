import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    TagFactory,
)
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
    expected_count,
):
    # directly readble
    applicant_category = CategoryFactory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = CategoryFactory(metainfo={"access": {"service": "InternalRead"}})

    DocumentFactory.create_batch(
        2, category=applicant_category, metainfo={"case_id": instance.pk}
    )
    DocumentFactory.create_batch(
        2, category=municipality_category, metainfo={"case_id": instance.pk}
    )

    # readable from service
    DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group,
        metainfo={"case_id": instance.pk},
    )
    DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group + 1,
        metainfo={"case_id": instance.pk},
    )

    # readable as invitee
    DocumentFactory(category=applicant_category, metainfo={"case_id": instance.pk})

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
    db,
    minio_mock,
    caluma_admin_user,
    instance,
    admin_client,
    role,
    expected_count,
):
    applicant_category = CategoryFactory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = CategoryFactory(metainfo={"access": {"service": "Internal"}})
    applicant_document = DocumentFactory(
        category=applicant_category, metainfo={"case_id": instance.pk}
    )
    municipality_document = DocumentFactory(
        category=municipality_category, metainfo={"case_id": instance.pk}
    )
    service_document = DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group,
        metainfo={"case_id": instance.pk},
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
def test_category_visibility(db, admin_client, role, expected_count, snapshot):
    CategoryFactory(
        metainfo={
            "access": {"applicant": "Admin", "municipality": "Read", "service": "Read"}
        }
    )
    CategoryFactory(metainfo={"access": {"municipality": "Read"}})
    CategoryFactory(
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

    url = reverse("tag-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
