import pytest

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
            "recipient_types": ["newest_acl"],
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
