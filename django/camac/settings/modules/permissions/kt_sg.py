from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE

# Instance state rules
STATES_ALL = RequireInstanceState(["new", "subm", "rejected"])

# Role rules
APPLICANT_ADMIN = HasApplicantRole(["ADMIN", "EDITOR"])
APPLICANT_WRITE = HasApplicantRole(["ADMIN", "EDITOR"])
ROLES_MUNICIPALITY = HasRole(["municipality-lead"])

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state / work item rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_COMMUNICATIONS = STATES_ALL
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL
MODULE_FORMAL_EXAM = RequireWorkItem("formal-exam") & ROLES_MUNICIPALITY
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL = STATES_ALL
MODULE_PERMISSIONS = STATES_ALL & ROLES_MUNICIPALITY
MODULE_REJECTION = RequireInstanceState(["subm", "rejected"])
MODULE_RESPONSIBLE = STATES_ALL
MODULE_WORK_ITEMS = STATES_ALL

MODULE_PORTAL_APPLICANTS = APPLICANT_ADMIN
MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_DOCUMENTS_WRITE = RequireWorkItem("submit", "ready") & APPLICANT_WRITE
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireWorkItem("submit", "ready") & APPLICANT_WRITE

ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & APPLICANT_ADMIN
ACTION_INSTANCE_SUBMIT = RequireWorkItem("submit", "ready") & APPLICANT_ADMIN

# Actual config
SG_PERMISSIONS_SETTINGS = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("applicant-add", MODULE_PORTAL_APPLICANTS),
            ("applicant-read", MODULE_PORTAL_APPLICANTS),
            ("applicant-remove", MODULE_PORTAL_APPLICANTS),
            ("communications-read", MODULE_PORTAL_COMMUNICATIONS_READ),
            ("communications-write", MODULE_PORTAL_COMMUNICATIONS_WRITE),
            ("documents-write", MODULE_PORTAL_DOCUMENTS_WRITE),
            ("form-read", MODULE_PORTAL_FORM_READ),
            ("form-write", MODULE_PORTAL_FORM_WRITE),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
        ],
        "distribution-service": [
            ("form-read", MODULE_FORM),
        ],
        "lead-authority": [
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("formal-exam-read", MODULE_FORMAL_EXAM),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("journal-write", MODULE_JOURNAL),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("rejection-read", MODULE_REJECTION),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("responsible-write", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
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
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_sg.PermissionEventHandlerSG",
    "PERMISSION_MODE": PERMISSION_MODE.FULL,
}
