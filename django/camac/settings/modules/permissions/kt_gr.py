from camac.permissions.conditions import Always
from camac.permissions.switcher import PERMISSION_MODE

GR_PERMISSIONS_SETTINGS = {
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
}
