import pytest


@pytest.fixture
def disable_deadline_progression(mocker):
    """Disable the InstanceDeadline.recalculate_progression method."""
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.recalculate_progression",
        return_value=False,
    )
