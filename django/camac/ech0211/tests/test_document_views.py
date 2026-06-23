from datetime import date
from functools import singledispatch
from io import StringIO

import pytest
from alexandria.core.factories import FileFactory
from alexandria.core.models import Document, File
from django.urls import reverse
from rest_framework import status
from syrupy.filters import paths

from camac.document import permissions
from camac.document.models import AttachmentSection
from camac.ech0211.models import ECH0211Document
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.modules.ech0211 import DocumentAPIFeature
from camac.utils import get_dict_item


@singledispatch
def iter_all_objects(val, prefix=""):
    yield val, prefix


@iter_all_objects.register
def iter_all_objects_dict(val: dict, prefix=""):
    yield val, prefix
    for k, v in val.items():
        yield from iter_all_objects(v, f"{prefix}.{k}")


@iter_all_objects.register
def iter_all_objects_list(val: list, prefix=""):
    yield val, prefix
    for i, v in enumerate(val):
        yield from iter_all_objects(v, f"{prefix}[{i}]")


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("document_backend", ["alexandria", "camac-ng"])
@pytest.mark.parametrize("role__name", ["municipality-lead"])
def test_document_details(
    settings,
    admin_client,
    document_backend,
    alexandria_document_factory,
    alexandria_file_factory,
    alexandria_category_factory,
    alexandria_mark_factory,
    be_instance,
    attachment_factory,
    admin_user,
    instance_acl_factory,
    be_permissions_settings,
    be_access_levels,
    attachment_section_factory,
    set_document_backend,
    be_alexandria_settings,
    disable_alexandria_features,
    role,
    mocker,
    snapshot,
):
    set_document_backend(document_backend)

    camac_cat = attachment_section_factory(description="foo")

    # We're only testing the view's data structure here, the visibilities
    # are tested in test_document_visibilities.py
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {role.name.lower(): {permissions.AdminPermission: [camac_cat.pk]}}},
    )

    alexandria_category_factory(
        slug="intern",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "service"},
            }
        },
    )

    user_service = admin_user.get_default_group().service

    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )

    camac_attachment = attachment_factory(
        instance=be_instance,
        user=admin_client.user,
        group=admin_client.user.get_default_group(),
        size=5,
    )
    alexandria_doc = alexandria_document_factory(
        category_id="intern",
        metainfo={"camac-instance-id": be_instance.pk},
        created_by_user=admin_client.user.pk,
        created_by_group=user_service.pk,
    )

    void_mark = alexandria_mark_factory(pk="void")
    alexandria_doc.marks.add(void_mark)

    # we want the attachment / document to have a file, so the test
    # represents that aspect as well
    camac_attachment.path.save("test.txt", StringIO("hello"), save=True)

    a_file = alexandria_file_factory(
        document=alexandria_doc, variant=File.Variant.ORIGINAL, size=5
    )
    a_file.content.save("test.txt", StringIO("hello"), save=True)

    camac_attachment.attachment_sections.set([camac_cat])

    docs = {
        "alexandria": alexandria_doc,
        "camac-ng": ECH0211Document.from_attachment(camac_attachment),
    }

    expected_pk = docs[document_backend].pk

    url = reverse("ech-document-detail", args=[expected_pk])
    ech_resp = admin_client.get(url, {"include": "category"})

    ech_doc = ech_resp.json()
    assert ech_resp.status_code == status.HTTP_200_OK, ech_doc

    def _t(expected_type):
        def require_type(val, key):
            assert isinstance(val, expected_type), (
                f"Check '{key}' for backend {document_backend}: "
                f"expected type {expected_type} but got {type(val)}"
            )

        return require_type

    def _v(expected_value):
        def require_value(val, key):
            assert val == expected_value, (
                f"Check '{key}' for backend {document_backend}: "
                f"expected value {expected_value} but got {val}"
            )

        return require_value

    seen_items = set()
    # We use the snapshot test to verify the full value of the returned
    # data - but we ensure that the structure exactly matches our expectations
    # explicitly
    checks = {
        "data": _t(dict),
        "data.id": _v(str(expected_pk)),
        "data.attributes": _t(dict),
        "data.attributes.date": _t(str),
        "data.attributes.title": _t(str),
        "data.attributes.description": _t(str | None),
        "data.attributes.created-at": _t(str),
        "data.attributes.mime-type": _t(str),
        "data.attributes.download-url": _t(str),
        "data.attributes.size": _v(5),
        "data.relationships": _t(dict),
        "data.relationships.category": _t(dict),
        "data.relationships.category.data.type": _v("ech0211-document-categories"),
        "data.relationships.category.data.id": _t(str),
        "data.relationships.instance": _t(dict),
        "data.relationships.instance.data.type": _v("instances"),
        "data.relationships.instance.data.id": _t(str),
        "data.relationships.created-by-user": _t(dict),
        "data.relationships.created-by-user.data.type": _v("users"),
        "data.relationships.created-by-user.data.id": _t(str),
        "data.relationships.created-by-service": _t(dict),
        "data.relationships.created-by-service.data.type": _v("services"),
        "data.relationships.created-by-service.data.id": _t(str),
        "data.type": _v("ech0211-documents"),
        "included": _t(list),
        "included.0.id": _t(str),
        "included.0.type": _v("ech0211-document-categories"),
        "included.0.attributes.name": _t(str),
        "included.0.attributes.full-name": _t(str),
        "included.0.attributes.description": _t(str | None),
        "included.0.relationships": _t(dict),
        "included.0.relationships.parent.data": _v(None),
    }

    if document_backend == "alexandria":
        checks.update(
            {
                "data.relationships.marks.meta.count": _t(int),
                "data.relationships.marks.data": _t(list),
                "data.relationships.marks.data.0.id": _v("void"),
                "data.relationships.marks.data.0.type": _v("marks"),
            }
        )

    for path, check in checks.items():
        val = get_dict_item(ech_doc, path, list_lookups=True, default=None)
        check(val, path)
        seen_items.add(id(val))

    # we want *only* the expected attributes here, nothing else
    for item, path in iter_all_objects(ech_doc):
        # We do not fully check that all the intermediate dicts are part of the
        # structure, therefore if it's a dict, and it's not in seen_items, we
        # don't fail the test
        assert id(item) in seen_items or isinstance(item, dict), (
            f"{path} was not checked, api has more data than test expects"
        )
    # In the snapshot, we don't want to compare DB identifiers either. The
    # Download URL also contains IDs as well as possible signatures, so can't
    # snapshot these either.
    assert ech_doc == snapshot(
        exclude=lambda prop, path: (
            prop == "download-url"
            # The marks ID is static so we can keep that, other id's should be removed.
            or (
                prop == "id"
                and not any(
                    segment[0] == "marks"
                    for segment in path
                    if isinstance(segment, tuple) and segment
                )
            )
        )
    )


