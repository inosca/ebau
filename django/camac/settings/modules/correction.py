from django.utils.translation import gettext_lazy as _

CORRECTION = {
    "default": {
        "INSTANCE_STATE": "correction",
        "ALLOWED_INSTANCE_STATES": ["subm"],
        "ALLOWED_WITH_PENDING_INQUIRIES": False,
        "HISTORY_ENTRY": _("Dossier corrected"),
    },
    "kt_gr": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            "init-distribution",
            "circulation",
            "decision",
        ],
        "ALLOWED_WITH_PENDING_INQUIRIES": True,
    },
    "kt_so": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            "material-exam",
            "init-distribution",
            "distribution",
        ],
    },
    "kt_ag": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            # TODO verify
            # "init-distribution",
            # "circulation",
        ],
    },
    "kt_bern": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "circulation_init",
            "in_progress",
            "in_progress_internal",
            "circulation",
        ],
    },
    "test": {"ENABLED": True},
}
