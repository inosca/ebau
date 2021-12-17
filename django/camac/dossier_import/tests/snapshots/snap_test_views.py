# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    "test_validation_errors[import-example-validation-errors.zip-kt_schwyz-None-400-Municipality] 1"
] = {
    "errors": [
        {
            'code': 'invalid',
            'detail': 'Kein Standort gesetzt.',
            'source': {
                'pointer': '/data/attributes/non-field-errors'
            },
            'status': '400'
        }
    ]
}

snapshots[
    "test_validation_errors[import-example-validation-errors.zip-kt_schwyz-location-201-Municipality] 1"
] = {
    "created-at": "2021-12-12T01:00:00+01:00",
    "dossier-loader-type": "zip-archive-xlsx",
    "messages": {
        "import": {
            "completed": None,
            "details": [],
            "summary": {
                "error": [],
                "stats": {"documents": 0, "dossiers": 0},
                "warning": [],
            },
        },
        "validation": {
            "completed": "2021-12-12T01:00:00+0100",
            "details": [
                {
                    "details": [
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "submit-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "publication-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "decision-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "construction-start-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "profile-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "final-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "not-a-date",
                            "field": "completion-date",
                            "level": 2,
                        },
                    ],
                    "dossier_id": "2017-84",
                    "status": "error",
                },
                {
                    "details": [
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "submit-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "publication-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "decision-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "construction-start-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "profile-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "final-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1872",
                            "field": "completion-date",
                            "level": 2,
                        },
                        {
                            "code": "status-choice-validation-error",
                            "detail": "DONKED",
                            "field": "status",
                            "level": 3,
                        },
                    ],
                    "dossier_id": "2017-86",
                    "status": "error",
                },
                {
                    "details": [
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "submit-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "publication-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "decision-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "construction-start-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "profile-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "final-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1873",
                            "field": "completion-date",
                            "level": 2,
                        },
                        {
                            "code": "missing-required-field-error",
                            "detail": None,
                            "field": "status",
                            "level": 3,
                        },
                    ],
                    "dossier_id": "2017-87",
                    "status": "error",
                },
                {
                    "details": [
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "submit-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "publication-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "decision-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "construction-start-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "profile-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "final-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1874",
                            "field": "completion-date",
                            "level": 2,
                        },
                    ],
                    "dossier_id": "2017-88",
                    "status": "error",
                },
                {
                    "details": [
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "publication-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "decision-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "construction-start-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "profile-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "final-approval-date",
                            "level": 2,
                        },
                        {
                            "code": "date-field-validation-error",
                            "detail": "22.01.1875",
                            "field": "completion-date",
                            "level": 2,
                        },
                        {
                            "code": "missing-required-field-error",
                            "detail": None,
                            "field": "submit_date",
                            "level": 3,
                        },
                    ],
                    "dossier_id": 9,
                    "status": "error",
                },
            ],
            'summary': {
                'error': [
                    '''1 Dossiers haben einen ungültigen Status. Betroffene Dossiers:
2017-86: 'DONKED' (status)''',
                    '''2 Dossiers fehlt ein Wert in einem zwingenden Feld. Betroffene Dossiers:
2017-87: status,
9: submit_date""",
                ],
                'stats': {
                    'attachments': 4,
                    'dossiers': 0
                },
                'warning': [
                    '''5 Dossiers haben ein ungültiges Datum. Datumsangaben bitte im Format "DD.MM.YYYY" (e.g. "13.04.2021") machen. Betroffene Dossiers:
2017-84: 'not-a-date' (submit-date), 'not-a-date' (publication-date), 'not-a-date' (decision-date), 'not-a-date' (construction-start-date), 'not-a-date' (profile-approval-date), 'not-a-date' (final-approval-date), 'not-a-date' (completion-date),
2017-86: '22.01.1872' (submit-date), '22.01.1872' (publication-date), '22.01.1872' (decision-date), '22.01.1872' (construction-start-date), '22.01.1872' (profile-approval-date), '22.01.1872' (final-approval-date), '22.01.1872' (completion-date),
2017-87: '22.01.1873' (submit-date), '22.01.1873' (publication-date), '22.01.1873' (decision-date), '22.01.1873' (construction-start-date), '22.01.1873' (profile-approval-date), '22.01.1873' (final-approval-date), '22.01.1873' (completion-date),
2017-88: '22.01.1874' (submit-date), '22.01.1874' (publication-date), '22.01.1874' (decision-date), '22.01.1874' (construction-start-date), '22.01.1874' (profile-approval-date), '22.01.1874' (final-approval-date), '22.01.1874' (completion-date),
9: '22.01.1875' (publication-date), '22.01.1875' (decision-date), '22.01.1875' (construction-start-date), '22.01.1875' (profile-approval-date), '22.01.1875' (final-approval-date), '22.01.1875' (completion-date)''',
                    '4 Dossiers ohne Dokumentenverzeichnis.'
                ]
            }
        }
    },
    "mime-type": None,
    "status": "failed",
}
