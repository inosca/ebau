from camac.permissions.conditions import (
    Always,
    Callback,
    HasApplicantRole,
    HasRole,
    IsAppeal,
    IsPaper,
    IsServiceGroup,
    IsUnversionedForm,
    RequireInstanceState,
    RequireWorkItem,
)
from camac.permissions.switcher import PERMISSION_MODE

# Instance state rules
STATES_ALL = RequireInstanceState(
    [
        "subm",
        "material-exam",
        "init-distribution",
        "distribution",
        "decision",
        "decided",
        "construction-monitoring",
        "finished",
        # Special cases
        "withdrawal",
        "withdrawn",
        "reject",
        "rejected",
    ]
)
NO_CORRECTION = ~RequireInstanceState(["correction"])

# Role rules
ROLES_NO_READONLY = ~HasRole(["municipality-read", "service-read"])
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
MODULE_ADDITIONAL_DEMANDS = NO_CORRECTION & (
    # We need to check the form here because the work item will exists in
    # preliminary clarification as we allow a distribution. However, only a
    # distribution is allowed but no additional demands.
    RequireWorkItem("init-additional-demand")
    & ~IsUnversionedForm(["voranfrage"])
    & ~IsAppeal()
)
MODULE_APPEAL = (
    NO_CORRECTION
    & RequireWorkItem("appeal")
    & (
        ROLES_MUNICIPALITY
        | (
            IsServiceGroup(["service-bab"])
            & Callback(
                lambda instance: instance.case.meta.get("is-bab", False),
                allow_caching=True,
                name="is_bab",
            )
        )
    )
)
MODULE_BILLING = STATES_ALL & ROLES_NO_READONLY
MODULE_COMMUNICATIONS = STATES_ALL & ROLES_NO_READONLY
MODULE_COMPLETE_INSTANCE = (
    RequireWorkItem("complete-instance", "ready") & ROLES_NO_READONLY
)
MODULE_CONSTRUCTION_MONITORING = (
    RequireWorkItem("init-construction-monitoring") & ROLES_NO_READONLY
)
MODULE_CORRECTIONS = (
    STATES_ALL | RequireInstanceState(["correction"])
) & ROLES_NO_READONLY
MODULE_DECISION = NO_CORRECTION & (
    (RequireWorkItem("decision") & ROLES_MUNICIPALITY)
    | RequireWorkItem("decision", "completed")
)
MODULE_DISTRIBUTION = NO_CORRECTION & RequireWorkItem("distribution")
MODULE_DMS_GENERATE = STATES_ALL & ROLES_NO_READONLY
MODULE_DOCUMENTS = STATES_ALL | (
    RequireInstanceState(["new"]) & ROLES_MUNICIPALITY & IsPaper()
)
MODULE_FORM = (
    STATES_ALL
    | RequireInstanceState(["correction"])
    | (RequireInstanceState(["new"]) & ROLES_MUNICIPALITY & IsPaper())
)
MODULE_FORMAL_EXAM = NO_CORRECTION & (
    (RequireWorkItem("formal-exam") & ROLES_MUNICIPALITY)
    | RequireWorkItem("formal-exam", "completed")
)
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL_READ = STATES_ALL
MODULE_JOURNAL_WRITE = MODULE_JOURNAL_READ & ROLES_NO_READONLY
MODULE_LEGAL_SUBMISSIONS = NO_CORRECTION & RequireWorkItem("objections")
MODULE_LINKED_INSTANCES = STATES_ALL
MODULE_MATERIAL_EXAM = NO_CORRECTION & (
    (RequireWorkItem("material-exam") & ROLES_MUNICIPALITY)
    | RequireWorkItem("material-exam", "completed")
)
MODULE_MATERIAL_EXAM_BAB = (
    NO_CORRECTION
    & RequireWorkItem("material-exam-bab")
    & IsServiceGroup(["service-bab", "service-cantonal", "canton"])
)
MODULE_AFU_CHECK_READ = RequireWorkItem("afu-form") & Callback(
    lambda userinfo: (
        userinfo.service.slug == "afu"
        or userinfo.service.service_parent is not None
        and userinfo.service.service_parent.slug == "afu"
    ),
    allow_caching=True,
    name="is_afu_or_subservice",
)
MODULE_AFU_CHECK_WRITE = MODULE_AFU_CHECK_READ & ~RequireInstanceState(["finished"])

