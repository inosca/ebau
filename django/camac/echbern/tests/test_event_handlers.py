import pytest
from django.conf import settings

from camac.constants.kt_bern import (
    CIRCULATION_ANSWER_POSITIV,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
)
from camac.echbern.signals import file_subsequently, instance_submitted

from ...core.models import InstanceService
from .. import event_handlers
from ..models import Message
from .caluma_document_data import baugesuch_data


def test_submit_event(ech_instance, role_factory, group_factory, mocker):
    group_factory(role=role_factory(name="support"))
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)
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
        ("Claim", "Leitbehörde Burgdorf"),
        ("ChangeResponsibility", "Leitbehörde Madiswil"),
    ],
)
def test_event_handlers(
    event_type,
    expected_receiver,
    ech_instance,
    role_factory,
    instance_service_factory,
    instance_state_factory,
    group_factory,
    mocker,
):
    if event_type == "FileSubsequently":
        group_factory(role=role_factory(name="support"))
        mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    if event_type == "StatusNotification":
        ech_instance.previous_instance_state = instance_state_factory(pk=20000)
        ech_instance.save()

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


@pytest.mark.parametrize("notices_exists", [True, False])
@pytest.mark.parametrize("circulation_answer_exists", [True, False])
def test_accompanying_report_event_handler(
    notices_exists,
    circulation_answer_exists,
    ech_instance,
    attachment,
    attachment_section_factory,
    activation_factory,
    notice_factory,
    notice_type_factory,
    circulation_answer_factory,
):
    attachment.instance = ech_instance
    attachment.save()
    attachment_section = attachment_section_factory(pk=7)
    attachment.attachment_sections.add(attachment_section)
    activation = activation_factory(
        circulation__instance=ech_instance, circulation_answer=None
    )

    if notices_exists:
        notice_factory(
            activation=activation,
            notice_type=notice_type_factory(pk=NOTICE_TYPE_STELLUNGNAHME),
            content="stellungnahme\r\nblablabla\r\nblu",
        )
        notice_factory(
            activation=activation,
            notice_type=notice_type_factory(pk=NOTICE_TYPE_NEBENBESTIMMUNG),
            content="nebenbestimmung\r\nblablabla\r\nblu; yeah",
        )

    if circulation_answer_exists:
        circulation_answer_factory(pk=CIRCULATION_ANSWER_POSITIV)

    eh = event_handlers.AccompanyingReportEventHandler(
        ech_instance, None, None, context={"activation-id": activation.pk}
    )
    eh.run()
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"


def test_task_event_handler(
    ech_instance, service_factory, circulation_factory, activation_factory, admin_user
):
    s1 = service_factory(email="s1@example.com")
    s2 = service_factory(email="s2@example.com")
    s3 = service_factory(email="s3@example.com")

    circulation = circulation_factory(instance=ech_instance)
    activation_factory(circulation=circulation, service=s1, email_sent=0)
    activation_factory(circulation=circulation, service=s2, email_sent=0)
    activation_factory(circulation=circulation, service=s3, ech_msg_created=True)

    eh = event_handlers.TaskEventHandler(ech_instance, user_pk=admin_user.pk)

    assert len(eh.run()) == 2
    assert Message.objects.count() == 2
    assert Message.objects.filter(receiver=s1)
    assert Message.objects.filter(receiver=s2)
    assert not Message.objects.filter(receiver=s3)


def test_file_subsequently_signal(ech_instance, mocker):
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)
    file_subsequently.send(
        sender=None, instance=ech_instance, user_pk=None, group_pk=None
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"
