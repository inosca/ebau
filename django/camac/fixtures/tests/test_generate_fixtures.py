from camac.settings.utils import (
    get_all_modules,
    get_enabled_cantons_for_module,
    get_enabled_modules_for_canton,
    is_module_enabled,
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
        {"default": {"ENABLED": True}, "kt_bern": {"ENABLED": True}},
    )

    assert get_enabled_cantons_for_module("distribution") == ["kt_bern"]


def test_get_enabled_modules_for_canton(mocker):
    mocker.patch(
        "camac.settings.utils.get_all_modules",
        return_value=["distribution", "dms"],
    )
    mocker.patch(
        "camac.settings.modules.distribution.DISTRIBUTION",
        {"default": {}, "kt_bern": {"ENABLED": True}},
    )
    mocker.patch(
        "camac.settings.modules.dms.DMS",
        {"default": {}},
    )

    assert get_enabled_modules_for_canton("kt_bern") == ["distribution"]


def test_is_module_enabled(mocker):
    assert is_module_enabled({"ENABLED": True}) is True
    assert is_module_enabled({"ENABLED": False}) is False
    # If `ENABLED` is passed from env
    assert is_module_enabled({"ENABLED": False}, True) is True