MODULE_PERMISSIONS = STATES_ALL & HasRole(["municipality-lead"])
MODULE_PUBLICATION = NO_CORRECTION & RequireWorkItem("fill-publication")
MODULE_REJECTION = RequireWorkItem("reject") & ROLES_NO_READONLY
MODULE_RELATED_GWR_PROJECTS = (
    (
        STATES_ALL
        & ~RequireInstanceState(["subm", "material-exam", "reject", "rejected"])
    )
    & IsUnversionedForm(["baugesuch", "migriertes-dossier"])
    & ROLES_MUNICIPALITY
    & ~IsAppeal()
)
MODULE_RESPONSIBLE = STATES_ALL & ROLES_NO_READONLY
MODULE_WORK_ITEMS = STATES_ALL & ROLES_NO_READONLY

MODULE_PORTAL_APPLICANTS = HasApplicantRole(["ADMIN"])
MODULE_PORTAL_COMMUNICATIONS_READ = ~RequireInstanceState(["new"])
MODULE_PORTAL_COMMUNICATIONS_WRITE = (
    MODULE_PORTAL_COMMUNICATIONS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_FORM_READ = Always()
MODULE_PORTAL_FORM_WRITE = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN", "EDITOR"]) | (ROLES_MUNICIPALITY & IsPaper())
)
MODULE_PORTAL_DOCUMENTS_WRITE = (
    RequireWorkItem("submit", "ready")
    | RequireWorkItem("fill-additional-demand", "ready")
) & (HasApplicantRole(["ADMIN", "EDITOR"]) | (ROLES_MUNICIPALITY & IsPaper()))
MODULE_PORTAL_ADDITIONAL_DEMANDS_READ = RequireWorkItem("fill-additional-demand")
MODULE_PORTAL_ADDITIONAL_DEMANDS_WRITE = (
    MODULE_PORTAL_ADDITIONAL_DEMANDS_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)
MODULE_PORTAL_CONSTRUCTION_MONITORING_READ = RequireWorkItem("construction-stage")
MODULE_PORTAL_CONSTRUCTION_MONITORING_WRITE = (
    MODULE_PORTAL_CONSTRUCTION_MONITORING_READ & HasApplicantRole(["ADMIN", "EDITOR"])
)

MODULE_DEADLINES_SUSPENSION = (
    STATES_ALL
    & IsServiceGroup(["municipality", "service-bab"])
    & HasRole(["municipality-lead", "service-lead"])
)
MODULE_DEADLINES_DEADLINE = (
    STATES_ALL
    & IsServiceGroup(["municipality", "service-bab"])
    & HasRole(["municipality-lead", "service-lead"])
)

