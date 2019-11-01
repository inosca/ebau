import pytest

from camac.echbern import data_preparation
from camac.echbern.signals import instance_submitted

from .. import event_handlers
from ..models import Message
from .caluma_responses import full_document


def test_submit_event(ech_instance, role_factory, group_factory, requests_mock, mocker):
    group_factory(role=role_factory(name="support"))
    requests_mock.post("http://caluma:8000/graphql/", json=full_document)
    mocker.patch.object(data_preparation, "get_admin_token", return_value="token")
    instance_submitted.send(
        sender=None, instance=ech_instance, auth_header="auth_header", group_pk=20003
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"


@pytest.mark.parametrize(
    "event_type",
    ["FileSubsequently", "WithdrawPlanningPermissionApplication", "AccompanyingReport"],
)
def test_event_handlers(
    event_type,
    ech_instance,
    attachment,
    attachment_section_factory,
    role_factory,
    group_factory,
    requests_mock,
    mocker,
):
    if event_type == "AccompanyingReport":
        attachment.instance = ech_instance
        attachment.save()
        attachment_section = attachment_section_factory(pk=7)
        attachment.attachment_sections.add(attachment_section)

    group_factory(role=role_factory(name="support"))
    requests_mock.post("http://caluma:8000/graphql/", json=full_document)
    mocker.patch.object(data_preparation, "get_admin_token", return_value="token")

    eh = getattr(event_handlers, f"{event_type}EventHandler")(ech_instance)
    eh.run()
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"
