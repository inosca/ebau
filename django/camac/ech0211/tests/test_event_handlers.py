import pytest
from pytest_factoryboy import LazyFixture

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
)
from camac.ech0211.signals import file_subsequently, instance_submitted

from ...conftest import FakeRequest
from ...core.models import InstanceService
from ...instance.serializers import InstanceSubmitSerializer
from .. import event_handlers
from ..models import Message


@pytest.mark.parametrize(
    "instance__user,location__communal_federal_number,instance_state__name",
    [(LazyFixture("admin_user"), "1311", "new")],
)
@pytest.mark.parametrize(
    "role__name,instance__location,form__name",
    [
        ("Support", LazyFixture("location"), "baugesuch"),
    ],
)
@pytest.mark.freeze_time("2022-07-07")
def test_submit_event_sz(
    db,
    set_application_sz,
    ech_instance_sz,
    sz_ech0211_settings,
    rf,
    admin_client,
    role,
    user_group,
    instance,
    instance_state,
    instance_state_factory,
    form,
    form_field_factory,
    caplog,
    ech_snapshot,
    master_data_is_visible_mock,
):
    instance_state_factory(name="subm")
    serializer = InstanceSubmitSerializer(
        context={
            "request": FakeRequest(
                user=ech_instance_sz.user,
                group=user_group.group,
            )
        }
    )

    caplog.clear()
    serializer.update(
        ech_instance_sz,
        validated_data={
            "data": {
                "type": "instances",
                "attributes": {
                    "copy-source": str(ech_instance_sz.pk),
                    "is-modification": True,
                },
            }
        },
    )

    caplog.clear()

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == ech_instance_sz.group.service.name
    ech_snapshot(message.body)


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("has_active_service", [True, False])
def test_submit_event_be(
    set_application_be,
    ech_instance_be,
    be_ech0211_settings,
    role_factory,
    group_factory,
    mocker,
    multilang,
    has_active_service,
    caplog,
    ech_snapshot,
    master_data_is_visible_mock,
):
    if not has_active_service:
        InstanceService.objects.filter(instance_id=ech_instance_be).update(active=False)

    group_factory(role=role_factory(name="support"))

    caplog.clear()

    instance_submitted.send(
        sender=None,
        instance=ech_instance_be,
        auth_header="auth_header",
        user_pk=None,
        group_pk=20003,
    )
    if has_active_service:
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver.get_name() == "Leitbehörde Burgdorf"
        ech_snapshot(message.body)
    else:
        assert not Message.objects.exists()
        assert len(caplog.messages) == 1


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize(
    "event_type",
    [
        "FileSubsequently",
        "WithdrawPlanningPermissionApplication",
        "StatusNotification",
        "Claim",
        "ChangeResponsibility",
    ],
)
def test_event_handlers(
    event_type,
    ech_instance_be,
    be_ech0211_settings,
    set_application_be,
    role_factory,
    instance_service_factory,
    service_t_factory,
    instance_state_factory,
    group_factory,
    mocker,
    multilang,
    ech_snapshot,
    master_data_is_visible_mock,
):
    if event_type == "FileSubsequently":
        group_factory(role=role_factory(name="support"))

    if event_type == "StatusNotification":
        ech_instance_be.instance_state = instance_state_factory(name="circulation_init")
        ech_instance_be.save()

    if event_type == "ChangeResponsibility":
        service = ech_instance_be.responsible_service(filter_type="municipality")
        instance_service = ech_instance_be.instance_services.filter(
            active=1, service=service
        ).first()
        instance_service.active = 0
        instance_service.save()
        inst_serv = instance_service_factory(
            instance=ech_instance_be,
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
    eh = getattr(event_handlers, f"{event_type}EventHandler")(ech_instance_be)
    eh.run()
    assert Message.objects.count() == 1
    message = Message.objects.first()
    if event_type == "ChangeResponsibility":
        assert message.receiver.get_name() == "Leitbehörde Madiswil"
    else:
        assert message.receiver.get_name() == "Leitbehörde Burgdorf"
    ech_snapshot(message.body)


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("notices_exists", [True, False])
def test_accompanying_report_event_handler(
    db,
    active_inquiry_factory,
    answer_factory,
    attachment_factory,
    attachment_section_factory,
    be_distribution_settings,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
    group_factory,
    multilang,
    notices_exists,
    service_factory,
    set_application_be,
    user,
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
        instance=ech_instance_be, group=parent_group, name="parent.pdf"
    )
    attachment_parent.save()
    attachment_parent.attachment_sections.add(attachment_section_bet_beh)

    attachment_child = attachment_factory(
        instance=ech_instance_be, group=child_group, name="child.pdf"
    )
    attachment_child.save()
    attachment_child.attachment_sections.add(attachment_section_bet_beh)

    # Should not show up, because it's from another service
    attachment_dummy = attachment_factory(
        instance=ech_instance_be, group=dummy_group, name="dummy1.pdf"
    )
    attachment_dummy.save()
    attachment_dummy.attachment_sections.add(attachment_section_bet_beh)

    # Should not show up, because it's in a different attachment section
    attachment_dummy2 = attachment_factory(
        instance=ech_instance_be, group=parent_group, name="dummy2.pdf"
    )
    attachment_dummy2.save()
    attachment_dummy2.attachment_sections.add(attachment_section_alle_bet)

    inquiry = active_inquiry_factory(
        for_instance=ech_instance_be,
        addressed_service=parent_service,
    )

    answer_factory(
        document=inquiry.child_case.document,
        question_id=be_distribution_settings["QUESTIONS"]["STATUS"],
        value=be_distribution_settings["ANSWERS"]["STATUS"]["UNKNOWN"],
    )

    if notices_exists:
        answer_factory(
            document=inquiry.child_case.document,
            question_id=be_distribution_settings["QUESTIONS"]["STATEMENT"],
            value="lorem ipsum " * 100,  # 1200 characters
        )
        answer_factory(
            document=inquiry.child_case.document,
            question_id=be_distribution_settings["QUESTIONS"]["ANCILLARY_CLAUSES"],
            value="nebenbestimmung\r\nblablabla\r\nblu; yeah ",
        )

    eh = event_handlers.AccompanyingReportEventHandler(ech_instance_be, inquiry=inquiry)
    eh.run()

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == "Leitbehörde Burgdorf"
    ech_snapshot(message.body)


@pytest.mark.freeze_time("2022-06-03")
def test_task_event_handler_stellungnahme(
    db,
    active_inquiry_factory,
    admin_user,
    attachment_attachment_section_factory,
    attachment_section_factory,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
    instance_state_factory,
    service_factory,
    set_application_be,
):
    asection_gesuch = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_GESUCH)
    attachment_attachment_section_factory(
        attachment__instance=ech_instance_be, attachmentsection=asection_gesuch
    )
    asection_sb1 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB1)
    attachment_attachment_section_factory(
        attachment__instance=ech_instance_be, attachmentsection=asection_sb1
    )

    ech_instance_be.instance_state = instance_state_factory(name="circulation")
    ech_instance_be.save()
    s1 = service_factory(email="s1@example.com")

    inquiry = active_inquiry_factory(for_instance=ech_instance_be, addressed_service=s1)

    eh = event_handlers.TaskEventHandler(
        ech_instance_be, user_pk=admin_user.pk, inquiry=inquiry
    )
    eh.run()

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver == s1
    ech_snapshot(message.body)


