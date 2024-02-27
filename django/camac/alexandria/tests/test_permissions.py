import datetime
import io

import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileData,
    FileFactory,
    MarkFactory,
    TagFactory,
)
from caluma.caluma_workflow.models import WorkItem
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
    "role__name,method,status_code,access",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                },
            },
        ),
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["description"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "patch",
            HTTP_200_OK,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "patch",
            HTTP_200_OK,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "patch",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["description"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "delete",
            HTTP_204_NO_CONTENT,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "delete",
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "applicant",
            "delete",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category"],
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "patch",
            HTTP_200_OK,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title"],
                            "scope": "All",
                        },
                    ],
                },
            },
        ),
    ],
)
def test_document_permission(
    db,
    role,
    applicant_factory,
    admin_client,
    caluma_admin_user,
    instance,
    access,
    method,
    status_code,
):
    applicant_factory(invitee=admin_client.user, instance=instance)
    alexandria_category = CategoryFactory(metainfo={"access": access})
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
    "role__name,method,status_code,access",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                },
            },
        ),
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "fields": ["files"], "scope": "All"},
                    ],
                },
            },
        ),
        (
            "applicant",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "fields": ["title"], "scope": "All"},
                    ],
                },
            },
        ),
        (
            "applicant",
            "patch",
            HTTP_405_METHOD_NOT_ALLOWED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "update", "scope": "All"},
                    ],
                },
            },
        ),
        (
            "applicant",
            "delete",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "delete", "scope": "All"},
                    ],
                },
            },
        ),
        (
            "municipality",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                },
            },
        ),
    ],
)
def test_file_permission(
    db, role, mocker, admin_client, instance, access, method, status_code
):
    mocker.patch(
        "alexandria.core.serializers.validate_file_infection", return_value=None
    )

    alexandria_category = CategoryFactory(metainfo={"access": access})
    doc = DocumentFactory(
        title="Foo",
        category=alexandria_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    url = reverse("file-list")

    data = {
        "name": "file.png",
        "document": str(doc.pk),
        "content": io.BytesIO(FileData.png),
        "variant": "original",
    }
    if method in ["patch", "delete"]:
        file = FileFactory(name="File", document=doc)
        url = reverse("file-detail", args=[file.pk])
        data["id"] = str(file.pk)

    response = getattr(admin_client, method)(url, data=data, format="multipart")

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,method,status_code",
    [
        ("applicant", "post", HTTP_403_FORBIDDEN),
        ("applicant", "delete", HTTP_403_FORBIDDEN),
        ("municipality", "post", HTTP_201_CREATED),
        ("municipality", "delete", HTTP_204_NO_CONTENT),
        ("service", "post", HTTP_201_CREATED),
        ("service", "patch", HTTP_200_OK),
        ("support", "post", HTTP_201_CREATED),
        ("support", "delete", HTTP_204_NO_CONTENT),
    ],
)
def test_tag_permission(
    db, role, alexandria_settings, caluma_admin_user, admin_client, method, status_code
):
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
        alexandria_tag = TagFactory(
            name="Alexandria", created_by_group=caluma_admin_user.group
        )
        url = reverse("tag-detail", args=[alexandria_tag.pk])
        data["data"]["id"] = str(alexandria_tag.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code
    if status_code != HTTP_403_FORBIDDEN and method != "delete":
        result = response.json()
        assert result["data"]["attributes"]["name"] == "Important"


@pytest.mark.parametrize(
    "role__name,method,result",
    [
        ("support", "patch", HTTP_405_METHOD_NOT_ALLOWED),
        ("support", "delete", HTTP_404_NOT_FOUND),
    ],
)
def test_category_permission(
    db,
    role,
    admin_client,
    method,
    result,
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

    assert response.status_code == result


@pytest.mark.parametrize("role__name", ["applicant"])
def test_nested_permission(db, role, applicant_factory, admin_client, instance):
    applicant_factory(invitee=admin_client.user, instance=instance)
    parent_category = CategoryFactory(
        metainfo={
            "access": {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                        {"permission": "update", "scope": "All"},
                    ],
                },
            }
        }
    )
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


