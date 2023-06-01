import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework.status import HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,instance__user,expected_count",
    [
        ("applicant", LazyFixture("user"), 3),
        ("municipality", LazyFixture("user"), 2),
        ("service", LazyFixture("user"), 1),
    ],
)
def test_document_visibility(
    db, user, client, instance, category_factory, document_factory, expected_count
):
    # directly readble
    applicant_category = category_factory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = category_factory(
        metainfo={"access": {"municipality": "Write"}}
    )
    service_category = category_factory(metainfo={"access": {"service": "Internal"}})

    document_factory(category=applicant_category)
    document_factory(category=municipality_category)

    # readable from service
    document_factory(category=service_category, created_by_group=user.group)

    # readable as invitee
    document_factory(instance_document=instance, category=applicant_category)

    url = reverse("document-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role,expected_count",
    [
        ("applicant", 3),
        ("municipality", 2),
        ("service", 1),
    ],
)
def test_file_visibility(db, client, role, expected_count):
    url = reverse("file-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role,expected_count",
    [
        ("applicant", 1),
        ("municipality", 3),
        ("service", 2),
    ],
)
def test_category_visibility(db, client, role, expected_count):
    url = reverse("category-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role,expected_count",
    [
        ("applicant", 1),
        ("municipality", 3),
        ("service", 2),
    ],
)
def test_tag_visibility(db, client, role, expected_count):
    url = reverse("tag-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
