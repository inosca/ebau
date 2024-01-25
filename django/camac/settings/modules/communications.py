COMMUNICATIONS = {
    "default": {
        "NOTIFICATIONS": {
            "APPLICANT": {"template_slug": "communications-new-message"},
            "INTERNAL_INVOLVED_ENTITIES": {
                "template_slug": "communications-new-message-internal"
            },
            "DOSSIER_NUMBER_LOOKUP": lambda instance: instance.case.meta.get(
                "ebau-number"
            ),
        },
    },
    "kt_bern": {
        "ENABLED": True,
    },
    "demo": {
        "ENABLED": True,
    },
    "test": {
        "ENABLED": True,
    },
}