@pytest.mark.parametrize("role__name", ["applicant"])
@pytest.mark.parametrize("expected_status", [HTTP_403_FORBIDDEN, HTTP_200_OK])
@pytest.mark.parametrize("changes", [["metainfo"], ["tags"], ["files"], ["date"]])
def test_patch_fields(
    db,
    role,
    caluma_admin_user,
    applicant_factory,
    admin_client,
    instance,
    expected_status,
    changes,
):
    applicant_factory(invitee=admin_client.user, instance=instance)

    fields = changes
    if expected_status == HTTP_403_FORBIDDEN:
        fields = ["title"]

    category = CategoryFactory(
        metainfo={
            "access": {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "update", "fields": fields, "scope": "All"},
                    ],
                },
            }
        }
    )
    metainfo = {"camac-instance-id": instance.pk}
    date = datetime.date(2023, 11, 30)
    document = DocumentFactory(
        title="Important",
        description="Important",
        category=category,
        metainfo=metainfo,
        created_by_group=caluma_admin_user.group,
        date=date,
    )
    tag = TagFactory()
    document.tags.add(tag)
    document.save()
    file = FileFactory(document=document)

    if "metainfo" in changes:
        metainfo = {}
    if "tags" in changes:
        tag = TagFactory()
    if "files" in changes:
        file = FileFactory()
    if "date" in changes:
        date = datetime.date(2023, 12, 1)

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
            "attributes": {
                "title": {"de": "Important"},
                "description": {"de": "Important"},
                "metainfo": metainfo,
                "date": date.isoformat(),
            },
            "relationships": {
                "tags": {
                    "data": [
                        {
                            "id": tag.pk,
                            "type": "tags",
                        }
                    ],
                },
                "files": {
                    "data": [
                        {
                            "id": file.pk,
                            "type": "files",
                        }
                    ],
                },
            },
        },
    }

    patch_response = admin_client.patch(
        reverse("document-detail", args=[document.pk]), data
    )
    assert patch_response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,method,status_code,access,include_fields",
    [
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category", "marks"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "marks",
        ),
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category", "tags"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "tags",
        ),
        (
            "applicant",
            "post",
            HTTP_201_CREATED,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": [
                                "title",
                                "metainfo",
                                "category",
                                "marks",
                                "tags",
                            ],
                            "scope": "All",
                        },
                    ],
                },
            },
            "marks+tags",
        ),
        (
            "applicant",
            "patch",
            HTTP_200_OK,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title", "metainfo", "category", "marks"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "marks",
        ),
        (
            "applicant",
            "patch",
            HTTP_200_OK,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title", "metainfo", "category", "tags"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "tags",
        ),
        (
            "applicant",
            "patch",
            HTTP_200_OK,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": [
                                "title",
                                "metainfo",
                                "category",
                                "marks",
                                "tags",
                            ],
                            "scope": "All",
                        },
                    ],
                },
            },
            "marks+tags",
        ),
        (
            "applicant",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "fields": ["title", "metainfo", "category", "tags"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "marks",
        ),
        (
            "applicant",
            "patch",
            HTTP_403_FORBIDDEN,
            {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title", "metainfo", "category", "marks"],
                            "scope": "All",
                        },
                    ],
                },
            },
            "tags",
        ),
    ],
)
def test_marks(
    db,
    role,
    alexandria_settings,
    set_application_gr,
    applicant_factory,
    admin_client,
    caluma_admin_user,
    instance,
    access,
    method,
    status_code,
    include_fields,
):
    applicant_factory(invitee=admin_client.user, instance=instance)
    alexandria_category = CategoryFactory(metainfo={"access": access})
    url = reverse("document-list")
    tag = TagFactory()
    mark = MarkFactory(slug="decision")

    tag_data = []
    mark_data = []
    if "marks" in include_fields:
        mark_data.append(
            {
                "id": mark.pk,
                "type": "marks",
            }
        )
    if "tags" in include_fields:
        tag_data.append(
            {
                "id": tag.pk,
                "type": "tags",
            }
        )

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
                "tags": {
                    "data": tag_data,
                },
                "marks": {
                    "data": mark_data,
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


@pytest.mark.parametrize("role__name", ["service"])
@pytest.mark.parametrize(
    "method,created_by,status_code",
    [
        ("patch", "own_service", HTTP_200_OK),
        ("delete", "own_service", HTTP_204_NO_CONTENT),
        ("patch", "other_service", HTTP_403_FORBIDDEN),
        ("delete", "other_service", HTTP_403_FORBIDDEN),
    ],
)
def test_scope_service(
    db,
    admin_client,
    created_by,
    instance,
    method,
    mocker,
    role,
    service_factory,
    service,
    status_code,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    alexandria_category = CategoryFactory(
        metainfo={
            "access": {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title"],
                            "scope": "Service",
                        },
                        {
                            "permission": "delete",
                            "scope": "Service",
                        },
                    ],
                },
            }
        }
    )

    services = {"own_service": service, "other_service": service_factory()}

    document = DocumentFactory(
        title="Foo",
        category=alexandria_category,
        metainfo={"camac-instance-id": instance.pk},
        created_by_group=str(services[created_by].pk),
    )

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
            "attributes": {
                "title": {"de": "Important"},
            },
        },
    }

    url = reverse("document-detail", args=[document.pk])

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", ["service", "subservice"])
@pytest.mark.parametrize(
    "method,created_by,status_code",
    [
        ("patch", "own_service", HTTP_200_OK),
        ("patch", "subservice_or_parent", HTTP_200_OK),
        ("delete", "own_service", HTTP_204_NO_CONTENT),
        ("delete", "subservice_or_parent", HTTP_204_NO_CONTENT),
        ("patch", "other_service", HTTP_403_FORBIDDEN),
        ("delete", "other_service", HTTP_403_FORBIDDEN),
    ],
)
def test_scope_service_and_subservice(
    db,
    admin_client,
    created_by,
    instance,
    method,
    mocker,
    role,
    service_factory,
    service,
    status_code,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    alexandria_category = CategoryFactory(
        metainfo={
            "access": {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title"],
                            "scope": "ServiceAndSubservice",
                        },
                        {
                            "permission": "delete",
                            "scope": "ServiceAndSubservice",
                        },
                    ],
                },
                "subservice": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "fields": ["title"],
                            "scope": "ServiceAndSubservice",
                        },
                        {
                            "permission": "delete",
                            "scope": "ServiceAndSubservice",
                        },
                    ],
                },
            }
        }
    )

    services = {
        "own_service": service,
        "other_service": service_factory(),
    }

    if role.name == "subservice":
        service.service_parent = service_factory()
        service.save()

        services["subservice_or_parent"] = service.service_parent
    else:
        services["subservice_or_parent"] = service_factory(service_parent=service)

    document = DocumentFactory(
        title="Foo",
        category=alexandria_category,
        metainfo={"camac-instance-id": instance.pk},
        created_by_group=str(services[created_by].pk),
    )

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
            "attributes": {
                "title": {"de": "Important"},
            },
        },
    }

    url = reverse("document-detail", args=[document.pk])

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", ["service"])
@pytest.mark.parametrize(
    "work_item_status,status_code",
    [
        (WorkItem.STATUS_READY, HTTP_204_NO_CONTENT),
        (WorkItem.STATUS_COMPLETED, HTTP_403_FORBIDDEN),
        (None, HTTP_403_FORBIDDEN),
    ],
)
def test_condition_ready_work_item(
    db,
    admin_client,
    gr_instance,
    mocker,
    status_code,
    work_item_factory,
    work_item_status,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[gr_instance.pk],
    )

    if work_item_status:
        work_item_factory(
            task__pk="some-work-item", case=gr_instance.case, status=work_item_status
        )

    document = DocumentFactory(
        title="Foo",
        category=CategoryFactory(
            metainfo={
                "access": {
                    "service": {
                        "visibility": "all",
                        "permissions": [
                            {
                                "permission": "delete",
                                "scope": "All",
                                "condition": {
                                    "ReadyWorkItem": "some-work-item",
                                },
                            },
                        ],
                    },
                }
            }
        ),
        metainfo={"camac-instance-id": gr_instance.pk},
    )

    url = reverse("document-detail", args=[document.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", ["applicant"])
@pytest.mark.parametrize(
    "method,work_item_status,has_document_id,status_code",
    [
        ("delete", WorkItem.STATUS_READY, True, HTTP_204_NO_CONTENT),
        ("delete", WorkItem.STATUS_READY, False, HTTP_403_FORBIDDEN),
        ("delete", WorkItem.STATUS_COMPLETED, True, HTTP_403_FORBIDDEN),
        ("post", WorkItem.STATUS_READY, True, HTTP_201_CREATED),
        ("post", WorkItem.STATUS_READY, False, HTTP_403_FORBIDDEN),
        ("post", WorkItem.STATUS_COMPLETED, True, HTTP_403_FORBIDDEN),
    ],
)
def test_condition_ready_work_item_additional_demand(
    db,
    admin_client,
    gr_instance,
    has_document_id,
    method,
    mocker,
    status_code,
    work_item_factory,
    work_item_status,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[gr_instance.pk],
    )

    work_item = work_item_factory(
        task__pk="fill-additional-demand",
        case=gr_instance.case,
        status=work_item_status,
    )

    category = CategoryFactory(
        metainfo={
            "access": {
                "applicant": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "scope": "All",
                            "condition": {
                                "ReadyWorkItem": "fill-additional-demand",
                            },
                        },
                        {
                            "permission": "delete",
                            "scope": "All",
                            "condition": {
                                "ReadyWorkItem": "fill-additional-demand",
                            },
                        },
                    ],
                },
            }
        }
    )

    metainfo = {"camac-instance-id": gr_instance.pk}
    if has_document_id:
        metainfo["caluma-document-id"] = str(work_item.document_id)

    if method == "delete":
        document = DocumentFactory(title="Foo", category=category, metainfo=metainfo)

        response = admin_client.delete(reverse("document-detail", args=[document.pk]))
    elif method == "post":
        data = {
            "data": {
                "type": "documents",
                "attributes": {"title": {"de": "Foo"}, "metainfo": metainfo},
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

        response = admin_client.post(reverse("document-list"), data=data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,method,status_code,access",
    [
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "InstanceState": "new",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "~InstanceState": "done",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "patch",
            HTTP_200_OK,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                            "condition": {
                                "InstanceState": ["new"],
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "delete",
            HTTP_204_NO_CONTENT,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "delete",
                            "scope": "All",
                            "condition": {
                                "InstanceState": "new",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "InstanceState": "done",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "~InstanceState": "new",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "patch",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                            "condition": {
                                "InstanceState": "done",
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "delete",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "delete",
                            "scope": "All",
                            "condition": {
                                "InstanceState": "done",
                            },
                        },
                    ],
                },
            },
        ),
    ],
)
def test_condition_instance_state(
    db,
    role,
    applicant_factory,
    admin_client,
    caluma_admin_user,
    instance_state_factory,
    gr_instance,
    access,
    method,
    status_code,
):
    state = instance_state_factory(name="new")
    gr_instance.instance_state = state
    gr_instance.save()
    applicant_factory(invitee=admin_client.user, instance=gr_instance)
    alexandria_category = CategoryFactory(metainfo={"access": access})
    url = reverse("document-list")

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
                "metainfo": {"camac-instance-id": gr_instance.pk},
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
            metainfo={"camac-instance-id": gr_instance.pk},
        )
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,method,status_code,access",
    [
        (
            "service",
            "post",
            HTTP_201_CREATED,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "patch",
            HTTP_200_OK,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "delete",
            HTTP_204_NO_CONTENT,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "delete",
                            "scope": "All",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "post",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "create",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "patch",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
        (
            "service",
            "delete",
            HTTP_403_FORBIDDEN,
            {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "delete",
                            "scope": "All",
                            "condition": {
                                "PaperInstance": True,
                            },
                        },
                    ],
                },
            },
        ),
    ],
)
def test_condition_paper_instance(
    db,
    role,
    applicant_factory,
    admin_client,
    caluma_admin_user,
    gr_instance,
    access,
    method,
    status_code,
):
    applicant_factory(invitee=admin_client.user, instance=gr_instance)
    alexandria_category = CategoryFactory(metainfo={"access": access})
    url = reverse("document-list")
    if status_code != HTTP_403_FORBIDDEN:
        gr_instance.case.document.answers.create(
            question_id="is-paper", value="is-paper-yes"
        )

    data = {
        "data": {
            "type": "documents",
            "attributes": {
                "title": {"de": "Important"},
                "metainfo": {"camac-instance-id": gr_instance.pk},
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
            metainfo={"camac-instance-id": gr_instance.pk},
        )
        url = reverse("document-detail", args=[doc.pk])
        data["data"]["id"] = str(doc.pk)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", ["municipality"])
@pytest.mark.parametrize(
    "has_marks,source_category,target_category,status_code",
    [
        (False, "source-category-1", "target-category-1", HTTP_200_OK),
        (False, "source-category-2", "target-category-1", HTTP_403_FORBIDDEN),
        (False, "source-category-1", "target-category-2", HTTP_403_FORBIDDEN),
        (False, "source-category-1", "target-category-3", HTTP_200_OK),
        (True, "source-category-1", "target-category-1", HTTP_403_FORBIDDEN),
        (True, "source-category-1", "target-category-3", HTTP_200_OK),
    ],
)
def test_move_document(
    db,
    admin_client,
    has_marks,
    instance,
    mocker,
    source_category,
    status_code,
    target_category,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    # source-category-1: allowed to update category
    CategoryFactory(
        slug="source-category-1",
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                            "fields": ["category"],
                        },
                    ],
                },
            }
        },
    )

    # source-category-1: only allowed to update tags
    CategoryFactory(
        slug="source-category-2",
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "update", "scope": "All", "fields": ["tags"]},
                    ],
                },
            }
        },
    )

    # target-category-1: allowed to create
    CategoryFactory(
        slug="target-category-1",
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                },
            }
        },
    )

    # target-category-2: not allowed to create
    CategoryFactory(
        slug="target-category-2",
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [],
                },
            }
        },
    )

    # target-category-3: allowed to create and update marks
    CategoryFactory(
        slug="target-category-3",
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                        {"permission": "update", "scope": "All", "fields": ["marks"]},
                    ],
                },
            }
        },
    )

    document = DocumentFactory(
        category_id=source_category,
        metainfo={"camac-instance-id": instance.pk},
    )

    if has_marks:
        document.marks.add(MarkFactory())

    data = {
        "data": {
            "type": "documents",
            "id": document.pk,
            "relationships": {
                "category": {
                    "data": {
                        "id": target_category,
                        "type": "categories",
                    },
                },
                "marks": {
                    "data": [
                        {"id": mark.pk, "type": "marks"}
                        for mark in document.marks.all()
                    ]
                },
            },
        },
    }

    response = admin_client.patch(reverse("document-detail", args=[document.pk]), data)

    assert response.status_code == status_code
