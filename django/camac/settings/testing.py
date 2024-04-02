import copy
import sys
from importlib import import_module

import pytest
from deepmerge import always_merger
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def generate_module_test_settings(module_name, cantons=[]):
    """Generate modular settings fixtures.

    This function generates fixtures for the modular settings concept we use for
    testing purposes. E.g `distribution_settings` or
    `[canton_shortname]_distribution_settings`.
    """

    def generate(canton=None, disable=False):
        @pytest.fixture
        def fn(settings, request):
            settings_module = f"camac.settings.modules.{module_name.lower()}"
            original_settings = getattr(
                import_module(settings_module),
                module_name.upper(),
            )

            if canton:
                if canton not in original_settings:  # pragma: no cover
                    raise ImproperlyConfigured(
                        f"Module '{module_name}' not configured for {canton}. "
                        "Consider removing it in "
                        "camac.settings.testing.MODULE_CONFIG_FIXTURES "
                        f"or configuring it properly in {settings_module}"
                    )

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

        return fn

    fixture_name = f"{module_name}_settings"

    setattr(sys.modules[__name__], fixture_name, generate())
    setattr(sys.modules[__name__], f"disable_{fixture_name}", generate(disable=True))

    for canton in cantons:
        prefix = settings.APPLICATIONS[canton].get("SHORT_NAME")
        scoped_fixture_name = f"{prefix}_{fixture_name}"

        setattr(sys.modules[__name__], scoped_fixture_name, generate(canton=canton))


ALL_APPS = list(settings.APPLICATIONS.keys())

MODULE_CONFIG_FIXTURES = {
    # TODO: Think about generating this list from the actual module settings,
    # which have keys depending on whether the settings are actually available
    "appeal": ["kt_bern", "kt_so"],
    "distribution": ["kt_bern", "kt_schwyz", "kt_gr", "kt_so", "kt_uri"],
    "publication": ["kt_gr"],
    "decision": ["kt_bern", "kt_gr", "kt_so"],
    "dms": ["kt_bern", "kt_gr", "kt_uri"],
    "additional_demand": ["kt_gr", "kt_so", "kt_uri"],
    "alexandria": ["kt_gr", "kt_so"],
    "rejection": ["kt_bern", "kt_so"],
    "withdrawal": ["kt_so"],
    "construction_monitoring": ["kt_schwyz"],
    "permissions": ["kt_bern", "kt_gr", "kt_so"],
    "communications": ["kt_bern", "kt_gr", "kt_so"],
    "placeholders": ["kt_bern", "kt_so"],
    "master_data": ["kt_bern", "kt_schwyz", "kt_uri", "kt_gr", "kt_so"],
    "dump": ALL_APPS,
    "ech0211": ["kt_schwyz", "kt_bern", "kt_gr"],
}

for modulename, cantons in MODULE_CONFIG_FIXTURES.items():
    generate_module_test_settings(modulename, cantons)
