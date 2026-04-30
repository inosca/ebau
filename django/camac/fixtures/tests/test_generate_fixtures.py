import pytest

from camac.settings.utils import (
    get_all_modules,
    get_enabled_cantons_for_module,
)


def test_get_all_modules(mocker, settings):
    settings.MODULE_SETTINGS_REGISTRY = {
        # intentionally unsorted
        "PERMISSIONS_ALEXANDRIA": "camac.settings.modules.permissions.alexandria",
        "DISTRIBUTION": "camac.settings.modules.distribution",
    }

    assert get_all_modules() == {
        # We expect the result here to be sorted, to ensure the generated
        # settings fixtures are in a predictable order
        "DISTRIBUTION": "camac.settings.modules.distribution",
        "PERMISSIONS_ALEXANDRIA": "camac.settings.modules.permissions.alexandria",
    }


def test_get_enabled_cantons_for_module(mocker):
    distribution_settings = "camac.settings.modules.distribution.DISTRIBUTION"
    permissions_alexandria_settings = (
        "camac.settings.modules.permissions.alexandria.PERMISSIONS_ALEXANDRIA"
    )
    mocker.patch(
        distribution_settings,
        {
            "default": {"ENABLED": True},
            "kt_bern": {"ENABLED": True},
            "kt_gr": {"RANDOM_SETTING": True},
        },
    )

    mocker.patch(
        permissions_alexandria_settings,
        {
            "default": {"ENABLED": True},
            "kt_bern": {"ENABLED": True},
            "kt_gr": {"RANDOM_SETTING": True},
        },
    )

    assert get_enabled_cantons_for_module(distribution_settings) == ["kt_bern"]
    assert set(get_enabled_cantons_for_module(distribution_settings, True)) == set(
        ["kt_bern", "kt_gr"]
    )

    assert get_enabled_cantons_for_module(permissions_alexandria_settings) == [
        "kt_bern"
    ]
    assert set(
        get_enabled_cantons_for_module(permissions_alexandria_settings, True)
    ) == set(["kt_bern", "kt_gr"])


@pytest.mark.parametrize("_", [1, 2])
def test_module_settings_leak(be_ech0211_settings, _):
    """Test that module settings do not leak between tests.

    We will run the same test twice, to ensure that between the two
    testcases the settings will be properly reset.
    """
    assert be_ech0211_settings["ACCOMPANYING_REPORT"].get("NESTED_VALUE") is None
    be_ech0211_settings["ACCOMPANYING_REPORT"]["NESTED_VALUE"] = {
        "inquiry-text-answer": {
            "tag": "situation",
        },
        "inquiry-checkbox": {
            "tag": "documentsAvailable",
            "true_value": "inquiry-checked",
        },
    }
