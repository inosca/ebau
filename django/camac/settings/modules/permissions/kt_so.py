from camac.permissions.conditions import (
    Always,
    Callback,
    HasRole,
    IsAppeal,
    IsForm,
    RequireInstanceState,
)
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.env import env

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
STATES_ACCESSIBLE = STATES_ALL & ~RequireInstanceState(["reject", "rejected"])
STATES_POST_DECISION = RequireInstanceState(
    ["decided", "construction-monitoring", "finished", "withdrawn"]
)

# Form rules
FORMS_ONLY_BUILDING_PERMIT = ~IsForm(["voranfrage", "meldung"])

# Role rules
ROLES_NO_READONLY = ~HasRole(["municipality-read", "service-read"])

# Module rules
#
# In order to have some kind of consistency, those rule should always be sorted
# by the following order:
#
# 1. Instance state rules
# 2. Form rules
# 3. Role rules
# 4. Other
MODULE_ADDITIONAL_DEMANDS = STATES_ALL & ~IsForm(["voranfrage"]) & ~IsAppeal()
MODULE_APPEAL = STATES_ACCESSIBLE & ROLES_NO_READONLY & IsAppeal()
MODULE_BILLING = STATES_ALL & ROLES_NO_READONLY
MODULE_CONSTRUCTION_MONITORING = (
    STATES_POST_DECISION
    & FORMS_ONLY_BUILDING_PERMIT
    & HasRole(["municipality-construction-monitoring"])
    & ~IsAppeal()
)
MODULE_COMMUNICATIONS = STATES_ALL & ROLES_NO_READONLY
MODULE_CORRECTIONS = (STATES_ALL | RequireInstanceState(["correction"])) & HasRole(
    ["municipality-lead", "municipality-clerk"]
)
MODULE_DECISION = STATES_ACCESSIBLE & ~RequireInstanceState(
    ["subm", "material-exam", "init-distribution", "distribution"]
)
MODULE_DISTRIBUTION = (
    (STATES_ACCESSIBLE & ~RequireInstanceState(["subm", "material-exam"]))
    & ~IsForm(["voranfrage"])
    & ~IsAppeal()
)
MODULE_DMS_GENERATE = STATES_ACCESSIBLE & ROLES_NO_READONLY
MODULE_DOCUMENTS = STATES_ALL
MODULE_FORM = STATES_ALL | RequireInstanceState(["correction"])
MODULE_FORMAL_EXAM = STATES_ALL & FORMS_ONLY_BUILDING_PERMIT & ~IsAppeal()
MODULE_HISTORY = STATES_ALL
MODULE_JOURNAL = STATES_ALL
MODULE_LEGAL_SUBMISSIONS = (
    (STATES_ACCESSIBLE & ~RequireInstanceState(["subm", "material-exam"]))
    & FORMS_ONLY_BUILDING_PERMIT
    & ~IsAppeal()
)
MODULE_LINKED_INSTANCES = STATES_ALL & ROLES_NO_READONLY
MODULE_MATERIAL_EXAM = (
    (STATES_ALL & ~RequireInstanceState(["subm"]))
    & FORMS_ONLY_BUILDING_PERMIT
    & ~IsAppeal()
)
MODULE_MATERIAL_EXAM_BAB = (
    STATES_ACCESSIBLE
    & Callback(
        lambda instance: instance.case.meta.get("is-bab", False),
        allow_caching=True,
        name="is_bab",
    )
    & Callback(
        lambda userinfo: userinfo.service.service_group.name == "service-bab",
        allow_caching=True,
        name="is_service_bab",
    )
)
MODULE_PERMISSIONS = STATES_ALL & HasRole(["municipality-lead"])
MODULE_PUBLICATION = (
    (STATES_ACCESSIBLE & ~RequireInstanceState(["subm", "material-exam"]))
    & FORMS_ONLY_BUILDING_PERMIT
    & ~IsAppeal()
)
MODULE_REJECTION = RequireInstanceState(["reject", "rejected"]) & HasRole(
    ["municipality-lead", "municipality-clerk"]
)
MODULE_RELATED_GWR_PROJECTS = (
    (STATES_ACCESSIBLE & ~RequireInstanceState(["subm", "material-exam"]))
    & FORMS_ONLY_BUILDING_PERMIT
    & HasRole(["municipality-lead", "municipality-clerk"])
    & ~IsAppeal()
)
MODULE_RESPONSIBLE = STATES_ALL & ROLES_NO_READONLY
MODULE_WORK_ITEMS = STATES_ALL & ROLES_NO_READONLY

