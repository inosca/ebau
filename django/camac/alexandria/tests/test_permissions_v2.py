import io
import json

import pytest
from alexandria.core.models import File
from django.apps import apps
from django.urls import reverse
from rest_framework import status

from camac.alexandria.permissions import AlexandriaPermissionContext
from camac.document.tests.data import django_file
from camac.permissions.api import P


@pytest.fixture
def permission_mock(settings, mocker):
    _original_visibility = settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES
    _original_permissions = settings.GENERIC_PERMISSIONS_PERMISSION_CLASSES

    settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES = []
    settings.GENERIC_PERMISSIONS_PERMISSION_CLASSES = [
        "camac.alexandria.extensions.permissions_v2.AlexandriaPermissions"
    ]

    apps.get_app_config("generic_permissions").ready()

    yield mocker.patch(
        "camac.permissions.api.PermissionManager.has_permission",
        return_value=True,
    )

    settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES = _original_visibility
    settings.GENERIC_PERMISSIONS_PERMISSION_CLASSES = _original_permissions

    apps.get_app_config("generic_permissions").ready()


@pytest.fixture
def alexandria_data(
    alexandria_category_factory,
    alexandria_document_factory,
    alexandria_file_factory,
    instance,
):
    def wrapper(in_child_category=False):
        parent_category = alexandria_category_factory(slug="test")
        child_category = alexandria_category_factory(
            slug="test-child", parent=parent_category
        )

        category = child_category if in_child_category else parent_category

        document = alexandria_document_factory(
            category=category, metainfo={"camac-instance-id": str(instance.pk)}
        )
        alexandria_file_factory(document=document)

        return category, document

    return wrapper


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_create_document(
    db, admin_client, alexandria_data, in_child_category, instance, permission_mock
):
    category, _ = alexandria_data(in_child_category)

    response = admin_client.post(
        reverse("document-list"),
        data={
            "content": django_file("multiple-pages.pdf"),
            "data": io.BytesIO(
                json.dumps(
                    {
                        "title": "Test.pdf",
                        "category": category.pk,
                        "metainfo": {"camac-instance-id": str(instance.pk)},
                    }
                ).encode("utf-8")
            ),
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_201_CREATED

    context, permissions = permission_mock.call_args[0]

    assert permission_mock.call_count == 1
    assert isinstance(context, AlexandriaPermissionContext)
    assert context.instance == instance
    assert permissions == P.any("test:all", "test:create")


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_delete_document(
    db, admin_client, alexandria_data, in_child_category, instance, permission_mock
):
    _, document = alexandria_data(in_child_category)

    response = admin_client.delete(reverse("document-detail", args=[document.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    context, permissions = permission_mock.call_args[0]

    assert permission_mock.call_count == 1
    assert isinstance(context, AlexandriaPermissionContext)
    assert context.instance == instance
    assert permissions == P.any("test:all", "test:delete")


@pytest.mark.parametrize("in_child_category", [False, True])
@pytest.mark.parametrize(
    ("data", "expected_permissions"),
    [
        pytest.param({}, None, id="no_changes"),
        pytest.param(
            {
                "attributes": {
                    "title": "Test!",
                    "date": "2025-11-12",
                    "description": "Test!",
                }
            },
            P("test:all") | P(P("test:update")),
            id="update",
        ),
        pytest.param(
            {
                "relationships": {
                    "marks": {"data": [{"id": "some-mark", "type": "marks"}]}
                }
            },
            P("test:all") | P(P.any("test:mark:all", P("test:mark:some-mark"))),
            id="mark",
        ),
        pytest.param(
            {
                "relationships": {
                    "tags": {
                        "data": [
                            {
                                "id": "aacb9ffe-acb5-4ebc-8262-9beaedad0cb6",
                                "type": "tags",
                            }
                        ]
                    }
                }
            },
            P("test:all") | P(P("test:tag")),
            id="tag",
        ),
        pytest.param(
            {
                "relationships": {
                    "category": {"data": {"id": "other-category", "type": "categories"}}
                },
            },
            (P("test:all") | P(P("test:move")))
            & P.any("other-category:all", "other-category:create"),
            id="move",
        ),
        pytest.param(
            {
                "attributes": {
                    "title": "Test!",
                },
                "relationships": {
                    "tags": {
                        "data": [
                            {
                                "id": "aacb9ffe-acb5-4ebc-8262-9beaedad0cb6",
                                "type": "tags",
                            }
                        ]
                    }
                },
            },
            P("test:all") | P.all(P("test:update"), P("test:tag")),
            id="update_and_tag",
        ),
    ],
)
def test_alexandria_permissions_update_document(
    db,
    admin_client,
    alexandria_category_factory,
    alexandria_data,
    alexandria_mark_factory,
    alexandria_tag_factory,
    data,
    expected_permissions,
    in_child_category,
    instance,
    permission_mock,
):
    _, document = alexandria_data(in_child_category)

    alexandria_tag_factory(pk="aacb9ffe-acb5-4ebc-8262-9beaedad0cb6")
    alexandria_mark_factory(pk="some-mark")
    alexandria_category_factory(pk="other-category")

    response = admin_client.patch(
        reverse("document-detail", args=[document.pk]),
        data={
            "data": {
                "id": document.pk,
                "type": "documents",
                **data,
            }
        },
    )

    assert response.status_code == status.HTTP_200_OK

    if expected_permissions is None:
        assert permission_mock.call_count == 0
    else:
        context, permissions = permission_mock.call_args[0]

        assert permission_mock.call_count == 1
        assert isinstance(context, AlexandriaPermissionContext)
        assert context.instance == instance
        assert permissions == expected_permissions


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_replace_document(
    db, admin_client, alexandria_data, in_child_category, instance, permission_mock
):
    _, document = alexandria_data(in_child_category)

    response = admin_client.post(
        reverse("file-list"),
        data={
            "content": django_file("multiple-pages.pdf"),
            "name": "multiple-pages.pdf",
            "variant": File.Variant.ORIGINAL,
            "document": document.pk,
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_201_CREATED

    context, permissions = permission_mock.call_args[0]

    assert permission_mock.call_count == 1
    assert isinstance(context, AlexandriaPermissionContext)
    assert context.instance == instance
    assert permissions == P.any("test:all", "test:replace")


@pytest.mark.parametrize("in_child_category", [False, True])
@pytest.mark.parametrize(
    ("target_category", "expected_permissions"),
    [
        (None, P.any("test:all", "test:create")),
        ("other-category", P.any("other-category:all", "other-category:create")),
        ("other-category-child", P.any("other-category:all", "other-category:create")),
    ],
)
def test_alexandria_permissions_copy_document(
    db,
    admin_client,
    alexandria_category_factory,
    alexandria_data,
    expected_permissions,
    in_child_category,
    instance,
    permission_mock,
    target_category,
):
    alexandria_category_factory(pk="other-category")
    alexandria_category_factory(pk="other-category-child", parent_id="other-category")

    _, document = alexandria_data(in_child_category)

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
        }
    }

    if target_category:
        data["data"]["relationships"] = {
            "category": {
                "data": {
                    "id": target_category,
                    "type": "categories",
                }
            }
        }

    response = admin_client.post(
        reverse("document-copy", args=[document.pk]), data=data
    )

    assert response.status_code == status.HTTP_201_CREATED

    context, permissions = permission_mock.call_args[0]

    assert permission_mock.call_count == 1
    assert isinstance(context, AlexandriaPermissionContext)
    assert context.instance == instance
    assert permissions == expected_permissions


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_convert_document(
    db,
    admin_client,
    alexandria_data,
    in_child_category,
    instance,
    permission_mock,
    requests_mock,
    settings,
):
    _, document = alexandria_data(in_child_category)

    requests_mock.post(
        f"{settings.ALEXANDRIA_DMS_URL}/convert",
        content=django_file("multiple-pages.pdf").read(),
    )

    response = admin_client.post(reverse("document-convert", args=[document.pk]))

    assert response.status_code == status.HTTP_201_CREATED

    context, permissions = permission_mock.call_args[0]

    assert permission_mock.call_count == 1
    assert isinstance(context, AlexandriaPermissionContext)
    assert context.instance == instance
    assert permissions == P.any("test:all", "test:create")


@pytest.mark.parametrize(
    ("role__name", "headers", "expected_status"),
    [
        ("Municipality", {}, status.HTTP_201_CREATED),
        ("Service", {}, status.HTTP_201_CREATED),
        ("Applicant", {}, status.HTTP_403_FORBIDDEN),
        ("Applicant", {"HTTP_X_CAMAC_PUBLIC_ACCESS": True}, status.HTTP_403_FORBIDDEN),
    ],
)
def test_alexandria_permissions_create_tag(
    db, admin_client, expected_status, headers, permission_mock
):
    response = admin_client.post(
        reverse("tag-list"),
        data={
            "data": {
                "id": None,
                "type": "tags",
                "attributes": {
                    "name": "test-tag",
                },
            }
        },
        **headers,
    )

    assert response.status_code == expected_status
    # A tag is a non-instance-related object, and thus it's creation cannot be
    # governed by the permissions module
    assert permission_mock.call_count == 0


def test_alexandria_base_permissions(
    db,
    permission_mock,
    admin_client,
    alexandria_file_factory,
    alexandria_mark_factory,
    alexandria_tag_factory,
):
    file = alexandria_file_factory()
    mark = alexandria_mark_factory()
    tag = alexandria_tag_factory()

    for url in [
        # Early return in `has_permission_for_file`
        reverse("file-detail", args=[file.pk]),
        # Early return in `has_permission_for_tag`
        reverse("tag-detail", args=[tag.pk]),
        # Fallback to `has_permission_default`
        reverse("mark-detail", args=[mark.pk]),
    ]:
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    assert permission_mock.call_count == 0
