from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone
from pytest_factoryboy.fixture import LazyFixture


@pytest.mark.parametrize("circulation__instance", [LazyFixture("be_instance")])
def test_send_activation_reminders(
    db,
    circulation,
    circulation_state,
    activation,
    notification_template,
    system_operation_user,
    mailoutbox,
    mocker,
):

    mocker.patch(
        "camac.notification.management.commands.send_activation_reminders.TEMPLATE_REMINDER_CIRCULATION",
        notification_template.slug,
    )

    instance_state = circulation.instance.instance_state
    instance_state.name = "circulation"
    instance_state.save()

    circulation_state.name = "RUN"
    circulation_state.save()

    activation.circulation = circulation
    activation.circulation_state = circulation_state
    activation.deadline_date = timezone.now() - timedelta(days=1)
    activation.save()

    call_command("send_activation_reminders")
    assert len(mailoutbox) == 1
