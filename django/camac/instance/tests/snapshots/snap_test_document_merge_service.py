# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_document_merge_service_full_document 1'] = [
    {
        'children': [
            {
                'hidden': False,
                'label': '',
                'slug': 'text-question',
                'type': 'TextQuestion',
                'value': 'some text answer'
            },
            {
                'columns': [
                    '',
                    ''
                ],
                'hidden': False,
                'label': '',
                'rows': [
                    [
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'text-question',
                            'type': 'TextQuestion',
                            'value': 'and another'
                        },
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'choice-question',
                            'type': 'TextQuestion',
                            'value': ''
                        }
                    ],
                    [
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'text-question',
                            'type': 'TextQuestion',
                            'value': 'second table answer'
                        },
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'choice-question',
                            'type': 'TextQuestion',
                            'value': ''
                        }
                    ],
                    [
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'text-question',
                            'type': 'TextQuestion',
                            'value': None
                        },
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'choice-question',
                            'type': 'TextQuestion',
                            'value': ''
                        }
                    ],
                    [
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'text-question',
                            'type': 'TextQuestion',
                            'value': 'first table answer'
                        },
                        {
                            'hidden': False,
                            'label': '',
                            'slug': 'choice-question',
                            'type': 'TextQuestion',
                            'value': ''
                        }
                    ]
                ],
                'slug': 'table-question',
                'type': 'TableQuestion'
            }
        ],
        'hidden': False,
        'label': '',
        'slug': 'f1',
        'type': 'FormQuestion'
    },
    {
        'children': [
            {
                'hidden': False,
                'label': '',
                'slug': 'float-question',
                'type': 'FloatQuestion',
                'value': 0.123
            },
            {
                'choices': [
                    {
                        'checked': False,
                        'label': ''
                    },
                    {
                        'checked': True,
                        'label': ''
                    }
                ],
                'hidden': False,
                'label': '',
                'slug': 'choice-question',
                'type': 'ChoiceQuestion'
            },
            {
                'choices': [
                    {
                        'checked': True,
                        'label': ''
                    },
                    {
                        'checked': True,
                        'label': ''
                    }
                ],
                'hidden': False,
                'label': '',
                'slug': 'choices-question',
                'type': 'MultipleChoiceQuestion'
            },
            {
                'hidden': False,
                'label': '',
                'slug': 'textarea-question',
                'type': 'TextareaQuestion',
                'value': 'a textarea answer'
            },
            {
                'hidden': False,
                'label': '',
                'slug': 'file-question',
                'type': 'FileQuestion'
            },
            {
                'hidden': False,
                'label': '',
                'slug': 'integer-question',
                'type': 'IntegerQuestion',
                'value': 123
            }
        ],
        'hidden': False,
        'label': '',
        'slug': 'f2',
        'type': 'FormQuestion'
    }
]
