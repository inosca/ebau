from django.db.models import F

COMMUNICATIONS = {
    "default": {
        "NOTIFICATIONS": {
            "APPLICANT": {"template_slug": "communications-new-message"},
            "INTERNAL_INVOLVED_ENTITIES": {
                "template_slug": "communications-new-message-internal"
            },
        },
        "DOSSIER_NUMBER_ANNOTATION": F("instance__case__meta__ebau-number"),
    },
    "kt_bern": {
        "ENABLED": True,
    },
    "kt_gr": {
        "ENABLED": True,
        "DOSSIER_NUMBER_ANNOTATION": F("instance__case__meta__dossier-number"),
    },
    "kt_so": {
        "ENABLED": True,
        "DOSSIER_NUMBER_ANNOTATION": F("instance__case__meta__dossier-number"),
    },
    "demo": {
        "ENABLED": True,
    },
    "test": {
        "ENABLED": True,
    },
}
