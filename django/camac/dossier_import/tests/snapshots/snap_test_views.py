# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_validation_errors[import-example-validation-errors.zip-Municipality] 1'] = {
    'import': {
        'completed': None,
        'details': [
        ],
        'summary': {
            'dossiers_error': {
            },
            'dossiers_success': 0,
            'dossiers_warning': {
            },
            'dossiers_written': 0,
            'errors': [
            ],
            'num_documents': 0,
            'warnings': [
            ]
        }
    },
    'validation': {
        'completed': '2021-12-01T16:30:48+0100',
        'details': [
            {
                'details': [
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'submit-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'publication-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'decision-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'construction-start-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'profile-approval-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'final-approval-date',
                        'level': 2
                    },
                    {
                        'code': 'field-validation-error',
                        'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                        'field': 'completion-date',
                        'level': 2
                    }
                ],
                'dossier_id': '2017-84',
                'instance_id': None,
                'status': 'error'
            }
        ],
        'summary': {
            'dossiers_error': {
            },
            'dossiers_success': 0,
            'dossiers_warning': {
                'field-validation-error': {
                    'code': 'field-validation-error',
                    'data': [
                        '2017-84'
                    ],
                    'detail': [
                        {
                            'details': [
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'submit-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'publication-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'decision-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'construction-start-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'profile-approval-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'final-approval-date',
                                    'level': 2
                                },
                                {
                                    'code': 'field-validation-error',
                                    'detail': 'not-a-date could not be parsed as date. Allowed format: dd.mm.YYYY',
                                    'field': 'completion-date',
                                    'level': 2
                                }
                            ],
                            'dossier_id': '2017-84',
                            'instance_id': None,
                            'status': 'error'
                        }
                    ],
                    'level': 2
                }
            },
            'dossiers_without_attachments': 0,
            'dossiers_written': 0,
            'errors': [
            ],
            'missing_metadata': [
            ],
            'num_documents': 4,
            'warnings': [
            ]
        }
    }
}