ACTION_INSTANCE_COPY_AFTER_REJECTION = RequireInstanceState(["rejected"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_DELETE = RequireInstanceState(["new"]) & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_SUBMIT = RequireWorkItem("submit", "ready") & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_WITHDRAW = (
    RequireInstanceState(
        [
            "subm",
            "material-exam",
            "init-distribution",
            "distribution",
            "decision",
        ]
    )
    & (HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper()))
    & ~IsAppeal()
)
ACTION_INSTANCE_CREATE_MODIFICATION = RequireWorkItem("construction-stage", "ready") & (
    HasApplicantRole(["ADMIN"]) | (ROLES_MUNICIPALITY & IsPaper())
)
ACTION_INSTANCE_DOWNLOAD_AS_PDF = STATES_ALL | RequireInstanceState(
    ["correction", "new"]
)

# Actual config
SO_PERMISSIONS_SETTINGS = {
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
            (
                "grant-municipality-before-submission",
                MODULE_PORTAL_APPLICANTS & RequireInstanceState(["new"]),
            ),
            ("instance-create-modification", ACTION_INSTANCE_CREATE_MODIFICATION),
            ("instance-copy-after-rejection", ACTION_INSTANCE_COPY_AFTER_REJECTION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-download-form-as-pdf", ACTION_INSTANCE_DOWNLOAD_AS_PDF),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),
            (
                "permissions-read-municipality-before-submission",
                MODULE_PORTAL_APPLICANTS,
            ),
        ],
        "distribution-service": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS),
            ("appeal-read", MODULE_APPEAL),
            ("billing-read", MODULE_BILLING),
            ("billing-write", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("deadlines-suspensions-read", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-suspensions-write", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-deadlines-read", MODULE_DEADLINES_DEADLINE),
            ("deadlines-deadlines-write", MODULE_DEADLINES_DEADLINE),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
            ("instance-download-form-as-pdf", ACTION_INSTANCE_DOWNLOAD_AS_PDF),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("publication-read", MODULE_PUBLICATION),
            ("material-exam-bab-read", MODULE_MATERIAL_EXAM_BAB),
            ("form-afu-form-read", MODULE_AFU_CHECK_READ),
            ("form-afu-form-write", MODULE_AFU_CHECK_WRITE),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("responsible-write", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("additional-demands-write", MODULE_ADDITIONAL_DEMANDS),
            ("appeal-read", MODULE_APPEAL),
            ("billing-read", MODULE_BILLING),
            ("billing-write", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("communications-convert-to-document", MODULE_COMMUNICATIONS),
            ("complete-instance-read", MODULE_COMPLETE_INSTANCE),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-write", MODULE_CONSTRUCTION_MONITORING),
            ("corrections-read", MODULE_CORRECTIONS),
            ("deadlines-suspensions-read", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-suspensions-write", MODULE_DEADLINES_SUSPENSION),
            ("deadlines-deadlines-read", MODULE_DEADLINES_DEADLINE),
            ("deadlines-deadlines-write", MODULE_DEADLINES_DEADLINE),
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
            ("formal-exam-read", MODULE_FORMAL_EXAM),
            ("history-read", MODULE_HISTORY),
            ("instance-copy-after-rejection", ACTION_INSTANCE_COPY_AFTER_REJECTION),
            ("instance-delete", ACTION_INSTANCE_DELETE),
            ("instance-download-form-as-pdf", ACTION_INSTANCE_DOWNLOAD_AS_PDF),
            ("instance-submit", ACTION_INSTANCE_SUBMIT),
            ("instance-withdraw", ACTION_INSTANCE_WITHDRAW),
            ("journal-read", MODULE_JOURNAL_READ),
            ("journal-write", MODULE_JOURNAL_WRITE),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("legal-submissions-write", MODULE_LEGAL_SUBMISSIONS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("material-exam-read", MODULE_MATERIAL_EXAM),
            ("material-exam-bab-read", MODULE_MATERIAL_EXAM_BAB),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION),
            ("permissions-revoke-read", MODULE_PERMISSIONS),
            ("rejection-read", MODULE_REJECTION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("responsible-write", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "municipality-before-submission": [
            ("documents-read", RequireInstanceState(["new"])),
            ("form-read", RequireInstanceState(["new"])),
            ("redirect-to-portal", RequireInstanceState(["new"])),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("instance-download-form-as-pdf", ACTION_INSTANCE_DOWNLOAD_AS_PDF),
            ("work-items-read", MODULE_WORK_ITEMS),
            ("form-afu-form-read", MODULE_AFU_CHECK_READ),
            ("form-afu-form-write", MODULE_AFU_CHECK_WRITE),
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
            ("instance-download-form-as-pdf", ACTION_INSTANCE_DOWNLOAD_AS_PDF),
            ("permissions-read-any", Always()),
            ("permissions-read", Always()),
        ],
        "geometer": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("communications-write", MODULE_COMMUNICATIONS),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-write", MODULE_CONSTRUCTION_MONITORING),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            (
                "instance-download-form-as-pdf",
                ACTION_INSTANCE_DOWNLOAD_AS_PDF,
            ),
            ("journal-read", MODULE_JOURNAL_READ),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("responsible-write", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_so.PermissionEventHandlerSO",
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "DISTRIBUTION_INVITEE": "distribution-service",
        "SUPPORT": "support",
    },
    "PERMISSION_MODE": PERMISSION_MODE.FULL,
}
