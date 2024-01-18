import pytest
from django.urls import reverse

from camac.permissions import api
from camac.permissions.conditions import Callback, InstanceState


@pytest.fixture
def configure_access_levels(permissions_settings, instance, access_level):
    def do_configure(has_functional_permission):
        # Configure a dynamic (functional) permission for our access level, along
        # with two static ones...
        def check_functional_permission(userinfo, instance):
            return has_functional_permission

        permissions_settings["ACCESS_LEVELS"] = {
            access_level.pk: [
                ("foo", InstanceState([instance.instance_state.name])),
                ("bar", InstanceState([instance.instance_state.name])),
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
    assert result.json() == {"data": []}

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
        ]
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
            ]
        }
