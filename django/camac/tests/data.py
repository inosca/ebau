from datetime import date

from faker import Faker

from camac.tests.form_utils import FormUtils


def so_personal_row_factory(
    is_juristic: bool = False,
    has_representation: bool = False,
    is_juristic_representation: bool = False,
) -> dict:
    fake = Faker()
    is_male = fake.pybool()

    data = {
        "juristische-person": "juristische-person-nein",
        "anrede": {
            "value": "anrede-herr" if is_male else "anrede-frau",
            "options": [
                ("anrede-herr", "Herr"),
                ("anrede-frau", "Frau"),
            ],
        },
        "juristische-person-name": None,
        "vertretung-juristische-person": None,
        "vertretung-juristische-person-name": None,
        "vertretung-anrede": None,
        "vertretung-nachname": None,
        "vertretung-vorname": None,
        "vertretung-strasse": None,
        "vertretung-nummer": None,
        "vertretung-plz": None,
        "vertretung-ort": None,
        "vertretung-land": None,
        "vertretung-titel": None,
        "vertretung-telefon": None,
        "vertretung-postfach": None,
        "vertretung-e-mail": None,
        "titel": fake.prefix_male() if is_male else fake.prefix_female(),
        "vorname": fake.first_name_male() if is_male else fake.first_name_female(),
        "nachname": fake.last_name_male() if is_male else fake.last_name_female(),
        "strasse": fake.street_name(),
        "strasse-nummer": fake.building_number(),
        "plz": str(fake.pyint(min_value=1000, max_value=9999)),
        "ort": fake.city(),
        "land": "Schweiz",
        "e-mail": fake.email(),
        "telefon": fake.phone_number(),
        "postfach": str(fake.pyint()),
        "vertretung": "vertretung-nein",
    }

    if is_juristic:
        data.update(
            {
                "juristische-person": "juristische-person-ja",
                "juristische-person-name": fake.company(),
            }
        )

    if has_representation:
        is_male = fake.pybool()

        data.update(
            {
                "vertretung": "vertretung-ja",
                "vertretung-juristische-person": "vertretung-juristische-person-nein",
                "vertretung-anrede": {
                    "value": "vertretung-anrede-herr"
                    if is_male
                    else "vertretung-anrede-frau",
                    "options": [
                        ("vertretung-anrede-herr", "Herr"),
                        ("vertretung-anrede-frau", "Frau"),
                    ],
                },
                "vertretung-titel": fake.prefix_male()
                if is_male
                else fake.prefix_female(),
                "vertretung-vorname": fake.first_name_male()
                if is_male
                else fake.first_name_female(),
                "vertretung-nachname": fake.last_name_male()
                if is_male
                else fake.last_name_female(),
                "vertretung-strasse": fake.street_name(),
                "vertretung-nummer": fake.building_number(),
                "vertretung-plz": fake.pyint(min_value=1000, max_value=9999),
                "vertretung-ort": fake.city(),
                "vertretung-land": "Schweiz",
                "vertretung-e-mail": fake.email(),
                "vertretung-telefon": fake.phone_number(),
                "vertretung-postfach": str(fake.pyint()),
            }
        )

        if is_juristic_representation:
            data.update(
                {
                    "vertretung-juristische-person": "vertretung-juristische-person-ja",
                    "vertretung-juristische-person-name": fake.company(),
                }
            )

    return data


def ag_personal_row_factory(is_juristic: bool = False) -> dict:
    fake = Faker()

    return {
        "name-gesuchstellerin": fake.last_name(),
        "vorname-gesuchstellerin": fake.first_name(),
        "strasse-gesuchstellerin": fake.street_name(),
        "nummer-gesuchstellerin": fake.building_number(),
        "plz-gesuchstellerin": fake.pyint(min_value=1000, max_value=9999),
        "ort-gesuchstellerin": fake.city(),
        "e-mail-gesuchstellerin": fake.email(),
        "telefon-oder-mobile-gesuchstellerin": fake.phone_number(),
        "juristische-person-gesuchstellerin": f"juristische-person-gesuchstellerin-{'ja' if is_juristic else 'nein'}",
        "name-juristische-person-gesuchstellerin": fake.company()
        if is_juristic
        else None,
        "referenznummer": str(fake.pyint(min_value=1000, max_value=9999)),
    }


def sg_personal_row_factory(is_juristic: bool = False) -> dict:
    fake = Faker()

    return {
        "nachname": fake.last_name(),
        "vorname": fake.first_name(),
        "strasse-und-nr": fake.street_address(),
        "plz": str(fake.pyint(min_value=1000, max_value=9999)),
        "ort": fake.city(),
        "land": "Schweiz",
        "e-mail": fake.email(),
        "telefon": fake.phone_number(),
        "postfach": str(fake.pyint()),
        "juristische-person": f"juristische-person-{'ja' if is_juristic else 'nein'}",
        "name-juristische-person": fake.company() if is_juristic else None,
    }


