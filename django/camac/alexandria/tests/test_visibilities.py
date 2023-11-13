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


@pytest.mark.parametrize("instance__user", [LazyFixture("user")])
@pytest.mark.parametrize(
    "role__name,is_nested_category,expected",
    [
        ("applicant", False, ["municipality", "invitee", "applicant"]),
        ("municipality", False, ["municipality"]),
        ("municipality", True, ["municipality"]),
        ("service", False, ["service"]),
        ("public", False, ["public"]),
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
    applicant_factory,
    create_caluma_publication,  # noqa: F811
    is_nested_category,
    expected,
):
    applicant_factory(invitee=admin_client.user, instance=instance)

    # directly readble
    applicant_category = CategoryFactory(
        metainfo={"access": {"applicant": {"visibility": "all"}}}
    )
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": {"visibility": "all"}}}
    )
    service_category = CategoryFactory(
        metainfo={"access": {"service": {"visibility": "service"}}}
    )

    if is_nested_category:
        municipality_category = CategoryFactory(parent=municipality_category)

    DocumentFactory(
        category=applicant_category,
        metainfo={"camac-instance-id": instance.pk},
        title="applicant",
    )
    document = DocumentFactory(
        category=municipality_category,
        metainfo={"camac-instance-id": instance.pk},
        title="municipality",
    )
    # decision document
    document.tags.add(TagFactory(slug="decision"))

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
    assert set([obj["attributes"]["title"]["de"] for obj in json["data"]]) == set(
        expected
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
    applicant_factory,
    caluma_admin_user,
    instance,
    admin_client,
    role,
    expected_count,
    is_nested_category,
):
    applicant_factory(invitee=admin_client.user, instance=instance)
    applicant_category = CategoryFactory(
        metainfo={"access": {"applicant": {"visibility": "all"}}}
    )
    municipality_category = CategoryFactory(
        metainfo={"access": {"municipality": {"visibility": "all"}}}
    )
    service_category = CategoryFactory(
        metainfo={"access": {"service": {"visibility": "service"}}}
    )

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
