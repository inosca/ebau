# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_sendreminders_caluma 1"] = set(
    [
        (
            "Erinnerung an Aufgaben",
            """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Prof. Brunhild Süßebier B.A."
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."


Freundliche Grüsse
""",
        ),
        (
            "Erinnerung an Aufgaben",
            """Guten Tag


Diese Ihnen unterstehenden Aufgaben wurden noch nicht abgeschlossen.

Überfällige Aufgaben:
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Prof. Brunhild Süßebier B.A."
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."


Freundliche Grüsse
""",
        ),
        (
            "Erinnerung an Aufgaben",
            """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 09.08.2020

---

Diese Ihnen unterstehenden Aufgaben wurden noch nicht abgeschlossen.

Überfällige Aufgaben:
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 09.08.2020

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Prof. Brunhild Süßebier B.A."
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."


Freundliche Grüsse
""",
        ),
        (
            "Erinnerung an Aufgaben",
            """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Überfällige Aufgaben:
 - Aufgabe "Faruk Hoffmann B.Sc." zu erledigen bis 09.08.2020
 - Aufgabe "Hagen Dehmel-Pärtzelt" zu erledigen bis 09.08.2020


Freundliche Grüsse
""",
        ),
        (
            "Erinnerung an Aufgaben",
            """Guten Tag

Dies ist eine Erinnerung an Ihre offenen Aufgaben.

Ungelesene Aufgaben:
 - Aufgabe "Cynthia Barth"
 - Aufgabe "Prof. Brunhild Süßebier B.A."
 - Aufgabe "Dipl.-Ing. Albrecht Schleich B.Sc."


Freundliche Grüsse
""",
        ),
    ]
)
