from camac.constants.kt_gr import BAUGESUCH_FORMS, SOLARANLAGE_FORMS
from camac.permissions.conditions import (
    Always,
    HasApplicantRole,
    HasRole,
    IsForm,
    IsPaper,
    IsServiceGroup,
    Never,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

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
        "withdrawal",
        "withdrawn",
        "rejected",
    ]
)
STATES_ACCESSIBLE = STATES_ALL & ~RequireInstanceState(["rejected"])
STATES_POST_DECISION = RequireInstanceState(["construction-acceptance", "finished"])

# Form rules
FORMS_ONLY_BUILDING_PERMIT = IsForm([*BAUGESUCH_FORMS, *SOLARANLAGE_FORMS])

# Role rules
ROLES_MUNICIPALITY = HasRole(["municipality-lead"])
ROLES_GEOMETER = HasRole(["geometer"])

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_ADDITIONAL_DEMANDS = STATES_ALL & RequireWorkItem("init-additional-demand")

MODULE_CONSTRUCTION_ACCEPTANCE = RequireWorkItem("construction-acceptance")
MODULE_CONSTRUCTION_MONITORING = (
    RequireWorkItem("init-construction-monitoring") | ROLES_GEOMETER
)
MODULE_COMMUNICATIONS = STATES_ALL
MODULE_CORRECTIONS = (
    STATES_ALL | RequireInstanceState(["correction"])
) & ROLES_MUNICIPALITY
MODULE_DECISION = (ROLES_MUNICIPALITY & RequireWorkItem("decision")) | (
    ~ROLES_MUNICIPALITY & RequireWorkItem("decision", "completed")
)
MODULE_DISTRIBUTION = RequireWorkItem("init-distribution")
MODULE_DMS_GENERATE = STATES_ALL
MODULE_DOCUMENTS = STATES_ALL | (
    RequireInstanceState(["new"]) & ROLES_MUNICIPALITY & IsPaper()
)
MODULE_FORM = (
    STATES_ALL
    | RequireInstanceState(["correction"])
    | (RequireInstanceState(["new"]) & ROLES_MUNICIPALITY & IsPaper())
)
MODULE_AUDIT = (ROLES_MUNICIPALITY & RequireWorkItem("formal-exam")) | (
    ~ROLES_MUNICIPALITY & RequireWorkItem("formal-exam", "completed")
)
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL = STATES_ALL
MODULE_LEGAL_SUBMISSIONS = IsForm(BAUGESUCH_FORMS) & (
    RequireWorkItem("objections", addressed_to_current_service=True)
    | IsServiceGroup(["authority-bab"])
)
MODULE_LEGAL_APPEALS = IsForm(BAUGESUCH_FORMS) & (
    RequireWorkItem("appeals", addressed_to_current_service=True)
    | IsServiceGroup(["authority-bab"])
)
MODULE_LINKED_INSTANCES = STATES_ALL
MODULE_PERMISSIONS = STATES_ALL
MODULE_PUBLICATION = RequireWorkItem("fill-publication")
MODULE_REJECTION = STATES_ALL
MODULE_RELATED_GWR_PROJECTS = STATES_ALL & FORMS_ONLY_BUILDING_PERMIT
MODULE_RESPONSIBLE = STATES_ALL
MODULE_WORK_ITEMS = STATES_ALL
MODULE_ADDRESS_ASSIGNMENT = STATES_ALL & (
    RequireWorkItem("address-assignment-make-suggestion")
    | RequireWorkItem("address-assignment-confirm-suggestion")
)

MODULE_DEADLINES_SUSPENSION = Never()
# Disabled for prod release
# MODULE_DEADLINES_SUSPENSION = (
#     STATES_ALL
#     & IsServiceGroup(["municipality", ARE_SERVICE_GROUP])
#     & HasRole(["municipality-lead", "service-lead"])
# )
MODULE_DEADLINES_DEADLINE = Never()
# Disabled for prod release
# MODULE_DEADLINES_DEADLINE = (
#     STATES_ALL
#     & IsServiceGroup(["municipality", ARE_SERVICE_GROUP])
#     & HasRole(["municipality-lead", "service-lead"])
# )

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
MODULE_PORTAL_CONSTRUCTION_MONITORING_READ = RequireWorkItem("construction-stage")
MODULE_PORTAL_CONSTRUCTION_MONITORING_WRITE = (
    MODULE_PORTAL_CONSTRUCTION_MONITORING_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)

