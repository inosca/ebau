# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_notify_completed_work_item[True-kt_bern] 1"] = [
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Univ.Prof. Janos Hartung B.Eng." zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["shannon92@yahoo.com"],
        [],
    ),
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Univ.Prof. Janos Hartung B.Eng." zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["larrysmith@cortez.com"],
        [],
    ),
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Univ.Prof. Janos Hartung B.Eng." zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["toddprice@yahoo.com"],
        [],
    ),
]

snapshots["test_notify_completed_work_item[True-kt_schwyz] 1"] = [
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Axel Roskoth" zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["josephwagner@hotmail.com"],
        [],
    ),
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Axel Roskoth" zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["carolyn82@davis.biz"],
        [],
    ),
    (
        "Abgeschlossene Aufgabe",
        """Guten Tag

Eine Ihrer verantwortlichen Aufgaben wurden abgeschlossen:
Aufgabe "Axel Roskoth" zu erledigen bis 11.08.2020
Abgeschlossen von User Admin (admin@example.com)

Freundliche Grüsse
""",
        ["kpark@simmons.net"],
        [],
    ),
]
