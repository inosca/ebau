import pytest
from alexandria.core.factories import DocumentFactory, FileFactory, TagFactory
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)


@pytest.mark.parametrize(
    "role__name,method,status_code,alexandria_category__metainfo",
    [
        (
            "Applicant",
            "post",
            HTTP_201_CREATED,
            {"access": {"applicant": "Admin"}},
        ),
        ("Applicant", "patch", HTTP_200_OK, {"access": {"applicant": "Admin"}}),
        (
            "Applicant",
            "delete",
            HTTP_204_NO_CONTENT,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Municipality",
            "patch",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Municipality",
            "delete",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Service",
            "post",
            HTTP_201_CREATED,
            {"access": {"service": "Write"}},
        ),
        ("Service", "patch", HTTP_200_OK, {"access": {"service": "Write"}}),
        (
            "Service",
            "delete",
            HTTP_403_FORBIDDEN,
            {"access": {"service": "Write"}},
        ),
    ],
)
def test_document_permission(
    db, role, admin_client, alexandria_category, method, status_code
):
    url = reverse("document-list")

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
            },
        },
        "relationships": {
            "category": {
                "data": {
                    "id": alexandria_category.pk,
                    "type": "category",
                },
            },
        },
    }

    if method in ["patch", "delete"]:
        doc = DocumentFactory(title="Foo", category=alexandria_category)
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code

    if method == "post":
        result = response.json()
        assert result["data"]["attributes"]["title"]["de"] == "Important"
    elif method == "patch":
        doc.refresh_from_db()
        assert doc.title == "Important"


@pytest.mark.parametrize(
    "role__name,method,status_code,alexandria_category__metainfo",
    [
        (
            "Applicant",
            "post",
            HTTP_201_CREATED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Applicant",
            "patch",
            HTTP_405_METHOD_NOT_ALLOWED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Applicant",
            "delete",
            HTTP_405_METHOD_NOT_ALLOWED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "Service",
            "post",
            HTTP_201_CREATED,
            {"access": {"service": "Write"}},
        ),
    ],
)
def test_file_permission(
    db, role, admin_client, alexandria_category, method, status_code
):
    doc = DocumentFactory(title="Foo", category=alexandria_category)
    url = reverse("file-list")

    data = {
        "data": {
            "type": "files",
            "attributes": {
                "title": {"de": "Important"},
            },
        },
        "relationships": {
            "document": {
                "data": {
                    "id": doc.pk,
                    "type": "document",
                },
            },
        },
    }

    if method in ["patch", "delete"]:
        file = FileFactory(name="File", document=doc)
        url = reverse("file-detail", args=[file.pk])
        data["data"]["id"] = str(file.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,method,status_code",
    [
        ("Applicant", "post", HTTP_403_FORBIDDEN),
        ("Applicant", "delete", HTTP_403_FORBIDDEN),
        ("Municipality", "post", HTTP_201_CREATED),
        ("Municipality", "delete", HTTP_204_NO_CONTENT),
        ("Municipality", "delete", HTTP_404_NOT_FOUND),
        ("Service", "post", HTTP_201_CREATED),
        ("Service", "patch", HTTP_200_OK),
        ("Service", "patch", HTTP_404_NOT_FOUND),
        ("Support", "post", HTTP_201_CREATED),
        ("Support", "delete", HTTP_204_NO_CONTENT),
    ],
)
def test_tag_permission(
    db, application_settings, role, caluma_admin_user, admin_client, method, status_code
):
    if role.name == "Applicant":
        application_settings["PORTAL_GROUP"] = caluma_admin_user.camac_group

    url = reverse("tag-list")

    data = {
        "data": {
            "type": "tags",
            "attributes": {
                "name": "Important",
            },
        },
    }

    if method in ["patch", "delete"]:
        alexandria_tag = TagFactory(name="Alexandria")
        url = reverse("tag-detail", args=[alexandria_tag.slug])
        data["data"]["id"] = str(alexandria_tag.slug)

        if status_code != HTTP_404_NOT_FOUND:
            alexandria_tag.created_by_group = caluma_admin_user.group
            alexandria_tag.save()

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code
    if (
        status_code not in [HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND]
        and method != "delete"
    ):
        result = response.json()
        assert result["data"]["attributes"]["name"] == "Important"


@pytest.mark.parametrize(
    "role__name,method",
    [
        ("Support", "patch"),
        ("Support", "post"),
        ("Support", "delete"),
    ],
)
def test_category_permission(
    db,
    role,
    admin_client,
    alexandria_category,
    method,
):
    url = reverse("category-list")

    data = {
        "data": {
            "type": "category",
            "attributes": {
                "name": "Important",
            },
        },
    }

    if method in ["patch", "delete"]:
        url = reverse("category-detail", args=[alexandria_category.pk])
        data["data"]["id"] = str(alexandria_category.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