ACTION_INSTANCE_CREATE_MODIFICATION = (
    HasApplicantRole(["ADMIN"])
    & STATES_POST_DECISION
    & IsForm(BAUGESUCH_FORMS)
    & (
        RequireWorkItem("construction-acceptance")
        | RequireWorkItem("init-construction-monitoring")
    )
) | (ROLES_MUNICIPALITY & IsPaper())
ACTION_INSTANCE_CREATE_ADDITIONAL_DEMAND = (
    MODULE_ADDITIONAL_DEMANDS
    & RequireInstanceState(["subm", "init-distribution", "circulation", "decision"])
)
ACTION_INSTANCE_COPY_AFTER_REJECTION = RequireInstanceState(["rejected"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF = STATES_ALL | RequireInstanceState(["correction"])

ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_SUBMIT = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)

ACTION_INSTANCE_WITHDRAW = RequireInstanceState(
    [
        "subm",
        "init-distribution",
        "circulation",
        "correction",
        "decision",
    ]
) & (HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper()))

GR_PERMISSIONS_SETTINGS = {
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
            ("instance-copy-after-rejection", ACTION_INSTANCE_COPY_AFTER_REJECTION),
            ("instance-create-modification", ACTION_INSTANCE_CREATE_MODIFICATION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            # ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),  # needs to be commented out otherwise module is shown in portal
        ],
        "distribution-service": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", ACTION_INSTANCE_CREATE_ADDITIONAL_DEMAND),
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
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("journal-read", MODULE_JOURNAL),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("legal-appeals-read", MODULE_LEGAL_APPEALS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
            ("address-assignment-read", MODULE_ADDRESS_ASSIGNMENT),
            ("deadlines-suspensions-read", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-suspensions-write", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-deadlines-read", MODULE_DEADLINES_DEADLINE),
            ("deadlines-deadlines-write", MODULE_DEADLINES_DEADLINE),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", ACTION_INSTANCE_CREATE_ADDITIONAL_DEMAND),
            ("audit-read", MODULE_AUDIT),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("construction-acceptance-read", MODULE_CONSTRUCTION_ACCEPTANCE),
            ("construction-acceptance-write", MODULE_CONSTRUCTION_ACCEPTANCE),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-write", MODULE_CONSTRUCTION_MONITORING),
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
            ("instance-copy-after-rejection", ACTION_INSTANCE_COPY_AFTER_REJECTION),
            ("instance-create-modification", ACTION_INSTANCE_CREATE_MODIFICATION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            # ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),  # needs to be commented out otherwise module is shown in portal
            ("journal-read", MODULE_JOURNAL),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("legal-submissions-write", MODULE_LEGAL_SUBMISSIONS),
            ("legal-appeals-read", MODULE_LEGAL_APPEALS),
            ("legal-appeals-write", MODULE_LEGAL_APPEALS),
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
            ("address-assignment-read", MODULE_ADDRESS_ASSIGNMENT),
            ("deadlines-suspensions-read", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-suspensions-write", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-deadlines-read", MODULE_DEADLINES_DEADLINE),
            ("deadlines-deadlines-write", MODULE_DEADLINES_DEADLINE),
        ],
        "read": [
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
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
            ("legal-submissions-read", Always()),
            ("history-read", Always()),
            ("instance-delete", RequireInstanceState(["new"])),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("permissions-read-any", Always()),
            ("permissions-read", Always()),
            ("publication-read", MODULE_PUBLICATION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", Always()),
            ("work-items-read", Always()),
            ("address-assignment-read", Always()),
            ("address-assignment-write", Always()),
        ],
        "uso": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "geometer": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("form-read", MODULE_FORM),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_FORM_AS_PDF,
            ),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("work-items-read", MODULE_WORK_ITEMS),
            ("address-assignment-read", MODULE_ADDRESS_ASSIGNMENT),
            ("address-assignment-write", MODULE_ADDRESS_ASSIGNMENT),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-write", MODULE_CONSTRUCTION_MONITORING),
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_gr.PermissionEventHandlerGR",
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "DISTRIBUTION_INVITEE": "distribution-service",
        "SUPPORT": "support",
        "USO": "uso",
    },
    "ENABLE_CACHE": env.bool("PERMISSION_MODULE_ENABLE_CACHE", default=True),
    "PERMISSION_MODE": PERMISSION_MODE.FULL,
}
