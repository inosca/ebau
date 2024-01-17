import pytest
from django.urls import reverse

from camac.permissions import api
from camac.permissions.conditions import Always

"""
Geometer permissions tests.

Note: This test suite is currently located in the permissions module,
but once the permissions module becomes fully active, it should probably
be moved to someplace else.
"""


@pytest.mark.parametrize(
    "role__name, expect_results",
    [
        ("Geometer", 1),
        ("Service", 0),
    ],
)
@pytest.mark.parametrize("grant_type", ["USER", "SERVICE"])
@pytest.mark.parametrize("access_level__slug", ["geometer"])
def test_geometer_instance_access(
    db,
    admin_client,
    instance,
    expect_results,
    group_factory,
    access_level,
    grant_type,
    permissions_settings,
):
    # Note: When the user's role is "Service", it should still go throught the
    # "_for_service" implementation in the mixin and therefore not actually
    # look at the ACLs, even if the user's ACLs would give full Geometer access.
    # TODO: this will need changing once the permissions module replaces the
    # `InstanceQuerysetMixin` logic

    # Geometer access
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("geometer", Always()),
            ("read-form", Always()),
        ]
    }

    # We need to clear out the access for the "service" user, otherwise we'll
    # get non-ACL'd access bypass
    instance.group = group_factory()
    instance.services.set([])  # the service of the regular user is *somewhere*
    instance.save()

    data_url = reverse("instance-list")
    permissions_url = reverse("instance-permissions-list")

    # Before ACL, there should be no access
    res_before_acl = admin_client.get(data_url)
    res_before_acl_data = res_before_acl.json()["data"]
    assert len(res_before_acl_data) == 0

    permissions_before_acl = admin_client.get(permissions_url)
    assert len(permissions_before_acl.json()["data"]) == 0

    user_active_service = admin_client.user.groups.get().service

    manager = api.PermissionManager.for_anonymous()
    manager.grant(
        instance,
        grant_type,
        access_level,
        service=user_active_service if grant_type == "SERVICE" else None,
        user=admin_client.user if grant_type == "USER" else None,
    )

    # Geometer should now have access, as an ACL is granted
    res_after_acl = admin_client.get(data_url)
    res_after_acl_data = res_after_acl.json()["data"]
    assert len(res_after_acl_data) == expect_results

    # the permissions endpoint doesn't respect the instance queryset mixin.
    # TODO: is this acceptable or a problem? We did grant the permission to
    # the non-geometer user, so the permission is in fact there, even if it's
    # currently restricted (User has "service" access but not to "our" instance,
    # so the instance queryset mixin won't grant visibility)
    permissions_after_acl = admin_client.get(permissions_url)
    assert len(permissions_after_acl.json()["data"]) == 1
    perm = permissions_after_acl.json()["data"][0]
    assert set(perm["attributes"]["permissions"]) == set(["geometer", "read-form"])

    if expect_results:
        # Just ensure it's the right instance (there should be only
        # one either way, but let's make sure we get the right one
        # nonetheless)
        assert res_after_acl_data[0]["id"] == str(instance.pk)
