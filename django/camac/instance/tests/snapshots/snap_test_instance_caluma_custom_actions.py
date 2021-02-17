# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_fix_work_items[Support-circulation_init-False-200-expected_work_items1-False-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (circulation_init):
\tCreated: 'skip-circulation', 'init-circulation'

Fixed 1 instances:
- INSTANCE_ID, circulation_init, Elizabeth Garcia, Missing work items
'''

snapshots['test_fix_work_items[Support-circulation_init-False-200-expected_work_items1-True-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (circulation_init):
\tCreated: 'skip-circulation', 'init-circulation'

Fixed 1 instances:
- INSTANCE_ID, circulation_init, Elizabeth Garcia, Missing work items
'''

snapshots['test_fix_work_items[Support-sb1-False-200-expected_work_items2-False-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (sb1):
\tCreated: 'sb1'

Fixed 1 instances:
- INSTANCE_ID, sb1, Elizabeth Garcia, Missing work items
'''

snapshots['test_fix_work_items[Support-sb1-False-200-expected_work_items2-True-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (sb1):
\tCreated: 'sb1'

Fixed 1 instances:
- INSTANCE_ID, sb1, Elizabeth Garcia, Missing work items
'''

snapshots['test_fix_work_items[Support-subm-False-200-expected_work_items0-False-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (subm):
\tCreated: 'ebau-number'

Fixed 1 instances:
- INSTANCE_ID, subm, Elizabeth Garcia, Missing work items
'''

snapshots['test_fix_work_items[Support-subm-False-200-expected_work_items0-True-instance__user0-municipality] 1'] = '''Fixed 0 wrong instances states
Fixed 0 missing circulation work items
Deleted 0 circulation and activation work items
Canceled 0 activation work items of finished circulations
Canceled 0 cases of closed instances
Reopened 0 wrongly closed cases
Suspended 0 rejected or in correction cases
INSTANCE_ID (subm):
\tCreated: 'ebau-number'

Fixed 1 instances:
- INSTANCE_ID, subm, Elizabeth Garcia, Missing work items
'''
