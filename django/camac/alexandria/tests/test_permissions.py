import pytest

from django.urls import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)


@pytest.mark.parametrize(
    "role,method,status_code,category__meta",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {"permissions": {"applicant": "Admin"}},
        ),
        ("applicant", "patch", HTTP_200_OK, {"permissions": {"applicant": "Admin"}}),
        (
            "applicant",
            "delete",
            HTTP_204_NO_CONTENT,
            {"permissions": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {"permissions": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "patch",
            HTTP_403_FORBIDDEN,
            {"permissions": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "delete",
            HTTP_403_FORBIDDEN,
            {"permissions": {"applicant": "Admin"}},
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {"permissions": {"service": "Write"}},
        ),
        ("service", "patch", HTTP_200_OK, {"permissions": {"service": "Write"}}),
        (
            "service",
            "delete",
            HTTP_403_FORBIDDEN,
            {"permissions": {"service": "Write"}},
        ),
    ],
)
def test_document_permission(
    db, client, document_factory, category, method, status_code, role
):
    url = reverse("document-list")

    data = {
        "data": {
            "type": "document",
            "attributes": {
                "title": {"de": "Important"},
            },
        },
        "relationships": {
            "category": {
                "data": {
                    "id": category.id,
                    "type": "category",
                },
            },
        },
    }

    if method in ["patch", "delete"]:
        doc = document_factory(title="Foo", category=category)
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(client, method)(url, data)

    assert response.status_code == status_code

    if method == "post":
        result = response.json()
        assert result["data"]["attributes"]["title"]["de"] == "Important"
    elif method == "patch":
        doc.refresh_from_db()
        assert doc.title == "Important"


def test_file_permission(db):
    url = reverse("file-list")


@pytest.mark.parametrize(
    "role,method,status_code",
    [
        ("applicant", "post", HTTP_403_FORBIDDEN),
        ("applicant", "delete", HTTP_403_FORBIDDEN),
        ("municipality", "post", HTTP_201_CREATED),
        ("municipality", "delete", HTTP_204_NO_CONTENT),
        ("municipality", "delete", HTTP_403_FORBIDDEN),
        ("service", "post", HTTP_201_CREATED),
        ("service", "patch", HTTP_200_OK),
        ("service", "patch", HTTP_403_FORBIDDEN),
        ("support", "post", HTTP_201_CREATED),
        ("support", "delete", HTTP_204_NO_CONTENT),
    ],
)
def test_tag_permission(db, client, tag_factory, role, method, status_code):
    tag = tag_factory(name="Foo")
    url = reverse("tag-list")

    data = {
        "data": {
            "type": "tag",
            "attributes": {
                "name": "Important",
            },
        },
    }

    if method in ["patch", "delete"]:
        url = reverse("tag-detail", args=[tag.pk])
        data["data"]["id"] = str(tag.pk)

    response = getattr(client, method)(url, data)

    assert response.status_code == status_code
    if status_code != HTTP_403_FORBIDDEN and method != "delete":
        result = response.json()
        assert result["data"]["attributes"]["name"] == "Important"


@pytest.mark.parametrize(
    "role,status_code",
    [
        ("applicant", HTTP_403_FORBIDDEN),
        ("municipality", HTTP_403_FORBIDDEN),
        ("service", HTTP_403_FORBIDDEN),
        ("support", HTTP_200_OK),
    ],
)
def test_category_permission(db, client, category, role, status_code):
    url = reverse("category-detail", args=[category.pk])

    response = client.delete(url)

    assert response.status_code == status_code