# Actual config
SO_PERMISSIONS_SETTINGS = {
    "ENABLED": True,
    "ACCESS_LEVELS": {
        "applicant": [
            ("applicant-add", Always()),
            ("applicant-read", Always()),
            ("applicant-remove", Always()),
            ("documents-write", Always()),
        ],
        "distribution-service": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("billing-read", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("material-exam-bab-read", MODULE_MATERIAL_EXAM_BAB),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "lead-authority": [
            ("additional-demands-read", MODULE_ADDITIONAL_DEMANDS),
            ("appeal-read", MODULE_APPEAL),
            ("billing-read", MODULE_BILLING),
            ("communications-read", MODULE_COMMUNICATIONS),
            ("complete-instance-read", MODULE_CONSTRUCTION_MONITORING),
            ("construction-monitoring-read", MODULE_CONSTRUCTION_MONITORING),
            ("corrections-read", MODULE_CORRECTIONS),
            ("decision-read", MODULE_DECISION),
            ("distribution-read", MODULE_DISTRIBUTION),
            ("dms-generate-read", MODULE_DMS_GENERATE),
            ("documents-read", MODULE_DOCUMENTS),
            ("documents-write", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
            ("formal-exam-read", MODULE_FORMAL_EXAM),
            ("history-read", MODULE_HISTORY),
            ("journal-read", MODULE_JOURNAL),
            ("legal-submissions-read", MODULE_LEGAL_SUBMISSIONS),
            ("linked-instances-read", MODULE_LINKED_INSTANCES),
            ("material-exam-read", MODULE_MATERIAL_EXAM),
            ("permissions-grant-read", MODULE_PERMISSIONS),
            ("permissions-read-any", MODULE_PERMISSIONS),
            ("permissions-read", MODULE_PERMISSIONS),
            ("publication-read", MODULE_PUBLICATION),
            ("rejection-read", MODULE_REJECTION),
            ("related-gwr-projects-read", MODULE_RELATED_GWR_PROJECTS),
            ("responsible-read", MODULE_RESPONSIBLE),
            ("work-items-read", MODULE_WORK_ITEMS),
        ],
        "municipality-before-submission": [
            ("form-read", RequireInstanceState(["new"])),
            ("redirect-to-portal", RequireInstanceState(["new"])),
        ],
        "read": [
            ("communications-read", MODULE_COMMUNICATIONS),
            ("documents-read", MODULE_DOCUMENTS),
            ("form-read", MODULE_FORM),
        ],
        "support": [
            ("documents-read", Always()),
            ("documents-write", Always()),
            ("form-read", Always()),
            ("history-read", Always()),
            ("permissions-read-any", Always()),
            ("permissions-read", Always()),
        ],
    },
    "EVENT_HANDLER": "camac.permissions.config.kt_so.PermissionEventHandlerSO",
    "MIGRATION": {
        "APPLICANT": "applicant",
        "MUNICIPALITY": "lead-authority",
        "DISTRIBUTION_INVITEE": "distribution-service",
        "SUPPORT": "support",
    },
    "ENABLE_CACHE": env.bool("PERMISSION_MODULE_ENABLE_CACHE", default=True),
    "PERMISSION_MODE": getattr(
        PERMISSION_MODE, env.bool("PERMISSION_MODULE_MODE", default="FULL")
    ),
}
