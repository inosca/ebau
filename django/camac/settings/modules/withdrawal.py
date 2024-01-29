from django.utils.translation import gettext_lazy as _

WITHDRAWAL = {
    "default": {
        "INSTANCE_STATE": "withdrawal",
        "INSTANCE_STATE_CONFIRMED": "withdrawn",
        "ALLOWED_INSTANCE_STATES": [],
        "PROCESS_WORK_ITEMS": [],
        "HISTORY_ENTRIES": {
            "REQUESTED": _("Instance withdrawn"),
            "CONFIRMED": _("Withdrawal confirmed"),
        },
        "NOTIFICATIONS": [],
    },
    "kt_so": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            "material-exam",
            "init-distribution",
            "distribution",
            "decision",
        ],
        "PROCESS_WORK_ITEMS": [
            # Exams
            ("formal-exam", "skip"),
            ("material-exam", "skip"),
            # Distribution
            ("complete-distribution", "complete"),
            # Additional demands
            ("init-additional-demand", "cancel"),
            ("additional-demand", "cancel"),
            # Publication
            ("create-publication", "cancel"),
            ("fill-publication", "cancel"),
            ("publication", "cancel"),
        ],
        "NOTIFICATIONS": [
            {
                "template_slug": "rueckzug",
                "recipient_types": ["leitbehoerde", "involved_in_distribution"],
            }
        ],
    },
    "test": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": ["subm"],
    },
}
