# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_notify_completed_work_item[True-kt_bern] 1'] = [
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Reinhart Mülichen" im Dossier 2020-01 (1) wurde von User Admin (Mark Ware) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Reinhart Mülichen" dans le dossier 2020-01 (1) a été terminée par User Admin (Mark Ware).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
''',
        [
            'dennis93@wilson.info'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Reinhart Mülichen" im Dossier 2020-01 (1) wurde von User Admin (Mark Ware) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Reinhart Mülichen" dans le dossier 2020-01 (1) a été terminée par User Admin (Mark Ware).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
''',
        [
            'nthomas@joseph.org'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (eBau-Nr. 2020-01 (1)) / tâche complétée (n° eBau 2020-01 (1))',
        '''Guten Tag

Die Aufgabe "Reinhart Mülichen" im Dossier 2020-01 (1) wurde von User Admin (Mark Ware) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.

*** version française ***

Bonjour,

La tâche "Reinhart Mülichen" dans le dossier 2020-01 (1) a été terminée par User Admin (Mark Ware).

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
''',
        [
            'shaffersuzanne@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_notify_completed_work_item[True-kt_schwyz] 1'] = [
    (
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Wanda Faust" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'carrollgabriella@horne-park.info'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Wanda Faust" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'elijahpeters@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Aufgabe abgeschlossen (Dossier-Nr. 1)',
        '''Guten Tag

Die Aufgabe "Wanda Faust" im Dossier 1 wurde von User Admin (Rebecca Gonzalez) abgeschlossen.

http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
''',
        [
            'acostaandrew@carter.com'
        ],
        [
        ]
    )
]
