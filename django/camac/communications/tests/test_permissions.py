import io
import json

import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)

from camac.document import permissions
from camac.permissions.conditions import Always, Never
from camac.permissions.switcher import PERMISSION_MODE

_admin = lf("admin_user")
_other = lf("some_other_user")


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
            "name": admin_client.user.get_default_group().service.get_name(),
        }
    assert data["data"]["attributes"]["involved-entities"] == [expected_entities]


_topic = lf("communications_topic")
_message = lf("communications_message")
_attachment = lf("communications_attachment")


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
    """Test whether we can create a topic where we shouldn't be allowed."""
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


@pytest.mark.parametrize("role__name", ["Applicant"])
@pytest.mark.parametrize("forge_entity", [False, True])
def test_rejected_create_topic_on_unsubmitted_instance(
    db,
    applicant_factory,
    instance_factory,
    service_factory,
    admin_client,
    forge_entity,
):
    """Test whether we can create a topic on an unsubmitted instance."""
    portal_group = admin_client.user.groups.first()
    portal_group.service = None
    portal_group.save()
    i = instance_factory(group=portal_group)
    applicant_factory(invitee=admin_client.user, instance=i)

    if forge_entity:
        # Scenario where the applicant attempts to fake an assigned service:
        s = service_factory()
        entities = [{"id": str(s.pk), "name": s.name}]
        errormsg = "Es existiert keine zuständige Organisation für dieses Dossier"
    else:
        # Normal behaviour of frontend on unsubmitted instance:
        entities = [{"id": None}]
        errormsg = "Involved entity must be either 'APPLICANT' or a valid service ID"

    url = reverse("communications-topic-list")
    resp = admin_client.post(
        url,
        {
            "data": {
                "type": "communications-topics",
                "attributes": {
                    "subject": "hello",
                    "involved-entities": entities,
                },
                "relationships": {
                    "instance": {
                        "data": {"type": "instances", "id": str(i.pk)},
                    }
                },
            }
        },
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json()["errors"] == [
        {
            "detail": errormsg,
            "status": "400",
            "source": {"pointer": "/data/attributes/involved-entities"},
            "code": "invalid",
        },
    ]


@pytest.mark.parametrize("role__name", ["Municipality", "Applicant"])
def test_rejected_create_message(
    db, be_instance, admin_client, role, communications_topic
):
    """Test whether we can create a message where we shouldn't be allowed."""
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


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("method", ["delete", "patch"])
def test_message_unallowed_methods(db, admin_client, communications_message, method):
    url = reverse("communications-message-detail", args=[communications_message.pk])
    response = getattr(admin_client, method)(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("method", ["post", "patch"])
def test_attachment_unallowed_methods(
    db,
    admin_client,
    communications_attachment,
    method,
):
    if method == "post":
        url = reverse("communications-attachment-list")
    else:
        url = reverse(
            "communications-attachment-detail", args=[communications_attachment.pk]
        )

    response = getattr(admin_client, method)(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


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
    communications_settings,
    expect_status,
):
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

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


@pytest.mark.parametrize("communications_attachment__document_attachment", [None])
@pytest.mark.parametrize("communications_attachment__file_type", ["text/plain"])
@pytest.mark.parametrize(
    "role__name,has_acl_permission,has_section_permission,expect_result",
    [
        # Permissions module: Document conversion requires
        # "communications-convert-to-document" permission and
        # a write section permission in the documents module
        ("municipality-lead", True, True, HTTP_200_OK),
        ("municipality-lead", False, True, HTTP_403_FORBIDDEN),
        ("municipality-lead", False, False, HTTP_403_FORBIDDEN),
        ("municipality-lead", True, False, HTTP_403_FORBIDDEN),
        ("Applicant", True, True, HTTP_200_OK),
        ("Applicant", False, True, HTTP_403_FORBIDDEN),
        ("Applicant", False, False, HTTP_403_FORBIDDEN),
        ("Applicant", True, False, HTTP_403_FORBIDDEN),
    ],
)
def test_permission_convert_attachment_to_document_acl(
    db,
    be_instance,
    role,
    admin_client,
    communications_message,
    communications_attachment,
    attachment_section,
    permissions_settings,
    application_settings,
    mocker,
    instance_acl_factory,
    access_level,
    has_acl_permission,
    has_section_permission,
    expect_result,
):
    application_settings["DOCUMENT_BACKEND"] = "camac-ng"
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-convert-to-document",
                Always() if has_acl_permission else Never(),
            )
        ]
    }

    mocker.patch(
        "camac.document.permissions.PERMISSIONS_BY_ACCESSLEVEL",
        {
            "test": {
                access_level.slug: {
                    permissions.AdminPermission: (
                        permissions._allow_always,
                        [attachment_section.pk] if has_section_permission else [],
                    ),
                }
            }
        },
    )

    service = admin_client.user.get_default_group().service
    communications_message.topic.involved_entities = [
        service.pk,
        "APPLICANT",
    ]
    communications_message.topic.save()

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )
    else:
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
        )

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


