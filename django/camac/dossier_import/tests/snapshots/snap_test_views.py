# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['test_validation_errors[import-example-validation-errors.zip-kt_schwyz-None-400-Municipality] 1'] = {
    'errors': [
        {
            'code': 'required-location-missing',
            'detail': 'Invalid input.',
            'source': {
                'pointer': '/data/attributes/non-field-errors'
            },
            'status': '400'
        }
    ]
}

snapshots['test_validation_errors[import-example-validation-errors.zip-kt_schwyz-location-201-Municipality] 1'] = {
    'data': {
        'attributes': {
            'created-at': '2021-12-12T01:00:00+01:00',
            'dossier-loader-type': 'zip-archive-xlsx',
            'messages': {
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
                    'completed': '2021-12-12T01:00:00+0100',
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
            },
            'mime-type': None,
            'source-file': None,
            'status': 'failed'
        },
        'id': '3c3138f9-beb4-4d1b-b044-3c9044544a07',
        'relationships': {
            'group': {
                'data': {
                    'id': '1034',
                    'type': 'groups'
                }
            },
            'location': {
                'data': {
                    'id': '1034',
                    'type': 'locations'
                }
            },
            'service': {
                'data': {
                    'id': '1036',
                    'type': 'services'
                }
            },
            'user': {
                'data': {
                    'id': '1596',
                    'type': 'users'
                }
            }
        },
        'type': 'dossier-imports'
    }
}
