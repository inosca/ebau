import io
import json

import pytest
from alexandria.core.models import File
from django.apps import apps
from django.urls import reverse
from rest_framework import status

from camac.alexandria.permissions import AlexandriaPermissionContext
from camac.document.tests.data import django_file
from camac.instance.models import Instance
from camac.permissions.api import P
from camac.permissions.switcher import PERMISSION_MODE


@pytest.fixture
def permission_mock(settings, mocker, permissions_settings, alexandria_settings):
    alexandria_settings["USE_V2_PERMISSIONS"] = True
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

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


def assert_permissions(
    mock, expected_instance, expected_permissions, expected_check_only_required=None
):
    """Ensure permissions were called as expected.

    In multiple tests, we expect the core permissions to be checked as well as
    the alexandria module-specific permissions.
    """

    assert mock.call_count == 2

    base_call, module_specific_call = mock.call_args_list

    base_context, base_permissions = base_call[0]
    module_specific_context, module_specific_permissions, check_only_required = (
        module_specific_call[0]
    )

    assert isinstance(base_context, Instance)
    assert isinstance(module_specific_context, AlexandriaPermissionContext)

    assert base_context == module_specific_context.instance == expected_instance

    assert base_permissions == P("documents-write")
    assert module_specific_permissions == expected_permissions

    if expected_check_only_required is not None:
        assert check_only_required == expected_check_only_required


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

    assert_permissions(
        permission_mock,
        instance,
        P.any("test:all", "test:create"),
        expected_check_only_required=False,
    )


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_delete_document(
    db, admin_client, alexandria_data, in_child_category, instance, permission_mock
):
    _, document = alexandria_data(in_child_category)

    response = admin_client.delete(reverse("document-detail", args=[document.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert_permissions(
        permission_mock,
        instance,
        P.any("test:all", "test:delete"),
    )


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
        assert permission_mock.call_count == 1
        context, permissions = permission_mock.call_args_list[0][0]

        assert isinstance(context, Instance)
        assert permissions == P("documents-write")

    else:
        assert_permissions(permission_mock, instance, expected_permissions)


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

    assert_permissions(
        permission_mock,
        instance,
        P.any("test:all", "test:replace"),
    )


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

    assert_permissions(permission_mock, instance, expected_permissions)


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

    assert_permissions(
        permission_mock,
        instance,
        P.any("test:all", "test:create"),
    )


@pytest.mark.parametrize("in_child_category", [False, True])
def test_alexandria_permissions_webdav_document(
    db,
    admin_client,
    alexandria_data,
    in_child_category,
    instance,
    permission_mock,
    settings,
):
    _, document = alexandria_data(in_child_category)

    file = document.get_latest_original()
    file.mime_type = settings.ALEXANDRIA_MANABI_ALLOWED_MIMETYPES[0]
    file.save()

    response = admin_client.get(reverse("alexandria-webdav-detail", args=[document.pk]))

    assert response.status_code == status.HTTP_200_OK

    assert_permissions(
        permission_mock,
        instance,
        P.any("test:all", "test:replace"),
    )


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


def test_alexandria_base_permission(
    db, admin_client, alexandria_data, instance, permission_mock
):
    permission_mock.return_value = False
    category, document = alexandria_data()

    # Trigger early return in `has_permission_for_document` when trying to
    # create a new document without the base alexandria permission.
    create_response = admin_client.post(
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
    assert create_response.status_code == status.HTTP_403_FORBIDDEN
    assert permission_mock.call_count == 1

    # Reset permission manager mock call count
    permission_mock.reset_mock()

    # Trigger early return in `has_object_permission_for_document` when trying
    # to delete a document without the base alexandria permission.
    delete_response = admin_client.delete(
        reverse("document-detail", args=[document.pk])
    )
    assert delete_response.status_code == status.HTTP_403_FORBIDDEN
    assert permission_mock.call_count == 1

    # Reset permission manager mock call count
    permission_mock.reset_mock()

    # Trigger early return in `has_permission_for_file` when trying to upload a
    # new document version (replace) without the base alexandria permission.
    replace_response = admin_client.post(
        reverse("file-list"),
        data={
            "content": django_file("multiple-pages.pdf"),
            "name": "multiple-pages.pdf",
            "variant": File.Variant.ORIGINAL,
            "document": document.pk,
        },
        format="multipart",
    )
    assert replace_response.status_code == status.HTTP_403_FORBIDDEN
    assert permission_mock.call_count == 1


def test_alexandria_permissions_rbac(
    db,
    admin_client,
    alexandria_data,
    caplog,
    instance,
    permission_mock,
    permissions_settings,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    _, document = alexandria_data()

    response = admin_client.delete(reverse("document-detail", args=[document.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert permission_mock.call_count == 0

    base_message = (
        f"Requesting base alexandria permission:\n"
        f"\tExpression: {P('documents-write')}\n"
        f"\tInstance ID: {instance.pk}\n"
        f"\tDocument UUID: {document.pk}\n"
        f"=> Returning `True` as permission module is not fully enabled"
    )

    specific_message = (
        f"Requesting alexandria permissions:\n"
        f"\tExpression: P(test:all | test:delete)\n"
        f"\tInstance ID: {instance.pk}\n"
        f"\tDocument UUID: {document.pk}\n"
        f"=> Returning `True` as permission module is not fully enabled"
    )

    assert base_message in caplog.messages
    assert specific_message in caplog.messages