def test_alexandria_full_category_name(
    settings,
    admin_client,
    alexandria_category_factory,
    set_document_backend,
    snapshot,
    mocker,
):
    set_document_backend("alexandria")

    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility.filter_queryset_for_category",
        side_effect=lambda queryset, request: queryset,
    )

    cat0, cat1, cat2 = alexandria_category_factory.create_batch(3)
    subcat0, subcat1 = alexandria_category_factory.create_batch(2, parent=cat1)

    url = reverse("ech-category-list")
    cat_list_data = admin_client.get(url).json()

    subcat0_data = next(c for c in cat_list_data["data"] if c["id"] == subcat0.pk)
    subcat1_data = next(c for c in cat_list_data["data"] if c["id"] == subcat1.pk)

    # Ensure proper hierarchical naming
    assert subcat0_data["attributes"]["full-name"] == f"{cat1.name} › {subcat0.name}"
    assert subcat1_data["attributes"]["full-name"] == f"{cat1.name} › {subcat1.name}"

    subcat0_parent = subcat0_data["relationships"]["parent"]
    subcat1_parent = subcat1_data["relationships"]["parent"]
    assert subcat0_parent["data"]["type"] == "ech0211-document-categories"
    assert subcat1_parent["data"]["type"] == "ech0211-document-categories"

    assert sorted(cat_list_data["data"], key=lambda x: x["id"]) == snapshot


