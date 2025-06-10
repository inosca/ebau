import pytest

from camac.settings.utils import generate_module_settings


@pytest.fixture
def disable_deadline_progression(mocker):
    """Disable the InstanceDeadline.recalculate_progression method."""
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.recalculate_progression",
        return_value=False,
    )


@pytest.fixture
def ag_deadlines_settings(settings, request):
    """Module-specific settings for deadlines (canton AG).

    This fixture should be removed once the module is enabled for AG,
    and replaced with a generated fixture through `manage.py generate_fixtures`.

    The logic for AG is already implemented, but the module is not yet enabled.
    So we need this fixture for the tests and coverage for now.
    """
    return generate_module_settings(
        settings=settings,
        request=request,
        module_name="deadlines",
        canton="kt_ag",
        disable=False,
    )
