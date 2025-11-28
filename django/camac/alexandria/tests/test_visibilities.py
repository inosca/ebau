import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    MarkFactory,
    TagFactory,
)
from alexandria.core.models import Document
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from camac.constants.kt_gr import ARE_SERVICE_GROUP


@pytest.fixture
def alexandria_setup(
    db,
    create_caluma_publication,
    so_instance,
    mocker,
    role,
    service_factory,
    service,
    so_publication_settings,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[so_instance.pk],
    )

    other_service = service_factory()

    if role.name == "subservice":
        parent_service = service_factory()
        service.service_parent = parent_service
        service.save()
        subservice_1 = service
    else:
        parent_service = service
        subservice_1 = service_factory(service_parent=parent_service)

    subservice_2 = service_factory(service_parent=parent_service)

    applicant_category = CategoryFactory(
        metainfo={"access": {"applicant": {"visibility": "all"}}}
    )
    applicant_nested_category = CategoryFactory(parent=applicant_category)
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": {"visibility": "all"}}}
    )
    service_category = CategoryFactory(
        metainfo={"access": {"service": {"visibility": "service"}}}
    )
    service_and_subservice_category = CategoryFactory(
        metainfo={
            "access": {
                "service": {"visibility": "service-and-subservice"},
                "subservice": {"visibility": "service-and-subservice"},
            }
        }
    )

    # applicant documents
    DocumentFactory(
        category=applicant_category,
        metainfo={"camac-instance-id": so_instance.pk},
        title="applicant",
    )
    DocumentFactory(
        category=applicant_nested_category,
        metainfo={"camac-instance-id": so_instance.pk},
        title="applicant nested",
    )

    # service documents
    DocumentFactory(
        category=service_category,
        created_by_group=str(service.pk),
        modified_by_group=str(service.pk),
        metainfo={"camac-instance-id": so_instance.pk},
        title="service",
    )
    DocumentFactory(
        category=service_category,
        created_by_group=str(other_service.pk),
        modified_by_group=str(other_service.pk),
        metainfo={"camac-instance-id": so_instance.pk},
        title="service 2",
    )

    # service and subservice documents
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(parent_service.pk),
        modified_by_group=str(parent_service.pk),
        metainfo={"camac-instance-id": so_instance.pk},
        title="subservice shared 1",
    )
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(subservice_1.pk),
        modified_by_group=str(subservice_1.pk),
        metainfo={"camac-instance-id": so_instance.pk},
        title="subservice shared 2",
    )
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(subservice_2.pk),
        modified_by_group=str(subservice_2.pk),
        metainfo={"camac-instance-id": so_instance.pk},
        title="subservice shared 3",
    )

    # decision document
    document = DocumentFactory(
        category=municipality_category,
        metainfo={"camac-instance-id": so_instance.pk},
        title="decision",
    )
    document.marks.add(MarkFactory(slug="decision"))

    # publication document
    create_caluma_publication(so_instance, module_settings=so_publication_settings)
    DocumentFactory(metainfo={"camac-instance-id": so_instance.pk}, title="hidden")
    public = DocumentFactory(
        metainfo={"camac-instance-id": so_instance.pk}, title="publication"
    )
    public.marks.add(MarkFactory(slug="publication"))

    # geometer document
    document = DocumentFactory(
        category=municipality_category,
        metainfo={"camac-instance-id": so_instance.pk},
        title="geometer",
    )
    document.marks.add(MarkFactory(slug="geometer"))

    for document in Document.objects.all():
        FileFactory(document=document, modified_by_group=document.modified_by_group)


@pytest.mark.parametrize("type", ["document", "file"])
@pytest.mark.parametrize(
    "role__name,expected",
    [
        ("applicant", ["applicant", "applicant nested", "decision"]),
        ("municipality", ["decision", "geometer"]),
        (
            "service",
            [
                "service",
                "subservice shared 1",
                "subservice shared 2",
                "subservice shared 3",
            ],
        ),
        (
            "subservice",
            ["subservice shared 1", "subservice shared 2", "subservice shared 3"],
        ),
        ("public", ["publication"]),
        ("geometer", ["geometer"]),
    ],
)
def test_document_and_file_visibility(
    db,
    admin_client,
    alexandria_setup,
    alexandria_settings,
    expected,
    role,
    type,
):
    url = reverse(f"{type}-list")

    alexandria_settings["MARK_VISIBILITY"]["GEOMETER"] = ["geometer"]

    if type == "file":
        data = {"include": "document"}
    else:
        data = {}

    if role.name == "public":
        response = admin_client.get(url, data=data, HTTP_X_CAMAC_PUBLIC_ACCESS=True)
    else:
        response = admin_client.get(url, data=data)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert set(
        [
            obj["attributes"]["title"]
            for obj in json["included" if type == "file" else "data"]
        ]
    ) == set(expected)


