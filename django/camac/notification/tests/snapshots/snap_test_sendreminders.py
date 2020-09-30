# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_sendreminders_caluma[True-True-True-True-3-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

*** version française ***

Bonjour,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 0 ungelesene Aufgaben
- 1 überfällige Controlling-Aufgabe

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 0 tâches de contrôle non lues
- 1 tâche en retard

http://camac-ng.local
''',
        [
            'stonecaleb@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[True-True-True-True-3-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 0 ungelesene Aufgaben
- 1 überfällige Controlling-Aufgabe

http://camac-ng.local
''',
        [
            'stonecaleb@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[True-True-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local

*** version française ***

Bonjour,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[True-True-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[True-False-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 1 tâche de contrôle en retard
- 0 tâches de contrôle non lues

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 1 tâche de contrôle en retard
- 0 tâches de contrôle non lues
- 0 tâches en retard

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[True-False-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 1 überfällige Aufgabe
- 0 ungelesene Aufgaben
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[False-True-True-False-2-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe

http://camac-ng.local

*** version française ***

Bonjour,

Vous avez les tâches suivantes dans eBau qui requièrent votre attention :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[False-True-True-False-2-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Sie haben folgende Aufgaben in eBau, welche Ihre Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe

http://camac-ng.local
''',
        [
            'cmiller@hotmail.com'
        ],
        [
        ]
    ),
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[False-True-False-False-1-True] 1'] = [
    (
        'Erinnerung an Aufgaben / Rappel des tâches',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local

*** version française ***

Bonjour,

Votre organisation a les tâches suivantes dans eBau qui requièrent une attention particulière :

- 0 tâches de contrôle en retard
- 1 tâche de contrôle non lue
- 0 tâches en retard

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[False-True-False-False-1-False] 1'] = [
    (
        'Erinnerung an Aufgaben',
        '''Guten Tag

Ihre Organisation hat folgende Aufgaben in eBau, welche Aufmerksamkeit benötigen:

- 0 überfällige Aufgaben
- 1 ungelesene Aufgabe
- 0 überfällige Controlling-Aufgaben

http://camac-ng.local
''',
        [
            'rfields@yahoo.com'
        ],
        [
        ]
    )
]

snapshots['test_sendreminders_caluma[False-False-True-False-0-True] 1'] = [
]

snapshots['test_sendreminders_caluma[False-False-True-False-0-False] 1'] = [
]
