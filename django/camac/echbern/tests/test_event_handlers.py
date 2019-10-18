from camac.echbern import event_handlers
from camac.echbern.signals import instance_submitted

from ..models import Message
from .caluma_responses import full_document


def test_submit_event(ech_instance, requests_mock, mocker):
    requests_mock.post("http://caluma:8000/graphql/", json=full_document)
    token = mocker.patch.object(event_handlers, "get_admin_token")
    token.return_value = "token"
    instance_submitted.send(
        sender=None, instance=ech_instance, auth_header="auth_header", group_pk=20003
    )
    assert Message.objects.count() == 1
    message = Message.objects.first()
    assert message.receiver.name == "Leitbehörde Burgdorf"
