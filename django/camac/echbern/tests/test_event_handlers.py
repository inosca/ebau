import pytest
from django.conf import settings

from camac.echbern import data_preparation
from camac.echbern.signals import instance_submitted

from ...core.models import InstanceService
from .. import event_handlers
from ..models import Message
from .caluma_responses import full_document


def test_submit_event(ech_instance, role_factory, group_factory, requests_mock, mocker):
    group_factory(role=role_factory(name="support"))
    requests_mock.post("http://caluma:8000/graphql/", json=full_document)
    mocker.patch.object(data_preparation, "get_admin_token", return_value="token")
    instance_submitted.send(
        sender=None,
        instance=ech_instance,
        auth_header="auth_header",
        user_pk=None,
        group_pk=20003,
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"


@pytest.mark.parametrize(
    "event_type,expected_receiver",
    [
        ("FileSubsequently", "Leitbehörde Burgdorf"),
        ("WithdrawPlanningPermissionApplication", "Leitbehörde Burgdorf"),
        ("StatusNotification", "Leitbehörde Burgdorf"),
        ("AccompanyingReport", "Leitbehörde Burgdorf"),
        ("Claim", "Leitbehörde Burgdorf"),
        ("ChangeResponsibility", "Leitbehörde Madiswil"),
    ],
)
def test_event_handlers(
    event_type,
    expected_receiver,
    ech_instance,
    attachment,
    attachment_section_factory,
    role_factory,
    instance_service_factory,
    instance_state_factory,
    group_factory,
    requests_mock,
    mocker,
):
    if event_type == "FileSubsequently":
        group_factory(role=role_factory(name="support"))
        requests_mock.post("http://caluma:8000/graphql/", json=full_document)
        mocker.patch.object(data_preparation, "get_admin_token", return_value="token")

    if event_type == "StatusNotification":
        ech_instance.previous_instance_state = instance_state_factory(pk=20000)
        ech_instance.save()

    if event_type == "AccompanyingReport":
        attachment.instance = ech_instance
        attachment.save()
        attachment_section = attachment_section_factory(pk=7)
        attachment.attachment_sections.add(attachment_section)

    if event_type == "ChangeResponsibility":
        instance_service = InstanceService.objects.filter(
            active=1,
            instance=ech_instance,
            **settings.APPLICATION.get("ACTIVE_SERVICE_FILTERS", {}),
        ).first()
        instance_service.active = 0
        instance_service.save()
        instance_service_factory(
            instance=ech_instance,
            service__name="Leitbehörde Madiswil",
            service__city="Madiswil",
            service__zip="3500",
            service__address="Testweg 5",
            active=1,
        )

    eh = getattr(event_handlers, f"{event_type}EventHandler")(ech_instance)
    eh.run()
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == expected_receiver


@pytest.mark.parametrize("fail_mail", [False, True])
def test_task_event_handler(
    fail_mail,
    ech_instance,
    service_factory,
    circulation_factory,
    notification_template_factory,
    activation_factory,
    admin_user,
    mailoutbox,
):
    s1 = service_factory(email="s1@example.com")
    s2 = service_factory(email="s2@example.com")
    s3 = service_factory(email="s3@example.com")
    if not fail_mail:
        notification_template_factory(pk=11)
    circulation = circulation_factory(instance=ech_instance)
    a1 = activation_factory(circulation=circulation, service=s1, email_sent=0)
    a2 = activation_factory(circulation=circulation, service=s2, email_sent=0)
    activation_factory(circulation=circulation, service=s3, ech_msg_created=True)

    eh = event_handlers.TaskEventHandler(ech_instance, user_pk=admin_user.pk)

    if fail_mail:
        with pytest.raises(event_handlers.EventHandlerException):
            eh.run()
    else:
        assert len(eh.run()) == 2
        assert Message.objects.count() == 2
        assert Message.objects.filter(receiver__in=[s1, s2]).count() == 2

        assert len(mailoutbox) == 1
        assert len(mailoutbox[0].bcc) == 2

        for a in [a1, a2]:
            a.refresh_from_db()
            assert a.ech_msg_created is True
            assert "s1@example.com" in mailoutbox[0].bcc
            assert "s2@example.com" in mailoutbox[0].bcc
