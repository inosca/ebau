from django.db.models import Q

from camac.permissions.conditions import (
    Always,
    HasRole,
    IsAppeal,
    RequireInstanceState,
)
from camac.permissions.switcher import PERMISSION_MODE

STATES_ALL_INTERNAL = RequireInstanceState(
    [
        # building permit
        "subm",  # eBau-Nummer vergeben
        "circulation_init",  # Zirkulation initialisieren
        "circulation",  # In Zirkulation
        "coordination",  # In Koordination
        "sb1",  # Selbstdeklaration (SB1)
        "sb2",  # Abschluss (SB2)
        "conclusion",  # Zum Abschluss
        "finished",  # Abgeschlossen
        "rejected",  # Zurückgewiesen
        "correction",  # In Korrektur
        "corrected",  # Korrigiert von Leitbehörde - TODO: still needed?
        "archived",  # Archiviert
        # preliminary clarification
        "evaluated",  # Beurteilung abgeschlossen
        # special procedures
        "in_progress",  # In Bearbeitung
        "in_progress_internal",  # In Bearbeitung (intern)
        "finished_internal",  # Abgeschlossen (intern)
    ]
)

# Internal roles that have access to instances
ROLES_INTERNAL = HasRole(
    [
        "municipality-lead",
        "municipality-clerk",
        "municipality-readonly",
        "service-lead",
        "service-clerk",
        "service-readonly",
        "construction-control-lead",
        "construction-control-clerk",
        "construction-control-readonly",
        "geometer-lead",
        "geometer-clerk",
        "geometer-readonly",
        "subservice",
        "support",
    ]
)

ROLES_INTERNAL_NO_READONLY = ROLES_INTERNAL & ~HasRole(
    [
        "municipality-readonly",
        "service-readonly",
        "construction-control-readonly",
        "geometer-readonly",
    ]
)

MODULE_FORM = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_DOCUMENTS_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_DOCUMENTS_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_HISTORY = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_COMMUNICATIONS_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_COMMUNICATIONS_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES = RequireInstanceState(
    [
        "sb1",
        "sb2",
        "conclusion",
        "finished",
    ]
)

BE_MUNICIPALITY_ACCESSIBLE_STATES = RequireInstanceState(
    [
        "rejected",
        "subm",
        "circulation_init",
        "circulation",
        "coordination",
        "archived",
        "evaluated",
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        "in_progress",
        "in_progress_internal",
        "finished_internal",
    ]
)
BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED = (
    BE_MUNICIPALITY_ACCESSIBLE_STATES
    & ~RequireInstanceState(
        ["in_progress", "in_progress_internal", "subm", "finished_internal"]
    )
)

BE_SERVICE_STATES_DEFAULT = RequireInstanceState(
    [
        "circulation",
        "coordination",
        "evaluated",
        "sb1",
        "sb2",
        "conclusion",
        "rejected",
        "finished",
        "archived",
        "in_progress",
        "in_progress_internal",
        "finished_internal",
    ]
)

BE_CONSTRUCTION_CONTROL_STATES = RequireInstanceState(
    [
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        "archived",
        "in_progress_internal",
        "finished_internal",
    ]
)

POST_DECISION_STATES = RequireInstanceState(
    [
        "evaluated",
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        "archived",
        "finished_internal",
    ]
)

