from faker import Faker


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
    }
