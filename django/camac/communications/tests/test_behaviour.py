import io

import pytest
from django.urls import reverse
from django.utils.translation import gettext
from rest_framework import status


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name, role_t__name",
    [
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
        )
    ],
)
def test_mark_as_read(db, admin_client, communications_message, be_instance):
    # Before marking as read, the message should be "unread"
    communications_message.topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    communications_message.topic.save()
    be_instance.services.add(admin_client.user.get_default_group().service)

    resp_before = admin_client.get(
        reverse("communications-message-detail", args=[communications_message.pk])
    )
    assert resp_before.status_code == status.HTTP_200_OK
    assert resp_before.json()["data"]["attributes"]["read-at"] is None

    # The modification should already return the new "read" status
    resp_mark = admin_client.patch(
        reverse("communications-message-read", args=[communications_message.pk])
    )
    assert resp_mark.status_code == status.HTTP_200_OK
    assert resp_mark.json()["data"]["attributes"]["read-at"]

    communications_message.read_by.create(entity="APPLICANT")
    communications_message.save()

    # Ensure the "read" mark is persisted
    resp_after = admin_client.get(
        reverse("communications-message-detail", args=[communications_message.pk])
    )
    assert resp_after.status_code == status.HTTP_200_OK
    assert resp_after.json()["data"]["attributes"]["read-at"]

    read_by_info = resp_after.json()["data"]["attributes"]["read-by-entity"]
    expected_read_by = [
        {
            "name": str(
                admin_client.user.get_default_group().service.get_trans_obj().name
            ),
            "id": str(admin_client.user.get_default_group().service.pk),
        },
        {
            "id": "APPLICANT",
            "name": gettext("Applicant"),
        },
    ]

    assert sorted(read_by_info, key=lambda x: x["id"]) == sorted(
        expected_read_by, key=lambda x: x["id"]
    )


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name, role_t__name",
    [
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
        )
    ],
)
def test_mark_as_unread(db, admin_client, communications_message, be_instance):
    communications_message.topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    my_entity = str(admin_client.user.get_default_group().service_id)
    communications_message.topic.save()
    be_instance.services.add(admin_client.user.get_default_group().service)

    # Mark as read directly on DB
    communications_message.read_by.get_or_create(entity=my_entity)

    # Mark as unread via API
    admin_client.patch(
        reverse("communications-message-unread", args=[communications_message.pk])
    )

    # Read flag gone?
    communications_message.refresh_from_db()
    assert not communications_message.read_by.filter(entity=my_entity).exists()


