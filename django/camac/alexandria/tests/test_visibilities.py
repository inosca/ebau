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

from camac.instance.tests.test_instance_public import (  # noqa: F401
    create_caluma_publication,
)


@pytest.fixture
def alexandria_setup(
    db,
    create_caluma_publication,  # noqa: F811
    instance_with_case,
    instance,
    mocker,
    publication_settings,
    role,
    service_factory,
    service,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    instance = instance_with_case(instance)
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
        metainfo={"camac-instance-id": instance.pk},
        title="applicant",
    )
    DocumentFactory(
        category=applicant_nested_category,
        metainfo={"camac-instance-id": instance.pk},
        title="applicant nested",
    )

    # service documents
    DocumentFactory(
        category=service_category,
        created_by_group=str(service.pk),
        metainfo={"camac-instance-id": instance.pk},
        title="service",
    )
    DocumentFactory(
        category=service_category,
        created_by_group=str(other_service.pk),
        metainfo={"camac-instance-id": instance.pk},
        title="service 2",
    )

    # service and subservice documents
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(parent_service.pk),
        metainfo={"camac-instance-id": instance.pk},
        title="subservice shared 1",
    )
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(subservice_1.pk),
        metainfo={"camac-instance-id": instance.pk},
        title="subservice shared 2",
    )
    DocumentFactory(
        category=service_and_subservice_category,
        created_by_group=str(subservice_2.pk),
        metainfo={"camac-instance-id": instance.pk},
        title="subservice shared 3",
    )

    # decision document
    document = DocumentFactory(
        category=municipality_category,
        metainfo={"camac-instance-id": instance.pk},
        title="decision",
    )
    document.marks.add(MarkFactory(slug="decision"))

    # publication document
    create_caluma_publication(instance)
    DocumentFactory(metainfo={"camac-instance-id": instance.pk}, title="hidden")
    public = DocumentFactory(
        metainfo={"camac-instance-id": instance.pk}, title="publication"
    )
    public.marks.add(MarkFactory(slug="publication"))

    for document in Document.objects.all():
        FileFactory(document=document)


@pytest.mark.parametrize("type", ["document", "file"])
@pytest.mark.parametrize(
    "role__name,expected",
    [
        ("applicant", ["applicant", "applicant nested", "decision"]),
        ("municipality", ["decision"]),
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
    ],
)
def test_document_and_file_visibility(
    db,
    admin_client,
    alexandria_setup,
    expected,
    role,
    type,
):
    url = reverse(f"{type}-list")

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
            obj["attributes"]["title"]["de"]
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
