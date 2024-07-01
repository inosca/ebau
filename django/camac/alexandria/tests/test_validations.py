import pytest
from alexandria.core.factories import DocumentFactory, MarkFactory
from alexandria.core.models import Mark
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "marks,expected_status",
    [
        (["exclusive"], status.HTTP_200_OK),
        (["mark-1", "mark-2"], status.HTTP_200_OK),
        (["exclusive", "mark-1"], status.HTTP_400_BAD_REQUEST),
    ],
)
def test_mark_exclusive_validation(
    admin_client,
    marks,
    expected_status,
    settings,
    alexandria_settings,
    mocker,
    instance,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[instance.pk],
    )

    alexandria_settings["EXCLUSIVE_MARKS"] = ["exclusive"]

    MarkFactory(slug="exclusive")
    MarkFactory(slug="mark-1")
    MarkFactory(slug="mark-2")

    document = DocumentFactory(
        metainfo={"camac-instance-id": instance.pk},
        category__metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [{"permission": "update", "scope": "All"}],
                }
            }
        },
    )

    response = admin_client.patch(
        reverse("document-detail", args=[document.pk]),
        data={
            "data": {
                "id": document.pk,
                "type": "documents",
                "attributes": {},
                "relationships": {
                    "marks": {
                        "data": [
                            {"id": mark.pk, "type": "marks"}
                            for mark in Mark.objects.filter(pk__in=marks)
                        ]
                    },
                },
            }
        },
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize("role__name", ["service"])
@pytest.mark.parametrize(
    "existing_marks,new_marks,expected_status",
    [
        ([], ["publication"], status.HTTP_200_OK),
        ([], ["sensitive"], status.HTTP_200_OK),
        (["sensitive"], ["publication"], status.HTTP_400_BAD_REQUEST),
        (["publication"], ["sensitive"], status.HTTP_400_BAD_REQUEST),
    ],
)
def test_mark_sensitive_validation(
    db,
    admin_client,
    mocker,
    gr_instance,
    alexandria_settings,
    existing_marks,
    new_marks,
    expected_status,
):
    mocker.patch(
        "camac.alexandria.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[gr_instance.pk],
    )
    alexandria_settings["MARK_VISIBILITY"] = {
        "PUBLIC": ["publication"],
        "SENSITIVE": ["sensitive"],
    }

    document = DocumentFactory(
        title="Foo",
        metainfo={"camac-instance-id": gr_instance.pk},
        category__metainfo={
            "access": {
                "service": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "permission": "update",
                            "scope": "All",
                        },
                    ],
                },
            },
        },
    )

    for slug in set(existing_marks + new_marks):
        MarkFactory(slug=slug)
    for slug in existing_marks:
        document.marks.add(Mark.objects.get(slug=slug))

    response = admin_client.patch(
        reverse("document-detail", args=[document.pk]),
        {
            "data": {
                "id": document.pk,
                "type": "documents",
                "attributes": {
                    "title": {"de": "Important"},
                },
                "relationships": {
                    "marks": {
                        "data": [
                            {"id": slug, "type": "marks"}
                            for slug in existing_marks + new_marks
                        ],
                    }
                },
            },
        },
    )

    assert response.status_code == expected_status
