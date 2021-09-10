from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone
from pytest_factoryboy.fixture import LazyFixture


@pytest.mark.parametrize("circulation__instance", [LazyFixture("be_instance")])
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
@pytest.mark.parametrize("multilingual", [True, False])
@pytest.mark.parametrize(
    "is_overdue,is_not_viewed,is_assigned,has_controlling,outbox_count",
    [
        (True, True, True, True, 3),
        (True, True, True, False, 2),
        (True, False, True, False, 2),
        (False, True, True, False, 2),
        (False, True, False, False, 1),
        (False, False, True, False, 0),
    ],
)
def test_sendreminders_caluma(
    application_settings,
    db,
    mailoutbox,
    be_instance,
    work_item_factory,
    task_factory,
    snapshot,
    service_factory,
    service_t_factory,
    user_factory,
    is_overdue,
    is_not_viewed,
    is_assigned,
    has_controlling,
    outbox_count,
    multilingual,
):
    application_settings["IS_MULTILINGUAL"] = multilingual

    user = user_factory()
    services = service_factory.create_batch(2)

    if multilingual:
        for service in services:
            for language in ["de", "fr"]:
                service_t_factory(language=language, service=service)

    deadline = (
        timezone.now() - timedelta(days=1)
        if is_overdue
        else timezone.now() + timedelta(days=1)
    )

    work_item_factory(
        status="ready",
        meta={"not-viewed": is_not_viewed},
        deadline=deadline,
        assigned_users=[user.username] if is_assigned else [],
        addressed_groups=[str(services[0].pk)],
        controlling_groups=[str(services[1].pk)] if has_controlling else [],
    )

    call_command("sendreminders", "--caluma")

    assert len(mailoutbox) == outbox_count
    snapshot.assert_match(
        [(mail.subject, mail.body, mail.to, mail.cc) for mail in mailoutbox]
    )


@pytest.mark.parametrize("user__disabled", [1])
def test_dont_send_reminders_caluma(db, user, service, work_item_factory, mailoutbox):
    service.disabled = 1
    service.save()
    work_item_factory(
        status="ready",
        meta={"not-viewed": True},
        deadline=timezone.now() - timedelta(days=1),
        assigned_users=[user.username],
        addressed_groups=[service.pk],
        controlling_groups=[service.pk],
    )
    call_command("sendreminders", "--caluma")
    assert len(mailoutbox) == 0
