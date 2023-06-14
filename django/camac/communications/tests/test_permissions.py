import pytest
from django.urls import reverse
from rest_framework import status

_admin = pytest.lazy_fixture("admin_user")
_other = pytest.lazy_fixture("some_other_user")


@pytest.mark.parametrize(
    "role__name, expect_status",
    [
        ("Municipality", status.HTTP_201_CREATED),
        ("Applicant", status.HTTP_201_CREATED),
    ],
)
def test_create_topic(
    db,
    be_instance,
    admin_client,
    expect_status,
    role,
):
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
        expected_entities = {"id": "APPLICANT", "name": "Gesuchsteller/in"}
    else:
        expected_entities = {
            "id": str(admin_client.user.get_default_group().service.pk),
            "name": admin_client.user.get_default_group().service.get_trans_obj().name,
        }
    assert data["data"]["attributes"]["involved-entities"] == [expected_entities]


_topic = pytest.lazy_fixture("communications_topic")
_message = pytest.lazy_fixture("communications_message")
_attachment = pytest.lazy_fixture("communications_attachment")


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
@pytest.mark.parametrize(
    "obj, url",
    [
        (_topic, "communications-topic-detail"),
        (_message, "communications-message-detail"),
        (_attachment, "communications-attachment-detail"),
    ],
)
def test_rejected_access(db, be_instance, admin_client, role, obj, url):
    url = reverse(url, args=[obj.pk])
    resp = admin_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant", "Service"])
def test_rejected_create_topic(db, be_instance, admin_client, role):
    """Test whether we can create a topic where we shouldn't be allowed"""
    url = reverse("communications-topic-list")
    if role.name != "Applicant":
        be_instance.services.set([])
        # Ensure "municipality" user doesn't have access either
        be_instance.location = None
        be_instance.save()

    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-topics",
                "attributes": {"subject": "hello", "involved-entities": []},
                "relationships": {
                    "instance": {
                        "data": {"id": str(be_instance.pk), "type": "instances"}
                    },
                },
            }
        },
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # check for proper validation error source
    assert (
        resp.json()["errors"][0]["source"]["pointer"] == "/data/relationships/instance"
    )


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_rejected_create_message(
    db, be_instance, admin_client, role, communications_topic
):
    """Test whether we can create a message where we shouldn't be allowed"""
    url = reverse("communications-message-list")
    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-messages",
                "attributes": {
                    "body": "hello",
                },
                "relationships": {
                    "topic": {
                        "data": {
                            "id": str(communications_topic.pk),
                            "type": "communications-topics",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # check for proper validation error source
    assert resp.json()["errors"][0]["source"]["pointer"] == "/data/relationships/topic"


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_rejected_create_attachment(
    db, be_instance, admin_client, role, communications_message
):
    """Test whether we can create a attachment where we shouldn't be allowed"""
    url = reverse("communications-attachment-list")
    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-attachments",
                "attributes": {},
                "relationships": {
                    "message": {
                        "data": {
                            "id": str(communications_message.pk),
                            "type": "communications-messages",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # check for proper validation error source
    assert (
        resp.json()["errors"][0]["source"]["pointer"] == "/data/relationships/message"
    )


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
@pytest.mark.parametrize(
    "communications_message__sent_at, communications_message__created_by_user, expect_status",
    [
        # Attachment on own, un-sent message should be OK
        (None, _admin, status.HTTP_201_CREATED),
        # Attachment on sent message should fail
        ("2022-12-12T01:02:03Z", _admin, status.HTTP_400_BAD_REQUEST),
        # Attachment on non-own message should fail
        (None, _other, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_message_status_on_attachments(
    db,
    be_instance,
    admin_client,
    role,
    communications_message,
    topic_with_admin_involved,
    attachment,
    expect_status,
):
    """Test whether we can create attachments with sent / unsent message status"""

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

    url = reverse("communications-attachment-list")
    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-attachments",
                "attributes": {},
                "relationships": {
                    "message": {
                        "data": {
                            "id": str(communications_message.pk),
                            "type": "communications-messages",
                        }
                    },
                    "document-attachment": {
                        "data": {
                            "id": str(attachment.pk),
                            "type": "attachments",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == expect_status
    # check for proper validation error source
    if expect_status == status.HTTP_400_BAD_REQUEST:
        assert (
            resp.json()["errors"][0]["source"]["pointer"]
            == "/data/relationships/message"
        )


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
@pytest.mark.parametrize(
    "communications_message__sent_at, communications_message__created_by_user, expect_status",
    [
        # Attachment on own, un-sent message should be OK
        (None, _admin, status.HTTP_200_OK),
        # Attachment on sent message should fail
        ("2022-12-12T01:02:03Z", _admin, status.HTTP_400_BAD_REQUEST),
        # Attachment on non-own message should fail
        (None, _other, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_message_status_on_modifying_message(
    db,
    be_instance,
    admin_client,
    role,
    communications_message,
    topic_with_admin_involved,
    attachment,
    expect_status,
):
    """Test whether we can modify a message with sent / unsent message status"""

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

    resp = admin_client.patch(
        reverse("communications-message-detail", args=[communications_message.pk]),
        {
            "data": {
                "id": communications_message.pk,
                "type": "communications-messages",
                "attributes": {"body": "revised body content"},
                "relationships": {
                    "topic": {
                        "data": {
                            "id": str(topic_with_admin_involved.pk),
                            "type": "communications-topics",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == expect_status


@pytest.fixture
def some_other_user(user_factory):
    return user_factory()


@pytest.mark.parametrize(
    ",".join(
        [
            "communications_topic__initiated_by",
            "communications_topic__allow_replies",
            "has_other_messages",
            "expect_status",
        ]
    ),
    [
        (_other, True, False, status.HTTP_201_CREATED),
        (_other, True, True, status.HTTP_201_CREATED),
        (_other, False, False, status.HTTP_400_BAD_REQUEST),
        (_other, False, True, status.HTTP_400_BAD_REQUEST),
        (_admin, True, False, status.HTTP_201_CREATED),
        (_admin, True, True, status.HTTP_201_CREATED),
        (_admin, False, False, status.HTTP_201_CREATED),
        (_admin, False, True, status.HTTP_201_CREATED),
    ],
)
@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_adding_message_with_allow_replies(
    db,
    be_instance,
    admin_client,
    communications_message_factory,
    role,
    topic_with_admin_involved,
    has_other_messages,
    notification_template,
    application_settings,
    expect_status,
):
    application_settings["COMMUNICATIONS"]["template_slug"] = notification_template.slug

    """Check whether we can add messages if topic forbids it"""
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        default_group = admin_client.user.get_default_group()
        default_group.service = None
        default_group.save()

    if has_other_messages:
        communications_message_factory(topic=topic_with_admin_involved)

    url = reverse("communications-message-list")
    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-messages",
                "attributes": {
                    "body": "hello",
                },
                "relationships": {
                    "topic": {
                        "data": {
                            "id": str(topic_with_admin_involved.pk),
                            "type": "communications-topics",
                        }
                    },
                },
            }
        },
    )
    assert resp.status_code == expect_status
