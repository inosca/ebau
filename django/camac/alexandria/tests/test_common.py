import pytest

from camac.alexandria.extensions.common import (
    get_permission_key,
    has_alexandria_create_permission,
)
from camac.permissions.api import GRANT_CHOICES, grant
from camac.permissions.conditions import Always, Never
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize(
    (
        "use_role_permission_mapping",
        "append_role",
        "service_group__name",
        "role__name",
        "expected_permission_key",
    ),
    [
        (False, False, "service-cantonal", "service-lead", "cantonal"),
        (False, False, "service-cantonal", "subservice", "cantonal"),
        (False, False, "municipality", "municipality-lead", "municipality-lead"),
        (False, False, "municipality", "subservice", "subservice"),
        (False, True, "service-cantonal", "service-lead", "cantonal-service-lead"),
        (False, True, "service-cantonal", "subservice", "cantonal-subservice"),
        (False, True, "municipality", "municipality-lead", "municipality-lead"),
        (False, True, "municipality", "subservice", "subservice"),
        (True, False, "service-cantonal", "service-lead", "cantonal"),
        (True, False, "service-cantonal", "subservice", "cantonal"),
        (True, False, "municipality", "municipality-lead", "municipality"),
        (True, False, "municipality", "subservice", "service"),
        (True, True, "service-cantonal", "service-lead", "cantonal-service"),
        (True, True, "service-cantonal", "subservice", "cantonal-service"),
        (True, True, "municipality", "municipality-lead", "municipality"),
        (True, True, "municipality", "subservice", "service"),
    ],
)
def test_get_permission_key(
    db,
    alexandria_settings,
    append_role,
    application_settings,
    expected_permission_key,
    group,
    use_role_permission_mapping,
):
    application_settings["ROLE_PERMISSIONS"] = {
        "service-lead": "service",
        "subservice": "service",
        "municipality-lead": "municipality",
    }

    alexandria_settings["PERMISSION_KEY"] = {
        "SERVICE_GROUP_MAPPING": {"service-cantonal": "cantonal"},
        "SERVICE_GROUP_APPEND_ROLE": append_role,
        "USE_ROLE_PERMISSIONS_MAPPING": use_role_permission_mapping,
    }

    assert get_permission_key(group) == expected_permission_key


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
