PUBLICATION = {
    "default": {
        "BACKEND": "caluma",
        "RANGE_QUESTIONS": [("publikation-startdatum", "publikation-ablaufdatum")],
        "FILL_TASKS": ["fill-publication"],
    },
    "test": {
        "ENABLED": True,
        "BACKEND": "camac-ng",
    },
    "demo": {
        "ENABLED": True,
        "BACKEND": "camac-ng",
    },
    "kt_bern": {
        "ENABLED": True,
        "FILL_TASKS": ["fill-publication", "information-of-neighbors"],
        "SCRUBBED_ANSWERS": [
            "e-mail-energie",
            "e-mail-gastgewerbe",
            "e-mail-gebaeudeeigentuemerin",
            "e-mail-gesuchstellerin",
            "e-mail-gewaesserschutzfragen",
            "e-mail-grundeigentuemerin",
            "e-mail-kontaktperson",
            "e-mail-projektverfasserin",
            "e-mail-sendeanlage",
            "e-mail-vertreterin",
            "e-mail-waermepumpen",
            "telefon-oder-mobile-energie",
            "telefon-oder-mobile-gastgewerbe",
            "telefon-oder-mobile-gebaeudeeigentuemerin",
            "telefon-oder-mobile-gesuchstellerin",
            "telefon-oder-mobile-gewaesserschutzfragen",
            "telefon-oder-mobile-grundeigentuemerin",
            "telefon-oder-mobile-kontaktperson",
            "telefon-oder-mobile-projektverfasserin",
            "telefon-oder-mobile-sendeanlage",
            "telefon-oder-mobile-vertreterin",
            "telefon-oder-mobile-vorabklaerungen",
            "telefon-oder-mobile-waermepumpen",
        ],
    },
    "kt_gr": {
        "ENABLED": True,
        "USE_CALCULATED_DATES": True,
        "RANGE_QUESTIONS": [
            (
                "beginn-publikationsorgan-gemeinde",
                "ende-publikationsorgan-gemeinde",
            ),
            (
                "beginn-publikation-kantonsamtsblatt",
                "ende-publikation-kantonsamtsblatt",
            ),
        ],
        "PUBLISH_QUESTION": "oeffentliche-auflage",
        "PUBLISH_ANSWER": ["oeffentliche-auflage-ja"],
        "SCRUBBED_ANSWERS": [
            "e-mail-gesuchstellerin",
            "telefon-oder-mobile-gesuchstellerin",
        ],
    },
    "kt_so": {
        "ENABLED": True,
        "RANGE_QUESTIONS": [("publikation-start", "publikation-ende")],
        "SCRUBBED_ANSWERS": [
            "e-mail",
            "vertretung-e-mail",
            "telefon",
            "vertretung-telefon",
            "telefon-oder-mobil",
        ],
    },
    "kt_schwyz": {
        "ENABLED": True,
        "BACKEND": "camac-ng",
    },
    "kt_uri": {
        "ENABLED": True,
        "BACKEND": "camac-ng",
    },
}
