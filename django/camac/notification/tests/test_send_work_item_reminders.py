from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone


@pytest.mark.freeze_time("2020-08-10")
@pytest.mark.parametrize("multilingual", [True, False])
@pytest.mark.parametrize(
    "is_overdue,is_not_viewed,is_assigned,has_controlling,multi_mail_service,is_applicant,outbox_count",
    [
        (True, True, True, True, False, False, 3),
        (True, True, True, False, True, False, 3),
        (True, False, True, False, False, False, 2),
        (False, True, True, False, True, False, 3),
        (False, True, False, False, False, False, 1),
        (False, False, True, False, False, False, 0),
        (True, True, True, True, False, True, 2),
        (True, False, True, False, False, True, 1),
    ],
)
def test_send_work_item_reminders(
    settings,
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
    multi_mail_service,
    is_applicant,
    outbox_count,
    multilingual,
):
    application_settings["IS_MULTILINGUAL"] = multilingual
    settings.INTERNAL_BASE_URL = "http://ebau.local"

    user = user_factory()
    services = service_factory.create_batch(2)

    if multilingual:
        for service in services:
            for language in ["de", "fr"]:
                service_t_factory(language=language, service=service)

    if multi_mail_service:
        services[0].email = f"{services[0].email},foo@bar.com"
        services[0].save()

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
        addressed_groups=[str(services[0].pk)] if not is_applicant else ["applicant"],
        controlling_groups=[str(services[1].pk)] if has_controlling else [],
    )

    call_command("send_work_item_reminders")

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
    call_command("send_work_item_reminders")
    assert len(mailoutbox) == 0
