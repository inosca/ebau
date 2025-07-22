import copy
from importlib import import_module
from typing import List

from deepmerge import always_merger
from django.conf import settings

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig

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
            original_settings[canton]
            if isinstance(original_settings, dict)
            else getattr(original_settings, canton),
        )
    elif disable:
        new_settings = {}
    else:
        new_settings = copy.deepcopy(
            original_settings["default"]
            if isinstance(original_settings, dict)
            else original_settings.default
        )

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

    cantons_config: dict | ModuleConfig = getattr(settings_module, module_name.upper())
    is_pydantic = isinstance(cantons_config, ModuleConfig)

    cantons = iter(cantons_config) if is_pydantic else cantons_config.items()

    return [
        canton
        for canton, config in cantons
        if config
        and is_module_enabled(config, ignore_enabled_value)
        and canton != "default"
    ]


def get_enabled_modules_for_canton(
    canton: str, ignore_enabled_value: bool = False
) -> List[str]:
    enabled_modules = []
    all_modules = get_all_modules()

    for module_name in all_modules:
        settings_module = import_module(f"camac.settings.modules.{module_name}")
        config: dict | ModuleConfig = getattr(settings_module, module_name.upper(), {})
        is_pydantic = isinstance(config, ModuleConfig)
        canton_config = (
            getattr(config, canton) if is_pydantic else config.get(canton, {})
        )

        if canton_config and is_module_enabled(canton_config, ignore_enabled_value):
            enabled_modules.append(module_name)

    return enabled_modules


def is_module_enabled(
    config: dict | ModuleApplicationConfig, ignore_enabled_value: bool = False
) -> bool:
    match config:
        case ModuleApplicationConfig(enabled=True):
            # Checking ignore_enabled_value makes no sense with pydantic
            return True
        case {"ENABLED": None | False}:
            return ignore_enabled_value
        case {"ENABLED": enabled}:
            return enabled
        case _:
            return False
