"""
Basic checking of API behaviour.

Detailed checks for permissions / visibilities are done in
the corresponding test modules.
"""
import io
import json
import os

import pytest
from django.urls import reverse
from rest_framework import status

from camac.communications import models

_admin = pytest.lazy_fixture("admin_user")
_other = pytest.lazy_fixture("some_other_user")


@pytest.mark.parametrize(
    "role__name, expect_status",
    [
        ("Municipality", status.HTTP_201_CREATED),
        ("Applicant", status.HTTP_201_CREATED),
    ],
)
def test_create_topic(db, be_instance, admin_client, expect_status, role):
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

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
            }
        },
    )

    assert resp.status_code == expect_status

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
            "name": admin_client.user.get_default_group().service.get_trans_obj().name,
        }
    assert data["data"]["attributes"]["involved-entities"] == [entity_id]
    assert data["data"]["attributes"]["initiated-by-entity"] == entity_id


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("with_file_attachments", [True, False])
@pytest.mark.parametrize("with_doc_attachments", [True, False])
def test_create_message(
    db,
    be_instance,
    admin_client,
    topic_with_admin_involved,
    tmpdir,
    with_doc_attachments,
    with_file_attachments,
    attachment_factory,
    notification_template,
    application_settings,
):
    application_settings["COMMUNICATIONS"]["template_slug"] = notification_template.slug

    attachments = []
    if with_file_attachments:
        for x in range(2):
            file = tmpdir / f"file_{x}.txt"
            file.open("w").write(f"hello {x}")
            attachments.append(file.open("r"))
    if with_doc_attachments:
        for x in range(2):
            attachments.append(
                json.dumps({"id": str(attachment_factory().pk), "type": "attachments"})
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
    assert resp.status_code == status.HTTP_201_CREATED

    new_message = topic_with_admin_involved.messages.get(pk=resp.json()["data"]["id"])
    assert new_message.attachments.count() == len(attachments)
    for attachment in new_message.attachments.all():
        if attachment.file_attachment:
            assert attachment.file_attachment.read()
        else:
            assert attachment.document_attachment


@pytest.mark.parametrize("communications_message__created_by_user", [_admin])
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "has_document, expect_status",
    [
        [False, status.HTTP_400_BAD_REQUEST],
        [True, status.HTTP_201_CREATED],
    ],
)
def test_attachment_create_jsonapi(
    db,
    be_instance,
    admin_client,
    topic_with_admin_involved,
    communications_message,
    has_document,
    attachment_factory,
    expect_status,
):
    post_data = {
        "data": {
            "type": "communications-attachments",
            "id": None,
            "attributes": {"body": "hello world"},
            "relationships": {
                "message": {
                    "data": {
                        "id": str(communications_message.pk),
                        "type": "communications-messages",
                    }
                },
            },
        }
    }
    if has_document:
        post_data["data"]["relationships"]["document-attachment"] = {
            "data": {
                "id": str(attachment_factory().pk),
                "type": "attachments",
            }
        }
    resp = admin_client.post(
        reverse("communications-attachment-list"),
        post_data,
    )
    assert resp.status_code == expect_status


@pytest.mark.parametrize("communications_message__created_by_user", [_admin])
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "has_document, has_file, expect_status",
    [
        [False, False, status.HTTP_400_BAD_REQUEST],
        [False, True, status.HTTP_201_CREATED],
        [True, False, status.HTTP_201_CREATED],
        [True, True, status.HTTP_400_BAD_REQUEST],
    ],
)
def test_attachment_create_with_upload(
    db,
    be_instance,
    admin_client,
    communications_message,
    topic_with_admin_involved,
    attachment_factory,
    has_document,
    has_file,
    expect_status,
    tmp_path,
):
    the_file = tmp_path / "foo.txt"
    with the_file.open("w") as fh_out:
        fh_out.write("hello")

    post_data = {
        "message": str(communications_message.pk),
    }

    if has_file:
        post_data["file-attachment"] = the_file.open("r")
    if has_document:
        post_data["document-attachment"] = attachment_factory().pk

    resp = admin_client.post(
        reverse("communications-attachment-list"),
        data=post_data,
        format="multipart",
    )

    assert resp.status_code == expect_status
    if expect_status == status.HTTP_201_CREATED:
        att = models.CommunicationsAttachment.objects.get(
            pk=(resp.json()["data"]["id"])
        )
        if has_file:
            assert att.file_attachment.read() == b"hello"
        else:
            assert att.document_attachment


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
        expected_file_content = (
            communications_attachment.document_attachment.path.read()
        )
    else:
        communications_attachment.document_attachment = None

    communications_attachment.save()

    resp = admin_client.get(
        reverse(
            "communications-attachment-download", args=[communications_attachment.pk]
        )
    )

    assert resp.status_code == expect_status
    if expect_status == status.HTTP_200_OK:
        assert os.path.exists(resp.headers["X-Sendfile"])
        with open(resp.headers["X-Sendfile"], "rb") as fh_download:
            assert fh_download.read() == expected_file_content


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_included_dossier_number(
    db,
    be_instance,
    admin_client,
    communications_topic,
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