@pytest.mark.parametrize(
    "role__name,expected",
    [
        ("applicant", ["common"]),
        ("municipality", ["common", "municipality", "municipality-parent", "service"]),
        ("service", ["common", "service"]),
    ],
)
def test_category_visibility(db, admin_client, role, expected):
    CategoryFactory(
        slug="common",
        metainfo={
            "access": {
                "applicant": {"visibility": "all"},
                "municipality": {"visibility": "all"},
                "service": {"visibility": "all"},
            }
        },
    )
    municipality_category = CategoryFactory(
        slug="municipality",
        metainfo={"access": {"municipality": {"visibility": "all"}}},
    )
    CategoryFactory(slug="municipality-parent", parent=municipality_category)
    CategoryFactory(
        slug="service",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "all"},
            }
        },
    )

    url = reverse("category-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert set([obj["id"] for obj in json["data"]]) == set(expected)


@pytest.mark.parametrize(
    "role__name,service_group__name,inquired_by_are,expected",
    [
        # babfiltered never visible for applicant
        ("applicant", "applicant", False, ["common"]),
        ("applicant", "applicant", True, ["common"]),
        # babfiltered always visible for ARE service
        ("service", ARE_SERVICE_GROUP, False, ["common", "babfiltered", "service"]),
        ("service", ARE_SERVICE_GROUP, True, ["common", "babfiltered", "service"]),
        # babfiltered only visible when invited by ARE
        ("service", "service", False, ["common", "service"]),
        ("service", "service", True, ["common", "babfiltered", "service"]),
        (
            "municipality",
            "municipality",
            False,
            ["common", "municipality", "municipality-parent", "service"],
        ),
        (
            "municipality",
            "municipality",
            True,
            ["common", "babfiltered", "municipality", "municipality-parent", "service"],
        ),
    ],
)
def test_category_visibility_camac_instance_gr(
    db,
    admin_client,
    service_factory,
    caluma_document_factory,
    caluma_work_item_factory,
    role,
    service_group,
    service,
    inquired_by_are,
    gr_instance,
    expected,
    distribution_settings,
    set_application_gr,
):
    are_service = service_factory(service_group__name=ARE_SERVICE_GROUP)

    CategoryFactory(
        slug="common",
        metainfo={
            "access": {
                "applicant": {"visibility": "all"},
                "municipality": {"visibility": "all"},
                "service": {"visibility": "all"},
            },
        },
    )
    CategoryFactory(
        slug="babfiltered",
        metainfo={
            "access": {
                "municipality": {"visibility": "all"},
                "service": {"visibility": "all"},
            },
            "hideInBab": True,
        },
    )
    municipality_category = CategoryFactory(
        slug="municipality",
        metainfo={"access": {"municipality": {"visibility": "all"}}},
    )
    CategoryFactory(slug="municipality-parent", parent=municipality_category)
    CategoryFactory(
        slug="service",
        metainfo={
            "access": {
                "service": {"visibility": "service"},
                "municipality": {"visibility": "all"},
            }
        },
    )

    # create an inquiry for the service
    inquired_by = are_service if inquired_by_are else service_factory()
    caluma_work_item_factory(
        case=gr_instance.case,
        task_id=distribution_settings["INQUIRY_TASK"],
        document=caluma_document_factory(form_id="inquiry"),
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(inquired_by.pk)],
    )

    url = reverse("category-list")
    response = admin_client.get(url, {"camac-instance-id": gr_instance.pk})

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert set([obj["id"] for obj in json["data"]]) == set(expected)


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("applicant", 0),
        ("municipality", 2),
        ("service", 2),
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
    TagFactory(created_by_group="abc")

    url = reverse("tag-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("service", 2),
        ("subservice", 2),
    ],
)
def test_tag_visibility_service_subservice(
    db,
    caluma_admin_user,
    set_application_so,
    so_alexandria_settings,
    admin_client,
    service_factory,
    service,
    role,
    expected_count,
):
    if role.name == "subservice":
        service2 = service_factory()
        service.service_parent = service2
        service.save()
    elif role.name == "service":
        service2 = service_factory(service_parent=service)

    TagFactory(created_by_group=service.pk)
    TagFactory(created_by_group=service2.pk)
    TagFactory(created_by_group=service_factory().pk)

    url = reverse("tag-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,visible_marks",
    [
        ("public", {"publication", "void"}),
        ("municipality", {"decision", "publication", "void"}),
    ],
)
def test_mark_visibility(db, admin_client, visible_marks):
    MarkFactory(pk="void", metainfo={"sort": 3})
    MarkFactory(pk="decision", metainfo={"sort": 1})
    MarkFactory(pk="publication", metainfo={"sort": 2})

    response = admin_client.get(reverse("mark-list"))

    assert response.status_code == HTTP_200_OK

    marks = set([mark["id"] for mark in response.json()["data"]])

    assert marks == visible_marks


@pytest.mark.parametrize("role__name", ["municipality"])
def test_detail_visibility(
    db,
    instance,
    admin_client,
    mocker,
    caluma_admin_user,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )
    category = CategoryFactory(
        metainfo={
            "access": {
                "municipality": {
                    "visibility": "all",
                    "permissions": [
                        {"permission": "create", "scope": "All"},
                    ],
                }
            }
        }
    )
    document = DocumentFactory(
        category=category,
        metainfo={"camac-instance-id": instance.pk},
        title="decision",
    )
    document.instance_document.instance = instance
    document.instance_document.save()
    tag = TagFactory(created_by_group=caluma_admin_user.group)
    file = FileFactory(document=document)

    response = admin_client.get(reverse("category-detail", args=[category.pk]))
    assert response.status_code == HTTP_200_OK
    response = admin_client.get(reverse("document-detail", args=[document.pk]))
    assert response.status_code == HTTP_200_OK
    response = admin_client.get(reverse("file-detail", args=[file.pk]))
    assert response.status_code == HTTP_200_OK
    response = admin_client.get(reverse("tag-detail", args=[tag.pk]))
    assert response.status_code == HTTP_200_OK


@pytest.mark.parametrize("role__name", ["applicant"])
def test_file_download(db, alexandria_setup, admin_client, client):
    response = admin_client.get(reverse("file-list"))
    url = response.json()["data"][0]["attributes"]["download-url"]

    result = client.get(url)
    assert result.status_code == HTTP_200_OK
