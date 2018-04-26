import os

import pytest
from django.core.management import call_command

from camac.core.models import InstanceLog


@pytest.mark.freeze_time('2017-7-27')
def test_deletelogs(db):
    InstanceLog.objects.create(
        id=1, action='test', user_id=1,
        modification_date='2017-07-26 13:09:56+00:00'
    )
    InstanceLog.objects.create(
        id=2, action='test', user_id=1,
        modification_date='2017-04-25 23:09:56+00:00'
    )

    call_command('deletelogs', days=2, stdout=open(os.devnull, 'w'))

    assert InstanceLog.objects.count() == 1
    assert InstanceLog.objects.first().id == 1
