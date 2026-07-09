from camac.permissions.conditions import (
    Always,
    HasRole,
    RequireInstanceState,
    RequireRunningCase,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

STATES_ALL_INTERNAL = RequireInstanceState(
    [
        # building permit
        "subm",  # Eingereicht
        "comm",  # Von Leitbehörde angenommen
        "nfd",  # Nachforderung
        "circ",  # In Zirkulation
        "redac",  # Bauentscheid ausstehend
        "done",  # Entschieden
        "construction-monitoring",  # Im Baubegleitungsprozess
        "instance-completed",  # Verfahren abgeschlossen
        "arch",  # Archiviert
        "stopped",  # Abgeschrieben
        # internal instances
        "internal",  # Internes Dossier
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

MODULE_WORK_ITEMS = STATES_ALL_INTERNAL


# Access level config part
#
# Note: For SZ we currently use additional `…-view` permissions that are only
# used for determining whether or not to show the corresponding instance
# resources (IRs).
#
# The reason for this is that SZ uses camac-ng forms, so we need to keep a
# separate IR tree for building permits and internal instances. But the
# currently active resource is actually irrelevant for the visibility behaviour
# of an IR, so e.g. two 'Documents' IRs (once on each of the trees) would show
# up in both types of instances, essentially leading to duplicate 'Documents'
# tabs.
#
# To avoid that, we now conceptually distinguish between `…-read` permissions
# (to control the module behaviour) and `…-view` permissions (to exclusively
# control the visibility of the IR). This allows using the same modules in two
# different IRs with correct visibility behaviour.
#
# Once SZ has switched to Caluma-based forms, we will no longer need two
# separate instance resource trees, and then we can get rid of the `…-view`
# permissions again.

SZ_PERMISSIONS_SETTINGS = {
    "ACCESS_LEVELS": {
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("documents-view", MODULE_DOCUMENT),
            ("documents-read", MODULE_DOCUMENT),
            ("form-view", MODULE_FORM),
            ("form-read", MODULE_FORM),
            ("integrity-dashboard-read", MODULE_INTEGRITY_DASHBOARD),
        ],
        "rpg2-demolition-premium-service": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("documents-view", MODULE_DOCUMENT),
            ("documents-read", MODULE_DOCUMENT),
            ("form-view", MODULE_FORM),
            ("form-read", MODULE_FORM),
            ("integrity-dashboard-read", MODULE_INTEGRITY_DASHBOARD),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "are-service": [
            ("form-view-internal", Always()),
            ("form-read", Always()),
            ("form-write", RequireRunningCase()),
            ("documents-view-internal", Always()),
            ("documents-read", Always()),
            ("documents-write", RequireRunningCase()),
            ("work-items-view-internal", Always()),
            ("work-items-read", Always()),
            ("journal-view-internal", Always()),
            ("journal-read", Always()),
            ("journal-write", Always()),
        ],
    },
    "ENABLED": True,
    "PERMISSION_MODE": getattr(
        PERMISSION_MODE, env.str("PERMISSION_MODULE_MODE", default="OFF")
    ),
    "EVENT_HANDLER": "camac.permissions.config.kt_sz.PermissionEventHandlerSZ",
}
