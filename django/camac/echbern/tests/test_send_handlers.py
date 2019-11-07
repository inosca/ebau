import pytest

from camac.constants.kt_bern import (
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_EBAU_NUMMER_VERGEBEN,
    INSTANCE_STATE_KOORDINATION,
)
from camac.core.models import InstanceService
from camac.echbern.tests.utils import xml_data

from ..schema.ech_0211_2_0 import CreateFromDocument
from ..send_handlers import (
    ChangeResponsibilitySendHandler,
    RulingNoticeSendHandler,
    SendHandlerException,
)


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

    dh = RulingNoticeSendHandler(
        data=data,
        instance=ech_instance,
        user=None,
        group=admin_user.groups.first(),
        auth_header=None,
    )
    assert dh.has_permission() == has_permission


@pytest.mark.parametrize("fail", [False, True])
def test_change_responsibility_send_handler(fail, service_factory, ech_instance):
    burgdorf = ech_instance.active_service

    if not fail:
        madiswil = service_factory(pk=20351)

    data = CreateFromDocument(xml_data("change_responsibility"))

    dh = ChangeResponsibilitySendHandler(
        data=data, instance=ech_instance, user=None, group=None, auth_header=None
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