@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
def test_category_list(
    settings,
    admin_client,
    alexandria_category_factory,
    set_document_backend,
    category_setup,
    document_backend,
    snapshot,
    mocker,
):
    set_document_backend(document_backend)

    alexandria_visibility_fn = mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility.filter_queryset_for_category",
        side_effect=lambda queryset, request: queryset,
    )

    camac_visibility_fn = mocker.patch(
        "camac.document.models.AttachmentSectionQuerySet.filter_group",
        side_effect=lambda self, *_: self,
        autospec=True,
    )

    some_cat, *cats = category_setup()

    view = reverse("ech-category-list")

    resp = admin_client.get(view)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == snapshot(
        exclude=paths(
            "data.0.id",
            "data.1.id",
            "data.2.id",
        )
    )

    # we've mocked the visibility functions / methods, but we still want to know
    # if the view code calls them correctly
    if document_backend == "camac-ng":
        assert camac_visibility_fn.call_count == 1
        assert alexandria_visibility_fn.call_count == 0
    elif document_backend == "alexandria":
        assert alexandria_visibility_fn.call_count == 1
        assert camac_visibility_fn.call_count == 0


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.django_db
def test_document_create_forbidden(
    set_document_backend,
    be_instance,
    set_application_be,
    admin_user,
    admin_client,
    document_backend,
):
    set_document_backend(document_backend)

    user_group = admin_user.get_default_group()

    data = {
        "data": {
            "type": "ech0211-documents",
            "attributes": {
                "name": "test.docx",
                "mime-type": "application/zip",
                "size": 1234,
            },
            "relationships": {
                "instance": {"data": {"id": None, "type": "instances"}},
                "category": {
                    "data": {"id": None, "type": "ech0211-document-categories"}
                },
            },
        }
    }
    url = reverse("ech-document-list")
    resp = admin_client.post(url, data, headers={"x-camac-group": str(user_group.pk)})

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert resp.json() == {
        "errors": [
            {
                "detail": 'Methode "POST" nicht erlaubt.',
                "status": "405",
                "source": {"pointer": "/data"},
                "code": "method_not_allowed",
            }
        ]
    }


