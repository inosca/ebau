import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
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
    minio_mock,
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
    document.tags.add(TagFactory(slug="decision"))

    # publication document
    create_caluma_publication(instance)
    DocumentFactory(metainfo={"camac-instance-id": instance.pk}, title="hidden")
    public = DocumentFactory(
        metainfo={"camac-instance-id": instance.pk}, title="publication"
    )
    public.tags.add(TagFactory(slug="publication"))

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
        ("municipality", 1),
        ("service", 1),
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

    url = reverse("tag-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
