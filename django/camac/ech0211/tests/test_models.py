from camac.ech0211.tests.utils import xml_data


def test_message_model(db, message_factory, snapshot):
    message = message_factory(body=xml_data("accompanying_report"))
    assert message.get_event_type() == "accompanying report"
    snapshot.assert_match(message.get_documents())
