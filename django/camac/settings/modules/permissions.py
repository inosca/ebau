from typing import Callable, Dict, List, Optional, Tuple, TypedDict

from camac.permissions.conditions import Always, HasRole, RequireInstanceState
from camac.permissions.switcher import PERMISSION_MODE

"""
Configuration for the permissions module.

Note: Full documentation for the configuration can be found here:

  -> ./permissions/docs/configuration.md

We provide type hints here. They should help your IDE with completion
and checks, and also serve as a documentation on what's allowed.
"""

# Actually Instance -> bool, but we can't import instance here
# so this is a slight inaccuracy
PermissionCallback = Callable[[object], bool]
PermissionCallback.__doc__ = """
With a Camac Instance, decide whether user has permission.

The callback takes a Camac instance object, and dynamically
decides whether the user may have the permission in question.

This can be used for more complex decisions, if the condition
is more than the instance's state.
"""

# (permission, condition)
PermissionLine = Tuple[str, PermissionCallback]
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
        "EVENT_HANDLER": str,
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

BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES = RequireInstanceState(
    [
        "sb1",
        "sb2",
        "conclusion",
        "finished",
    ]
)

PERMISSIONS: PermissionsConfig = {
    "default": {
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
    },
    "demo": {
        "ACCESS_LEVELS": {
            "service": [
                # (permission, list-of[instance-state or "*" for any])
                # (permission, (lambda instance -> True/False))
                ("foo", Always()),
                ("edit-form", RequireInstanceState(["new"])),
            ]
        },
        # Event handler that defines callbacks, which can grant/revoke
        # ACLs.
        "EVENT_HANDLER": "camac.permissions.events.EmptyEventHandler",
        "ENABLED": True,
    },
    "kt_bern": {
        "PERMISSION_MODE": PERMISSION_MODE.OFF,
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
                    "templates-read",
                    HasRole(["geometer-lead", "geometer-clerk"])
                    & BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES,
                ),
                ("geometer-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("responsible-service-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("journal-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
                ("history-read", BE_GEOMETER_DEFAULT_ACCESSIBLE_STATES),
            ],
            "applicant": [
                ("applicant-remove", Always()),
                ("applicant-add", Always()),
                ("applicant-read", Always()),
            ],
        },
        "EVENT_HANDLER": "camac.permissions.config.kt_bern.PermissionEventHandlerBE",
        "ENABLED": True,
        # Map INTERNAL -> CANTON access level names. The INTERNAL ones
        # are directly referenced by the migration tooling and may differ from
        # the ones used by the canton.
        "MIGRATION": {"APPLICANT": "applicant"},
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
    },
    "kt_so": {
        "ENABLED": True,
        "ACCESS_LEVELS": {
            "municipality-before-submission": [
                ("redirect-to-portal", RequireInstanceState(["new"])),
                ("form-read", RequireInstanceState(["new"])),
            ]
        },
        "EVENT_HANDLER": "camac.permissions.config.kt_so.PermissionEventHandlerSO",
    },
}
