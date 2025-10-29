import pytest


@pytest.fixture
def disable_deadline_side_effects(mocker):
    """Disable the InstanceDeadline.trigger_side_effect method."""
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )
