import io
import json

import pytest
from alexandria.core.factories import CategoryFactory, FileFactory
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status


@pytest.mark.parametrize(
    ("role__name", "communications_message__topic"),
    [("Municipality", lf("topic_with_admin_involved"))],
)
@pytest.mark.parametrize(
    ("communications_attachment__file_type", "content_disposition"),
    [
        ("application/pdf", "inline"),
        ("text/plain", "attachment"),
    ],
)
def test_s3_attachment_download_url(
    admin_client,
    communications_attachment,
    use_alexandria_backend,
    content_disposition,
):
    communications_attachment.document_attachment = None
    communications_attachment.alexandria_file = None
    communications_attachment.save()

    response = admin_client.get(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]["attributes"]

    assert data["download-url"].startswith(
        f"http://testserver/api/v1/communications-attachments/{communications_attachment.pk}/download?expires="
    )
    resp = admin_client.get(data["download-url"])
    assert resp.status_code == status.HTTP_200_OK
    assert content_disposition in resp.headers["Content-Disposition"]


@pytest.mark.parametrize(
    ("role__name", "communications_message__topic"),
    [("Municipality", lf("topic_with_admin_involved"))],
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

    alexandria_file = FileFactory(document__title="Document", name="myfile.pdf")

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
    attachment = new_message.attachments.first()
    assert attachment.alexandria_file == alexandria_file
    assert attachment.file_attachment.name.endswith("Document.pdf")
    assert attachment.file_attachment.read()


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db
def test_convert_linked_alexandria_attachment_from_hidden_category(
    admin_client,
    communications_attachment,
    service_factory,
    topic_with_admin_involved,
    use_alexandria_backend,
):
    recipient_service = admin_client.user.get_default_group().service
    sender_service = service_factory()

    source_category = CategoryFactory(
        metainfo={"access": {"Municipality": {"visibility": "service"}}}
    )
    source_file = FileFactory(
        document__category=source_category,
        document__created_by_group=str(sender_service.pk),
        document__modified_by_group=str(sender_service.pk),
        name="hidden.pdf",
    )

    target_category = CategoryFactory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [{"permission": "create", "scope": "All"}],
                }
            }
        }
    )

    communications_attachment.message.topic.involved_entities = [
        sender_service.pk,
        recipient_service.pk,
    ]
    communications_attachment.message.topic.save()

    communications_attachment.document_attachment = None
    communications_attachment.alexandria_file = source_file
    communications_attachment.file_type = "application/pdf"
    communications_attachment.file_attachment.save(
        "hidden.pdf",
        io.BytesIO(b"communication attachment"),
        save=False,
    )
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
                "relationships": {
                    "category": {
                        "data": {
                            "id": str(target_category.pk),
                            "type": "categories",
                        }
                    }
                },
            }
        },
    )

    assert response.status_code == status.HTTP_200_OK

    communications_attachment.refresh_from_db()

    assert communications_attachment.alexandria_file_id != source_file.pk
    assert (
        communications_attachment.alexandria_file.document.category == target_category
    )
    assert communications_attachment.alexandria_file.created_by_group == str(
        recipient_service.pk
    )


@pytest.mark.parametrize(
    ("role__name", "has_permission", "is_converted", "has_key", "expected_status"),
    [
        ("Municipality", True, False, True, status.HTTP_200_OK),
        (
            "Municipality",
            False,
            False,
            True,
            status.HTTP_403_FORBIDDEN,
        ),  # no permission
        (
            "Municipality",
            True,
            True,
            True,
            status.HTTP_400_BAD_REQUEST,
        ),  # already converted
        (
            "Municipality",
            True,
            False,
            False,
            status.HTTP_400_BAD_REQUEST,
        ),  # missing key
        ("Support", True, False, True, status.HTTP_403_FORBIDDEN),
    ],
)
def test_convert_to_alexandria_attachment(
    admin_client,
    admin_user,
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
        communications_attachment.alexandria_file = FileFactory(
            document__metainfo={
                "copied-from-communications-attachment": str(
                    communications_attachment.pk
                )
            }
        )

    communications_attachment.document_attachment = None
    communications_attachment.save()

    communications_attachment.message.created_by_user = admin_user
    communications_attachment.message.save()

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
        assert communications_attachment.alexandria_file.created_by_user == str(
            admin_user.pk
        )
        assert communications_attachment.file_attachment
