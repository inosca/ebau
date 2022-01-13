# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_send_work_item_reminders[False-False-True-False-0-False] 1'] = [
]

snapshots['test_send_work_item_reminders[False-False-True-False-0-True] 1'] = [
]

snapshots['test_send_work_item_reminders[False-True-False-False-1-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Jeffrey Zhang) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[False-True-False-False-1-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Jason Dickerson) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Derek Wagner) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[False-True-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Jeffrey Zhang) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[False-True-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour  Rebecca Gonzalez,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Jason Dickerson) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Derek Wagner) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-False-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Jeffrey Zhang) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-False-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour  Rebecca Gonzalez,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 0 tâches de contrôle non lues

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Jason Dickerson) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Derek Wagner) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 0 tâches de contrôle non lues
- 0 tâches en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-True-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Jeffrey Zhang) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-True-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour  Rebecca Gonzalez,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Jason Dickerson) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Derek Wagner) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-True-True-True-3-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Jeffrey Zhang) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation (Maria Fuentes) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 0 ungelesene Aufgaben
- 1 überfällige Controlling-Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.
''',
        [
            'calebsoto@example.net'
        ],
        [
        ]
    )
]

snapshots['test_send_work_item_reminders[True-True-True-True-3-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag  Rebecca Gonzalez

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour  Rebecca Gonzalez,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'fmalone@example.org'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Jason Dickerson) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Derek Wagner) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'nicolefields@example.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation (Kayla Ruiz) hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 0 ungelesene Aufgaben
- 1 überfällige Controlling-Aufgabe

http://camac-ng.local

Diese E-Mail wurde automatisch generiert, bitte antworten Sie nicht darauf.

*** version française ***

Bonjour,

Votre organisation (Brandi Vargas) a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 0 tâches de contrôle non lues
- 1 tâche en retard

http://camac-ng.local

Ce message a été généré automatiquement, veuillez ne pas y répondre.
''',
        [
            'calebsoto@example.net'
        ],
        [
        ]
    )
]
