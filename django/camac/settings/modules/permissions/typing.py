from typing import Dict, List, Optional, Tuple, TypedDict

from camac.permissions.conditions import Check
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
