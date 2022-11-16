# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_inquiry_and_decision_data[Municipality] 1'] = {
    'decision': 'Bewilligt',
    'decision-date': '2022-11-16',
    'involved-at': '2022-08-31T22:00:00Z'
}
