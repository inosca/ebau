APPEAL = {
    "default": {},
    "kt_bern": {
        "ENABLED": True,
        "ROW_FORM": "appeal-form",
        "INSTANCE_STATES_AFTER_DECISION": ["sb1", "finished"],
        "QUESTIONS": {
            "TABLE": "appeal-table",
            "TYPE": "appeal-type",
            "AUTHORITY": "appeal-authority",
            "DATE": "appeal-date",
            "DECISION": "decision-decision-assessment",
        },
        "ANSWERS": {
            "TYPE": {
                "DEADLINE": "appeal-type-frist-der-stellungnahme",
            },
            "AUTHORITY": {
                "LEGAL_DEPARTEMENT": "appeal-authority-rechtsamt",
            },
            "DECISION": {
                "CONFIRMED": "decision-decision-assessment-appeal-confirmed",
                "CHANGED": "decision-decision-assessment-appeal-changed",
                "REJECTED": "decision-decision-assessment-appeal-rejected",
            },
        },
        "NOTIFICATIONS": {
            "APPEAL_SUBMITTED": [
                {
                    "template_slug": "09-beschwerde-eingegangen",
                    "recipient_types": [
                        "applicant",  # Gesuchsteller/innen
                        "involved_in_distribution",  # Involvierte Stellen in Zirkulation
                        "construction_control",  # Baukontrolle
                        "geometer_acl_services",
                    ],
                }
            ],
            "APPEAL_DECISION": [
                {
                    "template_slug": "09-entscheid-nach-dem-beschwerdeverfahren",
                    "recipient_types": [
                        "applicant",  # Gesuchsteller/innen
                        "involved_in_distribution",  # Involvierte Stellen in Zirkulation
                    ],
                },
            ],
        },
    },
    "kt_so": {
        "ENABLED": True,
        "INSTANCE_STATES_AFTER_DECISION": ["construction-monitoring", "finished"],
        "QUESTIONS": {
            "TABLE": "beschwerde-tabelle",
            "TYPE": "beschwerdetyp",
            "AUTHORITY": "beschwerdeinstanz",
            "DATE": "entscheid-datum",
            "DECISION": "entscheid-entscheid",
        },
        "ANSWERS": {
            "TYPE": {
                "DEADLINE": "beschwerdetyp-frist-der-stellungnahme",
            },
            "AUTHORITY": {
                "LEGAL_DEPARTEMENT": "beschwerdeinstanz-bjd",
            },
            "DECISION": {
                "CONFIRMED": "entscheid-entscheid-beschwerde-bestaetigt",
                "CHANGED": "entscheid-entscheid-beschwerde-geaendert",
                "REJECTED": "entscheid-entscheid-beschwerde-zurueckgewiesen",
            },
        },
        "NOTIFICATIONS": {
            "APPEAL_SUBMITTED": [
                {
                    "template_slug": "beschwerde",
                    "recipient_types": [
                        "applicant",  # Gesuchsteller/innen
                        "involved_in_distribution",  # Involvierte Stellen in Zirkulation
                    ],
                }
            ],
        },
    },
}
