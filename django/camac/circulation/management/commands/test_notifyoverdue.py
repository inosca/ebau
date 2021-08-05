from datetime import datetime, timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone

from camac.constants import kt_uri as constants

from .notifyoverdue import (
    Notification,
    determine_notification,
    get_overdue_activations,
    notify_once,
)


@pytest.fixture
def running_state(db, circulation_state_factory):
    return circulation_state_factory(
        circulation_state_id=constants.CIRCULATION_STATE_RUN, name="RUN"
    )


@pytest.fixture
def future_date():
    return timezone.make_aware(datetime(2017, 5, 28))


@pytest.fixture
def past_date():
    return timezone.make_aware(datetime(2017, 5, 15))


@pytest.fixture
def pending_activation(db, activation_factory, running_state, future_date):
    return activation_factory(
        deadline_date=future_date, circulation_state=running_state
    )


@pytest.fixture
def due_activation(db, activation_factory, running_state, past_date, be_instance):
    return activation_factory(
        deadline_date=past_date,
        circulation_state=running_state,
        circulation__instance=be_instance,
    )


@pytest.mark.freeze_time("2017-05-21")
def test_get_overdue_activations(due_activation, pending_activation):
    """Ensure that only due activations are considered."""
    activations = get_overdue_activations()
    assert len(activations) == 1


@pytest.mark.freeze_time("2017-05-21")
def test_get_overdue_activations_excluded_services(
    due_activation, application_settings, service_factory
):
    """Ensure that get_overdue_activations ignores activations of excluded services."""
    service = service_factory()
    due_activation.service = service
    due_activation.save()

    application_settings["NOTIFY_OVERDUE_EXCLUDED_SERVICES"] = [service.pk]

    activations = get_overdue_activations()
    assert len(activations) == 0


@pytest.mark.freeze_time("2017-05-21")
@pytest.mark.parametrize(
    "day_offset,will_notify,template_slug,recipient_type",
    [
        (3, False, None, None),
        (7, False, None, None),
        (
            15,
            True,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_FACHSTELLE,
            "activation_service",
        ),
        (
            22,
            True,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_LEITBEHOERDE,
            "circulation_service",
        ),
    ],
)
def test_action_overdue_deadline_date(
    due_activation, day_offset, will_notify, template_slug, recipient_type
):
    """Ensure that activations with exceeded deadlines get handeled with the correct
    notification template and recipient type.
    """
    today = timezone.now()
    deadline_date = today - timedelta(days=day_offset)

    due_activation.deadline_date = deadline_date
    due_activation.save()

    deadline_leitbehoerde = today - timedelta(days=21)
    deadline_service = today - timedelta(days=14)

    notification = determine_notification(
        deadline_leitbehoerde, deadline_service, due_activation
    )
    if will_notify:
        assert notification.activation == due_activation
        assert notification.template_slug == template_slug
        assert notification.recipient_type == recipient_type
    else:
        assert notification is None


@pytest.mark.freeze_time("2017-05-21")
@pytest.mark.parametrize(
    "day_offset,will_notify,template_slug,recipient_type",
    [
        (3, False, None, None),
        (7, False, None, None),
        (
            15,
            True,
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_FACHSTELLE,
            "activation_service",
        ),
        (
            22,
            True,
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_LEITBEHOERDE,
            "circulation_service",
        ),
    ],
)
def test_action_overdue_completion_date(
    db,
    due_activation,
    nfd_completion_date,
    day_offset,
    will_notify,
    template_slug,
    recipient_type,
):
    """Ensure that activations that have an nfd completion date set get handeled
    with the correct notification template and recipient type.
    """
    today = timezone.now()
    completion_date = today - timedelta(days=day_offset)

    nfd_completion_date.answer = completion_date
    nfd_completion_date.activation = due_activation
    nfd_completion_date.save()

    deadline_leitbehoerde = today - timedelta(days=21)
    deadline_service = today - timedelta(days=14)

    notification = determine_notification(
        deadline_leitbehoerde, deadline_service, due_activation
    )
    if will_notify:
        assert notification.activation == due_activation
        assert notification.template_slug == template_slug
        assert notification.recipient_type == recipient_type
    else:
        assert notification is None


@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize("already_sent", [False, True])
def test_notify_once(
    db,
    mailoutbox,
    activation_callback_notice_factory,
    be_instance,
    activation,
    notification_template,
    admin_user,
    already_sent,
):
    notification = Notification(
        activation, notification_template.slug, recipient_type="service"
    )

    if already_sent:
        activation_callback_notice_factory(
            activation_id=notification.activation.pk, reason=notification.template_slug
        )

    notify_once(notification)

    if already_sent:
        assert len(mailoutbox) == 0
    else:
        assert len(mailoutbox) == 1


@pytest.mark.freeze_time("2017-05-21")
@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize(
    "notification_template__slug",
    [constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_LEITBEHOERDE],
)
@pytest.mark.parametrize("dryrun", [True, False])
def test_notifyoverdue(
    db, admin_user, group, dryrun, notification_template, due_activation, mailoutbox
):
    """Ensure mail delivery works for overdue activations.

    If dryrun is active no mail notifications should be sent.
    """

    today = timezone.now()
    deadline_date = today - timedelta(days=60)

    due_activation.deadline_date = deadline_date
    due_activation.circulation.service.groups.add(group)
    due_activation.save()

    args = []
    if dryrun:
        args.append("--dryrun")

    call_command("notifyoverdue", *args)

    if dryrun:
        assert len(mailoutbox) == 0
    else:
        assert len(mailoutbox) == 1