@pytest.mark.freeze_time("2026-11-22")
@pytest.mark.parametrize("mark_name", ["void", "decision", "publication", "sensitive"])
@pytest.mark.parametrize("mark_action", ["add", "remove"])
@pytest.mark.parametrize("has_feature", [True, False])
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db
def test_document_mark_has_feature(
    settings,
    admin_client,
    mark_name,
    mark_action,
    has_feature,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_category_factory,
    instance_acl_factory,
    instance_state_factory,
    be_instance,
    admin_user,
    be_ech0211_settings,
    set_document_backend,
    be_permissions_settings,
    # TODO: Use alexandria permissions settings fixture
    # be_permissions_alexandria_settings,
    be_access_levels,
    be_alexandria_settings,
    role,
):
    # TODO: Set permissions mode to full as soon as alexandria permissions
    # settings fixture is used.
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    set_document_backend("alexandria")
    mark = alexandria_mark_factory(pk=mark_name)
    if has_feature:
        if mark_name == "void":
            be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
                DocumentAPIFeature.DOCUMENTS_VOID_ADD,
                DocumentAPIFeature.DOCUMENTS_VOID_REMOVE,
            ]
        elif mark_name == "publication":
            be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
                DocumentAPIFeature.DOCUMENTS_PUBLICATION_ADD,
                DocumentAPIFeature.DOCUMENTS_PUBLICATION_REMOVE,
            ]
        elif mark_name == "decision":
            be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
                DocumentAPIFeature.DOCUMENTS_DECISION_ADD,
                DocumentAPIFeature.DOCUMENTS_DECISION_REMOVE,
            ]
        elif mark_name == "sensitive":
            be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
                DocumentAPIFeature.DOCUMENTS_SENSITIVE_ADD,
                DocumentAPIFeature.DOCUMENTS_SENSITIVE_REMOVE,
            ]
    else:
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = []

    user_service = admin_user.get_default_group().service
    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )

    be_instance.instance_state = instance_state_factory(name="subm")
    be_instance.save()

    alexandria_category_factory(
        slug="alle-beteiligten",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "service"},
            }
        },
    )
    alexandria_doc = alexandria_document_factory(
        category_id="alle-beteiligten",
        metainfo={"camac-instance-id": be_instance.pk},
        created_by_user=admin_client.user.pk,
        created_by_group=user_service.pk,
    )
    if mark_action == "remove":
        alexandria_doc.marks.add(mark)

    url = reverse(f"ech-document-{mark_name}", args=[alexandria_doc.pk])
    ech_resp = (
        admin_client.post(url) if mark_action == "add" else admin_client.delete(url)
    )

    if has_feature:
        assert ech_resp.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert ech_resp.status_code == status.HTTP_404_NOT_FOUND, ech_resp.json()


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("mark_name", ["void", "decision", "publication", "sensitive"])
@pytest.mark.parametrize("mark_action", ["add", "remove"])
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db
def test_document_mark_camac(
    settings,
    admin_client,
    mark_name,
    mark_action,
    be_instance,
    attachment_factory,
    admin_user,
    instance_acl_factory,
    be_permissions_settings,
    be_access_levels,
    attachment_section_factory,
    set_document_backend,
    be_ech0211_settings,
    role,
    mocker,
):
    if mark_name == "void":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_VOID_ADD,
            DocumentAPIFeature.DOCUMENTS_VOID_REMOVE,
        ]
    elif mark_name == "publication":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_ADD,
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_REMOVE,
        ]
    elif mark_name == "decision":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_DECISION_ADD,
            DocumentAPIFeature.DOCUMENTS_DECISION_REMOVE,
        ]
    elif mark_name == "sensitive":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_ADD,
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_REMOVE,
        ]
    set_document_backend("camac-ng")

    camac_cat = attachment_section_factory(description="foo")

    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {role.name.lower(): {permissions.AdminPermission: [camac_cat.pk]}}},
    )

    user_service = admin_user.get_default_group().service
    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )
    camac_attachment = attachment_factory(
        instance=be_instance,
        user=admin_client.user,
        group=admin_client.user.get_default_group(),
        size=5,
    )

    camac_attachment.path.save("test.txt", StringIO("hello"), save=True)
    camac_attachment.attachment_sections.set([camac_cat])

    doc = ECH0211Document.from_attachment(camac_attachment)
    expected_pk = doc.pk

    url = reverse(f"ech-document-{mark_name}", args=[expected_pk])
    ech_resp = (
        admin_client.post(url) if mark_action == "add" else admin_client.delete(url)
    )

    # always 404, feature has no use with camac backend.
    assert ech_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.freeze_time("2025-11-22")
