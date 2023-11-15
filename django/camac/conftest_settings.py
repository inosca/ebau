import copy
import sys
from importlib import import_module

import pytest
from deepmerge import always_merger
from django.conf import settings


def generate_module_test_settings(module_name, cantons=[]):
    """Generate modular settings fixtures.

    This function generates fixtures for the modular settings concept we use for
    testing purposes. E.g `distribution_settings` or
    `[canton_shortname]_distribution_settings`.
    """

    def generate(canton=None):
        @pytest.fixture
        def fn(settings, request):
            original_settings = getattr(
                import_module(f"camac.settings_{module_name.lower()}"),
                module_name.upper(),
            )

            if canton:
                new_settings = always_merger.merge(
                    copy.deepcopy(request.getfixturevalue(f"{module_name}_settings")),
                    original_settings[canton],
                )
            else:
                new_settings = copy.deepcopy(original_settings["default"])

            setattr(settings, module_name.upper(), new_settings)

            return new_settings

        return fn

    fixture_name = f"{module_name}_settings"

    setattr(sys.modules[__name__], fixture_name, generate())

    for canton in cantons:
        prefix = settings.APPLICATIONS[canton].get("SHORT_NAME")
        scoped_fixture_name = f"{prefix}_{fixture_name}"

        setattr(sys.modules[__name__], scoped_fixture_name, generate(canton))


generate_module_test_settings("appeal", ["kt_bern"])
generate_module_test_settings(
    "distribution", ["kt_bern", "kt_schwyz", "kt_gr", "kt_so"]
)
generate_module_test_settings("publication", ["kt_gr"])
generate_module_test_settings("decision", ["kt_bern", "kt_gr", "kt_so"])
generate_module_test_settings("dms", ["kt_bern", "kt_gr"])
generate_module_test_settings(
    "additional_demand", ["kt_gr", "kt_so", "kt_bern", "kt_uri"]
)
generate_module_test_settings("alexandria", ["kt_gr", "kt_so"])
generate_module_test_settings("rejection", ["kt_bern"])
