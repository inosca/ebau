from django.db.models import Q

from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    IsAppeal,
    IsCreatedByService,
    IsModification,
    IsPaper,
    IsUnversionedForm,
    IsWorkflow,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

WORK_ITEM_STATUS_READY = "ready"
WORK_ITEM_STATUS_COMPLETED = "completed"
WORKFLOW_BUILDING_PERMIT = "building-permit"
WORKFLOW_PRELIMINARY_CLARIFICATION = "preliminary-clarification"
WORKFLOW_INTERNAL = "internal"
WORKFLOW_MIGRATED = "migrated"

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
        # TODO: Is instance state "corrected" still needed?
        "corrected",  # Korrigiert von Leitbehörde
        "archived",  # Archiviert
        # preliminary clarification
        "evaluated",  # Beurteilung abgeschlossen
        # special procedures
        "in_progress_internal",  # In Bearbeitung (intern)
        "finished_internal",  # Abgeschlossen (intern)
        # RSTA import (migrated)
        "in_progress",  # In Bearbeitung
    ]
)

STATES_INTERNAL_NO_CORRECTION = RequireInstanceState(
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
        "archived",  # Archiviert
        # preliminary clarification
        "evaluated",  # Beurteilung abgeschlossen
        # special procedures
        "in_progress_internal",  # In Bearbeitung (intern)
        "finished_internal",  # Abgeschlossen (intern)
        # RSTA import (migrated)
        "in_progress",  # In Bearbeitung
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

ROLES_INTERNAL_NO_READONLY = HasRole(
    [
        "municipality-lead",
        "municipality-clerk",
        "service-lead",
        "service-clerk",
        "construction-control-lead",
        "construction-control-clerk",
        "geometer-lead",
        "geometer-clerk",
        "legal-authority-lead",
        "legal-authority-clerk",
        "subservice",
        "support",
    ]
)

ROLES_INTERNAL_LEAD = HasRole(["municipality-lead"])

NO_CORRECTION_IN_PROGRESS = ~RequireInstanceState(["correction"])
PAPER_CREATED_BY_SERVICE_NO_READONLY = (
    IsPaper() & IsCreatedByService() & ROLES_INTERNAL_NO_READONLY
)

STATES_AFTER_DECISION = RequireInstanceState(
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

BAUGESUCH_FORMS = ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"]

# Note: Additional demands not visible on migrated instances (RSTA) (defined
# by workflow "migrated", since workflow/tasks for additional-demands are not
# included).
# TODO: For portal additional demands shouldn't be hidden during correction.
# TODO: Are the additional-demands visible in the form to other access levels?
MODULE_ADDITIONAL_DEMANDS_READ = (
    RequireWorkItem("init-additional-demand")
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)
# Note: Additional demands are editable until decision (which cancels
# the work-item(s)).
MODULE_ADDITIONAL_DEMANDS_WRITE = (
    RequireWorkItem("init-additional-demand", WORK_ITEM_STATUS_READY, True)
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
    & ~IsPaper()
)

# Note: Appeal work-item created dynamic for appeal instances, which can
# be created on instances with a building permit workflow
# TODO: Not editable for read-only roles
MODULE_APPEAL_READ = (
    RequireWorkItem("appeal") & NO_CORRECTION_IN_PROGRESS & ROLES_INTERNAL
)

MODULE_APPLICANTS_READ = ROLES_INTERNAL

# TODO: Should eBau-Nr. be visible for involved lead authority?
# TODO: Should be visible on migrated workflow?
MODULE_ASSIGN_EBAU_NUMBER = (
    RequireWorkItem("ebau-number", WORK_ITEM_STATUS_READY, True)
    & ROLES_INTERNAL_NO_READONLY
)

# Note: Audit not available on migrated instances (workflow "migrated")
MODULE_AUDIT_READ = (
    RequireWorkItem("audit") & NO_CORRECTION_IN_PROGRESS & ROLES_INTERNAL
)
MODULE_AUDIT_WRITE = (
    RequireWorkItem("audit", WORK_ITEM_STATUS_READY, True)
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_BILLING_READ = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY
MODULE_BILLING_WRITE = MODULE_BILLING_READ & ~STATES_AFTER_DECISION

# Note: Construction control is only involved on building permits with
# a positive decision.
# TODO: Shown in decided state (finished) for negative decisions and for
# archived instances without decision as well.
# TODO: Is the module necessary for internal workflow?
MODULE_CHANGE_CONSTRUCTION_CONTROL_READ = (
    IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_INTERNAL])
    & (STATES_AFTER_DECISION | RequireInstanceState("in_progress_internal"))
    & ROLES_INTERNAL_NO_READONLY
)

# Note: Lead authority change not available on migrated (RSTA import) instances
MODULE_CHANGE_LEAD_AUTHORITY_READ = (
    IsWorkflow(
        [
            WORKFLOW_BUILDING_PERMIT,
            WORKFLOW_PRELIMINARY_CLARIFICATION,
            WORKFLOW_INTERNAL,
        ]
    )
    & STATES_INTERNAL_NO_CORRECTION
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_COMMUNICATIONS = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

MODULE_CORRECTIONS = STATES_ALL_INTERNAL & ROLES_INTERNAL_LEAD

# Note: Decision work-item is set to status "redo" when distribution is reopened
# (decision module is hidden during distribution).
# During correction and rejection the decision work-item becomes suspended
# (the decision module is hidden during correction and rejection).
MODULE_DECISION_READ = RequireWorkItem(
    "decision", WORK_ITEM_STATUS_READY, True
) | RequireWorkItem("decision", WORK_ITEM_STATUS_COMPLETED)
MODULE_DECISION_WRITE = (
    RequireWorkItem("decision", WORK_ITEM_STATUS_READY, True) & ROLES_INTERNAL_LEAD
)

# Note: Distribution not available in internal and migrated (RSTA import)
# workflows (distribution task only configured for building-permit and
# preliminary-clarification workflows - the work-item will only be generated
# in those cases, which we use to determine visibility of the module).
MODULE_DISTRIBUTION_READ = (
    RequireWorkItem("distribution")
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_DMS_GENERATE = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

MODULE_FORM_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_FORM_WRITE = RequireInstanceState(["correction"]) & ROLES_INTERNAL_NO_READONLY

MODULE_GEOMETER_READ = RequireWorkItem("geometer")
MODULE_GEOMETER_WRITE = RequireWorkItem("geometer", WORK_ITEM_STATUS_READY, True)

MODULE_JOURNAL_READ = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL
MODULE_JOURNAL_WRITE = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

MODULE_HEADER_READ = STATES_ALL_INTERNAL & ROLES_INTERNAL
MODULE_HEADER_WRITE = STATES_ALL_INTERNAL & ROLES_INTERNAL_NO_READONLY

MODULE_HISTORY = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL

# Note: Information of neighbors not available on internal workflow
# TODO: Instance state and workflow don't match for migrated - when is it visible?
MODULE_INFORMATION_OF_NEIGHBORS_READ = (
    RequireWorkItem("create-information-of-neighbors")
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL
)
MODULE_INFORMATION_OF_NEIGHBORS_WRITE = (
    (
        RequireWorkItem("create-information-of-neighbors", WORK_ITEM_STATUS_READY, True)
        | RequireWorkItem("information-of-neighbors", WORK_ITEM_STATUS_READY, True)
    )
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)

# TODO: service-read does not see legal submissions
MODULE_LEGAL_SUBMISSIONS_READ = (
    RequireWorkItem("legal-submission") & NO_CORRECTION_IN_PROGRESS & ROLES_INTERNAL
)
MODULE_LEGAL_SUBMISSIONS_WRITE = (
    RequireWorkItem("legal-submission", WORK_ITEM_STATUS_READY, True)
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_PERMISSIONS = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

# TODO: Instance state and workflow don't match for migrated - when is it visible?
MODULE_PUBLICATION_READ = (
    RequireWorkItem("create-publication")
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL
)
# TODO: Publication writeable after decision
MODULE_PUBLICATION_WRITE = (
    (
        RequireWorkItem("create-publication", WORK_ITEM_STATUS_READY, True)
        | RequireWorkItem("fill-publication", WORK_ITEM_STATUS_READY, True)
    )
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & NO_CORRECTION_IN_PROGRESS
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_RELATED_GWR_PROJECTS = (
    STATES_INTERNAL_NO_CORRECTION
    & ~RequireInstanceState(["subm"])
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_REJECTION = (
    STATES_INTERNAL_NO_CORRECTION
    & ~RequireInstanceState(["subm", "archived"])
    & IsWorkflow([WORKFLOW_BUILDING_PERMIT, WORKFLOW_PRELIMINARY_CLARIFICATION])
    & ROLES_INTERNAL_NO_READONLY
)

MODULE_RESPONSIBLE_READ = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL
MODULE_RESPONSIBLE_WRITE = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

MODULE_REVISION_HISTORY_READ = (
    STATES_ALL_INTERNAL
    & ROLES_INTERNAL
    & (NO_CORRECTION_IN_PROGRESS | ROLES_INTERNAL_NO_READONLY)
)

MODULE_SB1_READ = RequireWorkItem("sb1", WORK_ITEM_STATUS_COMPLETED)

MODULE_SB2_READ = RequireWorkItem("sb2", WORK_ITEM_STATUS_COMPLETED)

MODULE_WORK_ITEMS = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

MODULE_DOCUMENTS_READ = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL
MODULE_DOCUMENTS_WRITE = STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY

INSTANCE_ARCHIVE_CONDITION = ~RequireInstanceState(["archived"])
ACTION_INSTANCE_ARCHIVE = (
    STATES_ALL_INTERNAL & ROLES_INTERNAL_LEAD & INSTANCE_ARCHIVE_CONDITION
)

ACTION_INSTANCE_CHANGE_EBAU_NUMBER = (
    STATES_ALL_INTERNAL
    & RequireWorkItem("ebau-number", WORK_ITEM_STATUS_COMPLETED)
    & ROLES_INTERNAL_LEAD
)

# TODO: In the future we could only show this action on building-permit forms
ACTION_INSTANCE_CHANGE_FORM = STATES_ALL_INTERNAL & ROLES_INTERNAL_LEAD

# Note: Lead authority change possible until decision
ACTION_INSTANCE_CHANGE_LEAD_AUTHORITY = (
    MODULE_CHANGE_LEAD_AUTHORITY_READ & ~STATES_AFTER_DECISION
)

ACTION_INSTANCE_CHANGE_CONSTRUCTION_CONTROL = MODULE_CHANGE_CONSTRUCTION_CONTROL_READ

# Note: Don't allow creating service of paper instance to unsubscribe (behavior change)
ACTION_INSTANCE_UNSUBSCRIBE_LEAD_AUTHORITY = ACTION_INSTANCE_CHANGE_LEAD_AUTHORITY & ~(
    IsPaper() & IsCreatedByService()
)
ACTION_INSTANCE_UNSUBSCRIBE_CONSTRUCTION_CONTROL = (
    ACTION_INSTANCE_CHANGE_CONSTRUCTION_CONTROL
)

INSTANCE_CONVERT_MODIFICATION_CONDITION = IsModification() & ~IsAppeal()
ACTION_INSTANCE_CONVERT_MODIFICATION = (
    STATES_ALL_INTERNAL & ROLES_INTERNAL_LEAD & INSTANCE_CONVERT_MODIFICATION_CONDITION
)

# TODO: Might make sense to split the start and finish of
# the correction in two permissions
INSTANCE_CORRECT_CONDITION = RequireInstanceState(
    [
        "circulation_init",
        "circulation",
        "in_progress",
        "in_progress_internal",
        "correction",
    ]
)
ACTION_INSTANCE_CORRECT = INSTANCE_CORRECT_CONDITION & ROLES_INTERNAL_LEAD

ACTION_SUPPORT_INSTANCE_COPY = RequireInstanceState(
    [
        "archived",
        "evaluated",
        "finished_internal",
        "finished",
    ]
)

# Portal permissions

MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = RequireWorkItem(
    "fill-additional-demand", WORK_ITEM_STATUS_READY
) & HasApplicantRole(["ADMIN", "EDITOR"])

# TODO: Should be same as portal documents read / write
MODULE_PORTAL_ALEXANDRIA_READ = Always()
MODULE_PORTAL_ALEXANDRIA_WRITE = HasApplicantRole(["ADMIN", "EDITOR"])

MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])

MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)

PORTAL_FORM_WRITE_CONDITION = RequireWorkItem("submit", WORK_ITEM_STATUS_READY)
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = PORTAL_FORM_WRITE_CONDITION & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
MODULE_PORTAL_PAPER_FORM_READ = PAPER_CREATED_BY_SERVICE_NO_READONLY
MODULE_PORTAL_PAPER_FORM_WRITE = (
    PORTAL_FORM_WRITE_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

MODULE_PORTAL_SB1_READ = RequireWorkItem("sb1")
PORTAL_SB1_WRITE_CONDITION = RequireWorkItem("sb1", WORK_ITEM_STATUS_READY)
MODULE_PORTAL_SB1_WRITE = PORTAL_SB1_WRITE_CONDITION & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
MODULE_PORTAL_PAPER_SB1_WRITE = (
    PORTAL_SB1_WRITE_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

MODULE_PORTAL_SB2_READ = RequireWorkItem("sb2")
PORTAL_SB2_WRITE_CONDITION = RequireWorkItem("sb2", WORK_ITEM_STATUS_READY)
MODULE_PORTAL_SB2_WRITE = PORTAL_SB2_WRITE_CONDITION & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
MODULE_PORTAL_PAPER_SB2_WRITE = (
    PORTAL_SB2_WRITE_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

MODULE_PORTAL_DOCUMENTS_READ = Always()
MODULE_PORTAL_DOCUMENTS_WRITE = (
    RequireWorkItem("submit", WORK_ITEM_STATUS_READY)
    | RequireWorkItem("fill-additional-demand", WORK_ITEM_STATUS_READY)
    | RequireWorkItem("sb1", WORK_ITEM_STATUS_READY)
    | RequireWorkItem("sb2", WORK_ITEM_STATUS_READY)
) & HasApplicantRole(["ADMIN", "EDITOR"])
# Note: Additional demands are not editable on paper instances
MODULE_PORTAL_PAPER_DOCUMENTS_READ = PAPER_CREATED_BY_SERVICE_NO_READONLY
MODULE_PORTAL_PAPER_DOCUMENTS_WRITE = (
    RequireWorkItem("submit", WORK_ITEM_STATUS_READY)
    | RequireWorkItem("sb1", WORK_ITEM_STATUS_READY)
    | RequireWorkItem("sb2", WORK_ITEM_STATUS_READY)
) & PAPER_CREATED_BY_SERVICE_NO_READONLY

PORTAL_INSTANCE_CREATE_MODIFICATION_CONDITION = (
    ~RequireInstanceState(["new", "finished", "archived"])
    & IsUnversionedForm(BAUGESUCH_FORMS)
    & ~IsModification()
)
ACTION_PORTAL_INSTANCE_CREATE_MODIFICATION = (
    PORTAL_INSTANCE_CREATE_MODIFICATION_CONDITION & HasApplicantRole(["ADMIN"])
)
ACTION_PORTAL_PAPER_INSTANCE_CREATE_MODIFICATION = (
    PORTAL_INSTANCE_CREATE_MODIFICATION_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT_CONDITION = IsUnversionedForm(
    "vorabklaerung-vollstaendig"
)
ACTION_PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT = (
    PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT_CONDITION & HasApplicantRole(["ADMIN"])
)
ACTION_PORTAL_PAPER_INSTANCE_CONVERT_TO_BUILDING_PERMIT = (
    PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT_CONDITION
    & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_INSTANCE_COPY_AFTER_REJECTION_CONDITION = RequireInstanceState(["rejected"])
ACTION_PORTAL_INSTANCE_COPY_AFTER_REJECTION = (
    PORTAL_INSTANCE_COPY_AFTER_REJECTION_CONDITION & HasApplicantRole(["ADMIN"])
)
ACTION_PORTAL_PAPER_INSTANCE_COPY_AFTER_REJECTION = (
    PORTAL_INSTANCE_COPY_AFTER_REJECTION_CONDITION
    & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_INSTANCE_DELETE_CONDITION = RequireInstanceState(["new"])
ACTION_PORTAL_INSTANCE_DELETE = PORTAL_INSTANCE_DELETE_CONDITION & HasApplicantRole(
    ["ADMIN"]
)
ACTION_PORTAL_PAPER_INSTANCE_DELETE = (
    PORTAL_INSTANCE_DELETE_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_INSTANCE_EXTEND_VALIDITY_CONDITION = RequireInstanceState(["sb1", "sb2"])
ACTION_PORTAL_INSTANCE_EXTEND_VALIDITY = (
    PORTAL_INSTANCE_EXTEND_VALIDITY_CONDITION & HasApplicantRole(["ADMIN"])
)
ACTION_PORTAL_PAPER_INSTANCE_EXTEND_VALIDITY = (
    PORTAL_INSTANCE_EXTEND_VALIDITY_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF = STATES_ALL_INTERNAL

PORTAL_INSTANCE_SUBMIT_CONDITION = RequireWorkItem("submit", WORK_ITEM_STATUS_READY)
ACTION_PORTAL_INSTANCE_SUBMIT = PORTAL_INSTANCE_SUBMIT_CONDITION & HasApplicantRole(
    ["ADMIN"]
)
ACTION_PORTAL_PAPER_INSTANCE_SUBMIT = (
    PORTAL_INSTANCE_SUBMIT_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_SB1_SUBMIT_CONDITION = RequireWorkItem("sb1", WORK_ITEM_STATUS_READY)
ACTION_PORTAL_SB1_SUBMIT = PORTAL_SB1_SUBMIT_CONDITION & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
ACTION_PORTAL_PAPER_SB1_SUBMIT = (
    PORTAL_SB1_SUBMIT_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
)

PORTAL_SB2_SUBMIT_CONDITION = RequireWorkItem("sb2", WORK_ITEM_STATUS_READY)
ACTION_PORTAL_SB2_SUBMIT = PORTAL_SB2_SUBMIT_CONDITION & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
ACTION_PORTAL_PAPER_SB2_SUBMIT = (
    PORTAL_SB2_SUBMIT_CONDITION & PAPER_CREATED_BY_SERVICE_NO_READONLY
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


# TODO: ROLES_NO_READONLY / ROLES_LEAD / ROLES_MUNICIPALITY
# TODO: Portal view of communications and additional-demands mirror internal area
# TODO: Mirrored applicant view (for support)
BE_PERMISSIONS_SETTINGS = {
    "PERMISSION_MODE": PERMISSION_MODE.FULL,
    "MIGRATED_ROLE_PERMISSIONS": env.list("MIGRATED_ROLE_PERMISSIONS", default=[]),
    "ACCESS_LEVELS": {
        "geometer": [
            ("case-meta-read", MODULE_HEADER_READ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_SB1_READ),
            ("form-sb2-read", MODULE_SB2_READ),
            ("geometer-read", MODULE_GEOMETER_READ),
            ("geometer-write", MODULE_GEOMETER_WRITE),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("form-read", MODULE_FORM_READ),
            ("history-read", MODULE_HISTORY),
        ],
        "legal-authority": [
            ("case-meta-read", MODULE_HEADER_READ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_SB1_READ),
            ("form-sb2-read", MODULE_SB2_READ),
            ("history-read", MODULE_HISTORY),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
        ],
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
            # TODO: Permission integration instance-convert-to-building-permit
            (
                "instance-convert-to-building-permit",
                ACTION_PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT,
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
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS_READ),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS_WRITE),
            # TODO: alexandria-read permission
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            # TODO: Use permissions module for form-write permission on appeal
            ("appeal-read", MODULE_APPEAL_READ),
            ("applicant-read", MODULE_APPLICANTS_READ),
            ("assign-ebau-number-read", MODULE_ASSIGN_EBAU_NUMBER),
            ("assign-ebau-number-write", MODULE_ASSIGN_EBAU_NUMBER),
            ("audit-read", MODULE_AUDIT_READ),
            ("audit-write", MODULE_AUDIT_WRITE),
            ("billing-read", MODULE_BILLING_READ),
            ("billing-write", MODULE_BILLING_WRITE),
            # TODO: Permission integration case-meta-read
            ("case-meta-read", MODULE_HEADER_READ),
            ("case-meta-write", MODULE_HEADER_WRITE),
            (
                "change-construction-control-read",
                MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("change-lead-authority-read", MODULE_CHANGE_LEAD_AUTHORITY_READ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("corrections-read", MODULE_CORRECTIONS),
            ("decision-read", MODULE_DECISION_READ),
            ("decision-write", MODULE_DECISION_WRITE),
            ("distribution-read", MODULE_DISTRIBUTION_READ),
            (
                "documents-read",
                MODULE_DOCUMENTS_READ | MODULE_PORTAL_PAPER_DOCUMENTS_READ,
            ),
            (
                "documents-write",
                MODULE_DOCUMENTS_WRITE | MODULE_PORTAL_PAPER_DOCUMENTS_WRITE,
            ),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ | MODULE_PORTAL_PAPER_FORM_READ),
            ("form-write", MODULE_FORM_WRITE | MODULE_PORTAL_PAPER_FORM_WRITE),
            ("form-sb1-read", MODULE_PORTAL_SB1_READ),
            ("form-sb1-write", MODULE_PORTAL_PAPER_SB1_WRITE),
            ("form-sb1-submit", ACTION_PORTAL_PAPER_SB1_SUBMIT),
            ("form-sb2-read", MODULE_PORTAL_SB2_READ),
            ("form-sb2-write", MODULE_PORTAL_PAPER_SB2_WRITE),
            ("form-sb2-submit", ACTION_PORTAL_PAPER_SB2_SUBMIT),
            ("history-read", MODULE_HISTORY),
            ("information-of-neighbors-read", MODULE_INFORMATION_OF_NEIGHBORS_READ),
            ("information-of-neighbors-write", MODULE_INFORMATION_OF_NEIGHBORS_WRITE),
            # TODO: Permission integration instance-archive
            ("instance-archive", ACTION_INSTANCE_ARCHIVE),
            # TODO: Permission integration instance-change-ebau-number
            ("instance-change-ebau-number", ACTION_INSTANCE_CHANGE_EBAU_NUMBER),
            ("instance-change-form", ACTION_INSTANCE_CHANGE_FORM),
            (
                "instance-change-responsible-service",
                ACTION_INSTANCE_CHANGE_LEAD_AUTHORITY,
            ),
            # TODO: Permission integration instance-convert-modification
            (
                "instance-convert-modification",
                ACTION_INSTANCE_CONVERT_MODIFICATION,
            ),
            # TODO: Permission integration instance-convert-to-building-permit
            (
                "instance-convert-to-building-permit",
                ACTION_PORTAL_PAPER_INSTANCE_CONVERT_TO_BUILDING_PERMIT,
            ),
            # TODO: Permission integration instance-correct
            ("instance-correct", ACTION_INSTANCE_CORRECT),
            (
                "instance-create-modification",
                ACTION_PORTAL_PAPER_INSTANCE_CREATE_MODIFICATION,
            ),
            (
                "instance-copy-after-rejection",
                ACTION_PORTAL_PAPER_INSTANCE_COPY_AFTER_REJECTION,
            ),
            ("instance-delete", ACTION_PORTAL_PAPER_INSTANCE_DELETE),
            ("instance-download-form-as-pdf", ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF),
            ("instance-extend-validity", ACTION_PORTAL_PAPER_INSTANCE_EXTEND_VALIDITY),
            ("instance-submit", ACTION_PORTAL_PAPER_INSTANCE_SUBMIT),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            # TODO: Use permissions module for form-write permission on legal submissions
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS_READ),
            ("legal-submissions-write", MODULE_LEGAL_SUBMISSIONS_WRITE),
            ("permissions-grant-geometer", MODULE_PERMISSIONS),
            ("permissions-grant-legal-authority", MODULE_PERMISSIONS),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-revoke-geometer", MODULE_PERMISSIONS),
            ("permissions-revoke-legal-authority", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION_READ),
            ("publication-write", MODULE_PUBLICATION_WRITE),
            ("rejection-read", MODULE_REJECTION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("revision-history-read", MODULE_REVISION_HISTORY_READ),
            # TODO: Permission integration tags-read
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "involved-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS_READ),
            # TODO: alexandria-read permission
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("appeal-read", MODULE_APPEAL_READ),
            ("applicant-read", MODULE_APPLICANTS_READ),
            ("audit-read", MODULE_AUDIT_READ),
            ("billing-read", MODULE_BILLING_READ),
            ("billing-write", MODULE_BILLING_WRITE),
            ("case-meta-read", MODULE_HEADER_READ),
            ("case-meta-write", MODULE_HEADER_WRITE),
            (
                "change-construction-control-read",
                MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("change-lead-authority-read", MODULE_CHANGE_LEAD_AUTHORITY_READ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION_READ),
            ("distribution-read", MODULE_DISTRIBUTION_READ),
            ("documents-read", MODULE_DOCUMENTS_READ),
            (
                "documents-write",
                MODULE_DOCUMENTS_WRITE | MODULE_PORTAL_PAPER_DOCUMENTS_WRITE,
            ),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_PORTAL_SB1_READ),
            ("form-sb1-write", MODULE_PORTAL_PAPER_SB1_WRITE),
            ("form-sb1-submit", ACTION_PORTAL_PAPER_SB1_SUBMIT),
            ("form-sb2-read", MODULE_PORTAL_SB2_READ),
            ("form-sb2-write", MODULE_PORTAL_PAPER_SB2_WRITE),
            ("form-sb2-submit", ACTION_PORTAL_PAPER_SB2_SUBMIT),
            ("history-read", MODULE_HISTORY),
            ("information-of-neighbors-read", MODULE_INFORMATION_OF_NEIGHBORS_READ),
            (
                "instance-create-modification",
                ACTION_PORTAL_PAPER_INSTANCE_CREATE_MODIFICATION,
            ),
            (
                "instance-copy-after-rejection",
                ACTION_PORTAL_PAPER_INSTANCE_COPY_AFTER_REJECTION,
            ),
            ("instance-delete", ACTION_PORTAL_PAPER_INSTANCE_DELETE),
            ("instance-download-form-as-pdf", ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF),
            ("instance-extend-validity", ACTION_PORTAL_PAPER_INSTANCE_EXTEND_VALIDITY),
            (
                "instance-unsubscribe-responsible-service",
                ACTION_INSTANCE_UNSUBSCRIBE_LEAD_AUTHORITY,
            ),
            ("instance-submit", ACTION_PORTAL_PAPER_INSTANCE_SUBMIT),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS_READ),
            ("permissions-grant-geometer", MODULE_PERMISSIONS),
            ("permissions-grant-legal-authority", MODULE_PERMISSIONS),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-revoke-geometer", MODULE_PERMISSIONS),
            ("permissions-revoke-legal-authority", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION_READ),
            ("rejection-read", MODULE_REJECTION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("revision-history-read", MODULE_REVISION_HISTORY_READ),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "construction-control": [
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("applicant-read", MODULE_APPLICANTS_READ),
            ("case-meta-read", MODULE_HEADER_READ),
            (
                "change-construction-control-read",
                MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION_READ),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_SB1_READ),
            ("form-sb2-read", MODULE_SB2_READ),
            ("history-read", MODULE_HISTORY),
            (
                "instance-change-responsible-service",
                ACTION_INSTANCE_CHANGE_CONSTRUCTION_CONTROL,
            ),
            ("instance-download-form-as-pdf", ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("revision-history-read", MODULE_REVISION_HISTORY_READ),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "involved-construction-control": [
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("applicant-read", MODULE_APPLICANTS_READ),
            ("case-meta-read", MODULE_HEADER_READ),
            (
                "change-construction-control-read",
                MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION_READ),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_SB1_READ),
            ("form-sb2-read", MODULE_SB2_READ),
            ("history-read", MODULE_HISTORY),
            (
                "instance-unsubscribe-responsible-service",
                ACTION_INSTANCE_UNSUBSCRIBE_CONSTRUCTION_CONTROL,
            ),
            ("instance-download-form-as-pdf", ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            ("revision-history-read", MODULE_REVISION_HISTORY_READ),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        # TODO: Some form permissions were previously possible via API
        "support": [
            ("alexandria-write", SUPPORT_CONDITION),
            ("applicant-add", SUPPORT_CONDITION),
            ("applicant-read", SUPPORT_CONDITION),
            ("applicant-remove", SUPPORT_CONDITION),
            ("audit-log-read", SUPPORT_CONDITION),
            ("case-meta-read", SUPPORT_CONDITION),
            ("case-meta-write", SUPPORT_CONDITION),
            # TODO: Behavior change, support previously also allowed to
            # change construction control before decision
            (
                "change-construction-control-read",
                MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("change-lead-authority-read", MODULE_CHANGE_LEAD_AUTHORITY_READ),
            ("communications-read", STATES_ALL_INTERNAL),
            ("communications-delete-attachment", STATES_ALL_INTERNAL),
            ("support-read", SUPPORT_CONDITION),
            ("documents-read", SUPPORT_CONDITION),
            ("documents-write", SUPPORT_CONDITION),
            ("form-read", SUPPORT_CONDITION),
            ("form-write", SUPPORT_CONDITION),
            ("form-sb1-read", MODULE_PORTAL_SB1_READ),
            ("form-sb1-write", MODULE_PORTAL_SB1_READ),
            ("form-sb2-read", MODULE_PORTAL_SB2_READ),
            ("form-sb2-write", MODULE_PORTAL_SB2_READ),
            ("history-read", SUPPORT_CONDITION),
            ("instance-archive", INSTANCE_ARCHIVE_CONDITION),
            ("instance-change-ebau-number", STATES_ALL_INTERNAL),
            ("instance-change-form", SUPPORT_CONDITION),
            (
                "instance-change-responsible-service",
                MODULE_CHANGE_LEAD_AUTHORITY_READ
                | MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            (
                "instance-convert-modification",
                INSTANCE_CONVERT_MODIFICATION_CONDITION,
            ),
            (
                "instance-convert-to-building-permit",
                PORTAL_INSTANCE_CONVERT_TO_BUILDING_PERMIT_CONDITION,
            ),
            ("instance-copy", ACTION_SUPPORT_INSTANCE_COPY),
            ("instance-correct", INSTANCE_CORRECT_CONDITION),
            (
                "instance-create-modification",
                PORTAL_INSTANCE_CREATE_MODIFICATION_CONDITION,
            ),
            # TODO: Are they able to delete instance? Backend seems to prohibit it.
            ("instance-delete", PORTAL_INSTANCE_DELETE_CONDITION),
            ("instance-download-form-as-pdf", ACTION_PORTAL_INSTANCE_DOWNLOAD_AS_PDF),
            ("instance-extend-validity", PORTAL_INSTANCE_EXTEND_VALIDITY_CONDITION),
            (
                "instance-unsubscribe-responsible-service",
                MODULE_CHANGE_LEAD_AUTHORITY_READ
                | MODULE_CHANGE_CONSTRUCTION_CONTROL_READ,
            ),
            ("revision-history-read", SUPPORT_CONDITION),
        ],
        "distribution-service": [
            ("alexandria-write", MODULE_DOCUMENTS_WRITE),
            ("audit-read", MODULE_AUDIT_READ),
            ("billing-read", MODULE_BILLING_READ),
            ("billing-write", MODULE_BILLING_WRITE),
            ("case-meta-read", MODULE_HEADER_READ),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION_READ),
            ("distribution-read", MODULE_DISTRIBUTION_READ),
            ("documents-read", MODULE_DOCUMENTS_READ),
            ("documents-write", MODULE_DOCUMENTS_WRITE),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM_READ),
            ("form-sb1-read", MODULE_SB1_READ),
            ("form-sb2-read", MODULE_SB2_READ),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS_READ),
            ("responsible-read", MODULE_RESPONSIBLE_READ),
            ("responsible-write", MODULE_RESPONSIBLE_WRITE),
            (
                "revision-history-read",
                STATES_INTERNAL_NO_CORRECTION & ROLES_INTERNAL_NO_READONLY,
            ),
            ("tags-read", MODULE_HEADER_READ),
            ("tags-write", MODULE_HEADER_WRITE),
            ("work-items-read", MODULE_WORK_ITEMS),
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
