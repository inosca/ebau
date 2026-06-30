from camac.permissions.conditions import (
    Always,
    HasApplicantConfirmationRound,
    HasApplicantRole,
    HasRole,
    IsServiceGroup,
    RequireInstanceState,
    RequireWorkItem,
    Static,
)
from camac.permissions.switcher import PERMISSION_MODE

# Instance state rules
STATES_ALL = RequireInstanceState(
    [
        "new",
        "subm",
        "rejected",
        "init-distribution",
        "distribution",
        "decision",
        "decided",
        "construction-monitoring",
        "to-finish",
        "finished",
    ]
)

# Role rules
APPLICANT_ADMIN = HasApplicantRole(["ADMIN"])
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
MODULE_ADDITIONAL_DEMANDS = RequireWorkItem("init-additional-demand")
MODULE_BILLING = STATES_ALL
MODULE_COMMUNICATIONS = STATES_ALL
MODULE_COMPLETE_INSTANCE = RequireWorkItem("complete-instance", "ready")
MODULE_CONSTRUCTION_MONITORING = RequireWorkItem("init-construction-monitoring")
MODULE_CONSTRUCTION_MONITORING_COMPLETE = (
    MODULE_CONSTRUCTION_MONITORING
    & RequireInstanceState(["decided", "construction-monitoring"])
)
MODULE_CONSTRUCTION_MONITORING_SKIP = MODULE_CONSTRUCTION_MONITORING_COMPLETE
MODULE_DECISION = (RequireWorkItem("decision") & ROLES_MUNICIPALITY) | RequireWorkItem(
    "decision", "completed"
)
MODULE_DISTRIBUTION = RequireWorkItem("distribution")
MODULE_DMS_GENERATE = STATES_ALL
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL
MODULE_FORMAL_EXAM = (
    RequireWorkItem("formal-exam") & ROLES_MUNICIPALITY
) | RequireWorkItem("formal-exam", "completed")
MODULE_HISTORY = STATES_ALL
MODULE_INFORMATION_OF_NEIGHBORS = RequireWorkItem(
    "create-information-of-neighbors"
) | RequireWorkItem("fill-information-of-neighbors")
MODULE_JOURNAL = STATES_ALL
MODULE_LINKED_INSTANCES = STATES_ALL
MODULE_MATERIAL_EXAM = (
    RequireWorkItem("material-exam") & ROLES_MUNICIPALITY
) | RequireWorkItem("material-exam", "completed")
MODULE_PERMISSIONS = STATES_ALL & ROLES_MUNICIPALITY
MODULE_PUBLICATION = RequireWorkItem("create-publication") | RequireWorkItem(
    "fill-publication"
)
MODULE_REJECTION = RequireInstanceState(["subm", "rejected"])
MODULE_RESPONSIBLE = STATES_ALL
MODULE_WORK_ITEMS = STATES_ALL

MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = (
    MODULE_PORTAL_ADDITIONAL_DEMANDS_READ & APPLICANT_WRITE
)
MODULE_PORTAL_APPLICANTS = APPLICANT_ADMIN
MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = MODULE_PORTAL_COMMUNICATIONS_READ & APPLICANT_WRITE
MODULE_PORTAL_CONSTRUCTION_MONITORING_READ = RequireWorkItem("construction-stage")
MODULE_PORTAL_CONSTRUCTION_MONITORING_WRITE = (
    MODULE_PORTAL_CONSTRUCTION_MONITORING_READ & APPLICANT_WRITE
)
MODULE_PORTAL_DOCUMENTS_WRITE = (
    RequireWorkItem("submit", "ready") & APPLICANT_WRITE
) | MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = (
    RequireWorkItem("submit", "ready")
    & APPLICANT_WRITE
    & ~HasApplicantConfirmationRound(["running", "completed"])
)

