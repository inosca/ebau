import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    TagFactory,
)
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

import camac.alexandria.extensions.permissions_kt_gr as permissions_kt_gr


@pytest.mark.parametrize(
    "role__name,method,status_code,metainfo",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {"access": {"applicant": "Admin"}},
        ),
        ("applicant", "patch", HTTP_200_OK, {"access": {"applicant": "Admin"}}),
        (
            "applicant",
            "delete",
            HTTP_204_NO_CONTENT,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "patch",
            HTTP_404_NOT_FOUND,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "delete",
            HTTP_404_NOT_FOUND,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {"access": {"service": "Write"}},
        ),
        ("service", "patch", HTTP_200_OK, {"access": {"service": "Write"}}),
        ("service", "patch", HTTP_200_OK, {"access": {"service": "InternalAdmin"}}),
        (
            "service",
            "delete",
            HTTP_403_FORBIDDEN,
            {"access": {"service": "Write"}},
        ),
    ],
)
def test_document_permission(
    db, role, admin_client, caluma_admin_user, instance, metainfo, method, status_code
):
    alexandria_category = CategoryFactory(metainfo=metainfo)
    url = reverse("document-list")

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
                "metainfo": {"camac-instance-id": instance.pk},
            },
            "relationships": {
                "category": {
                    "data": {
                        "id": alexandria_category.pk,
                        "type": "categories",
                    },
                },
            },
        },
    }

    if method in ["patch", "delete"]:
        doc = DocumentFactory(
            title="Foo",
            category=alexandria_category,
            metainfo={"camac-instance-id": instance.pk},
            created_by_group=caluma_admin_user.group,
        )
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code

    if method == "post" and status_code == HTTP_201_CREATED:
        result = response.json()
        assert result["data"]["attributes"]["title"]["de"] == "Important"


@pytest.mark.parametrize(
    "role__name,method,status_code,metainfo",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "applicant",
            "patch",
            HTTP_405_METHOD_NOT_ALLOWED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "applicant",
            "delete",
            HTTP_405_METHOD_NOT_ALLOWED,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "Admin"}},
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {"access": {"service": "Write"}},
        ),
    ],
)
def test_file_permission(
    db, role, minio_mock, admin_client, instance, metainfo, method, status_code
):
    alexandria_category = CategoryFactory(metainfo=metainfo)
    doc = DocumentFactory(
        title="Foo",
        category=alexandria_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    url = reverse("file-list")

    data = {
        "data": {
            "type": "files",
            "attributes": {
                "name": "Old",
                "variant": "original",
            },
            "relationships": {
                "document": {
                    "data": {
                        "id": doc.pk,
                        "type": "documents",
                    },
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
        ("applicant", "post", HTTP_403_FORBIDDEN),
        ("applicant", "delete", HTTP_403_FORBIDDEN),
        ("municipality", "post", HTTP_201_CREATED),
        ("municipality", "delete", HTTP_204_NO_CONTENT),
        ("municipality", "delete", HTTP_404_NOT_FOUND),
        ("service", "post", HTTP_201_CREATED),
        ("service", "patch", HTTP_200_OK),
        ("service", "patch", HTTP_404_NOT_FOUND),
        ("support", "post", HTTP_201_CREATED),
        ("support", "delete", HTTP_204_NO_CONTENT),
    ],
)
def test_tag_permission(db, role, caluma_admin_user, admin_client, method, status_code):
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
        ("support", "patch"),
        ("support", "post"),
        ("support", "delete"),
    ],
)
def test_category_permission(
    db,
    role,
    admin_client,
    method,
):
    alexandria_category = CategoryFactory()
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


@pytest.mark.parametrize(
    "instance_state__name,role__name,service_group__name,method,status_code,metainfo",
    [
        # AdminNew
        (
            "new",
            "applicant",
            None,
            "post",
            HTTP_201_CREATED,
            {"access": {"applicant": "AdminNew"}},
        ),
        (
            "new",
            "applicant",
            None,
            "patch",
            HTTP_200_OK,
            {"access": {"applicant": "AdminNew"}},
        ),
        (
            "subm",
            "applicant",
            None,
            "post",
            HTTP_403_FORBIDDEN,
            {"access": {"applicant": "AdminNew"}},
        ),
        # InternalAdminCirculation
        (
            "subm",
            "service",
            "authority-bab",
            "delete",
            HTTP_404_NOT_FOUND,
            {"access": {"service": "InternalAdminCirculation"}},
        ),
        (
            "subm",
            "service",
            "service",
            "post",
            HTTP_201_CREATED,
            {"access": {"service": "InternalAdminCirculation"}},
        ),
        (
            "subm",
            "service",
            "service",
            "delete",
            HTTP_403_FORBIDDEN,
            {"access": {"service": "InternalAdminCirculation"}},
        ),
        (
            "circulation",
            "service",
            "service",
            "delete",
            HTTP_204_NO_CONTENT,
            {"access": {"service": "InternalAdminCirculation"}},
        ),
    ],
)
def test_kt_gr_permissions(
    db,
    role,
    set_application_gr,
    settings,
    mocker,
    admin_client,
    caluma_admin_user,
    instance,
    metainfo,
    method,
    status_code,
):
    settings.APPLICATION_NAME = "kt_gr"
    mocker.patch(
        "camac.alexandria.extensions.permissions.permissions", permissions_kt_gr
    )

    alexandria_category = CategoryFactory(metainfo=metainfo)
    url = reverse("document-list")

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
                "metainfo": {"camac-instance-id": instance.pk},
            },
            "relationships": {
                "category": {
                    "data": {
                        "id": alexandria_category.pk,
                        "type": "categories",
                    },
                },
            },
        },
    }

    if method in ["patch", "delete"]:
        doc = DocumentFactory(
            title="Foo",
            category=alexandria_category,
            metainfo={"camac-instance-id": instance.pk},
            created_by_group=caluma_admin_user.group,
        )
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code

    if method == "post" and status_code == HTTP_201_CREATED:
        result = response.json()
        assert result["data"]["attributes"]["title"]["de"] == "Important"


@pytest.mark.parametrize("role__name", ["applicant"])
def test_nested_permission(db, role, admin_client, instance):
    parent_category = CategoryFactory(metainfo={"access": {"applicant": "Admin"}})
    category = CategoryFactory(parent=parent_category)

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
                "metainfo": {"camac-instance-id": instance.pk},
            },
            "relationships": {
                "category": {
                    "data": {
                        "id": category.pk,
                        "type": "categories",
                    },
                },
            },
        },
    }

    response = admin_client.post(reverse("document-list"), data)
    assert response.status_code == HTTP_201_CREATED

    result = response.json()
    assert result["data"]["attributes"]["title"]["de"] == "Important"

    data["data"]["id"] = result["data"]["id"]
    data["data"]["attributes"]["title"]["de"] = "More important"

    patch_response = admin_client.patch(
        reverse("document-detail", args=[result["data"]["id"]]), data
    )
    assert patch_response.status_code == HTTP_200_OK

    patch_result = patch_response.json()
    assert patch_result["data"]["attributes"]["title"]["de"] == "More important"
