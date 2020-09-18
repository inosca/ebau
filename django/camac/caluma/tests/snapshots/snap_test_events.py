# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_notify_completed_work_item[True-kt_bern] 1'] = [
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Univ.Prof. Janos Hartung B.Eng." im Dossier 2020-01 (1) wurde von User Admin (Stacey Fields) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Univ.Prof. Janos Hartung B.Eng." dans le dossier 2020-01 (1) a été terminée par User Admin (Stacey Fields).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
''',
        [
            'shannon92@yahoo.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Univ.Prof. Janos Hartung B.Eng." im Dossier 2020-01 (1) wurde von User Admin (Stacey Fields) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Univ.Prof. Janos Hartung B.Eng." dans le dossier 2020-01 (1) a été terminée par User Admin (Stacey Fields).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
''',
        [
            'larrysmith@cortez.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Univ.Prof. Janos Hartung B.Eng." im Dossier 2020-01 (1) wurde von User Admin (Stacey Fields) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Univ.Prof. Janos Hartung B.Eng." dans le dossier 2020-01 (1) a été terminée par User Admin (Stacey Fields).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
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
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Axel Roskoth" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'josephwagner@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Axel Roskoth" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'carolyn82@davis.biz'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Axel Roskoth" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'kpark@simmons.net'
        ],
        [
        ]
    )
]
