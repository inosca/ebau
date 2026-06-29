import copy
import re
from typing import List

from deepmerge import always_merger
from django.conf import settings
from django.utils.module_loading import import_string

from camac.settings.ebau_schema import ModuleApplicationConfig, ModuleConfig


class InvalidFixtureUseError(Exception): ...


def generate_module_settings(
    settings, request, settings_name, import_path, canton, disable, base_fixture
):
    """Generate modular settings fixtures.

    This function generates fixtures for the modular settings concept we use for
    testing purposes. E.g `distribution_settings` or
    `[canton_shortname]_distribution_settings`.
    """

    def _enable(module_settings: ModuleApplicationConfig | dict):
        if isinstance(module_settings, ModuleApplicationConfig):
            module_settings.enabled = True
        else:
            module_settings["ENABLED"] = True

    module_name = settings_name.lower()
    # Implementation details: Tests can request `module_settings` and
    # `canton_module_settings`     at the same time. Those two settings must not
    # shadow each other: for example:     if a test uses foo_module_settings, but
    # uses a fixture that implies be_foo_module_settings,     then those two settings
    # objects should be the same (but of course with the be_ config as content).

    original_settings = import_string(import_path)

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

        # when creating a canton fixture, it is assumed to be enabled, even
        # when the original setting is only enabled by an env flag.
        _enable(canton_settings)

        yield canton_settings

    elif disable:
        if isinstance(base_fixture, dict):
            base_fixture.clear()

        yield base_fixture

    else:
        # Genereate "base" settings
        default_settings = (
            copy.deepcopy(original_settings["default"])
            if isinstance(original_settings, dict)
            else original_settings.default.model_copy(deep=True)
        )

        # When using the default settings, we need to make sure they pass the
        # `is_module_enabled` check
        _enable(default_settings)

        # base settings are responsible for cleanup, so we do the whole set,
        # yield, reset sequence here. Relying on the settings fixture may not be
        # enough (TODO verify / validate assumption)
        before_settings = getattr(settings, settings_name, {})
        setattr(settings, settings_name, default_settings)
        yield default_settings

        setattr(settings, settings_name, before_settings)


def get_all_modules() -> dict[str, str]:
    """Return a dict that maps the settings names to the corresponding import paths."""
    return {
        name: settings.MODULE_SETTINGS_REGISTRY[name]
        # sorted for stable template generation (fixtures generated for module settings)
        for name in sorted(settings.MODULE_SETTINGS_REGISTRY.keys())
    }


def get_enabled_cantons_for_module(
    import_path: str, ignore_enabled_value: bool = False
) -> List[str]:
    cantons_config: dict | ModuleConfig = import_string(import_path)

    is_pydantic = isinstance(cantons_config, ModuleConfig)

    cantons = iter(cantons_config) if is_pydantic else cantons_config.items()

    return [
        canton
        for canton, config in cantons
        if config
        and (ignore_enabled_value or is_module_config_enabled(config))
        and canton != "default"
    ]


def is_module_config_enabled(config: dict | ModuleApplicationConfig) -> bool:
    """Determine if a module is enabled based on configuration.

    It will use the configuration key based on the config type:
    - For `ModuleApplicationConfig` (pydantic) it will use the `enabled` attribute.
    - For dict-based config, it will look for the `ENABLED` key, defaulting to False
    if not found.
    """
    if isinstance(config, ModuleApplicationConfig):
        return config.enabled
    else:
        return config.get("ENABLED", False)


def is_module_enabled(module_name: str) -> bool:
    """Check if a settings module is enabled or not.

    Works for pydantic and regular dict configs.
    """
    return is_module_config_enabled(getattr(settings, module_name))
