import pytest

from camac.constants.kt_bern import (
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_EBAU_NUMMER_VERGEBEN,
    INSTANCE_STATE_FINISHED,
    INSTANCE_STATE_KOORDINATION,
    INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT,
    INSTANCE_STATE_ZIRKULATION,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
)
from camac.core.models import Activation, Circulation, InstanceService, Notice
from camac.echbern.tests.utils import xml_data
from camac.instance.models import Instance

from ..models import Message
from ..schema.ech_0211_2_0 import CreateFromDocument
from ..send_handlers import (
    AccompanyingReportSendHandler,
    ChangeResponsibilitySendHandler,
    CloseArchiveDossierSendHandler,
    NoticeKindOfProceedingsSendHandler,
    NoticeRulingSendHandler,
    SendHandlerException,
    TaskSendHandler,
    resolve_send_handler,
)


@pytest.mark.parametrize(
    "xml_file,expected_send_handler",
    [
        ("accompanying_report", AccompanyingReportSendHandler),
        ("change_responsibility", ChangeResponsibilitySendHandler),
        ("close_dossier", CloseArchiveDossierSendHandler),
        ("notice_ruling", NoticeRulingSendHandler),
        ("task", TaskSendHandler),
        ("kind_of_proceedings", NoticeKindOfProceedingsSendHandler),
        ("accompanying_report", None),
    ],
)
def test_resolve_send_handler(xml_file, expected_send_handler):
    data = CreateFromDocument(xml_data(xml_file))
    if not expected_send_handler:
        data.eventAccompanyingReport = None
        with pytest.raises(SendHandlerException):
            resolve_send_handler(data)
    else:
        assert resolve_send_handler(data) == expected_send_handler


@pytest.mark.parametrize(
    "judgement,instance_state_pk,has_permission",
    [
        (4, INSTANCE_STATE_DOSSIERPRUEFUNG, True),
        (3, INSTANCE_STATE_DOSSIERPRUEFUNG, False),
        (1, INSTANCE_STATE_KOORDINATION, True),
        (4, INSTANCE_STATE_EBAU_NUMMER_VERGEBEN, False),
    ],
)
def test_ruling_notice_permissions(
    judgement,
    instance_state_pk,
    has_permission,
    admin_user,
    ech_instance,
    instance_state_factory,
):
    data = CreateFromDocument(xml_data("notice_ruling"))

    data.eventNotice.decisionRuling.judgement = judgement

    state = instance_state_factory(pk=instance_state_pk)
    ech_instance.instance_state = state
    ech_instance.save()

    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    dh = NoticeRulingSendHandler(
        data=data,
        queryset=Instance.objects,
        user=None,
        group=admin_user.groups.first(),
        auth_header=None,
    )
    assert dh.has_permission() == has_permission


@pytest.mark.parametrize("fail", [False, True])
def test_change_responsibility_send_handler(
    fail, admin_user, service_factory, ech_instance
):
    burgdorf = ech_instance.active_service

    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    if not fail:
        madiswil = service_factory(pk=20351)

    data = CreateFromDocument(xml_data("change_responsibility"))

    dh = ChangeResponsibilitySendHandler(
        data=data, queryset=Instance.objects, user=None, group=group, auth_header=None
    )
    assert dh.has_permission() is True

    if not fail:
        dh.apply()
        assert ech_instance.active_service == madiswil
        assert InstanceService.objects.get(
            instance=ech_instance, service=burgdorf, active=0
        )
        assert InstanceService.objects.get(
            instance=ech_instance, service=madiswil, active=1
        )
    else:
        with pytest.raises(SendHandlerException):
            dh.apply()


@pytest.mark.parametrize(
    "requesting_service,success",
    [("leitbehörde", True), ("baukontrolle", True), ("nobody", False)],
)
def test_close_dossier_send_handler(
    requesting_service,
    success,
    ech_instance,
    admin_user,
    instance_service_factory,
    instance_state_factory,
):
    instance_state_factory(pk=INSTANCE_STATE_FINISHED)

    inst_serv = instance_service_factory(
        instance=ech_instance, service__name="Baukontrolle Burgdorf", active=1
    )

    group = admin_user.groups.first()

    if requesting_service == "leitbehörde":
        group.service = ech_instance.services.first()
    elif requesting_service == "baukontrolle":
        group.service = inst_serv.service

    group.save()

    data = CreateFromDocument(xml_data("close_dossier"))

    dh = CloseArchiveDossierSendHandler(
        data=data, queryset=Instance.objects, user=None, group=group, auth_header=None
    )

    assert dh.has_permission() is success

    if success:
        dh.apply()
        ech_instance.refresh_from_db()

        assert ech_instance.instance_state.pk == INSTANCE_STATE_FINISHED


