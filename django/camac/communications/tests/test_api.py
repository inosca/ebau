"""
Basic checking of API behaviour.

Detailed checks for permissions / visibilities are done in
the corresponding test modules.
"""

import io
import json
from contextlib import nullcontext as no_exception

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError

from camac.communications.models import (
    CommunicationsAttachment,
    CommunicationsMessage,
    entity_for_current_user,
)
from camac.communications.serializers import validate_mime_type
from camac.document.tests.data import django_file

MS_OFFICE_MIME_TYPES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


@pytest.mark.parametrize(
    "role__name, expect_status",
    [
        ("Municipality", status.HTTP_201_CREATED),
        ("Applicant", status.HTTP_201_CREATED),
        ("Support", status.HTTP_403_FORBIDDEN),
    ],
)
def test_create_topic(db, be_instance, admin_client, expect_status, role):
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

    resp = admin_client.post(
        reverse("communications-topic-list"),
        {
            "data": {
                "type": "communications-topics",
                "id": None,
                "attributes": {
                    "subject": "bar",
                    "involved-entities": [],
                    # intentionally using a wrong entity, to see if
                    # serializer properly overwrites it
                    "initiated-by-entity": {"id": "someone"},
                },
                "relationships": {
                    "instance": {
                        "data": {"id": str(be_instance.pk), "type": "instances"}
                    },
                },
            },
        },
    )

    assert resp.status_code == expect_status

    if expect_status != status.HTTP_403_FORBIDDEN:
        # Check that initiator is added to involved as well as set as
        # initiator
        data = resp.json()
        assert data["data"]["relationships"]["initiated-by"] == {
            "data": {
                "type": "users",
                "id": str(admin_client.user.pk),
            }
        }

        if role.name == "Applicant":
            entity_id = {"id": "APPLICANT", "name": "Gesuchsteller/in"}
        else:
            entity_id = {
                "id": str(admin_client.user.get_default_group().service.pk),
                "name": admin_client.user.get_default_group().service.get_name(),
            }
        assert data["data"]["attributes"]["involved-entities"] == [entity_id]
        assert data["data"]["attributes"]["initiated-by-entity"] == entity_id


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Municipality", status.HTTP_201_CREATED),
        ("Support", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize("with_file_attachments", [True, False])
@pytest.mark.parametrize("with_doc_attachments", [True, False])
def test_create_message(
    db,
    be_instance,
    admin_user,
    admin_client,
    topic_with_admin_involved,
    tmpdir,
    expected_status,
    with_doc_attachments,
    with_file_attachments,
    attachment_factory,
    notification_template,
    communications_settings,
):
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug
    communications_settings["ALLOWED_MIME_TYPES"] = ["text/plain"]

    attachments = []
    if with_file_attachments:
        for x in range(2):
            file = tmpdir / f"file_{x}.txt"
            file.open("w").write(f"hello {x}")
            attachments.append(file.open("r"))
    if with_doc_attachments:
        for x in range(2):
            attachments.append(
                json.dumps(
                    {
                        "id": str(
                            attachment_factory(
                                path=django_file("multiple-pages.pdf"),
                                context={"displayName": "Doc"},
                                name=f"file_{x}.pdf",
                            ).pk
                        ),
                        "type": "attachments",
                    }
                )
            )

    resp = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "hello world",
            "topic": json.dumps(
                {
                    "id": str(topic_with_admin_involved.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": attachments,
        },
        format="multipart",
    )
    assert resp.status_code == expected_status

    if expected_status != status.HTTP_403_FORBIDDEN:
        new_message = topic_with_admin_involved.messages.get(
            pk=resp.json()["data"]["id"]
        )
        assert new_message.attachments.count() == len(attachments)
        for attachment in new_message.attachments.all():
            assert attachment.file_attachment.read()

            if with_doc_attachments and attachment.document_attachment:
                assert attachment.document_attachment
                assert attachment.file_attachment.name.endswith("Doc.pdf")


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
@pytest.mark.parametrize(
    "has_document, has_file, expect_status",
    [
        [False, False, status.HTTP_404_NOT_FOUND],
        [False, True, status.HTTP_200_OK],
        [True, False, status.HTTP_200_OK],
        [True, True, status.HTTP_200_OK],
    ],
)
def test_attachment_download(
    db,
    be_instance,
    role,
    admin_client,
    communications_message,
    communications_attachment,
    attachment_factory,
    has_document,
    has_file,
    expect_status,
):
    expected_file_content = None
    communications_message.topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    communications_message.topic.save()

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

    if has_file:
        communications_attachment.file_attachment.save(
            "foo.txt", io.BytesIO(b"asdfasdf")
        )
        expected_file_content = communications_attachment.file_attachment.read()
    else:
        communications_attachment.file_attachment = None

    if has_document:
        communications_attachment.document_attachment = attachment_factory()
        if not has_file:
            expected_file_content = (
                communications_attachment.document_attachment.path.read()
            )
    else:
        communications_attachment.document_attachment = None

    communications_attachment.save()

    get_response = admin_client.get(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    url = get_response.json()["data"]["attributes"]["download-url"]

    resp = admin_client.get(url)

    assert resp.status_code == expect_status
    if expect_status == status.HTTP_200_OK:
        assert resp.status_code == status.HTTP_200_OK
        assert resp.getvalue() == expected_file_content


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_included_dossier_number(
    db,
    be_instance,
    admin_client,
    communications_topic,
    be_communications_settings,
):
    be_instance.case.meta["ebau-number"] = "2022-1299"
    be_instance.case.save()
    communications_topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    communications_topic.save()

    resp = admin_client.get(reverse("communications-topic-list"))

    assert be_instance.case.meta["ebau-number"]

    assert (
        resp.json()["data"][0]["attributes"]["dossier-number"]
        == be_instance.case.meta["ebau-number"]
    )


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
@pytest.mark.parametrize("notifications_enabled", [1, 0])
def test_notification_email(
    db,
    admin_client,
    communications_topic,
    be_instance,
    admin_user,
    mailoutbox,
    notification_template,
    communications_settings,
    service_factory,
    role,
    notifications_enabled,
):
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

    other_service = service_factory(notification=notifications_enabled)
    communications_topic.involved_entities = [
        admin_user.get_default_group().service_id,
        other_service.pk,
        "APPLICANT",
    ]
    communications_topic.save()

    if role.name == "Applicant":
        be_instance.involved_applicants.update(invitee=admin_user)
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

    resp = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "hello world",
            "topic": json.dumps(
                {
                    "id": str(communications_topic.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": [],
        },
        format="multipart",
    )
    assert resp.status_code == status.HTTP_201_CREATED
    if notifications_enabled:
        assert len(mailoutbox) == 2
        recipient_emails = [email.recipients()[0] for email in mailoutbox]
        assert other_service.email in recipient_emails
        assert notification_template.subject in mailoutbox[0].subject
        assert notification_template.subject in mailoutbox[1].subject
    else:
        assert len(mailoutbox) == 1
        recipient_emails = [email.recipients()[0] for email in mailoutbox]
        assert other_service.email not in recipient_emails
        assert notification_template.subject in mailoutbox[0].subject


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("error_type", ["extension", "content", "unallowed"])
def test_mime_type_validation(
    db,
    admin_client,
    topic_with_admin_involved,
    tmpdir,
    communications_settings,
    mocker,
    error_type,
):
    mocker.patch("camac.notification.utils.send_mail")

    communications_settings["ALLOWED_MIME_TYPES"] = ["text/plain"]
    file = django_file("no-thumbnail.txt")

    if error_type == "unallowed":
        communications_settings["ALLOWED_MIME_TYPES"] = ["application/pdf"]
    elif error_type == "extension":
        file.name = "test.pdf"
    elif error_type == "content":
        file = django_file("test-thumbnail.jpg")

    response = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "hello world",
            "topic": json.dumps(
                {
                    "id": str(topic_with_admin_involved.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": [file],
        },
        format="multipart",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name,expected_status,expected_count",
    [
        ("Support", status.HTTP_204_NO_CONTENT, 0),
        ("Municipality", status.HTTP_403_FORBIDDEN, 1),
        ("Applicant", status.HTTP_403_FORBIDDEN, 1),
    ],
)
def test_delete_attachment(
    db,
    admin_user,
    admin_client,
    communications_message,
    communications_attachment,
    expected_status,
    expected_count,
):
    communications_message.topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    communications_message.topic.save()

    communications_attachment.file_attachment.save("test.txt", io.BytesIO(b"foobar"))

    communications_attachment.document_attachment.instance.involved_applicants.update(
        invitee=admin_user
    )

    response = admin_client.delete(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == expected_status

    assert len(CommunicationsAttachment.objects.all()) == expected_count


def test_create_message_without_group(
    db,
    be_instance,
    admin_client,
    topic_with_admin_involved,
    notification_template,
    communications_settings,
):
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug
    communications_settings["ALLOWED_MIME_TYPES"] = ["text/plain"]

    attachments = []
    admin_client.user.groups.set([])

    resp = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "hello world",
            "topic": json.dumps(
                {
                    "id": str(topic_with_admin_involved.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": attachments,
        },
        format="multipart",
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("has_group", [True, False])
def test_entity_for_current_user(db, admin_user, be_instance, has_group, rf):
    request = rf.request()
    request.user = admin_user
    if has_group:
        request.group = admin_user.get_default_group()
        expected_result = str(request.group.service_id)
    else:
        request.group = None
        expected_result = None

    assert entity_for_current_user(request) == expected_result


@pytest.mark.parametrize(
    "role__name",
    ["Municipality"],
)
@pytest.mark.parametrize(
    "display_name,corrected_display_name",
    [
        ("foo/bar", "foobar.pdf"),
        ("test", "test.pdf"),
        ("fo.bär", "fo.bär.pdf"),
        ("t e s t", "t_e_s_t.pdf"),
        ("foo:bar", "foobar.pdf"),
        ("is this a file?", "is_this_a_file.pdf"),
        (None, "file.pdf"),
    ],
)
def test_validation_of_display_name_by_message_creation(
    db,
    be_instance,
    admin_client,
    topic_with_admin_involved,
    display_name,
    corrected_display_name,
    attachment_factory,
    notification_template,
    communications_settings,
):
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

    attachment = json.dumps(
        {
            "id": str(
                attachment_factory(
                    path=django_file("multiple-pages.pdf"),
                    context={"displayName": display_name},
                    name="file.pdf",
                ).pk
            ),
            "type": "attachments",
        }
    )

    resp = admin_client.post(
        reverse("communications-message-list"),
        data={
            "body": "hello world",
            "topic": json.dumps(
                {
                    "id": str(topic_with_admin_involved.pk),
                    "type": "communications-topics",
                }
            ),
            "attachments": [attachment],
        },
        format="multipart",
    )
    assert resp.status_code == status.HTTP_201_CREATED

    for attachment in CommunicationsMessage.objects.get(
        pk=resp.json()["data"]["id"]
    ).attachments.all():
        assert attachment.file_attachment.name.endswith(corrected_display_name)


@pytest.mark.parametrize(
    "content_type, expectation",
    [
        ("application/x-zip-compressed", no_exception()),
        ("application/zip-compressed", no_exception()),
        ("application/x-zip", no_exception()),
        ("application/zip", no_exception()),
        ("application/x-not-a-zip-archive", pytest.raises(ValidationError)),
    ],
)
def test_validate_mime_type_alternative_mime_for_zip(
    caplog,
    content_type,
    expectation,
    mocker,
    settings,
):

    raw_file = django_file("simple-archive.zip")
    filename = "testfile.zip"

    file = InMemoryUploadedFile(
        file=raw_file,
        name=filename,
        content_type=content_type,
        size=raw_file.size,
        charset="utf8",
        field_name="irrelevant",
    )

    with expectation:
        validate_mime_type(file)


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_display_of_instance_marks(
    db, admin_client, instance_mark_factory, topic_with_admin_involved
):
    instance_mark = instance_mark_factory()
    topic_with_admin_involved.instance.instance_marks.add(instance_mark)

    resp = admin_client.get(
        reverse("communications-topic-list"),
        data={
            "include": "instance_marks",
            "page[number]": "1",
            "page[size]": "20",
            "sort": "-last_message_date",
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    expected_relationship = {
        "data": [{"id": str(instance_mark.pk), "type": "instance-marks"}],
        "meta": {"count": 1},
    }
    assert data["data"][0]["relationships"]["instance-marks"] == expected_relationship
    assert data["included"][0]["id"] == str(instance_mark.pk)
