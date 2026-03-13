from django.db.models import Q

from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    IsAppeal,
    IsForm,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

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
        "legal-authority-lead",
        "legal-authority-clerk",
        "legal-authority-readonly",
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
        "legal-authority-readonly",
    ]
)

BAUGESUCH_FORM_VERSIONS = [
    "baugesuch",
    "baugesuch-v2",
    "baugesuch-v3",
    "baugesuch-v5",
    "baugesuch-v6",
    "baugesuch-generell",
    "baugesuch-generell-v2",
    "baugesuch-generell-v3",
    "baugesuch-generell-v5",
    "baugesuch-generell-v6",
    "baugesuch-mit-uvp",
    "baugesuch-mit-uvp-v2",
    "baugesuch-mit-uvp-v3",
    "baugesuch-mit-uvp-v5",
    "baugesuch-mit-uvp-v6",
]

MODULE_FORM = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_DOCUMENTS_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_DOCUMENTS_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_HISTORY = STATES_ALL_INTERNAL & ROLES_INTERNAL

MODULE_COMMUNICATIONS_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_COMMUNICATIONS_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_DMS_GENERATE_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_DMS_GENERATE_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_JOURNAL_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_JOURNAL_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_RESPONSIBLE_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_RESPONSIBLE_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_HEADER_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_HEADER_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

# Portal permissions - TODO: Paper instances
MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = RequireWorkItem(
    "fill-additional-demand", "ready"
) & HasApplicantRole(["ADMIN", "EDITOR"])

MODULE_PORTAL_ALEXANDRIA_READ = Always()
MODULE_PORTAL_ALEXANDRIA_WRITE = HasApplicantRole(["ADMIN", "EDITOR"])

MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])

MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)

MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN", "EDITOR"])
)

MODULE_PORTAL_SB1_READ = RequireWorkItem("sb1")
MODULE_PORTAL_SB1_WRITE = RequireWorkItem("sb1", "ready") & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)

MODULE_PORTAL_SB2_READ = RequireWorkItem("sb2")
MODULE_PORTAL_SB2_WRITE = RequireWorkItem("sb2", "ready") & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)

MODULE_PORTAL_DOCUMENTS_READ = Always()
MODULE_PORTAL_DOCUMENTS_WRITE = (
    MODULE_PORTAL_FORM_WRITE
    | MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE
    | MODULE_PORTAL_SB1_WRITE
    | MODULE_PORTAL_SB2_WRITE
)

ACTION_PORTAL_INSTANCE_CREATE_MODIFICATION = (
    ~RequireInstanceState(["new", "finished", "archived"])
    & IsForm(BAUGESUCH_FORM_VERSIONS)
    & HasApplicantRole(["ADMIN"])
    # TODO: Support should also be allowed to create a project modification
)

ACTION_PORTAL_INSTANCE_COPY_AFTER_REJECTION = RequireInstanceState(["rejected"]) & (
    HasApplicantRole(["ADMIN"])
)

ACTION_PORTAL_INSTANCE_DELETE = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"])
)

ACTION_PORTAL_INSTANCE_EXTEND_VALIDITY = RequireInstanceState(["sb1", "sb2"]) & (
    HasApplicantRole(["ADMIN"])
)

ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF = STATES_ALL_INTERNAL

ACTION_PORTAL_INSTANCE_SUBMIT = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN"])
)

ACTION_PORTAL_SB1_SUBMIT = RequireWorkItem("sb1", "ready") & (
    HasApplicantRole(["ADMIN", "EDITOR"])
)