@pytest.mark.parametrize(
    "has_circulation,has_service,valid_service_id,has_template,success",
    [
        (True, True, True, True, True),
        (False, True, True, True, True),
        (True, False, True, True, False),
        (True, True, False, True, False),
        (True, True, True, False, False),
    ],
)
def test_task_send_handler(
    has_circulation,
    has_service,
    valid_service_id,
    has_template,
    success,
    admin_user,
    circulation_factory,
    ech_instance,
    instance_state_factory,
    service_factory,
    circulation_state_factory,
    instance_resource_factory,
    notification_template_factory,
    mailoutbox,
):
    if has_template:
        notification_template_factory(pk=11)

    instance_resource_factory(pk=INSTANCE_STATE_ZIRKULATION)
    circulation_state_factory(pk=1, name="RUN")
    state = instance_state_factory(pk=INSTANCE_STATE_ZIRKULATION)
    ech_instance.instance_state = state
    ech_instance.save()

    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    if has_service:
        service = service_factory(pk=23, email="s1@example.com")

    if has_circulation:
        circulation_factory(instance=ech_instance)  # dummy
        circulation = circulation_factory(instance=ech_instance)

    xml = xml_data("task")
    if not valid_service_id:
        xml = xml.replace("<serviceId>23</serviceId>", "<serviceId>string</serviceId>")

    data = CreateFromDocument(xml)

    dh = TaskSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header="Bearer: some token",
    )
    assert dh.has_permission() is True

    if success:
        dh.apply()
        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == service
        assert Activation.objects.count() == 1
        activation = Activation.objects.first()
        assert activation.service == service
        if has_circulation:
            assert activation.circulation == circulation

        assert len(mailoutbox) == 1

        assert activation.ech_msg_created is True
        assert "s1@example.com" in mailoutbox[0].bcc

    else:
        with pytest.raises(SendHandlerException):
            dh.apply()


def test_task_send_handler_no_permission(admin_user, ech_instance):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    data = CreateFromDocument(xml_data("task"))

    dh = TaskSendHandler(
        data=data, queryset=Instance.objects, user=None, group=group, auth_header=None
    )
    assert dh.has_permission() is False


def test_notice_kind_of_proceedings_send_handler(
    admin_user, ech_instance, instance_state_factory, instance_resource_factory
):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    state = instance_state_factory(pk=INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT)
    ech_instance.instance_state = state
    ech_instance.save()

    instance_state_factory(pk=INSTANCE_STATE_ZIRKULATION)
    instance_resource_factory(pk=INSTANCE_STATE_ZIRKULATION)

    data = CreateFromDocument(xml_data("kind_of_proceedings"))

    dh = NoticeKindOfProceedingsSendHandler(
        data=data,
        queryset=Instance.objects,
        user=admin_user,
        group=group,
        auth_header=None,
    )
    assert dh.has_permission() is True

    dh.apply()
    assert Circulation.objects.count() == 1
    ech_instance.refresh_from_db()
    assert ech_instance.instance_state.pk == INSTANCE_STATE_ZIRKULATION

    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver == ech_instance.active_service


@pytest.mark.parametrize("has_attachment", [True, False])
@pytest.mark.parametrize("has_activation", [True, False])
def test_accompanying_report_send_handler(
    has_attachment,
    has_activation,
    admin_user,
    ech_instance,
    attachment_factory,
    attachment_section_factory,
    circulation_state_factory,
    instance_state_factory,
    activation_factory,
    user_group_factory,
    notice_type_factory,
):
    user_group = user_group_factory(default_group=1)

    notice_type_factory(pk=NOTICE_TYPE_STELLUNGNAHME)
    notice_type_factory(pk=NOTICE_TYPE_NEBENBESTIMMUNG)

    if has_activation:
        activation_factory(
            circulation__instance=ech_instance,
            circulation_state=circulation_state_factory(pk=1, name="RUN"),
            service=user_group.group.service,
            user=user_group.user,
            circulation_answer=None,
        )

    done_state = circulation_state_factory(pk=2, name="DONE")

    support_group = admin_user.groups.first()
    support_group.service = ech_instance.services.first()
    support_group.save()

    state = instance_state_factory(pk=INSTANCE_STATE_ZIRKULATION)
    ech_instance.instance_state = state
    ech_instance.save()

    if has_attachment:
        attachment = attachment_factory(
            name="MyFile.pdf", uuid="b9ec16fc-cdde-49dd-81f9-43fc6629f2a9"
        )
        attachment.attachment_sections.add(attachment_section_factory(pk=7))

    data = CreateFromDocument(xml_data("accompanying_report"))

    dh = AccompanyingReportSendHandler(
        data=data,
        queryset=Instance.objects,
        user=user_group.user,
        group=user_group.group,
        auth_header=None,
    )
    if not has_activation:
        assert dh.has_permission() is False
        return

    assert dh.has_permission() is True

    if has_attachment:
        dh.apply()

        assert Message.objects.count() == 1
        message = Message.objects.first()
        assert message.receiver == support_group.service
        assert Activation.objects.count() == 1
        activation = Activation.objects.first()
        assert activation.circulation_state == done_state
        assert Notice.objects.count() == 2

    else:
        with pytest.raises(SendHandlerException):
            dh.apply()
