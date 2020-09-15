# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_notify_completed_work_item[True-kt_bern] 1'] = [
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Univ.Prof. Janos Hartung B.Eng. im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'shannon92@yahoo.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Univ.Prof. Janos Hartung B.Eng. im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'larrysmith@cortez.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Univ.Prof. Janos Hartung B.Eng. im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'toddprice@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_notify_completed_work_item[True-kt_schwyz] 1'] = [
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Axel Roskoth im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'josephwagner@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Axel Roskoth im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'carolyn82@davis.biz'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. None)',
        '''Guten Tag

Die Aufgabe Axel Roskoth im Dossier None wurde von User Admin  abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/None

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'kpark@simmons.net'
        ],
        [
        ]
    )
]