ACTION_PORTAL_SB2_SUBMIT = RequireWorkItem("sb2", "ready") & (
    HasApplicantRole(["ADMIN", "EDITOR"])
)

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
BE_BASE_CONSTRUCTION_CONTROL_PERMISSIONS = [
    ("history-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("documents-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("alexandria-write", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
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
    ("journal-write", MODULE_JOURNAL_WRITE),
    ("changelog-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("form-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("work-items-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
    ("communications-read", BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES),
]

BE_INVOLVED_CONSTRUCTION_CONTROL_PERMISSIONS = (
    BE_BASE_CONSTRUCTION_CONTROL_PERMISSIONS
    + [
        (
            "instance-unsubscribe-responsible-service",
            BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES
            & ~RequireInstanceState(["finished_internal", "archived", "finished"]),
        ),
    ]
)
BE_ACTIVE_CONSTRUCTION_CONTROL_PERMISSIONS = (
    BE_BASE_CONSTRUCTION_CONTROL_PERMISSIONS
    + [
        (
            "instance-change-responsible-service",
            BE_CONSTRUCTION_CONTROL_ACCESSIBLE_STATES
            & ~RequireInstanceState(["finished_internal", "archived", "finished"]),
        ),
    ]
)

# Support always has access to instance (and (almost?) all IRs on it)
SUPPORT_CONDITION = Always()

BE_BASE_AUTHORITY_PERMISSIONS = [
    ("communications-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("geometer-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("responsible-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("responsible-write", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("journal-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("journal-write", MODULE_JOURNAL_WRITE),
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
    ("alexandria-write", MODULE_DOCUMENTS_READ),
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

BE_INVOLVED_LEAD_AUTHORITY_PERMISSIONS = BE_BASE_AUTHORITY_PERMISSIONS + [
    (
        "instance-unsubscribe-responsible-service",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["in_progress"]),
    )
]

BE_ACTIVE_LEAD_AUTHORITY_PERMISSIONS = BE_BASE_AUTHORITY_PERMISSIONS + [
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
    (
        "instance-change-responsible-service",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["in_progress"]),
    ),
    (
        "additional-demands-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & RequireWorkItem("init-additional-demand"),
    ),
    (
        "additional-demands-write",
        BE_MUNICIPALITY_ACCESSIBLE_STATES
        & RequireWorkItem("init-additional-demand")
        & HasRole(["municipality-lead"]),
    ),
]

GEOMETER_RW = (
    HasRole(["geometer-lead", "geometer-clerk"]) & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES
)


BE_PERMISSIONS_SETTINGS = {
    "PERMISSION_MODE": PERMISSION_MODE.OFF,
    "MIGRATED_ROLE_PERMISSIONS": env.list("MIGRATED_ROLE_PERMISSIONS", default=[]),
    "ACCESS_LEVELS": {
        "geometer": [
            # TODO: Check if any logic is missing for geometers before
            # switching entirely to permissions module
            ("communications-read", GEOMETER_RW),
            ("communications-write", GEOMETER_RW),
            ("communications-convert-to-document", GEOMETER_RW),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", GEOMETER_RW),
            ("form-read", MODULE_FORM),
            ("geometer-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("history-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("journal-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("journal-write", GEOMETER_RW),
            ("responsible-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ("responsible-write", GEOMETER_RW),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", GEOMETER_RW),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS_READ),
            ("communications-write", MODULE_COMMUNICATIONS_WRITE),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
        ],
        "legal-authority": [
            # TODO: Check if any logic is missing for legal-authority before
            # switching entirely to permissions module
            ("communications-read", MODULE_COMMUNICATIONS_READ),
            ("communications-write", MODULE_COMMUNICATIONS_WRITE),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS_WRITE),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
            ("dms-generate-read", MODULE_DMS_GENERATE_READ),
            ("dms-generate-write", MODULE_DMS_GENERATE_WRITE),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
        ],
        # TODO: The following access levels have not beeen released yet
        "applicant": [
            ("additional-demands-read", MODULE_PORTAL_ADDITIONAL_DEMANDS_READ),
            ("additional-demands-write", MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE),
            # TODO: alexandria-read permission
            ("alexandria-write", MODULE_PORTAL_ALEXANDRIA_WRITE),
            ("applicant-add", MODULE_PORTAL_APPLICANTS),
            ("applicant-read", MODULE_PORTAL_APPLICANTS),
            ("applicant-remove", MODULE_PORTAL_APPLICANTS),
            ("communications-read", MODULE_PORTAL_COMMUNICATIONS_READ),
            ("communications-write", MODULE_PORTAL_COMMUNICATIONS_WRITE),
            ("documents-read", MODULE_PORTAL_DOCUMENTS_READ),
            ("documents-write", MODULE_PORTAL_DOCUMENTS_WRITE),
            ("form-read", MODULE_PORTAL_FORM_READ),
            ("form-write", MODULE_PORTAL_FORM_WRITE),
            ("form-sb1-read", MODULE_PORTAL_SB1_READ),
            ("form-sb1-write", MODULE_PORTAL_SB1_WRITE),
            ("form-sb1-submit", ACTION_PORTAL_SB1_SUBMIT),
            ("form-sb2-read", MODULE_PORTAL_SB2_READ),
            ("form-sb2-write", MODULE_PORTAL_SB2_WRITE),
            ("form-sb2-submit", ACTION_PORTAL_SB2_SUBMIT),
            (
                "instance-create-modification",
                ACTION_PORTAL_INSTANCE_CREATE_MODIFICATION,
            ),
            (
                "instance-copy-after-rejection",
                ACTION_PORTAL_INSTANCE_COPY_AFTER_REJECTION,
            ),
            ("instance-delete", ACTION_PORTAL_INSTANCE_DELETE),
            (
                "instance-download-form-as-pdf",
                ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF,
            ),
            (
                "instance-extend-validity",
                ACTION_PORTAL_INSTANCE_EXTEND_VALIDITY,
            ),
            ("instance-submit", ACTION_PORTAL_INSTANCE_SUBMIT),
        ],
        "lead-authority": BE_ACTIVE_LEAD_AUTHORITY_PERMISSIONS,
        "involved-authority": BE_INVOLVED_LEAD_AUTHORITY_PERMISSIONS,
        "construction-control": BE_ACTIVE_CONSTRUCTION_CONTROL_PERMISSIONS,
        "involved-construction-control": BE_INVOLVED_CONSTRUCTION_CONTROL_PERMISSIONS,
        "support": [
            ("support-read", SUPPORT_CONDITION),
            ("form-read", SUPPORT_CONDITION),
            ("documents-read", SUPPORT_CONDITION),
            ("alexandria-write", SUPPORT_CONDITION),
            ("audit-log-read", SUPPORT_CONDITION),
            ("changelog-read", SUPPORT_CONDITION),
            ("history-read", SUPPORT_CONDITION),
            ("instance-change-form", SUPPORT_CONDITION),
            ("communications-read", SUPPORT_CONDITION),
            ("communications-delete-attachment", SUPPORT_CONDITION),
        ],
        "distribution-service": [
            ("work-items-read", BE_SERVICE_STATES_DEFAULT),
            ("communications-read", BE_SERVICE_STATES_DEFAULT),
            ("form-read", BE_SERVICE_STATES_DEFAULT),
            ("documents-read", BE_SERVICE_STATES_DEFAULT),
            ("alexandria-write", BE_SERVICE_STATES_DEFAULT),
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
            ("journal-write", MODULE_JOURNAL_WRITE),
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
}
