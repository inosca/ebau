# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_category_visibility[Applicant-1] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}

snapshots['test_category_visibility[Municipality-3] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}

snapshots['test_category_visibility[Service-2] 1'] = {
    'access': {
        'applicant': 'Admin',
        'municipality': 'Read',
        'service': 'Read'
    }
}
