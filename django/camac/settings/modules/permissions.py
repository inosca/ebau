from typing import Dict, List, Optional, Tuple, TypedDict

from camac.permissions.conditions import Always, Check, HasRole, RequireInstanceState
from camac.permissions.switcher import PERMISSION_MODE

"""
Configuration for the permissions module.

Note: Full documentation for the configuration can be found here:

  -> ./permissions/docs/configuration.md

We provide type hints here. They should help your IDE with completion
and checks, and also serve as a documentation on what's allowed.
"""

# (permission, condition)
PermissionLine = Tuple[str, Check]
PermissionLine.__doc__ = """
A tuple that maps a given permission (str) to a condition.

The condition is a callback that can optionally take the instance,
or camac.permissions.api.UserInfo object as parameter.

There are predefined and composable permission checks in
the module camac.permissions.conditions.
"""

PermissionConfigEntry = TypedDict(
    "PermissionConfigEntry",
    {
        "ENABLED": bool,
        "EVENT_HANDLER": Optional[str],
        # each access level entry here must refer to an existing
        # access level model.
        "ACCESS_LEVELS": Dict[str, List[PermissionLine]],
        "PERMISSION_MODE": Optional[PERMISSION_MODE],
        # If set to False, caching will never happen. If set to True,
        # Caching only happens if the permissions are cacheable
        "ENABLE_CACHE": Optional[bool],
        # Map INTERNAL -> CANTON access level names. The INTERNAL ones
        # are directly referenced by the migration tooling and may differ from
        # the ones used by the canton.
        "MIGRATION": Dict[str, str],
    },
)

PermissionsConfig = Dict[str, PermissionConfigEntry]

REQUIRE_NEW_STATE = RequireInstanceState(["new"])

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
BE_MUNICIPALITY_READ_PERMISSIONS = [
    ("communications-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("geometer-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("responsible-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("journal-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("history-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    ("permissions-read-any", BE_MUNICIPALITY_ACCESSIBLE_STATES),
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
        "information-of-neighbors",
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
        "legal-submission-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES & ~RequireInstanceState(["subm"]),
    ),
    (
        "form-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES | RequireInstanceState(["correction"]),
    ),
    ("documents-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
    (
        "dms-generate-read",
        BE_MUNICIPALITY_ACCESSIBLE_STATES,
    ),
    (
        "assign-ebau-number-read",
        RequireInstanceState(["subm", "in_progress_internal"]),
    ),
    ("distribution-read", BE_MUNICIPALITY_STATES_EXCEPT_MIGRATED),
    ("workitems-read", BE_MUNICIPALITY_ACCESSIBLE_STATES),
]

PERMISSIONS: PermissionsConfig = {
    "default": {
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
        "ENABLED": False,
        "ENABLE_CACHE": False,
        "MIGRATION": {},
        "EVENT_HANDLER": None,
        "ACCESS_LEVELS": {},
    },
    "demo": {
        "ACCESS_LEVELS": {
            "service": [
                # (permission, list-of[instance-state or "*" for any])
                # (permission, (lambda instance -> True/False))
                ("foo", Always()),
                ("edit-form", REQUIRE_NEW_STATE),
            ]
        },
        # Event handler that defines callbacks, which can grant/revoke
        # ACLs.
        "EVENT_HANDLER": "camac.permissions.events.EmptyEventHandler",
        "ENABLED": True,
        "ENABLE_CACHE": True,
        "MIGRATION": {},
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
    },
    "kt_bern": {
        "PERMISSION_MODE": PERMISSION_MODE.AUTO_OFF,
        "ACCESS_LEVELS": {
            "geometer": [
                # TODO: For ACLs that can be manually granted, read-permissions
                # for the relevant modules should be available at any time the
                # ACL can be granted. System-managed ACLs and write permissions
                # should be more restrictive, since we know when they are created.
                ("form-read", Always()),
                # all documents can be read, but only a specific category can be written
                ("documents-read", Always()),
                # TODO: Handle attachment section permissions through permissions module?
                # ("documents-write-sb1-paper", ["sb1", "sb2"]),
                # TODO: permission "document" corresponds to editable permission, should be changed
                # to permissions module naming convention once the InstanceEditableMixin
                # is refactored / removed
                ("document", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                (
                    "workitems-read",
                    HasRole(["geometer-lead", "geometer-clerk"])
                    & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES,
                ),
                (
                    "communications-read",
                    HasRole(["geometer-lead", "geometer-clerk"])
                    & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES,
                ),
                (
                    "dms-generate-read",
                    HasRole(["geometer-lead", "geometer-clerk"])
                    & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES,
                ),
                ("geometer-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("responsible-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("journal-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("history-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ],
            "applicant": [
                ("applicant-remove", Always()),
                ("applicant-add", Always()),
                ("applicant-read", Always()),
            ],
            "lead-authority": BE_MUNICIPALITY_READ_PERMISSIONS,
            "involved-authority": BE_MUNICIPALITY_READ_PERMISSIONS,
        },
        "EVENT_HANDLER": "camac.permissions.config.kt_bern.PermissionEventHandlerBE",
        "ENABLED": True,
        # Map INTERNAL -> CANTON access level names. The INTERNAL ones
        # are directly referenced by the migration tooling and may differ from
        # the ones used by the canton.
        "MIGRATION": {
            "APPLICANT": "applicant",
            "MUNICIPALITY": "lead-authority",
            "MUNICIPALITY_INVOLVED": "involved-authority",
        },
        "ENABLE_CACHE": True,
    },
    "kt_gr": {
        "ACCESS_LEVELS": {
            "read": [
                # all forms can be read
                ("form-read", Always()),
                # all documents can be read
                ("documents-read", Always()),
            ],
        },
        "EVENT_HANDLER": "camac.permissions.config.kt_gr.PermissionEventHandlerGR",
        "ENABLED": True,
        "MIGRATION": {},
        "ENABLE_CACHE": True,
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
    },
    "kt_so": {
        "ENABLED": True,
        "ACCESS_LEVELS": {
            "municipality-before-submission": [
                ("redirect-to-portal", REQUIRE_NEW_STATE),
                ("form-read", REQUIRE_NEW_STATE),
            ]
        },
        "EVENT_HANDLER": "camac.permissions.config.kt_so.PermissionEventHandlerSO",
        "MIGRATION": {},
        "ENABLE_CACHE": True,
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
    },
}
