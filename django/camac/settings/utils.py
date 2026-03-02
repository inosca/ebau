import copy
import re
from importlib import import_module
from typing import List

from deepmerge import always_merger
from django.conf import settings

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig

from . import modules as settings_modules


class InvalidFixtureUseError(Exception): ...


def generate_module_settings(
    settings, request, module_name, canton, disable, base_fixture
):
    """Generate modular settings fixtures.

    This function generates fixtures for the modular settings concept we use for
    testing purposes. E.g `distribution_settings` or
    `[canton_shortname]_distribution_settings`.
    """

    # Implementation details: Tests can request `module_settings` and
    # `canton_module_settings`     at the same time. Those two settings must not
    # shadow each other: for example:     if a test uses foo_module_settings, but
    # uses a fixture that implies be_foo_module_settings,     then those two settings
    # objects should be the same (but of course with the be_ config as content).

    settings_module = f"camac.settings.modules.{module_name.lower()}"
    original_settings = getattr(
        import_module(settings_module),
        module_name.upper(),
    )

    # Validation: There are only ever allowed to be two module fixtures per
    # module in use:
    # * (optionally) the base module settings (`foo_settings`)
    # * one derived settings fixture, like (`disable_foo_settings`,
    #   or `be_foo_settings`)
    # Using two conflicting settings (like `be_foo_settings` and `ag_foo_settings`
    # in the same test is forbidden)

    specialisation = (
        # "disable" or "be"/"ag"/"gr" etc ... or None
        "disable"
        if disable
        else (settings.APPLICATIONS[canton]["SHORT_NAME"] if canton else None)
    )

    requested = (
        f"{specialisation}_{module_name}_settings"
        if specialisation
        else f"{module_name}_settings"
    )
    if specialisation:
        other_specialisations = [
            f
            for f in request.fixturenames
            if re.match(rf"(\w\w|disable)_{module_name}_settings", f) and f != requested
        ]

        if other_specialisations:
            existing = other_specialisations[0]
            raise InvalidFixtureUseError(
                f"Requested fixture `{requested}` is in conflict with `{existing}`. "
                "Only one of these is allowed to be in use at a time"
            )

    if canton:
        # Cantonal specialisation will *update* the base setting, but not
        # generate a copy
        if isinstance(base_fixture, dict):
            canton_settings = always_merger.merge(
                base_fixture, copy.deepcopy(original_settings[canton])
            )
            # we do not want a copy in the specialisation mode
            assert canton_settings is base_fixture
        else:
            canton_as_defined = getattr(original_settings, canton)
            # root object needs to be the same. However the attributess within
            # can be merged via merger strategy (recursive, copy settings from
            # canton over the default settings).
            for attr, val in vars(canton_as_defined).items():
                setattr(
                    base_fixture,
                    attr,
                    always_merger.merge(
                        getattr(base_fixture, attr, None),
                        copy.deepcopy(getattr(canton_as_defined, attr)),
                    ),
                )
            # in this mode, the base_fixture is now updated to contain the
            # canton settings. These are the same thing
            canton_settings = base_fixture

        yield canton_settings

    elif disable:
        base_fixture.clear()
        yield base_fixture

    else:
        # Genereate "base" settings
        default_settings = (
            copy.deepcopy(original_settings["default"])
            if isinstance(original_settings, dict)
            else original_settings.default.model_copy(deep=True)
        )

        # base settings are responsible for cleanup, so we do the whole set,
        # yield, reset sequence here. Relying on the settings fixture may not be
        # enough (TODO verify / validate assumption)
        before_settings = getattr(settings, module_name.upper(), {})
        setattr(settings, module_name.upper(), default_settings)
        yield default_settings

        setattr(settings, module_name.upper(), before_settings)


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
