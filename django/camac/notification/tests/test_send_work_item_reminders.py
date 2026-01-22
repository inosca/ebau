from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from camac.notification.tasks import send_notification_for_overdue_workitems


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
    caluma_work_item_factory,
    caluma_task_factory,
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
    settings.INTERNAL_BASE_URL = "http://ebau.localhost"

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

    caluma_work_item_factory(
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
def test_dont_send_reminders_caluma(
    db, user, service, caluma_work_item_factory, mailoutbox
):
    service.disabled = 1
    service.save()
    caluma_work_item_factory(
        status="ready",
        meta={"not-viewed": True},
        deadline=timezone.now() - timedelta(days=1),
        assigned_users=[user.username],
        addressed_groups=[service.pk],
        controlling_groups=[service.pk],
    )
    call_command("send_work_item_reminders")
    assert len(mailoutbox) == 0


@pytest.mark.freeze_time("2020-08-10")
def test_notify_manual_work_item(
    db,
    caluma_admin_user,
    service_factory,
    instance,
    caluma_work_item_factory,
    mailoutbox,
    application_settings,
    notification_template_factory,
    caluma_task_factory,
    support_role,
    settings,
):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.APPLICATION["NOTIFICATIONS"]["PROCESS_DEADLINES_FROM"] = "2020-08-09"

    notification_template_expired = notification_template_factory()
    application_settings["NOTIFICATIONS"]["WORKITEM_DEADLINE_OVERDUE"] = {
        "create-manual-workitems": {
            "template_slug": notification_template_expired.slug,
            "recipient_types": ["work_item_controlling"],
        },
    }

    controlling_service = service_factory()
    addressed_service = service_factory()

    deadline_past_initial_check = timezone.now() - timedelta(days=3)
    deadline = timezone.now() - timedelta(days=1)
    deadline_future = timezone.now() + timedelta(days=2)
    task = caluma_task_factory(
        slug=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
    )
    task_ignored = caluma_task_factory()
    work_item_args = {
        "status": "ready",
        "addressed_groups": [str(addressed_service.pk)],
        "controlling_groups": [str(controlling_service.pk)],
        "child_case": None,
        "deadline": deadline,
    }
    work_item = caluma_work_item_factory(
        task=task,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
        },
        **work_item_args,
    )
    instance.case = work_item.case
    instance.save()

    caluma_work_item_factory(
        task=task,
        case=instance.case,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": False,
        },
        **work_item_args,
    )

    caluma_work_item_factory(
        task=task_ignored,
        case=instance.case,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
        },
        **work_item_args,
    )
    caluma_work_item_factory(
        task=task,
        case=instance.case,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
            "deadline_notification_sent_at": "Some random date",
        },
        **work_item_args,
    )
    caluma_work_item_factory(
        task=task,
        case=instance.case,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
        },
        **{**work_item_args, "deadline": deadline_future},
    )
    caluma_work_item_factory(
        task=task,
        case=instance.case,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
        },
        **{**work_item_args, "deadline": deadline_past_initial_check},
    )

    # Setup periodic task

    task_name = "camac.notification.tasks.send_notification_for_overdue_workitems"
    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=timezone.now())
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f"{task_name}, This should send notifications.",
        task=task_name,
        one_off=True,
        enabled=True,
    )

    send_notification_for_overdue_workitems.delay()

    assert len(mailoutbox) == 1
    assert mailoutbox[0].recipients()[0] == controlling_service.email
