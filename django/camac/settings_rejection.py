from django.utils.translation import gettext_lazy as _

REJECTION = {
    "default": {
        "INSTANCE_STATE": "rejected",
        "ALLOWED_INSTANCE_STATES": [],
        "HISTORY_ENTRIES": {
            "REJECTED": _("Instance rejected"),
            "REVERTED": _("Instance rejection reverted"),
        },
        "NOTIFICATIONS": {
            "REJECTED": [],
            "REVERTED": [],
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["circulation", "circulation_init"],
        "NOTIFICATIONS": {
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "02-baugesuch-aufgrund-mangel-abweisen-oder-nicht-eintreten-art-18-bewd",
                },
                {
                    "recipient_types": ["inactive_municipality"],
                    "template_slug": "02-rueckweisung-gemeinde",
                },
            ],
            "REVERTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "02-aufhebung-rueckweisung-gesuchsteller",
                },
                {
                    "recipient_types": ["inactive_municipality"],
                    "template_slug": "02-aufhebung-rueckweisung-gemeinde",
                },
            ],
        },
    },
    "test": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["circulation_init"],
    },
}
