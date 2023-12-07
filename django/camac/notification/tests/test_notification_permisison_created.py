import pytest

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.permissions import api as permissions_api


@pytest.mark.parametrize("grant_type", ["USER", "SERVICE"])
@pytest.mark.parametrize("acl_active", [True, False])
def test_notification_of_new_acl(
    db,
    be_instance,
    system_operation_user,
    notification_template,
    instance_acl_factory,
    access_level,
    admin_user,
    application_settings,
    permissions_settings,
    group_factory,
    service_factory,
    mailoutbox,
    grant_type,
    acl_active,
):
    # Setup service so we have someone to notify
    service = service_factory()
    group = group_factory(service=service)
    group.users.add(admin_user, through_defaults={"default_group": True})

    # Configure permisisons module
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            # No fancy permissions required, just... *something*
            ("foo", ["*"]),
        ]
    }
    # Configure notifications module
    application_settings["NOTIFICATIONS"]["PERMISSION_ACL_GRANTED"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["acl_authorized"],
        }
    ]

    # Trigger the notification event
    the_acl = permissions_api.grant(
        be_instance,
        grant_type=grant_type,
        access_level=access_level,
        user=(admin_user if grant_type == "USER" else None),
        service=(service if grant_type == "SERVICE" else None),
    )
    if not acl_active:
        permissions_api.revoke(the_acl)

    if acl_active:
        assert len(mailoutbox) == 1
        expected_subj = notification_template.get_trans_attr("subject", "de")
        assert mailoutbox[0].subject == f"[eBau Test]: {expected_subj}"


@pytest.mark.parametrize("instance_acl__grant_type", ["SERVICE"])
@pytest.mark.parametrize("access_level__slug", ["geometer"])
@pytest.mark.parametrize("notification", [1, 0])
def test_get_recipients_acl_by_accesslevel(
    db,
    access_level,
    instance_acl,
    be_instance,
    notification_template,
    application_settings,
    notification,
):
    # I'd love to just call the serializer "as normal", but the
    # `recipient_types` field is initialized long before this test runs
    # and it's a bit tricky (or at least ugly) to extend it's valid choices
    # after-the-fact. So we're just calling the getter for the corresponding
    # recipient type.
    serializer = PermissionlessNotificationTemplateSendmailSerializer()

    instance_acl.service.notification = notification
    instance_acl.service.save()

    recipient_type = f"{access_level.slug}_acl_services"

    getter = getattr(serializer, f"_get_recipients_{recipient_type}")

    if notification:
        assert getter(be_instance) == [{"to": instance_acl.service.email}]
    else:
        assert getter(be_instance) == []
