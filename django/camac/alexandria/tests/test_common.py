import pytest

from camac.alexandria.extensions.common import (
    get_role,
    has_alexandria_create_permission,
)
from camac.permissions.api import GRANT_CHOICES, grant
from camac.permissions.conditions import Always, Never
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize(
    "append_role,service_group__name,role__name,expected_permission_key",
    [
        (False, "service-cantonal", "service-lead", "cantonal"),
        (False, "service-cantonal", "subservice", "cantonal"),
        (False, "municipality", "municipality-lead", "municipality-lead"),
        (False, "municipality", "subservice", "subservice"),
        (True, "service-cantonal", "service-lead", "cantonal-service-lead"),
        (True, "service-cantonal", "subservice", "cantonal-subservice"),
        (True, "municipality", "municipality-lead", "municipality-lead"),
        (True, "municipality", "subservice", "subservice"),
    ],
)
def test_get_role(db, group, append_role, expected_permission_key, alexandria_settings):
    alexandria_settings["CUSTOM_ROLE_MAPPINGS"] = {"service-cantonal": "cantonal"}
    alexandria_settings["APPEND_ROLE_TO_CUSTOM_ROLE_MAPPING"] = append_role

    assert get_role(group) == expected_permission_key


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_has_alexandria_create_permission_v1(
    db,
    alexandria_category_factory,
    alexandria_settings,
    fake_request,
    instance,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = False

    allowed_category = alexandria_category_factory(
        metainfo={
            "access": {
                "Municipality": {
                    "visibility": "all",
                    "permissions": [
                        {
                            "scope": "All",
                            "permission": "create",
                        }
                    ],
                }
            }
        }
    )
    disallowed_category = alexandria_category_factory()

    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is True
    )
    assert (
        has_alexandria_create_permission(fake_request, instance, disallowed_category)
        is False
    )


def test_has_alexandria_create_permission_v2(
    db,
    access_level_factory,
    alexandria_category_factory,
    alexandria_settings,
    fake_request,
    instance,
    permissions_settings,
    service,
    settings,
):
    alexandria_settings["USE_V2_PERMISSIONS"] = True
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL

    access_level = access_level_factory()
    allowed_category = alexandria_category_factory()
    disallowed_category = alexandria_category_factory()

    settings.PERMISSIONS_ALEXANDRIA["ACCESS_LEVELS"] = {
        access_level.pk: [
            (f"{allowed_category.pk}:create", Always()),
            (f"{disallowed_category.pk}:create", Never()),
        ]
    }

    # allowed category, but permission not granted yet
    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is False
    )

    grant(
        instance,
        grant_type=GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )

    # allowed category, now permission is granted
    assert (
        has_alexandria_create_permission(fake_request, instance, allowed_category)
        is True
    )

    # disallowed category
    assert (
        has_alexandria_create_permission(fake_request, instance, disallowed_category)
        is False
    )
