from camac.permissions.conditions import Always
from camac.permissions.switcher import PERMISSION_MODE

from .common import REQUIRE_NEW_STATE
from .kt_bern import BE_PERMISSIONS_SETTINGS
from .kt_gr import GR_PERMISSIONS_SETTINGS
from .kt_so import SO_PERMISSIONS_SETTINGS
from .typing import PermissionsConfig

"""
Configuration for the permissions module.

Note: Full documentation for the configuration can be found here:

  -> ./permissions/docs/configuration.md

We provide type hints here. They should help your IDE with completion
and checks, and also serve as a documentation on what's allowed.
"""


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
    "kt_bern": BE_PERMISSIONS_SETTINGS,
    "kt_gr": GR_PERMISSIONS_SETTINGS,
    "kt_so": SO_PERMISSIONS_SETTINGS,
}
