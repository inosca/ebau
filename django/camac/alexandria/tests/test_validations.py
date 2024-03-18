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
def test_mark_validation(
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