BE_REJECTION_POSSIBLE_STATES = RequireInstanceState(
    ["rejected", "circulation_init", "circulation"]
)
BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES = RequireInstanceState(
    ["sb1", "sb2", "conclusion", "finished", "archived", "finished_internal"]
)
BE_CONSTRUCTION_CONTROL_PERMISSIONS = [
    ("history-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("documents-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("dms-generate-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("responsibilities-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("decision-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    (
        # TODO is this a bug in the configuration or why does this differ
        # from all the other construction control permissions?
        "construction-control-read",
        BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES
        & ~RequireInstanceState(["finished_internal", "archived", "finished"]),
    ),
    ("journal-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("changelog-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("form-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("work-items-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("communications-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
]

# Support always has access to instance (and (almost?) all IRs on it)
SUPPORT_CONDITION = Always()

BE_INVOLVED_LEAD_AUTHORITY_PERMISSIONS = [
    ("communications-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("geometer-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("responsible-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("journal-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("history-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-read-any", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-grant-applicant", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-grant-geometer", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("construction-control-read", BE_CONSTRUCTION_CONTROL_STATES),
    (
        "lead-authority-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["in_progress"]),
    ),
    (
        "additional-demands-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["in_progress"]),
    ),
    (
        "appeal-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        & ~RequireInstanceState(
            [
                "in_progress",
                "in_progress_internal",
                "subm",
                "finished_internal",
            ]
        ),
    ),
    ("related-gwr-projects-read", BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED),
    ("billing-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    (
        "information-of-neighbors-read",
        BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED,
    ),
    ("publication-read", BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED),
    (
        "decision-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        & ~RequireInstanceState(
            ["circulation", "circulation_init", "rejected", "subm"]
        ),
    ),
    (
        "revisionhistory-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES | RequireInstanceState(["correction"]),
    ),
    ("rejection-read", BE_REJECTION_POSSIBLE_STATES),
    (
        "audit-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        & ~RequireInstanceState(["subm", "in_progress"]),
    ),
    (
        "corrections-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        | RequireInstanceState(["corrected", "correction"]),
    ),
    (
        "legal-submissions-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["subm"]),
    ),
    (
        "form-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES | RequireInstanceState(["correction"]),
    ),
    ("documents-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    (
        "dms-generate-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES,
    ),
    (
        "assign-ebau-number-read",
        RequireInstanceState(["subm", "in_progress_internal"]),
    ),
    ("distribution-read", BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED),
    ("work-items-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("appeal-read", IsAppeal()),
]

BE_ACTIVE_LEAD_AUTHORITY_PERMISSIONS = BE_INVOLVED_LEAD_AUTHORITY_PERMISSIONS + [
    (
        "corrections-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        | RequireInstanceState(["corrected", "correction"]),
    ),
    (
        "instance-change-form",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        | RequireInstanceState(["corrected", "correction"]),
    ),
]

GEOMETER_RW = (
    HasRole(["geometer-lead", "geometer-clerk"]) & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES
)


BE_PERMISSIONS_SETTINGS = {
    "PERMISSION_MODE": PERMISSION_MODE.OFF,
    "ACCESS_LEVELS": {
        "geometer": [
            ("communications-read", GEOMETER_RW),
            ("communications-write", GEOMETER_RW),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", GEOMETER_RW),
            ("form-read", MODULE_FORM),
            ("geometer-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("history-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("journal-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("responsible-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("work-items-read", GEOMETER_RW),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS_READ),
            ("communications-write", MODULE_COMMUNICATIONS_WRITE),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
        ],
        # TODO: The following access levels have not beeen released yet
        "applicant": [
            ("applicant-remove", Always()),
            ("applicant-add", Always()),
            ("applicant-read", Always()),
        ],
        "lead-authority": BE_ACTIVE_LEAD_AUTHORITY_PERMISSIONS,
        "involved-authority": BE_INVOLVED_LEAD_AUTHORITY_PERMISSIONS,
        "construction-control": BE_CONSTRUCTION_CONTROL_PERMISSIONS,
        "involved-construction-control": BE_CONSTRUCTION_CONTROL_PERMISSIONS,
        "support": [
            ("support-read", SUPPORT_CONDITION),
            ("form-read", SUPPORT_CONDITION),
            ("documents-read", SUPPORT_CONDITION),
            ("audit-log-read", SUPPORT_CONDITION),
            ("changelog-read", SUPPORT_CONDITION),
            ("history-read", SUPPORT_CONDITION),
            ("instance-change-form", SUPPORT_CONDITION),
        ],
        "distribution-service": [
            ("work-items-read", BE_SERVICE_STATES_DEFAULT),
            ("communications-read", BE_SERVICE_STATES_DEFAULT),
            ("form-read", BE_SERVICE_STATES_DEFAULT),
            ("documents-read", BE_SERVICE_STATES_DEFAULT),
            ("dms-generate-read", BE_SERVICE_STATES_DEFAULT),
            ("responsibilities-read", BE_SERVICE_STATES_DEFAULT),
            ("audit-read", BE_SERVICE_STATES_DEFAULT),
            (
                "distribution-read",
                BE_SERVICE_STATES_DEFAULT
                & ~RequireInstanceState(
                    ["finished_internal", "in_progress", "in_progress_internal"]
                ),
            ),
            ("billing-read", BE_SERVICE_STATES_DEFAULT),
            ("legal-submissions-read", BE_SERVICE_STATES_DEFAULT),
            ("journal-read", BE_SERVICE_STATES_DEFAULT),
            ("changelog-read", BE_SERVICE_STATES_DEFAULT),
            ("history-read", BE_SERVICE_STATES_DEFAULT),
            ("decision-read", POST_DECISION_STATES),
        ],
    },
    "EVENTS_WITH_NOTIFICATION": ["manual-creation", "grant-geometer-access"],
    "EVENT_HANDLER": "camac.permissions.config.kt_bern.PermissionEventHandlerBE",
    "ENABLED": True,
    # Map INTERNAL -> CANTON access level names. The INTERNAL ones
    # are directly referenced by the migration tooling and may differ from
    # the ones used by the canton.
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "MUNICIPALITY_INVOLVED": "involved-authority",
        "DISTRIBUTION_INVITEE": "distribution-service",
        "CONSTRUCTION_CONTROL": "construction-control",
        "CONSTRUCTION_CONTROL_INVOLVED": "involved-construction-control",
        # TODO refactor somehow to something more explicit
    },
    "MIGRATION_FILTERS": {
        # Specific filters for being more exact about what data to fetch,
        # where neccessary
        "municipality": Q(
            Q(service__service_group__name="municipality")
            | Q(service__service_group__name="district")
        ),
        "construction_control": Q(service__service_group__name="consruction-control"),
    },
    "ENABLE_CACHE": True,
}
