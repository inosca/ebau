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
        "ROLES_WITH_APPLICANT_CONTACT": ["active_or_involved_lead_authority"],
    },
    "kt_bern": {
        "ENABLED": True,
    },
    "kt_gr": {
        "ENABLED": True,
        "DOSSIER_NUMBER_ANNOTATION": F("instance__case__meta__dossier-number"),
        "ROLES_WITH_APPLICANT_CONTACT": [
            "active_or_involved_lead_authority",
            "service",
        ],
    },
    "kt_so": {
        "ENABLED": True,
        "DOSSIER_NUMBER_ANNOTATION": F("instance__case__meta__dossier-number"),
        "ROLES_WITH_APPLICANT_CONTACT": [
            "active_or_involved_lead_authority",
            "service",
        ],
    },
    "kt_schwyz": {
        "ENABLED": True,
    },
    "demo": {
        "ENABLED": True,
    },
    "test": {
        "ENABLED": True,
    },
}
