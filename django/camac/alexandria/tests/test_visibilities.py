import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory,
    FileFactory,
    TagFactory,
)
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework.status import HTTP_200_OK

from camac.instance.tests.test_instance_public import (  # noqa: F401
    create_caluma_publication,
)


@pytest.mark.parametrize("is_nested_category", [True, False])
@pytest.mark.parametrize(
    "role__name,instance__user,expected_count",
    [
        ("applicant", LazyFixture("user"), 3),
        ("municipality", LazyFixture("user"), 2),
        ("service", LazyFixture("user"), 1),
        ("public", LazyFixture("user"), 1),
    ],
)
def test_document_visibility(
    db,
    role,
    caluma_admin_user,
    admin_client,
    instance,
    instance_factory,
    instance_with_case,
    publication_settings,
    create_caluma_publication,  # noqa: F811
    snapshot,
    expected_count,
    is_nested_category,
):
    # directly readble
    applicant_category = CategoryFactory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = CategoryFactory(metainfo={"access": {"service": "InternalRead"}})

    if is_nested_category:
        applicant_category = CategoryFactory(parent=applicant_category)
        municipality_category = CategoryFactory(parent=municipality_category)
        service_category = CategoryFactory(parent=service_category)

    DocumentFactory.create_batch(
        2,
        category=applicant_category,
        metainfo={"camac-instance-id": instance.pk},
        title="applicant",
    )
    DocumentFactory.create_batch(
        2,
        category=municipality_category,
        metainfo={"camac-instance-id": instance.pk},
        title="municipality",
    )

    # readable from service
    DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group,
        metainfo={"camac-instance-id": instance.pk},
        title="service",
    )
    DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group + 1,
        metainfo={"camac-instance-id": instance.pk},
        title="service 2",
    )

    # readable as invitee
    DocumentFactory(
        category=applicant_category,
        metainfo={"camac-instance-id": instance.pk},
        title="invitee",
    )

    # published instance
    public_instance = instance_with_case(instance_factory())
    create_caluma_publication(public_instance)
    DocumentFactory(metainfo={"camac-instance-id": public_instance.pk}, title="hidden")
    public = DocumentFactory(
        metainfo={"camac-instance-id": public_instance.pk}, title="public"
    )
    public.tags.add(TagFactory(slug="publication"))

    url = reverse("document-list")
    if role.name == "public":
        response = admin_client.get(url, HTTP_X_CAMAC_PUBLIC_ACCESS=True)
    else:
        response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
    snapshot.assert_match(
        sorted(
            [{"title": obj["attributes"]["title"]["de"]} for obj in json["data"]],
            key=lambda o: o["title"],
        )
    )


@pytest.mark.parametrize("is_nested_category", [True, False])
@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("applicant", 3),
        ("municipality", 2),
        ("service", 1),
    ],
)
def test_file_visibility(
    db,
    minio_mock,
    caluma_admin_user,
    instance,
    admin_client,
    role,
    expected_count,
    is_nested_category,
):
    applicant_category = CategoryFactory(metainfo={"access": {"applicant": "Admin"}})
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": "Read"}}
    )
    service_category = CategoryFactory(metainfo={"access": {"service": "Internal"}})

    if is_nested_category:
        applicant_category = CategoryFactory(parent=applicant_category)
        municipality_category = CategoryFactory(parent=municipality_category)
        service_category = CategoryFactory(parent=service_category)

    applicant_document = DocumentFactory(
        category=applicant_category, metainfo={"camac-instance-id": instance.pk}
    )
    municipality_document = DocumentFactory(
        category=municipality_category, metainfo={"camac-instance-id": instance.pk}
    )
    service_document = DocumentFactory(
        category=service_category,
        created_by_group=caluma_admin_user.group,
        metainfo={"camac-instance-id": instance.pk},
    )
    FileFactory.create_batch(3, document=applicant_document)
    FileFactory.create_batch(2, document=municipality_document)
    FileFactory.create_batch(1, document=service_document)

    url = reverse("file-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count


@pytest.mark.parametrize("is_nested_category", [True, False])
@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("applicant", 1),
        ("municipality", 3),
        ("service", 2),
    ],
)
def test_category_visibility(
    db, admin_client, role, expected_count, snapshot, is_nested_category
):
    categories = [
        CategoryFactory(
            metainfo={
                "access": {
                    "applicant": "Admin",
                    "municipality": "Read",
                    "service": "Read",
                }
            }
        ),
        CategoryFactory(metainfo={"access": {"municipality": "Read"}}),
        CategoryFactory(
            metainfo={"access": {"service": "Internal", "municipality": "Read"}}
        ),
    ]

    if is_nested_category:
        for category in categories:
            CategoryFactory(parent=category)

        expected_count *= 2

    url = reverse("category-list")
    response = admin_client.get(url)

    assert response.status_code == HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == expected_count
    snapshot.assert_match(
        [
            {"id": obj["id"], "metainfo": obj["attributes"]["metainfo"]}
            for obj in json["data"]
        ]
    )


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
