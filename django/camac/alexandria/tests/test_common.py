import pytest

from camac.alexandria.extensions.common import get_role


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