@pytest.mark.parametrize("communications_attachment__document_attachment", [None])
@pytest.mark.parametrize("communications_attachment__file_type", ["text/plain"])
@pytest.mark.parametrize(
    "role__name,has_section_permission,expect_result",
    [
        # RBAC: Internal roles except for support can convert to document,
        # as long as they are involved and have the section write permission
        # in the documents module, applicants are not allowed.
        ("municipality-lead", True, HTTP_200_OK),
        ("municipality-lead", False, HTTP_403_FORBIDDEN),
        ("Applicant", True, HTTP_403_FORBIDDEN),
        ("Applicant", False, HTTP_403_FORBIDDEN),
        ("Support", True, HTTP_403_FORBIDDEN),
        ("Support", False, HTTP_403_FORBIDDEN),
    ],
)
def test_permission_convert_attachment_to_document_rbac(
    db,
    be_instance,
    role,
    admin_client,
    communications_message,
    communications_attachment,
    attachment_section,
    permissions_settings,
    application_settings,
    mocker,
    instance_acl_factory,
    access_level,
    has_section_permission,
    expect_result,
):
    application_settings["DOCUMENT_BACKEND"] = "camac-ng"
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "test": {
                role.name: {
                    permissions.AdminPermission: [attachment_section.pk]
                    if has_section_permission
                    else []
                }
            }
        },
    )

    service = admin_client.user.get_default_group().service
    communications_message.topic.involved_entities = [service.pk, "APPLICANT"]
    communications_message.topic.save()

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

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


@pytest.mark.parametrize(
    "role__name,has_permission, expect_status",
    [
        # Permissions module: Topic creation requires
        # communications-write permission
        ("Municipality", True, status.HTTP_201_CREATED),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_201_CREATED),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_create_topic_acl(
    db,
    be_instance,
    admin_client,
    expect_status,
    role,
    permissions_settings,
    instance_acl_factory,
    access_level,
    has_permission,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-write",
                Always() if has_permission else Never(),
            )
        ]
    }

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )

    else:
        service = admin_client.user.get_default_group().service
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
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


@pytest.mark.parametrize(
    "role__name,expect_status",
    [
        # RBAC: Everybody can create topic, except for the support
        ("Municipality", status.HTTP_201_CREATED),
        ("Applicant", status.HTTP_201_CREATED),
        ("Support", status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_create_topic_rbac(
    db,
    be_instance,
    admin_client,
    expect_status,
    role,
    permissions_settings,
    instance_acl_factory,
    access_level,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF
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


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Marking as read requires
        # "communications-write" permission
        ("municipality-lead", True, status.HTTP_200_OK),
        ("municipality-lead", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Support", False, status.HTTP_403_FORBIDDEN),
        ("Support", True, status.HTTP_200_OK),
    ],
)
def test_permission_mark_as_read_acl(
    db,
    admin_client,
    role,
    access_level,
    communications_message,
    topic_with_admin_involved,
    be_instance,
    instance_acl_factory,
    permissions_settings,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-write",
                Always() if has_permission else Never(),
            )
        ]
    }

    service = admin_client.user.get_default_group().service
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )

    else:
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
        )

    resp_mark = admin_client.patch(
        reverse("communications-message-read", args=[communications_message.pk])
    )
    assert resp_mark.status_code == expected_status


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        # RBAC: Everybody can mark as read, except for support
        ("municipality-lead", status.HTTP_200_OK),
        ("Applicant", status.HTTP_200_OK),
        ("Support", status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_mark_as_read_rbac(
    db,
    admin_client,
    role,
    communications_message,
    topic_with_admin_involved,
    be_instance,
    permissions_settings,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

    resp_mark = admin_client.patch(
        reverse("communications-message-read", args=[communications_message.pk])
    )
    assert resp_mark.status_code == expected_status


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Marking as unread requires
        # "communications-write" permission
        ("municipality-lead", True, status.HTTP_200_OK),
        ("municipality-lead", False, status.HTTP_403_FORBIDDEN),
        ("Support", True, status.HTTP_200_OK),
        ("Support", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_200_OK),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_mark_as_unread_acl(
    db,
    admin_client,
    role,
    communications_message,
    topic_with_admin_involved,
    instance_acl_factory,
    access_level,
    permissions_settings,
    be_instance,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-write",
                Always() if has_permission else Never(),
            )
        ]
    }

    service = admin_client.user.get_default_group().service
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )

    else:
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
        )

    # Mark as read directly on DB
    communications_message.read_by.get_or_create(entity=str(service.pk))

    # Mark as unread via API
    resp = admin_client.patch(
        reverse("communications-message-unread", args=[communications_message.pk])
    )

    assert resp.status_code == expected_status


