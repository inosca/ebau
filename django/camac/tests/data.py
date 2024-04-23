from faker import Faker


def so_personal_row_factory(
    is_juristic: bool = False,
    has_representation: bool = False,
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
        "vorname": fake.first_name_male() if is_male else fake.first_name_female(),
        "nachname": fake.last_name_male() if is_male else fake.last_name_female(),
        "strasse": fake.street_name(),
        "strasse-nummer": fake.building_number(),
        "plz": fake.pyint(min_value=1000, max_value=9999),
        "ort": fake.city(),
        "land": "Schweiz",
        "e-mail": fake.email(),
        "telefon": fake.phone_number(),
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
                "vertretung-anrede": {
                    "value": "vertretung-anrede-herr"
                    if is_male
                    else "vertretung-anrede-frau",
                    "options": [
                        ("vertretung-anrede-herr", "Herr"),
                        ("vertretung-anrede-frau", "Frau"),
                    ],
                },
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
            }
        )

    return data
