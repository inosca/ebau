import datetime
from io import StringIO

import pytest
from django.core.management import call_command

from camac.instance.serializers import SUBMIT_DATE_FORMAT


@pytest.mark.parametrize(
    "call_args,expected_queries",
    [
        (("12345",), 2),
        ((), 811),
        (("--dry-run",), 508),
        (("--no-recompute",), 811),
    ],
)
def test_calculate_cycle_times_command(
    db,
    admin_user,
    be_instance,
    instance_factory,
    instance_with_case,
    docx_decision_factory,
    django_assert_num_queries,
    call_args,
    expected_queries,
):

    # one instance to optionally omit
    be_instance.case.meta.update({"total_cycle_time": 11, "net_cycle_time": 10})
    be_instance.case.save()
    docx_decision_factory(
        instance=be_instance,
        decision_date=(be_instance.creation_date + datetime.timedelta(days=1)).date(),
    )

    for _ in range(100):
        # Min. 100 cases needed to get progress printed at least once
        instance = instance_with_case(instance_factory(user=admin_user))
        instance.case.meta.update(
            {
                "submit-date": instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
                "paper-submit-date": instance.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            }
        )
        instance.case.save()
        docx_decision_factory(
            instance=instance,
            decision_date=(instance.creation_date + datetime.timedelta(days=1)).date(),
        )
    out = StringIO()
    with django_assert_num_queries(expected_queries):
        call_command(
            "calculate_cycle_times",
            *call_args,
            stdout=out,
            stderr=StringIO(),
        )
    out.getvalue()
