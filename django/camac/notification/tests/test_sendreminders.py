from datetime import timedelta

import pytest
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


@pytest.mark.freeze_time("2020-08-10")
def test_sendreminders_caluma(
    db,
    mailoutbox,
    instance,
    work_item_factory,
    task_factory,
    snapshot,
    service_factory,
    user_factory,
):

    users = user_factory.create_batch(4)
    services = service_factory.create_batch(4)

    work_item_factory.create_batch(
        2,
        status="ready",
        deadline=timezone.now() - timedelta(days=1),
        assigned_users=[user.username for user in users[:2]],
        addressed_groups=[str(s.pk) for s in services[:2]],
        controlling_groups=[str(s.pk) for s in [services[0], services[3]]],
    )
    work_item_factory.create_batch(
        3,
        status="ready",
        meta={"not-viewed": True},
        assigned_users=[user.username for user in users[1:3]],
        addressed_groups=[str(s.pk) for s in services[1:3]],
        controlling_groups=[str(s.pk) for s in [services[0], services[3]]],
    )

    call_command("sendreminders", "--caluma")

    assert len(mailoutbox) == 7
    assert users[3].email not in [addr for mail in mailoutbox for addr in mail.to]
    snapshot.assert_match(set((mail.subject, mail.body) for mail in mailoutbox))
