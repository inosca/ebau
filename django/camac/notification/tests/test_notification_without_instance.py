from camac.notification.utils import send_mail_without_instance


def test_recipient_unanswered_inquiries(
    db,
    notification_template_factory,
    mailoutbox,
    settings,
):
    template = notification_template_factory(body="Hello {{INTERNAL_BASE_URL}} {{FOO}}")
    send_mail_without_instance(template.slug, ["foo@example.com"], {"FOO": "BAR"})
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == template.subject
    assert mailoutbox[0].body == f"Hello {settings.INTERNAL_BASE_URL} BAR"
