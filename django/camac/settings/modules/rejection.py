from django.utils.translation import gettext_lazy as _

REJECTION = {
    "default": {
        "INSTANCE_STATE": "rejected",
        "ALLOWED_INSTANCE_STATES": [],
        "ALLOW_REVERT": True,
        "INSTANCE_STATE_REJECTION_COMPLETE": "finished",
        "HISTORY_ENTRIES": {
            "REJECTED": _("Instance rejected"),
            "REVERTED": _("Instance rejection reverted"),
            "COMPLETE": _("Instance resubmitted (instance %(dossier_number)s)"),
        },
        "NOTIFICATIONS": {
            "REJECTED": [],
            "REVERTED": [],
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["circulation", "circulation_init"],
        "HISTORY_ENTRIES": {
            "COMPLETE": _("Instance completed by resubmission"),
        },
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
    "kt_gr": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            "init-distribution",
            "circulation",
            "decision",
        ],
        "INSTANCE_STATE_REJECTION_COMPLETE": None,
        "NOTIFICATIONS": {
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "rueckweisung",
                }
            ]
        },
    },
    "kt_so": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["reject"],
        "ALLOW_REVERT": False,
        "INSTANCE_STATE_REJECTION_COMPLETE": None,
        "WORK_ITEM": {
            "TASK": "reject",
            "INSTANCE_STATE": "reject",
            "ON_ANSWER": {
                "formal-exam": (
                    "formelle-pruefung-resultat",
                    "formelle-pruefung-resultat-rueckweisung",
                ),
                "material-exam": (
                    "materielle-pruefung-resultat",
                    "materielle-pruefung-resultat-rueckweisung",
                ),
            },
        },
        "NOTIFICATIONS": {
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "rueckweisung",
                }
            ]
        },
    },
    "test": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["circulation_init"],
    },
}
