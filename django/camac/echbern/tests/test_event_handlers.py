import pytest

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
)
from camac.echbern.schema.ech_0211_2_0 import CreateFromDocument
from camac.echbern.signals import file_subsequently, instance_submitted

from ...core.models import InstanceService
from .. import event_handlers
from ..models import Message
from .caluma_document_data import baugesuch_data


@pytest.mark.parametrize("has_active_service", [True, False])
def test_submit_event(
    ech_instance,
    role_factory,
    group_factory,
    mocker,
    multilang,
    has_active_service,
    caplog,
):

    if not has_active_service:
        InstanceService.objects.filter(instance_id=ech_instance).update(active=False)

    group_factory(role=role_factory(name="support"))
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    caplog.clear()

    instance_submitted.send(
        sender=None,
        instance=ech_instance,
        auth_header="auth_header",
        user_pk=None,
        group_pk=20003,
    )
    if has_active_service:
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver.get_name() == "Leitbehörde Burgdorf"

    else:
        assert not Message.objects.exists()
        assert len(caplog.messages) == 1


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
    service_t_factory,
    instance_state_factory,
    group_factory,
    mocker,
    multilang,
):
    if event_type == "FileSubsequently":
        group_factory(role=role_factory(name="support"))
        mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)

    if event_type == "StatusNotification":
        ech_instance.previous_instance_state = instance_state_factory(pk=20000)
        ech_instance.save()

    if event_type == "ChangeResponsibility":
        service = ech_instance.responsible_service(filter_type="municipality")
        instance_service = ech_instance.instance_services.filter(
            active=1, service=service
        ).first()
        instance_service.active = 0
        instance_service.save()
        inst_serv = instance_service_factory(
            instance=ech_instance,
            service__name=None,
            service__city=None,
            service__zip="3500",
            service__address="Testweg 5",
            service__trans=None,
            service__service_group=instance_service.service.service_group,
            active=1,
        )
        service_t_factory(
            service=inst_serv.service,
            language="de",
            name="Leitbehörde Madiswil",
            city="Madiswil",
        )

    eh = getattr(event_handlers, f"{event_type}EventHandler")(ech_instance)
    eh.run()
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == expected_receiver


@pytest.mark.parametrize("notices_exists", [True, False])
@pytest.mark.parametrize("circulation_answer_exists", [True, False])
def test_accompanying_report_event_handler(
    db,
    notices_exists,
    circulation_answer_exists,
    user,
    service_factory,
    group_factory,
    ech_instance,
    attachment_factory,
    attachment_section_factory,
    activation_factory,
    notice_factory,
    notice_type_factory,
    circulation_answer_factory,
    multilang,
):
    parent_service = service_factory()
    parent_group = group_factory(service=parent_service)

    child_service = service_factory(service_parent=parent_service)
    child_group = group_factory(service=child_service)

    dummy_service = service_factory()
    dummy_group = group_factory(service=dummy_service)

    attachment_section_bet_beh = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_alle_bet = attachment_section_factory(
        pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN
    )

    attachment_parent = attachment_factory(
        instance=ech_instance, group=parent_group, name="parent.pdf"
    )
    attachment_parent.save()
    attachment_parent.attachment_sections.add(attachment_section_bet_beh)

    attachment_child = attachment_factory(
        instance=ech_instance, group=child_group, name="child.pdf"
    )
    attachment_child.save()
    attachment_child.attachment_sections.add(attachment_section_bet_beh)

    # Should not show up, because it's from another service
    attachment_dummy = attachment_factory(
        instance=ech_instance, group=dummy_group, name="dummy1.pdf"
    )
    attachment_dummy.save()
    attachment_dummy.attachment_sections.add(attachment_section_bet_beh)

    # Should not show up, because it's in a different attachment section
    attachment_dummy2 = attachment_factory(
        instance=ech_instance, group=parent_group, name="dummy2.pdf"
    )
    attachment_dummy2.save()
    attachment_dummy2.attachment_sections.add(attachment_section_alle_bet)

    activation = activation_factory(
        circulation__instance=ech_instance,
        circulation_answer=None,
        service=parent_service,
    )

    if notices_exists:
        notice_factory(
            activation=activation,
            notice_type=notice_type_factory(pk=NOTICE_TYPE_STELLUNGNAHME),
            content="lorem ipsum " * 100,  # 1200 characters
        )
        notice_factory(
            activation=activation,
            notice_type=notice_type_factory(pk=NOTICE_TYPE_NEBENBESTIMMUNG),
            content="nebenbestimmung\r\nblablabla\r\nblu; yeah ",
        )

    if circulation_answer_exists:
        circulation_answer_factory(name="positive")

    eh = event_handlers.AccompanyingReportEventHandler(
        ech_instance, None, None, context={"activation-id": activation.pk}
    )
    eh.run()

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == "Leitbehörde Burgdorf"

    xml = CreateFromDocument(message.body)

    assert len(xml.eventAccompanyingReport.document) == 2
    names = sorted(
        [
            xml.eventAccompanyingReport.document[0].titles.title[0].value(),
            xml.eventAccompanyingReport.document[1].titles.title[0].value(),
        ]
    )
    assert names == [attachment_child.display_name, attachment_parent.display_name]


