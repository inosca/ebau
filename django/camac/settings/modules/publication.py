PUBLICATION = {
    "default": {
        "BACKEND": "caluma",
        "RANGE_QUESTIONS": {
            "PUBLIC": [],
            "NEIGHBORS": [],
        },
        "FILL_TASKS": {
            "PUBLIC": "fill-publication",
            "NEIGHBORS": "fill-information-of-neighbors",
        },
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
        "FILL_TASKS": {"NEIGHBORS": "information-of-neighbors"},
        "RANGE_QUESTIONS": {
            "PUBLIC": [("publikation-startdatum", "publikation-ablaufdatum")],
            "NEIGHBORS": [
                (
                    "information-of-neighbors-start-date",
                    "information-of-neighbors-end-date",
                )
            ],
        },
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
        "RANGE_QUESTIONS": {
            "PUBLIC": [
                (
                    "beginn-publikationsorgan-gemeinde",
                    "ende-publikationsorgan-gemeinde",
                ),
                (
                    "beginn-publikation-kantonsamtsblatt",
                    "ende-publikation-kantonsamtsblatt",
                ),
            ]
        },
        "PUBLISH_QUESTION": "oeffentliche-auflage",
        "PUBLISH_ANSWER": ["oeffentliche-auflage-ja"],
        "SCRUBBED_ANSWERS": [
            "e-mail-gesuchstellerin",
            "telefon-oder-mobile-gesuchstellerin",
        ],
        "AFTER_FORMAL_EXAM_PUBLICATION_TASKS": [
            "fill-publication",
            "publication",
            "distribution",
        ],
    },
    "kt_so": {
        "ENABLED": True,
        "RANGE_QUESTIONS": {
            "PUBLIC": [("publikation-start", "publikation-ende")],
        },
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
    "kt_ag": {
        "ENABLED": True,
        "RANGE_QUESTIONS": {
            "PUBLIC": [
                (
                    "beginn-publikationsorgan-gemeinde",
                    "ende-publikationsorgan-gemeinde",
                ),
                (
                    "beginn-publikation-kantonsamtsblatt",
                    "ende-publikation-kantonsamtsblatt",
                ),
            ],
            "NEIGHBORS": [
                ("nachbarschaftsorientierung-beginn", "nachbarschaftsorientierung-ende")
            ],
        },
        "PUBLISH_QUESTION": "oeffentliche-auflage",
        "PUBLISH_ANSWER": ["oeffentliche-auflage-ja"],
        "SCRUBBED_ANSWERS": [
            "e-mail-gesuchstellerin",
            "telefon-oder-mobile-gesuchstellerin",
        ],
    },
}
