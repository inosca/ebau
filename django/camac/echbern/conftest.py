import pytest


@pytest.fixture
def mandatory_answers(db):
    return {
        "beschreibung-bauvorhaben": "test beschreibung",
        "form-name": "Baugesuch",
        "parzelle": [
            {
                "baurecht-nummer": "23",
                "e-grid-nr": "23",
                "lagekoordinaten-nord": "1070500.000",
                "lagekoordinaten-ost": "2480034.0",
                "liegenschaftsnummer": 23,
                "nummer-parzelle": "23",
                "ort-parzelle": "Burgdorf",
                "parzellennummer": "1586",
                "plz-parzelle": 2323,
                "strasse-parzelle": "Teststrasse",
            }
        ],
        "personalien-gesuchstellerin": [
            {
                "e-mail-gesuchstellerin": "test@example.com",
                "juristische-person-gesuchstellerin": "Nein",
                "name-gesuchstellerin": "Testname",
                "nummer-gesuchstellerin": "23",
                "ort-gesuchstellerin": "Burgdorf",
                "plz-gesuchstellerin": 2323,
                "strasse-gesuchstellerin": "Teststrasse",
                "telefon-oder-mobile-gesuchstellerin": "0781234567",
                "vorname-gesuchstellerin": "Testvorname",
            }
        ],
    }
