PLACEHOLDERS = {
    "default": {
        "KEEP_TECHNICAL_KEY": True,
        "LEGAL_SUBMISSIONS": {
            "FORM": "legal-submission-form",
            "LEGAL_CLAIMANTS_TABLE_QUESTION": "legal-submission-legal-claimants-table-question",
        },
        "PERSON_MAPPING": {
            "IS_JURISTIC": "juristische-person-gesuchstellerin",
            "IS_JURISTIC_YES": "juristische-person-gesuchstellerin-ja",
            "JURISTIC_NAME": "name-juristische-person-gesuchstellerin",
            "FIRST_NAME": "vorname-gesuchstellerin",
            "LAST_NAME": "name-gesuchstellerin",
            "STREET": "strasse-gesuchstellerin",
            "STREET_NUMBER": "nummer-gesuchstellerin",
            "ZIP": "plz-gesuchstellerin",
            "TOWN": "ort-gesuchstellerin",
        },
    },
    "kt_so": {
        "ENABLED": True,
        "KEEP_TECHNICAL_KEY": False,
        "LEGAL_SUBMISSIONS": {
            "FORM": "einsprache",
            "LEGAL_CLAIMANTS_TABLE_QUESTION": "einsprache-einsprechende",
        },
        "PERSON_MAPPING": {
            "IS_JURISTIC": "juristische-person",
            "IS_JURISTIC_YES": "juristische-person-ja",
            "JURISTIC_NAME": "juristische-person-name",
            "FIRST_NAME": "vorname",
            "LAST_NAME": "nachname",
            "STREET": "strasse",
            "STREET_NUMBER": "strasse-nummer",
            "ZIP": "plz",
            "TOWN": "ort",
        },
    },
    "kt_bern": {"ENABLED": True},
    "kt_gr": {"ENABLED": True},
    "test": {"ENABLED": True},
}
