from camac.permissions.conditions import (
    Always,
    Callback,
    HasApplicantRole,
    HasRole,
    IsPaper,
    IsServiceGroup,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

# Instance state rules
STATES_ALL = RequireInstanceState(
    [
        "new",
        "subm",
        "circulation",
        "finished",
        "decision",
        "init-distribution",
        "construction-acceptance",
        "rejected",
        "withdrawal",
        "withdrawn",
    ]
)
NO_CORRECTION = ~RequireInstanceState(["correction"])

# Role rules
ROLES_NO_READONLY = ~HasRole(
    ["municipality-read", "service-read", "trusted-service-read"]
)
ROLES_MUNICIPALITY = HasRole(["municipality-lead", "municipality-clerk"])

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state / work item rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_ADDITIONAL_DEMANDS = NO_CORRECTION & RequireWorkItem("init-additional-demand")
MODULE_AUDIT = NO_CORRECTION & (
    (RequireWorkItem("formal-exam") & ROLES_MUNICIPALITY)
    | RequireWorkItem("formal-exam", "completed")
)
MODULE_BILLING = (
    STATES_ALL
    & ROLES_NO_READONLY
    & IsServiceGroup(["municipality", "service-cantonal", "service-afb"])
)
MODULE_CANTONAL_EXAM = RequireWorkItem("cantonal-exam") & (
    Callback(
        lambda userinfo: userinfo.service.slug == "afb",
        allow_caching=True,
        name="is_afb",
    )
)
MODULE_COMMUNICATIONS = STATES_ALL & ROLES_NO_READONLY
MODULE_CORRECTIONS = (
    STATES_ALL | RequireInstanceState(["correction"])
) & ROLES_NO_READONLY
MODULE_DECISION = NO_CORRECTION & (
    (RequireWorkItem("decision") & ROLES_MUNICIPALITY)
    | RequireWorkItem("decision", "completed")
)
MODULE_DISTRIBUTION = NO_CORRECTION & RequireWorkItem("distribution")
MODULE_DMS_GENERATE = STATES_ALL & ROLES_NO_READONLY
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL | RequireInstanceState(["correction"])
MODULE_HISTORY = STATES_ALL
MODULE_INFORMATION_OF_NEIGHBORS = NO_CORRECTION & RequireWorkItem(
    "fill-information-of-neighbors"
)
MODULE_JOURNAL = STATES_ALL
MODULE_LINKED_INSTANCES = STATES_ALL
MODULE_LEGAL_SUBMISSIONS = NO_CORRECTION & RequireWorkItem("objections")
MODULE_PERMISSIONS = STATES_ALL & HasRole(["municipality-lead"])
MODULE_PUBLICATION = NO_CORRECTION & RequireWorkItem("fill-publication")
MODULE_REJECTION = RequireInstanceState(["subm", "rejected"])
MODULE_RESPONSIBLE = STATES_ALL & ROLES_NO_READONLY
MODULE_WORK_ITEMS = STATES_ALL & ROLES_NO_READONLY

MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = (
    MODULE_PORTAL_ADDITIONAL_DEMANDS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])
MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_DOCUMENTS_WRITE = (
    RequireWorkItem("submit", "ready")
    | RequireWorkItem("fill-additional-demand", "ready")
) & HasApplicantRole(["ADMIN", "EDITOR"])
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN", "EDITOR"]) | (ROLES_MUNICIPALITY & IsPaper())
)

ACTION_INSTANCE_COPY_AFTER_REJECTION = RequireInstanceState(
    ["rejected"]
) & HasApplicantRole(["ADMIN"])
ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & HasApplicantRole(["ADMIN"])
ACTION_INSTANCE_SUBMIT = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_CHANGE_FORM = RequireInstanceState(
    [
        "subm",
        "init-distribution",
        "circulation",
        "correction",
    ]
)

ACTION_INSTANCE_WITHDRAW = RequireInstanceState(
    [
        "subm",
        "init-distribution",
        "circulation",
        "correction",
        "decision",
    ]
) & HasApplicantRole(["ADMIN"])

# Actual config
AG_PERMISSIONS_SETTINGS = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("additional-demands-read", MODULE_PORTAL_ADDITIONAL_DEMANDS_READ),
            ("additional-demands-write", MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE),
            ("applicant-add", MODULE_PORTAL_APPLICANTS),
            ("applicant-read", MODULE_PORTAL_APPLICANTS),
            ("applicant-remove", MODULE_PORTAL_APPLICANTS),
            ("communications-read", MODULE_PORTAL_COMMUNICATIONS_READ),
            ("communications-write", MODULE_PORTAL_COMMUNICATIONS_WRITE),
            ("documents-write", MODULE_PORTAL_DOCUMENTS_WRITE),
            ("form-read", MODULE_PORTAL_FORM_READ),
            ("form-write", MODULE_PORTAL_FORM_WRITE),
            ("instance-copy-after-rejection", ACTION_INSTANCE_COPY_AFTER_REJECTION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),
        ],
        "distribution-service": [
            ("billing-read", MODULE_BILLING),
            (
                "billing-charge",
                MODULE_BILLING
                & IsServiceGroup(["service-afb"])
                & ~HasRole("subservice"),
            ),
            ("cantonal-exam-read", MODULE_CANTONAL_EXAM),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-kantonale-pruefung-write", MODULE_CANTONAL_EXAM),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS),
            ("audit-read", MODULE_AUDIT),
            ("billing-read", MODULE_BILLING),
            ("billing-charge", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("corrections-read", MODULE_CORRECTIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            (
                "form-write",
                MODULE_PORTAL_FORM_WRITE
                | (RequireInstanceState(["correction"]) & ROLES_MUNICIPALITY),
            ),
            ("history-read", MODULE_HISTORY),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            ("information-of-neighbors-read", MODULE_INFORMATION_OF_NEIGHBORS),
            ("journal-read", MODULE_JOURNAL),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("legal-submissions-write", MODULE_LEGAL_SUBMISSIONS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION),
            ("rejection-read", MODULE_REJECTION),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
            ("instance-change-form", ACTION_INSTANCE_CHANGE_FORM),
            ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),
        ],
        "read": [
            ("documents-read", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
        ],
        "support": [
            ("applicant-add", Always()),
            ("applicant-read", Always()),
            ("applicant-remove", Always()),
            ("documents-read", Always()),
            ("documents-write", Always()),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("form-read", Always()),
            ("form-write", Always()),
            ("history-read", Always()),
            ("instance-delete", RequireInstanceState(["new"])),
            ("permissions-read-any", Always()),
            ("permissions-read", Always()),
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_ag.PermissionEventHandlerAG",
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "SUPPORT": "support",
    },
    "ENABLE_CACHE": env.bool("PERMISSION_MODULE_ENABLE_CACHE", default=True),
    "PERMISSION_MODE": getattr(
        PERMISSION_MODE, env.str("PERMISSION_MODULE_MODE", default="FULL")
    ),
}
