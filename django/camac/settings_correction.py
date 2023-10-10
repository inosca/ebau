from django.utils.translation import gettext_lazy as _

CORRECTION = {
    "default": {
        "INSTANCE_STATE": "correction",
        "ALLOWED_INSTANCE_STATES": ["subm"],
        "HISTORY_ENTRY": _("Dossier corrected"),
    },
    "kt_gr": {
        "ENABLED": True,
        "ALLOWED_INSTANCE_STATES": [
            "subm",
            "init-distribution",
            "circulation",
        ],
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
    "test": {"ENABLED": True},
}
