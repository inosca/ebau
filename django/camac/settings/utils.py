import copy
from importlib import import_module
from typing import List

from deepmerge import always_merger
from django.conf import settings

from . import modules as settings_modules


def generate_module_settings(settings, request, module_name, canton, disable):
    """Generate modular settings fixtures.

    This function generates fixtures for the modular settings concept we use for
    testing purposes. E.g `distribution_settings` or
    `[canton_shortname]_distribution_settings`.
    """

    settings_module = f"camac.settings.modules.{module_name.lower()}"
    original_settings = getattr(
        import_module(settings_module),
        module_name.upper(),
    )

    if canton:
        new_settings = always_merger.merge(
            copy.deepcopy(request.getfixturevalue(f"{module_name}_settings")),
            original_settings[canton],
        )
    elif disable:
        new_settings = {}
    else:
        new_settings = copy.deepcopy(original_settings["default"])

    setattr(settings, module_name.upper(), new_settings)

    return new_settings


def get_all_modules():
    return [
        module_name
        for module_name in dir(settings_modules)
        if hasattr(settings, module_name.upper())
    ]


def get_enabled_cantons_for_module(
    module_name: str, ignore_enabled_value: bool = False
) -> List[str]:
    settings_module = import_module(f"camac.settings.modules.{module_name}")

    return [
        canton
        for canton, config in getattr(settings_module, module_name.upper()).items()
        if is_module_enabled(config, ignore_enabled_value) and canton != "default"
    ]


def get_enabled_modules_for_canton(
    canton: str, ignore_enabled_value: bool = False
) -> List[str]:
    enabled_modules = []
    all_modules = get_all_modules()

    for module_name in all_modules:
        settings_module = import_module(f"camac.settings.modules.{module_name}")
        config = getattr(settings_module, module_name.upper(), {}).get(canton, {})

        if is_module_enabled(config, ignore_enabled_value):
            enabled_modules.append(module_name)

    return enabled_modules


def is_module_enabled(config: dict, ignore_enabled_value: bool = False) -> bool:
    if ignore_enabled_value:
        return "ENABLED" in config

    return config.get("ENABLED", False)
