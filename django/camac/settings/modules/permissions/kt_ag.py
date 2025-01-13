from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

# Instance state rules
STATES_ALL = RequireInstanceState(
    [
        "subm",
        "circulation",
        "finished",
        "decision",
        "init-distribution",
        "construction-acceptance",
        "rejected",
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
MODULE_AUDIT = NO_CORRECTION & (
    (RequireWorkItem("formal-exam") & ROLES_MUNICIPALITY)
    | RequireWorkItem("formal-exam", "completed")
)
MODULE_CORRECTIONS = (
    STATES_ALL | RequireInstanceState(["correction"])
) & ROLES_NO_READONLY
MODULE_DMS_GENERATE = STATES_ALL & ROLES_NO_READONLY
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL | RequireInstanceState(["correction"])
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL = STATES_ALL
MODULE_PERMISSIONS = STATES_ALL & HasRole(["municipality-lead"])
MODULE_RESPONSIBLE = STATES_ALL & ROLES_NO_READONLY
MODULE_WORK_ITEMS = STATES_ALL & ROLES_NO_READONLY

MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])
MODULE_PORTAL_DOCUMENTS_WRITE = RequireWorkItem("submit", "ready") & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireWorkItem("submit", "ready") & HasApplicantRole(
    ["ADMIN", "EDITOR"]
)

ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & HasApplicantRole(["ADMIN"])
ACTION_INSTANCE_SUBMIT = RequireWorkItem("submit", "ready") & HasApplicantRole(
    ["ADMIN"]
)

# Actual config
AG_PERMISSIONS_SETTINGS = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("applicant-add", MODULE_PORTAL_APPLICANTS),
            ("applicant-read", MODULE_PORTAL_APPLICANTS),
            ("applicant-remove", MODULE_PORTAL_APPLICANTS),
            ("documents-write", MODULE_PORTAL_DOCUMENTS_WRITE),
            ("form-read", MODULE_PORTAL_FORM_READ),
            ("form-write", MODULE_PORTAL_FORM_WRITE),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
        ],
        "lead-authority": [
            ("audit-read", MODULE_AUDIT),
            ("corrections-read", MODULE_CORRECTIONS),
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
            ("journal-read", MODULE_JOURNAL),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
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
