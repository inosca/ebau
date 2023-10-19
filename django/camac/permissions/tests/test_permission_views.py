import pytest
from django.urls import reverse

from camac.permissions import api


@pytest.mark.parametrize("has_functional_permission", [True, False])
def test_permissions_view(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    has_functional_permission,
):
    url = reverse("instance-permissions-list")

    # Configure a dynamic (functional) permission for our access level, along
    # with two static ones...
    def check_functional_permission(userinfo, instance):
        return has_functional_permission

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("foo", instance.instance_state),
            ("bar", instance.instance_state),
            ("func", check_functional_permission),
        ]
    }

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
        ["foo", "bar", "func"] if has_functional_permission else ["foo", "bar"]
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