@pytest.mark.freeze_time("2022-06-03")
@pytest.mark.parametrize("instance_state_name", ["sb2", "conclusion"])
def test_task_event_handler_SBs(
    ech_instance_be,
    be_ech0211_settings,
    set_application_be,
    instance_state_name,
    instance_state_factory,
    admin_user,
    attachment_attachment_section_factory,
    attachment_section_factory,
    service_factory,
    instance_service_factory,
    ech_snapshot,
):
    service_baukontrolle = service_factory(
        service_group__name="construction-control",
        name=None,
        trans__name="Baukontrolle Burgdorf",
        trans__city="Burgdorf",
        trans__language="de",
    )
    instance_service_factory(
        instance=ech_instance_be, service=service_baukontrolle, active=1
    )

    asection_sb1 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB1)
    attachment_attachment_section_factory(
        attachment__instance=ech_instance_be, attachmentsection=asection_sb1
    )
    asection_sb2 = attachment_section_factory(pk=ATTACHMENT_SECTION_BEILAGEN_SB2)
    attachment_attachment_section_factory(
        attachment__instance=ech_instance_be, attachmentsection=asection_sb2
    )

    ech_instance_be.instance_state = instance_state_factory(name=instance_state_name)
    ech_instance_be.save()

    eh = event_handlers.TaskEventHandler(ech_instance_be, user_pk=admin_user.pk)
    eh.run()

    assert Message.objects.count() == 1
    ech_snapshot(Message.objects.first().body)


@pytest.mark.freeze_time("2022-06-03")
def test_file_subsequently_signal(
    set_application_be,
    ech_instance_be,
    be_ech0211_settings,
    ech_snapshot,
):
    file_subsequently.send(
        sender=None, instance=ech_instance_be, user_pk=None, group_pk=None
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.get_name() == "Leitbehörde Burgdorf"
    ech_snapshot(message.body)


def test_skip_events_sz(
    set_application_sz,
    ech_instance_sz,
    sz_ech0211_settings,
):
    file_subsequently.send(
        sender=None, instance=ech_instance_sz, user_pk=None, group_pk=None
    )
    assert Message.objects.count() == 0