@pytest.mark.parametrize("communications_message__sent_at", ["2022-12-12T12:12:12Z"])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        # RBAC: Everbody can mark as unread, except for support
        ("municipality-lead", status.HTTP_200_OK),
        ("Support", status.HTTP_403_FORBIDDEN),
        ("Applicant", status.HTTP_200_OK),
    ],
)
def test_permission_mark_as_unread_rbac(
    db,
    admin_client,
    role,
    communications_message,
    topic_with_admin_involved,
    instance_acl_factory,
    access_level,
    permissions_settings,
    be_instance,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    service = admin_client.user.get_default_group().service
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

    # Mark as read directly on DB
    communications_message.read_by.get_or_create(entity=str(service.pk))

    # Mark as unread via API
    resp = admin_client.patch(
        reverse("communications-message-unread", args=[communications_message.pk])
    )

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Creating message requires
        # "communications-write" permission
        ("Municipality", True, status.HTTP_201_CREATED),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_201_CREATED),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
        ("Support", True, status.HTTP_201_CREATED),
        ("Support", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_create_message_acl(
    db,
    be_instance,
    admin_client,
    role,
    communications_topic,
    topic_with_admin_involved,
    notification_template,
    permissions_settings,
    communications_settings,
    access_level,
    instance_acl_factory,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-write",
                Always() if has_permission else Never(),
            )
        ]
    }
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

    service = admin_client.user.get_default_group().service
    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )

    else:
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
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
        },
        format="multipart",
    )
    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        # RBAC: Everybody except for support can create message
        ("Municipality", status.HTTP_201_CREATED),
        ("Applicant", status.HTTP_201_CREATED),
        ("Support", status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_create_message_rbac(
    db,
    be_instance,
    admin_client,
    role,
    communications_topic,
    topic_with_admin_involved,
    notification_template,
    permissions_settings,
    communications_settings,
    access_level,
    instance_acl_factory,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF
    communications_settings["NOTIFICATIONS"]["APPLICANT"]["template_slug"] = (
        notification_template.slug
    )
    communications_settings["NOTIFICATIONS"]["INTERNAL_INVOLVED_ENTITIES"][
        "template_slug"
    ] = notification_template.slug

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
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
        },
        format="multipart",
    )
    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        # Permissions module: Deleting attachment requires
        # "communications-delete-attachment" permission
        ("Support", True, status.HTTP_204_NO_CONTENT),
        ("Support", False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, status.HTTP_204_NO_CONTENT),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_204_NO_CONTENT),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_delete_attachment_acl(
    db,
    admin_user,
    admin_client,
    role,
    be_instance,
    communications_message,
    topic_with_admin_involved,
    communications_attachment,
    permissions_settings,
    access_level,
    instance_acl_factory,
    has_permission,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (
                "communications-delete-attachment",
                Always() if has_permission else Never(),
            )
        ]
    }

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )
        instance_acl_factory(
            access_level=access_level, instance=be_instance, user=admin_client.user
        )

    else:
        service = admin_client.user.get_default_group().service
        instance_acl_factory(
            access_level=access_level, instance=be_instance, service=service
        )

    communications_attachment.file_attachment.save("test.txt", io.BytesIO(b"foobar"))

    response = admin_client.delete(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        # RBAC: Only support can delete attachments
        ("Support", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_permission_delete_attachment_rbac(
    db,
    admin_user,
    admin_client,
    role,
    be_instance,
    topic_with_admin_involved,
    communications_attachment,
    permissions_settings,
    expected_status,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    if role.name == "Applicant":
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

    communications_attachment.file_attachment.save("test.txt", io.BytesIO(b"foobar"))

    response = admin_client.delete(
        reverse("communications-attachment-detail", args=[communications_attachment.pk])
    )

    assert response.status_code == expected_status