@pytest.mark.parametrize("mark_name", ["void", "decision", "publication", "sensitive"])
@pytest.mark.parametrize("mark_action", ["add", "remove"])
@pytest.mark.parametrize("has_void_mark", [True, False])
@pytest.mark.parametrize("has_permission", [True, False])
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db
def test_document_mark_alexandria(
    settings,
    role,
    set_document_backend,
    admin_client,
    mark_name,
    mark_action,
    has_void_mark,
    has_permission,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_category_factory,
    be_instance,
    admin_user,
    instance_acl_factory,
    be_ech0211_settings,
    be_permissions_settings,
    be_access_levels,
    be_alexandria_settings,
    mocker,
):
    set_document_backend("alexandria")

    if mark_name == "void":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_VOID_ADD,
            DocumentAPIFeature.DOCUMENTS_VOID_REMOVE,
        ]
    elif mark_name == "publication":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_ADD,
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_REMOVE,
        ]
    elif mark_name == "decision":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_DECISION_ADD,
            DocumentAPIFeature.DOCUMENTS_DECISION_REMOVE,
        ]
    elif mark_name == "sensitive":
        be_ech0211_settings["DOCUMENT_API_FEATURES"] = [
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_ADD,
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_REMOVE,
        ]

    mocker.patch(
        "camac.ech0211.views.has_alexandria_mark_permission",
        return_value=has_permission,
    )

    mark = alexandria_mark_factory(pk=mark_name)

    alexandria_category_factory(
        slug="intern",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "service"},
            }
        },
    )

    user_service = admin_user.get_default_group().service
    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )

    alexandria_doc = alexandria_document_factory(
        category_id="intern",
        metainfo={"camac-instance-id": be_instance.pk},
        created_by_user=admin_client.user.pk,
        created_by_group=user_service.pk,
    )
    if has_void_mark:
        alexandria_doc.marks.add(mark)

    url = reverse(f"ech-document-{mark_name}", args=[alexandria_doc.pk])
    ech_resp = (
        admin_client.post(url) if mark_action == "add" else admin_client.delete(url)
    )

    if not has_permission:
        assert ech_resp.status_code == status.HTTP_403_FORBIDDEN, ech_resp.json()
    elif (has_void_mark and mark_action == "add") or (
        not has_void_mark and mark_action == "remove"
    ):
        assert ech_resp.status_code == status.HTTP_400_BAD_REQUEST, ech_resp.json()
    else:
        assert ech_resp.status_code == status.HTTP_204_NO_CONTENT

        alexandria_doc.refresh_from_db()
        if mark_action == "add":
            assert alexandria_doc.marks.filter(pk=mark.pk).exists()
        else:
            assert not alexandria_doc.marks.filter(pk=mark.pk).exists()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    ("has_feature", "has_permission", "has_attachment", "expected_status"),
    [
        (False, False, True, status.HTTP_404_NOT_FOUND),
        (False, False, False, status.HTTP_404_NOT_FOUND),
        (False, True, True, status.HTTP_404_NOT_FOUND),
        (False, True, False, status.HTTP_404_NOT_FOUND),
        (True, False, True, status.HTTP_403_FORBIDDEN),
        (True, False, False, status.HTTP_403_FORBIDDEN),
        (True, True, True, status.HTTP_403_FORBIDDEN),
        (True, True, False, status.HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.django_db
def test_delete(
    admin_client,
    category_setup,
    communications_attachment_factory,
    has_attachment,
    has_feature,
    has_permission,
    expected_status,
    instance,
    ech0211_settings,
    mocker,
    set_document_backend,
    reload_ech0211_urls,
):
    ech0211_settings["DOCUMENT_API_FEATURES"] = (
        [DocumentAPIFeature.DOCUMENTS_DELETE] if has_feature else []
    )
    set_document_backend("alexandria")

    mocker.patch(
        "camac.ech0211.views.has_alexandria_delete_permission",
        return_value=has_permission,
    )

    file = FileFactory(
        document__metainfo={"camac-instance-id": str(instance.pk)},
        document__category=category_setup()[1],
    )
    communications_attachment = (
        communications_attachment_factory(alexandria_file=file)
        if has_attachment
        else None
    )

    document = file.document
    response = admin_client.delete(
        reverse("ech-document-detail", args=[file.document.pk])
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not Document.objects.filter(pk=document.pk).exists()
    else:
        assert Document.objects.filter(pk=document.pk).exists()

    if communications_attachment:
        communications_attachment.delete()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    ("has_feature", "has_attachment", "has_other_category", "expected_status"),
    [
        (False, False, True, status.HTTP_404_NOT_FOUND),
        (False, False, False, status.HTTP_404_NOT_FOUND),
        (False, True, True, status.HTTP_404_NOT_FOUND),
        (False, True, False, status.HTTP_404_NOT_FOUND),
        (True, False, True, status.HTTP_204_NO_CONTENT),
        (True, False, False, status.HTTP_204_NO_CONTENT),
        (True, True, True, status.HTTP_204_NO_CONTENT),
        (True, True, False, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_delete_camac(
    admin_client,
    communications_attachment_factory,
    has_other_category,
    has_attachment,
    has_feature,
    expected_status,
    ech0211_settings,
    file_setup,
    set_document_backend,
    reload_ech0211_urls,
):
    ech0211_settings["DOCUMENT_API_FEATURES"] = (
        [DocumentAPIFeature.DOCUMENTS_DELETE] if has_feature else []
    )
    set_document_backend("camac-ng")

    file, invisible_by_category, __ = file_setup()

    communications_attachment = (
        communications_attachment_factory(document_attachment=file.attachment)
        if has_attachment
        else None
    )
    if has_other_category:
        file.attachment.attachment_sections.add(
            AttachmentSection.objects.get(pk=invisible_by_category.category.pk)
        )

    response = admin_client.delete(reverse("ech-document-detail", args=[file.pk]))
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not ECH0211Document.objects.filter(pk=file.pk).exists()
    else:
        assert ECH0211Document.objects.filter(pk=file.pk).exists()

    if communications_attachment:
        communications_attachment.delete()


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize(
    ("testcase", "expected_status"),
    [
        ("success", status.HTTP_200_OK),
        ("move-permission-denied", status.HTTP_403_FORBIDDEN),
        ("feature-disabled", status.HTTP_404_NOT_FOUND),
        ("disallowed-category", status.HTTP_403_FORBIDDEN),
    ],
)
def test_document_update_alexandria(
    admin_client,
    alexandria_document_factory,
    alexandria_category_factory,
    instance_acl_factory,
    be_instance,
    set_document_backend,
    be_ech0211_settings,
    be_permissions_settings,
    be_access_levels,
    be_alexandria_settings,
    role,
    mocker,
    testcase,
    expected_status,
):
    set_document_backend("alexandria")
    be_ech0211_settings["DOCUMENT_API_FEATURES"] = (
        [] if testcase == "feature-disabled" else [DocumentAPIFeature.DOCUMENTS_UPDATE]
    )
    has_move_permission = testcase != "move-permission-denied"

    source_category = alexandria_category_factory(
        slug="intern",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "service"},
            }
        },
    )
    target_category = alexandria_category_factory(
        slug="target",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "service"},
            }
        },
    )
    be_ech0211_settings["ALLOWED_CATEGORIES"] = (
        [] if testcase == "disallowed-category" else [target_category.pk]
    )

    user_service = admin_client.user.get_default_group().service
    instance_acl_factory(
        instance=be_instance,
        service=user_service,
        access_level_id="lead-authority",
        grant_type="SERVICE",
    )

    old_date = date(2002, 7, 5)
    alexandria_doc = alexandria_document_factory(
        category=source_category,
        metainfo={"camac-instance-id": be_instance.pk},
        title="Old Title",
        description="Old Description",
        date=old_date,
        created_by_group=user_service.pk,
    )
    original_user = alexandria_doc.created_by_user
    move_permission = mocker.patch(
        "camac.ech0211.serializers.has_alexandria_move_permission",
        return_value=has_move_permission,
    )

    new_date = date(2024, 6, 1)
    url = reverse("ech-document-detail", args=[alexandria_doc.pk])
    data = {
        "data": {
            "type": "ech0211-documents",
            "id": str(alexandria_doc.pk),
            "attributes": {
                "title": "New Title",
                "description": "New Description",
                "date": new_date.isoformat(),
                "created-by-user": "test",  # should be ignored
            },
            "relationships": {
                "category": {
                    "data": {
                        "id": target_category.pk,
                        "type": "ech0211-document-categories",
                    }
                }
            },
        }
    }
    response = admin_client.patch(url, data, content_type="application/vnd.api+json")
    assert response.status_code == expected_status

    alexandria_doc.refresh_from_db()

    # verify that invalid field was ignored.
    assert alexandria_doc.created_by_user == original_user

    if testcase == "success":
        assert alexandria_doc.title == "New Title"
        assert alexandria_doc.description == "New Description"
        assert alexandria_doc.date == new_date
        assert alexandria_doc.category_id == target_category.pk
    else:
        assert alexandria_doc.title == "Old Title"
        assert alexandria_doc.description == "Old Description"
        assert alexandria_doc.date == old_date
        assert alexandria_doc.category_id == source_category.pk

    if testcase in ["success", "move-permission-denied"]:
        move_permission.assert_called_once()
    else:
        move_permission.assert_not_called()
