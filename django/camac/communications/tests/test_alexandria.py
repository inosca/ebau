import json

import pytest
from alexandria.core.factories import CategoryFactory, FileFactory
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,communications_message__topic",
    [("Municipality", pytest.lazy_fixture("topic_with_admin_involved"))],
)
def test_s3_attachment_download_url(
    admin_client,
    communications_attachment,
    use_alexandria_backend,
):
    communications_attachment.document_attachment = None
    communications_attachment.alexandria_file = None
    communications_attachment.save()

    response = admin_client.get(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]["attributes"]

    assert "X-Amz-Signature" in data["download-url"]
    assert communications_attachment.file_attachment.name in data["download-url"]


@pytest.mark.parametrize(
    "role__name,communications_message__topic",
    [("Municipality", pytest.lazy_fixture("topic_with_admin_involved"))],
)
def test_alexandria_attachment_download_url(
    admin_client,
    communications_attachment,
    use_alexandria_backend,
):
    alexandria_file = FileFactory(
        document__title="My Alexandria Document", name="myfile.pdf"
    )

    communications_attachment.file_attachment = None
    communications_attachment.document_attachment = None
    communications_attachment.alexandria_file = alexandria_file
    communications_attachment.save()

    response = admin_client.get(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]["attributes"]

    assert "signature" in data["download-url"]
    assert str(alexandria_file.pk) in data["download-url"]


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_create_message_with_alexandria_attachment(
    admin_client,
    communications_settings,
    notification_template,
    so_instance,
    topic_with_admin_involved,
    use_alexandria_backend,
):
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

    alexandria_file = FileFactory(
        document__title="My Alexandria Document", name="myfile.pdf"
    )

    response = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "new message",
            "topic": json.dumps(
                {
                    "id": str(topic_with_admin_involved.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": [
                json.dumps(
                    {
                        "id": str(alexandria_file.pk),
                        "type": "file",
                    }
                )
            ],
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_201_CREATED

    new_message = topic_with_admin_involved.messages.get(
        pk=response.json()["data"]["id"]
    )

    assert new_message.attachments.count() == 1
    assert new_message.attachments.first().alexandria_file == alexandria_file


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "has_permission,is_converted,has_key,expected_status",
    [
        (True, False, True, status.HTTP_200_OK),
        (False, False, True, status.HTTP_403_FORBIDDEN),  # no permission
        (True, True, True, status.HTTP_400_BAD_REQUEST),  # already converted
        (True, False, False, status.HTTP_400_BAD_REQUEST),  # missing key
    ],
)
def test_convert_to_alexandria_attachment(
    admin_client,
    communications_attachment,
    expected_status,
    has_key,
    has_permission,
    is_converted,
    topic_with_admin_involved,
    use_alexandria_backend,
):
    category = CategoryFactory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": (
                        [
                            {"permission": "create", "scope": "All"},
                        ]
                        if has_permission
                        else []
                    ),
                },
            }
        }
    )

    if is_converted:
        communications_attachment.file_attachment = None
        communications_attachment.alexandria_file = FileFactory()

    communications_attachment.document_attachment = None
    communications_attachment.save()

    response = admin_client.patch(
        reverse(
            "communications-attachment-convert-to-document",
            args=[communications_attachment.pk],
        ),
        {
            "data": {
                "type": "communications-attachments",
                "id": communications_attachment.pk,
                "attributes": {},
                "relationships": (
                    {
                        "category": {
                            "data": {
                                "id": str(category.pk),
                                "type": "categories",
                            }
                        },
                    }
                    if has_key
                    else {}
                ),
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        communications_attachment.refresh_from_db()
        assert communications_attachment.alexandria_file
        assert not communications_attachment.file_attachment
