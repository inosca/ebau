import pytest
from django.urls import reverse
from rest_framework import status

from camac.permissions import api
from camac.permissions.conditions import Always, Callback, RequireInstanceState
from camac.permissions.models import AccessLevel
from camac.permissions.switcher import (
    get_permission_mode,
    is_permission_mode_fully_enabled,
)


@pytest.fixture
def configure_access_levels(permissions_settings, instance, access_level):
    def do_configure(has_functional_permission):
        # Configure a dynamic (functional) permission for our access level, along
        # with two static ones...
        def check_functional_permission(userinfo, instance):
            return has_functional_permission

        permissions_settings["ACCESS_LEVELS"] = {
            access_level.pk: [
                ("foo", RequireInstanceState([instance.instance_state.name])),
                ("bar", RequireInstanceState([instance.instance_state.name])),
                ("func", Callback(check_functional_permission)),
            ]
        }

    return do_configure


@pytest.mark.parametrize("has_functional_permission", [True, False])
def test_permissions_view(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    configure_access_levels,
    has_functional_permission,
):
    url = reverse("instance-permissions-list")

    configure_access_levels(has_functional_permission=has_functional_permission)

    # Check permissions before...
    result = admin_client.get(url, {"instance": instance.pk})
    assert result.json() == {
        "data": [],
        "meta": {
            "permission-mode": get_permission_mode().value,
            "fully-enabled": is_permission_mode_fully_enabled(),
        },
    }

    # Grant this access level to our user
    api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )

    # And check the permissions after.
    result = admin_client.get(url, {"instance": instance.pk})

    # Expectations depending on functional permissions check...
    expect_permissions = (
        sorted(["foo", "bar", "func"])
        if has_functional_permission
        else sorted(["foo", "bar"])
    )

    assert result.json() == {
        "data": [
            {
                "id": str(instance.pk),
                "attributes": {"permissions": expect_permissions},
                "relationships": {
                    "instance": {"data": {"id": str(instance.pk), "type": "instances"}}
                },
                "type": "instance-permissions",
            }
        ],
        "meta": {
            "permission-mode": get_permission_mode().value,
            "fully-enabled": is_permission_mode_fully_enabled(),
        },
    }


@pytest.mark.parametrize("do_include", [True, False])
def test_no_include_instance(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    configure_access_levels,
    do_include,
):
    # Querying the permissions should not give you the ability to read data via
    # includes that you're not supposed to. Therefore, the permissions endpoint
    # shall not allow any includes.

    url = reverse("instance-permissions-list")
    configure_access_levels(has_functional_permission=False)

    # Grant this access level to our user
    api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )

    # And check the permissions after.
    params = {"instance": instance.pk}
    if do_include:
        params["include"] = "instance"

        with pytest.raises(Exception) as exc:
            admin_client.get(url, params)
        assert exc.match("This endpoint does not support the include parameter")

    else:
        # no includes = all good
        result = admin_client.get(url, params)
        assert result.json() == {
            "data": [
                {
                    "attributes": {"permissions": ["bar", "foo"]},
                    "id": str(instance.pk),
                    "relationships": {
                        "instance": {
                            "data": {"id": str(instance.pk), "type": "instances"}
                        }
                    },
                    "type": "instance-permissions",
                }
            ],
            "meta": {
                "permission-mode": get_permission_mode().value,
                "fully-enabled": is_permission_mode_fully_enabled(),
            },
        }


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "do_filter,grant,expect_results",
    [
        (True, "geometer", 1),
        (True, None, 0),
        (False, None, "ALL"),
        (False, "geometer", "ALL"),
        (True, "any", "ALL"),
        (False, "any", "ALL"),
    ],
)
def test_assignable_filter(
    db,
    be_instance,
    admin_client,
    instance_acl_factory,
    be_permissions_settings,
    be_access_levels,
    # params
    do_filter,
    grant,
    expect_results,
):
    """
    Test the asssignable_in_instance filter on the access levels.

    The filter is supposed to only return the access levels that the current
    user can assign to someone on the given instance.
    """
    if expect_results == "ALL":
        expect_results = AccessLevel.objects.all().count()

    # Drop any configured "grant" permisisons, so we can test the exact
    # behaviour
    be_permissions_settings["ACCESS_LEVELS"]["lead-authority"] = [
        (p, c)
        for p, c in be_permissions_settings["ACCESS_LEVELS"]["lead-authority"]
        if not p.startswith("permissions-grant-")
    ]
    if grant:
        # Allow granting of some access levels
        be_permissions_settings["ACCESS_LEVELS"]["lead-authority"].append(
            (f"permissions-grant-{grant}", Always())
        )

    instance_acl_factory(
        instance=be_instance,
        service=admin_client.user.get_default_group().service,
        access_level=AccessLevel.objects.get(pk="lead-authority"),
    )

    url = reverse("access-levels-list")

    filter_param = {"assignable_in_instance": str(be_instance.pk)}

    resp = admin_client.get(url, filter_param if do_filter else {})
    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()
    assert len(resp_data["data"]) == expect_results
