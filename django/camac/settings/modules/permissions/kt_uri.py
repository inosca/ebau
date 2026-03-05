from camac.permissions.conditions import (
    HasRole,
    RequireInstanceState,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

STATES_ALL_INTERNAL = RequireInstanceState(
    [
        "comm",
        "ext",
        "circ",
        "redac",
        "done",
        "arch",
        "del",
        "nfd",
        "subm",
        "rejected",
        "ext_gem",
        "old",
        "control",
    ]
)

ROLES_INTERNAL = HasRole(
    [
        "Bundesstelle",
        "Gemeinde als Vernehmlassungsstelle",  # TODO: Still needed?
        "Koordinationsstelle Baudirektion BD",
        "Koordinationsstelle Baugesuche BG",
        "Koordinationsstelle Nutzungsplanung NP",
        "Koordinationsstelle Energie AfE",
        "Koordinationsstelle Forst und Jagd AFJ",
        "Koordinationsstelle Landwirtschaft ALA",
        "Koordinationsstelle Sicherheitsdirektion SD",
        "Koordinationsstelle Umwelt AfU",
        "Koordinationsstelle Amt für das Grundbuch AfG",
        "Mitglied der Gemeindebaubehörde",
        "Mitglied einer Kommission oder Fachgruppe",
        "Organisation mit Leseberechtigung",  # TODO: Still needed?
        "Sekretariat der Gemeindebaubehörde",
        "Vernehmlassungsstelle Gemeindezirkulation",
        "Vernehmlassungsstelle mit Koordinationsaufgaben",
        "Vernehmlassungsstelle ohne Koordinationsaufgaben",
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
MODULE_DASHBOARD_READ = STATES_ALL_INTERNAL & ~RequireInstanceState(["subm"])

MODULE_DOCUMENTS_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_FORM = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_HISTORY = STATES_ALL_INTERNAL & ROLES_INTERNAL

# Access level config part
UR_PERMISSIONS_SETTINGS = {
    "ACCESS_LEVELS": {
        "read": [
            ("dashboard-read", MODULE_DASHBOARD_READ),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
        ],
    },
    "ENABLED": True,
    "PERMISSION_MODE": getattr(
        PERMISSION_MODE, env.str("PERMISSION_MODULE_MODE", default="OFF")
    ),
    "EVENT_HANDLER": "camac.permissions.config.kt_ur.PermissionEventHandlerUR",
}
