import datetime

import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    TagFactory,
)
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
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
            HTTP_405_METHOD_NOT_ALLOWED,
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
    db, role, minio_mock, admin_client, instance, access, method, status_code
):
    alexandria_category = CategoryFactory(metainfo={"access": access})
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
        url = reverse("tag-detail", args=[alexandria_tag.slug])
        data["data"]["id"] = str(alexandria_tag.slug)

    response = getattr(admin_client, method)(url, data)

    assert response.status_code == status_code
    if status_code != HTTP_403_FORBIDDEN and method != "delete":
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
@pytest.mark.parametrize(
    "changes", [["metainfo"], ["category"], ["tags"], ["files"], ["date"]]
)
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
    if "category" in changes:
        category = CategoryFactory()
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
                "category": {
                    "data": {
                        "id": category.pk,
                        "type": "categories",
                    },
                },
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
    mark = TagFactory(slug="decision")

    tag_data = []
    if "marks" in include_fields:
        tag_data.append(
            {
                "id": mark.pk,
                "type": "tags",
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
            task__slug="some-work-item", case=gr_instance.case, status=work_item_status
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
        task__slug="fill-additional-demand",
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
