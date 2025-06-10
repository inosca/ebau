import pytest

from camac.deadlines.management.commands.update_deadline_progression import (
    Command as UpdateDeadlineProgressionCommand,
)


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
def test_management_command_deadline_progression(
    db,
    service,
    instance_deadline_factory,
    gr_instance,
    gr_deadlines_settings,
    mocker,
):
    """Test the management command for updating deadline progression in GR."""
    mock_stdout = mocker.patch("sys.stdout.write")
    mock_stderr = mocker.patch("sys.stderr.write")

    instance_deadline_factory(
        instance=gr_instance,
        service=service,
    )

    cmd = UpdateDeadlineProgressionCommand(stdout=mock_stdout, stderr=mock_stderr)
    cmd.handle()

    mock_stdout.write.assert_called_once()
    mock_stderr.write.assert_not_called()
