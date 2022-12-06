from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone


@pytest.mark.freeze_time("2022-11-30T17:00:00.123456+00:00")
@pytest.mark.parametrize("instance_state__name", ["circulation"])
def test_send_inquiry_reminders(
    db,
    be_instance,
    active_inquiry_factory,
    notification_template,
    system_operation_user,
    mailoutbox,
    mocker,
):
    mocker.patch(
        "camac.notification.management.commands.send_inquiry_reminders.TEMPLATE_REMINDER_CIRCULATION",
        notification_template.slug,
    )

    inquiry = active_inquiry_factory(
        deadline=timezone.now() - timedelta(days=1),
        meta={"reminders": ["2022-11-30T16:00:00.000000+00:00"]},
    )

    call_command("send_inquiry_reminders")

    inquiry.refresh_from_db()

    assert len(mailoutbox) == 1
    assert inquiry.meta["reminders"] == [
        "2022-11-30T17:00:00.123456+00:00",
        "2022-11-30T16:00:00.000000+00:00",
    ]
