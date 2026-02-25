import pytest

from camac.settings.utils import (
    get_all_modules,
    get_enabled_cantons_for_module,
    get_enabled_modules_for_canton,
)


def test_get_all_modules(mocker):
    class FakeModule:
        distribution = None
        not_a_module = None

    mocker.patch("camac.settings.utils.settings_modules", FakeModule)

    assert get_all_modules() == ["distribution"]


def test_get_enabled_cantons_for_module(mocker):
    mocker.patch(
        "camac.settings.modules.distribution.DISTRIBUTION",
        {
            "default": {"ENABLED": True},
            "kt_bern": {"ENABLED": True},
            "kt_gr": {"RANDOM_SETTING": True},
        },
    )

    assert get_enabled_cantons_for_module("distribution") == ["kt_bern"]
    assert set(get_enabled_cantons_for_module("distribution", True)) == set(
        ["kt_bern", "kt_gr"]
    )


def test_get_enabled_modules_for_canton(mocker):
    mocker.patch(
        "camac.settings.utils.get_all_modules",
        return_value=["distribution", "dms"],
    )
    mocker.patch(
        "camac.settings.modules.distribution.DISTRIBUTION",
        {
            "default": {},
            "kt_bern": {"ENABLED": True},
            "kt_gr": {"RANDOM_SETTING": True},
        },
    )
    mocker.patch(
        "camac.settings.modules.dms.DMS",
        {"default": {}},
    )

    assert get_enabled_modules_for_canton("kt_bern") == ["distribution"]
    assert get_enabled_modules_for_canton("kt_bern", True) == ["distribution"]
    assert get_enabled_modules_for_canton("kt_gr") == []
    assert get_enabled_modules_for_canton("kt_gr", True) == ["distribution"]


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