ACTION_APPLICANT_CONFIRMATION_ADMIN = (
    RequireWorkItem("submit", "ready") & APPLICANT_ADMIN
)
ACTION_APPLICANT_CONFIRMATION_CONFIRM = RequireWorkItem("submit", "ready")

ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & APPLICANT_ADMIN
ACTION_INSTANCE_MARK = IsServiceGroup(["coordination"])
ACTION_INSTANCE_SUBMIT = (
    RequireWorkItem("submit", "ready")
    & APPLICANT_ADMIN
    & HasApplicantConfirmationRound(["completed"])
)
ACTION_INSTANCE_WITHDRAW = (
    RequireWorkItem("withdrawal-request", ["ready", "completed"]) & APPLICANT_ADMIN
)

# Actual config
SG_PERMISSIONS_SETTINGS = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("additional-demands-read", MODULE_PORTAL_ADDITIONAL_DEMANDS_READ),
            ("additional-demands-write", MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE),
            ("applicant-confirmation-cancel", ACTION_APPLICANT_CONFIRMATION_ADMIN),
            ("applicant-confirmation-confirm", ACTION_APPLICANT_CONFIRMATION_CONFIRM),
            ("applicant-confirmation-invalidate", ACTION_APPLICANT_CONFIRMATION_ADMIN),
            ("applicant-confirmation-read", Static()),
            ("applicant-confirmation-start", ACTION_APPLICANT_CONFIRMATION_ADMIN),
            ("applicant-add", MODULE_PORTAL_APPLICANTS),
            ("applicant-read", MODULE_PORTAL_APPLICANTS),
            ("applicant-remove", MODULE_PORTAL_APPLICANTS),
            ("communications-read", MODULE_PORTAL_COMMUNICATIONS_READ),
            ("communications-write", MODULE_PORTAL_COMMUNICATIONS_WRITE),
            (
                "construction-monitoring-read",
                MODULE_PORTAL_CONSTRUCTION_MONITORING_READ,
            ),
            (
                "construction-monitoring-write",
                MODULE_PORTAL_CONSTRUCTION_MONITORING_WRITE,
            ),
            ("documents-write", MODULE_PORTAL_DOCUMENTS_WRITE),
            ("form-read", MODULE_PORTAL_FORM_READ),
            ("form-write", MODULE_PORTAL_FORM_WRITE),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),
        ],
        "distribution-service": [
            ("billing-read", MODULE_BILLING),
            ("billing-write", MODULE_BILLING),
            ("billing-charge", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("formal-exam-read", MODULE_FORMAL_EXAM),
            ("material-exam-read", MODULE_MATERIAL_EXAM),
            ("history-read", MODULE_HISTORY),
            ("instance-mark-write", ACTION_INSTANCE_MARK),
            ("journal-read", MODULE_JOURNAL),
            ("journal-write", MODULE_JOURNAL),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("responsible-write", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS),
            ("applicant-confirmation-read", Static()),
            ("billing-read", MODULE_BILLING),
            ("billing-write", MODULE_BILLING),
            ("billing-charge", MODULE_BILLING),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("complete-instance-read", MODULE_COMPLETE_INSTANCE),
            (
                "construction-monitoring-complete",
                MODULE_CONSTRUCTION_MONITORING_COMPLETE,
            ),
            ("construction-monitoring-init", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-skip", MODULE_CONSTRUCTION_MONITORING_SKIP),
            ("construction-monitoring-write", MODULE_CONSTRUCTION_MONITORING),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("formal-exam-read", MODULE_FORMAL_EXAM),
            ("formal-exam-write", MODULE_FORMAL_EXAM),
            ("material-exam-read", MODULE_MATERIAL_EXAM),
            ("material-exam-write", MODULE_MATERIAL_EXAM),
            ("history-read", MODULE_HISTORY),
            ("information-of-neighbors-read", MODULE_INFORMATION_OF_NEIGHBORS),
            ("instance-mark-write", ACTION_INSTANCE_MARK),
            ("journal-read", MODULE_JOURNAL),
            ("journal-write", MODULE_JOURNAL),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION),
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
            ("applicant-confirmation-read", Static()),
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
