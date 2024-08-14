from camac.permissions.conditions import (
    HasRole,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

STATES_ALL_INTERNAL = RequireInstanceState(
    [
        "subm",
        "comm",
        "nfd",
        "circ",
        "redac",
        "done",
        "construction-monitoring",
        "instance-completed",
        "arch",
        "stopped",
        "internal",
    ]
)

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state / work item rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_COMMUNICATIONS = STATES_ALL_INTERNAL & ~HasRole(["readonly"])

MODULE_DISTRIBUTION = RequireWorkItem("distribution")

MODULE_DOCUMENT = STATES_ALL_INTERNAL

MODULE_FORM = STATES_ALL_INTERNAL

MODULE_INTEGRITY_DASHBOARD = STATES_ALL_INTERNAL & ~RequireInstanceState(["subm"])


# Access level config part
SZ_PERMISSIONS_SETTINGS = {
    "ACCESS_LEVELS": {
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("documents-read", MODULE_DOCUMENT),
            ("form-read", MODULE_FORM),
            ("integrity-dashboard-read", MODULE_INTEGRITY_DASHBOARD),
        ],
    },
    "ENABLED": True,
    "ENABLE_CACHE": env.bool("PERMISSION_MODULE_ENABLE_CACHE", default=True),
    "PERMISSION_MODE": getattr(
        PERMISSION_MODE, env.str("PERMISSION_MODULE_MODE", default="OFF")
    ),
}
