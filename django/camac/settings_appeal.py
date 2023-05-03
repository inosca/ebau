APPEAL = {
    "default": {},
    "kt_bern": {
        "ENABLED": True,
        "ROW_FORM": "appeal-form",
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
    },
}