def test_task_event_handler_stellungnahme(
    ech_instance,
    service_factory,
    circulation_factory,
    activation_factory,
    instance_state_factory,
    attachment_attachment_section_factory,
    attachment_section_factory,
    admin_user,
):
    asection_gesuch = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_GESUCH)
    aas_gesuch = attachment_attachment_section_factory(
        attachment__instance=ech_instance, attachmentsection=asection_gesuch
    )
    asection_sb1 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB1)
    attachment_attachment_section_factory(
        attachment__instance=ech_instance, attachmentsection=asection_sb1
    )

    expected_name = aas_gesuch.attachment.display_name

    ech_instance.instance_state = instance_state_factory(name="circulation")
    ech_instance.save()
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
    for message in Message.objects.iterator():
        xml = CreateFromDocument(message.body)
        assert len(xml.eventRequest.document) == 1
        assert xml.eventRequest.document[0].titles.title[0].value() == expected_name


@pytest.mark.parametrize("instance_state_name", ["sb2", "conclusion"])
def test_task_event_handler_SBs(
    instance_state_name,
    ech_instance,
    instance_state_factory,
    admin_user,
    attachment_attachment_section_factory,
    attachment_section_factory,
    service_factory,
    instance_service_factory,
):
    service_baukontrolle = service_factory(
        service_group__name="construction-control",
        name=None,
        trans__name="Baukontrolle Burgdorf",
        trans__city="Burgdorf",
        trans__language="de",
    )
    instance_service_factory(
        instance=ech_instance, service=service_baukontrolle, active=1
    )

    asection_sb1 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB1)
    aas_sb1 = attachment_attachment_section_factory(
        attachment__instance=ech_instance, attachmentsection=asection_sb1
    )
    asection_sb2 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB2)
    aas_sb2 = attachment_attachment_section_factory(
        attachment__instance=ech_instance, attachmentsection=asection_sb2
    )

    expected_name = aas_sb1.attachment.display_name
    if instance_state_name == "conclusion":
        expected_name = aas_sb2.attachment.display_name

    ech_instance.instance_state = instance_state_factory(name=instance_state_name)
    ech_instance.save()

    eh = event_handlers.TaskEventHandler(ech_instance, user_pk=admin_user.pk)

    assert len(eh.run()) == 1
    assert Message.objects.count() == 1
    message = Message.objects.first()
    xml = CreateFromDocument(message.body)

    assert len(xml.eventRequest.document) == 1
    assert xml.eventRequest.document[0].titles.title[0].value() == expected_name


def test_file_subsequently_signal(ech_instance, mocker, multilang):
    mocker.patch.object(event_handlers, "get_document", return_value=baugesuch_data)
    file_subsequently.send(
        sender=None, instance=ech_instance, user_pk=None, group_pk=None
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == "Leitbehörde Burgdorf"
