# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_param_client 1'] = {
    'parzellen': {
        'label': 'Suse Junk',
        'value': {
            'lagekoordinaten-nord': {
                'label': 'Elwira Pärtzelt',
                'value': 1228434.884375
            },
            'lagekoordinaten-ost': {
                'label': 'Trudi Thanel',
                'value': 2607160.642708333
            }
        }
    }
}
