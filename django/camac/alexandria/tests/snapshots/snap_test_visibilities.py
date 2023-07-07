# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_category_visibility[applicant-1] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}

snapshots['test_category_visibility[municipality-3] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}

snapshots['test_category_visibility[service-2] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}
