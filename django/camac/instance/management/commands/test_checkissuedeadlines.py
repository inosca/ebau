import os
from datetime import date, timedelta

import pytest
from django.core.management import CommandError, call_command

from camac.instance.models import Issue


def test_checkissuedeadlines(
    db, issue_factory, service, user, mailoutbox, notification_template
):
    delayed_issue = issue_factory(
        service=service, user=user, deadline_date=date.today() - timedelta(1)
    )
    open_issue = issue_factory(service=service, user=user, deadline_date=date.today())

    call_command(
        "checkissuedeadlines",
        template=notification_template.pk,
        stdout=open(os.devnull, "w"),
    )

    assert len(mailoutbox) == 1

    delayed_issue.refresh_from_db()
    assert delayed_issue.state == Issue.STATE_DELAYED

    open_issue.refresh_from_db()
    assert open_issue.state == Issue.STATE_OPEN


@pytest.mark.parametrize(
    "notification_template__subject,issue__deadline_date",
    [("{{$invalid}}", "2018-01-01")],
)
def test_checkissuedeadlines_invalid_template(db, issue, notification_template):
    with pytest.raises(CommandError):
        call_command(
            "checkissuedeadlines",
            template=notification_template.pk,
            stdout=open(os.devnull, "w"),
        )
