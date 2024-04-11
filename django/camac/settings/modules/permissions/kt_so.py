from camac.permissions.switcher import PERMISSION_MODE

from .common import REQUIRE_NEW_STATE

SO_PERMISSIONS_SETTINGS = {
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
}
