from django.core.management import call_command
from django.utils import timezone


def test_sendreminders(
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
        "camac.notification.management.commands.sendreminders.TEMPLATE_REMINDER_CIRCULATION",
        notification_template.slug,
    )

    instance_state = circulation.instance.instance_state
    instance_state.name = "circulation"
    instance_state.save()

    circulation_state.name = "RUN"
    circulation_state.save()

    activation.circulation = circulation
    activation.circulation_state = circulation_state
    activation.deadline_date = timezone.now()
    activation.save()

    call_command("sendreminders")
    assert len(mailoutbox) == 1
