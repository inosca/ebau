from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    IsForm,
    IsPaper,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE

# Instance state rules
STATES_ALL = RequireInstanceState(
    [
        "subm",
        "init-distribution",
        "circulation",
        "decision",
        "construction-acceptance",
        "finished",
        # Special cases
        "rejected",
    ]
)
STATES_ACCESSIBLE = STATES_ALL & ~RequireInstanceState(["rejected"])
STATES_POST_DECISION = RequireInstanceState(["construction-acceptance", "finished"])

# Form rules
FORMS_ONLY_BUILDING_PERMIT = IsForm(["baugesuch", "solaranlage"])

# Role rules
ROLES_MUNICIPALITY = HasRole(["municipality-lead"])

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_ADDITIONAL_DEMANDS = (
    STATES_ALL & ~RequireInstanceState(["subm"]) & ~IsForm(["vorlaeufige-beurteilung"])
)  # TODO bauanzeige?
MODULE_CONSTRUCTION_MONITORING = RequireWorkItem("construction-acceptance")
MODULE_COMMUNICATIONS = STATES_ALL
MODULE_CORRECTIONS = (
    STATES_ALL | RequireInstanceState(["correction"])
) & ROLES_MUNICIPALITY
MODULE_DECISION = (ROLES_MUNICIPALITY & RequireWorkItem("decision")) | (
    ~ROLES_MUNICIPALITY & RequireWorkItem("decision", "completed")
)
MODULE_DISTRIBUTION = RequireWorkItem("init-distribution")
MODULE_DMS_GENERATE = STATES_ALL
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL | RequireInstanceState(["correction"])
MODULE_AUDIT = (ROLES_MUNICIPALITY & RequireWorkItem("formal-exam")) | (
    ~ROLES_MUNICIPALITY & RequireWorkItem("formal-exam", "completed")
)
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL = STATES_ALL
MODULE_LINKED_INSTANCES = STATES_ALL
MODULE_PERMISSIONS = STATES_ALL
MODULE_PUBLICATION = RequireWorkItem("fill-publication")
MODULE_REJECTION = STATES_ALL
MODULE_RELATED_GWR_PROJECTS = STATES_ALL & FORMS_ONLY_BUILDING_PERMIT
MODULE_RESPONSIBLE = STATES_ALL
MODULE_WORK_ITEMS = STATES_ALL

MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])
MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN", "EDITOR"]) | (ROLES_MUNICIPALITY & IsPaper())
)
MODULE_PORTAL_DOCUMENTS_WRITE = (
    RequireInstanceState(["new"]) | RequireWorkItem("fill-additional-demand", "ready")
) & (HasApplicantRole(["ADMIN", "EDITOR"]) | (ROLES_MUNICIPALITY & IsPaper()))
MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = (
    MODULE_PORTAL_ADDITIONAL_DEMANDS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)

ACTION_INSTANCE_CREATE_MODIFICATION = (
    HasApplicantRole(["ADMIN"]) & ~RequireInstanceState(["new"]) & IsForm(["baugesuch"])
) | (ROLES_MUNICIPALITY & IsPaper())

ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_SUBMIT = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)

GR_PERMISSIONS_SETTINGS = {
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
            ("instance-create-modification", ACTION_INSTANCE_CREATE_MODIFICATION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
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
            ("audit-read", MODULE_AUDIT),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("rejection-read", MODULE_REJECTION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "distribution-service": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS),
            ("audit-read", MODULE_AUDIT),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
        ],
        "support": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("applicant-add", Always()),
            ("applicant-read", Always()),
            ("applicant-remove", Always()),
            ("audit-read", RequireWorkItem("formal-exam")),
            ("communications-read", Always()),
            ("decision-read", RequireWorkItem("decision")),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", Always()),
            ("documents-read", Always()),
            ("documents-write", Always()),
            ("form-read", Always()),
            ("history-read", Always()),
            ("instance-delete", RequireInstanceState(["new"])),
            ("permissions-read-any", Always()),
            ("permissions-read", Always()),
            ("publication-read", MODULE_PUBLICATION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", Always()),
            ("work-items-read", Always()),
            # TODO still incomplete
        ],
        "uso": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_gr.PermissionEventHandlerGR",
    "ENABLED": True,
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "DISTRIBUTION_INVITEE": "distribution-service",
        "SUPPORT": "support",
        "USO": "uso",
    },
    "ENABLE_CACHE": False,
    "PERMISSION_MODE": PERMISSION_MODE.OFF,
}
