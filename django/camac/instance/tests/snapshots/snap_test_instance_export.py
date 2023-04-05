# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_caluma_export_sz[False-Gemeinde Schwyz-Municipality] 1'] = [
    '123-45-77',
    'Test form',
    'Test location',
    'Smoothie-licious Inc., Red Apple',
    'Test intent',
    'Test location',
    'Test instance state',
    '',
    '02.03.2023',
    '',
    '',
    '',
    '01.04.2023',
    '03.04.2023'
]

snapshots['test_caluma_export_sz[True-Gemeinde Schwyz-Municipality] 1'] = [
    '123-45-77',
    'Test form',
    'Test location',
    'Smoothie-not-so-licious Inc., Red Apple',
    'Test intent override',
    'Test address, Test special name, Test location',
    'Test instance state',
    '',
    '02.03.2023',
    '',
    '',
    '',
    '01.04.2023',
    '03.04.2023'
]