def so_fill_cantonal_exam(document, form_utils: FormUtils):
    form_utils.add_answer(document, "mp-bab-datum-eingang-arp", date(2025, 2, 13))
    form_utils.add_answer(
        document, "mp-bab-terminvorgabe-bei-erfassung", date(2023, 1, 2)
    )
    form_utils.add_answer(
        document, "mp-bab-massgebliche-terminvorgabe", date(2023, 1, 5)
    )
    form_utils.add_answer(
        document,
        "mp-bab-verfahrensstand",
        "mp-bab-verfahrensstand-entscheid",
        label="Entscheid",
    )
    form_utils.add_answer(
        document,
        "mp-bab-bearbeitungsstatus",
        "mp-bab-bearbeitungsstatus-in-bearbeitung",
        label="in Bearbeitung",
    )
    form_utils.add_table_answer(
        document,
        "mp-bab-grund-der-sistierung",
        [
            {
                "mp-bab-sistierungsgrund": {
                    "value": "mp-bab-sistierungsgrund-rechtliches-gehoer",
                    "options": [
                        (
                            "mp-bab-sistierungsgrund-rechtliches-gehoer",
                            "rechtliches Gehör",
                        )
                    ],
                },
                "mp-bab-sistiert-von": date(2020, 1, 1),
                "mp-bab-sistiert-bis": date(2020, 1, 10),
            }
        ],
    )
    form_utils.add_answer(
        document,
        "mp-bab-bewilligungsbehoerde",
        "mp-bab-bewilligungsbehoerde-oertliche-baubehoerde",
        label="örtliche Baubehörde",
    )
    form_utils.add_answer(
        document,
        "mp-bab-interesse-am-vorhaben",
        "mp-bab-interesse-am-vorhaben-privat",
        label="privat",
    )
    form_utils.add_table_answer(
        document,
        "mp-bab-journal-tabelle",
        [
            {
                "mp-bab-datum-eintrag": date(2024, 5, 7),
                "mp-bab-art-des-eintrages": {
                    "value": "mp-bab-art-des-eintrages-info",
                    "options": [("mp-bab-art-des-eintrages-info", "Info")],
                },
                "mp-bab-beteiligte-anwesende": "Beteiligte Anwesende",
                "mp-bab-sachverhalt": "Sachverhalt",
            }
        ],
    )
    form_utils.add_answer(
        document,
        "mp-bab-gemeindenummer-kantonal-arp",
        "1234",
    )
    form_utils.add_answer(
        document,
        "mp-bab-bauzone",
        "mp-bab-bauzone-ausserhalb",
        label="ausserhalb",
    )
    form_utils.add_answer(
        document,
        "mp-bab-objektschutz",
        "mp-bab-objektschutz-geschuetzt",
        label="geschützt",
    )
    form_utils.add_answer(
        document,
        "mp-bab-checkliste-bab-so-nach-rpg",
        [
            "mp-bab-checkliste-bab-so-nach-rpg-a1",
            "mp-bab-checkliste-bab-so-nach-rpg-a2",
        ],
        options=[
            ("mp-bab-checkliste-bab-so-nach-rpg-a1", "A1 - standortgebunden"),
            ("mp-bab-checkliste-bab-so-nach-rpg-a2", "A2 - Weilerzone"),
        ],
    )
    form_utils.add_answer(
        document,
        "mp-bab-entscheid-kanton",
        "mp-bab-entscheid-kanton-ablehnung",
        label="Ablehnung",
    )
    form_utils.add_answer(
        document, "mp-bab-datum-des-entscheides-kanton", date(2025, 7, 8)
    )
    form_utils.add_answer(
        document,
        "mp-bab-eroeffnungsart-des-entscheides-kanton",
        "mp-bab-eroeffnungsart-des-entscheides-kanton-e-mail",
        label="E-Mail",
    )
    form_utils.add_table_answer(
        document,
        "mp-bab-angaben-zur-unterschutzstellung",
        [
            {
                "mp-bab-schutzobjekt-bezeichnung": "Bezeichnung",
                "mp-bab-beschlussnummer": "Beschlussnummer",
                "mp-bab-datum-beschluss": date(2001, 12, 1),
                "mp-bab-datum-verfuegung": date(1999, 9, 1),
                "mp-bab-verfuegende-behoerde": {
                    "value": "mp-bab-verfuegende-behoerde-kantonal",
                    "options": [
                        (
                            "mp-bab-verfuegende-behoerde-kantonal",
                            "kantonal",
                        )
                    ],
                },
            }
        ],
    )
