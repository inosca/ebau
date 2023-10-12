# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_view_structure 1'] = {
    'data': {
        'table-question': {
            'form': 'table-form',
            'hidden': False,
            'label': 'Table Question',
            'value': [
                {
                    'table-question-1': {
                        'label': 'Question 1 in table',
                        'value': 'row 1 value 1'
                    },
                    'table-question-2': {
                        'label': 'Question 2 in table',
                        'value': 'row 1 value 2'
                    }
                },
                {
                    'table-question-1': {
                        'label': 'Question 1 in table',
                        'value': 'row 2 value 1'
                    },
                    'table-question-2': {
                        'label': 'Question 2 in table',
                        'value': 'row 2 value 2'
                    }
                }
            ]
        },
        'text-question': {
            'hidden': False,
            'label': 'Text Question',
            'value': 'foo'
        }
    }
}
