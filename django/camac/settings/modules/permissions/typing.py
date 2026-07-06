from typing import TypedDict

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
type PermissionLine = tuple[str, Check]
"""A tuple that maps a given permission (str) to a condition.

The condition is a callback that can optionally take the instance,
or camac.permissions.api.UserInfo object as parameter.

There are predefined and composable permission checks in
the module camac.permissions.conditions.
"""


class PermissionConfigEntry(TypedDict):
    ENABLED: bool
    EVENT_HANDLER: str | None
    ACCESS_LEVELS: dict[str, list[PermissionLine]]
    PERMISSION_MODE: PERMISSION_MODE | None
    ENABLE_CACHE: bool | None
    MIGRATION: dict[str, str]


type PermissionsConfig = dict[str, PermissionConfigEntry]