@pytest.mark.parametrize("applicant_involved, expect_mail", [(True, 1), (False, 0)])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_send_message(
    db,
    admin_client,
    communications_message,
    mailoutbox,
    topic_with_admin_involved,
    be_instance,
    applicant_involved,
    expect_mail,
    notification_template,
    application_settings,
):
    application_settings["COMMUNICATIONS"]["template_slug"] = notification_template.slug

    topic = communications_message.topic

    if applicant_involved:
        topic.involved_entities.append("APPLICANT")
    else:
        # Just make sure we don't have an applicant involved
        topic.involved_entities = [
            e for e in topic.involved_entities if e != "APPLICANT"
        ]
    topic.save()

    # topic.refresh_from_db()
    # assert ('APPLICANT' in topic.involved_entities) == applicant_involved

    # Before sending, the message should not have a sent-at date
    resp_before = admin_client.get(
        reverse("communications-message-detail", args=[communications_message.pk])
    )
    assert resp_before.status_code == status.HTTP_200_OK
    assert resp_before.json()["data"]["attributes"]["sent-at"] is None

    assert len(mailoutbox) == 0

    # When triggering the send action, the sent-at field should get set
    resp_mark = admin_client.patch(
        reverse("communications-message-send", args=[communications_message.pk])
    )
    assert resp_mark.status_code == status.HTTP_200_OK
    assert resp_mark.json()["data"]["attributes"]["sent-at"]

    # If applicants are involved, we expect a notification is
    # now sent
    assert len(mailoutbox) == expect_mail

    # Ensure the "sent-at" date is persisted
    resp_after = admin_client.get(
        reverse("communications-message-detail", args=[communications_message.pk])
    )
    assert resp_after.status_code == status.HTTP_200_OK
    assert resp_after.json()["data"]["attributes"]["sent-at"]

    # Ensure we cannot send the message twice
    resp_mark_again = admin_client.patch(
        reverse("communications-message-send", args=[communications_message.pk])
    )
    assert resp_mark_again.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "entities, expect_status",
    [
        (["APPLICANT"], status.HTTP_201_CREATED),
        (["APPLICANT", "_valid_entity_"], status.HTTP_201_CREATED),
        (["APPLICANT", "9999999"], status.HTTP_400_BAD_REQUEST),
        (["applicant", "_valid_entity_"], status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_validate_entities(
    db,
    role,
    be_instance,
    admin_client,
    entities,
    expect_status,
):
    entity_ids = [
        e.replace(
            "_valid_entity_", str(admin_client.user.get_default_group().service_id)
        )
        for e in entities
    ]
    entities = [{"id": e} for e in entity_ids]  # No need to write the name here

    resp = admin_client.post(
        reverse("communications-topic-list"),
        {
            "data": {
                "type": "communications-topics",
                "id": None,
                "attributes": {
                    "subject": "bar",
                    "involved-entities": entities,
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

    if expect_status == status.HTTP_201_CREATED:
        # Check that initiator is added to involved as well as set as
        # initiator
        data = resp.json()
        returned_entities = [
            entity["id"] for entity in data["data"]["attributes"]["involved-entities"]
        ]
        # Since we're "municipality" here, we expect that "our"
        # entity is added always
        municipality_entity = str(
            be_instance.instance_services.filter(active=1).get().service_id
        )
        if municipality_entity not in entity_ids:
            entity_ids.append(municipality_entity)

        assert sorted(returned_entities) == sorted(entity_ids)


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_set_initial_entity(db, be_instance, admin_client, role):
    if role.name == "Applicant":
        expect_entities = ["APPLICANT"]
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()
    else:
        expect_entities = [str(admin_client.user.get_default_group().service_id)]

    resp = admin_client.post(
        reverse("communications-topic-list"),
        {
            "data": {
                "type": "communications-topics",
                "id": None,
                "attributes": {
                    "subject": "bar",
                    "involved-entities": [],
                },
                "relationships": {
                    "instance": {
                        "data": {"id": str(be_instance.pk), "type": "instances"}
                    },
                },
            }
        },
    )

    assert resp.status_code == status.HTTP_201_CREATED

    # Check that initiator is added to involved as well as set as
    # initiator
    data = resp.json()
    returned_entities = [
        entity["id"] for entity in data["data"]["attributes"]["involved-entities"]
    ]

    assert returned_entities == expect_entities


@pytest.mark.parametrize(
    "send_entities, expect_entities,expect_status",
    [
        # No entities - expect to add applicant itself
        ([], ["APPLICANT"], status.HTTP_201_CREATED),
        # Invalid entity - should trigger validation
        (["9999999999"], [], status.HTTP_400_BAD_REQUEST),
        # LB service - should be allowed in validation. "APPLICANT" should
        # be added always when applicant creates topic
        (["LB"], ["LB", "APPLICANT"], status.HTTP_201_CREATED),
        (["OTHER"], [], status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.parametrize("role__name", ["Applicant"])
def test_validate_topic_entities_for_applicant(
    db,
    be_instance,
    admin_client,
    service_factory,
    send_entities,
    expect_entities,
    expect_status,
):
    be_instance.involved_applicants.create(
        invitee=admin_client.user, user=admin_client.user
    )
    lb_entity = str(be_instance.instance_services.filter(active=1).get().service_id)

    default_group = admin_client.user.get_default_group()
    default_group.service = None
    default_group.save()

    # decode "LB" and "other" markers ("APPLICANT" and fixed IDS remain)
    entities_lookup = {"LB": lb_entity, "OTHER": str(service_factory().pk)}
    send_entities = [{"id": entities_lookup.get(e, e)} for e in send_entities]
    expect_entities = [entities_lookup.get(e, e) for e in expect_entities]

    resp = admin_client.post(
        reverse("communications-topic-list"),
        {
            "data": {
                "type": "communications-topics",
                "id": None,
                "attributes": {
                    "subject": "bar",
                    "involved-entities": send_entities,
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

    if expect_status < 400:
        # Check that initiator is added to involved as well as set as
        # initiator
        data = resp.json()
        returned_entities = [
            entity["id"] for entity in data["data"]["attributes"]["involved-entities"]
        ]

        assert returned_entities == expect_entities


@pytest.mark.parametrize("communications_attachment__document_attachment", [None])
@pytest.mark.parametrize("communications_attachment__file_type", ["text/plain"])
@pytest.mark.parametrize(
    "role__name, expect_result",
    [("Municipality", status.HTTP_200_OK), ("Applicant", status.HTTP_403_FORBIDDEN)],
)
def test_convert_attachment_to_document(
    db,
    be_instance,
    role,
    expect_result,
    admin_client,
    communications_message,
    communications_attachment,
    attachment_section,
):
    communications_message.topic.involved_entities = [
        admin_client.user.get_default_group().service_id,
        "APPLICANT",
    ]
    communications_message.topic.save()

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

    communications_attachment.file_attachment.save("foo.txt", io.BytesIO(b"asdfasdf"))
    communications_attachment.save()

    url = reverse(
        "communications-attachment-convert-to-document",
        args=[communications_attachment.pk],
    )

    resp = admin_client.patch(
        url,
        {
            "data": {
                "type": "communications-attachments",
                "id": communications_attachment.pk,
                "attributes": {},
                "relationships": {
                    "section": {
                        "data": {
                            "id": str(attachment_section.pk),
                            "type": "attachment-sections",
                        }
                    },
                },
            }
        },
    )

    assert resp.status_code == expect_result

    communications_attachment.refresh_from_db()

    if expect_result == status.HTTP_403_FORBIDDEN:
        # no change should have happened
        assert not communications_attachment.document_attachment
        assert communications_attachment.file_attachment
        return

    assert communications_attachment.document_attachment
    assert not communications_attachment.file_attachment

    expected_json = {
        "data": {
            "attributes": {"filename": "foo.txt"},
            "id": str(communications_attachment.pk),
            "relationships": {
                "document-attachment": {
                    "data": {
                        "id": str(communications_attachment.document_attachment_id),
                        "type": "attachments",
                    }
                }
            },
            "type": "communications-attachments",
        }
    }
    assert resp.json() == expected_json
