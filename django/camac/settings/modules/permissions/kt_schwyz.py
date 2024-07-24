from camac.permissions.conditions import Always

SZ_PERMISSIONS_SETTINGS = {
    "ACCESS_LEVELS": {
        "read": [
            # all forms can be read
            ("form-read", Always()),
            # all documents can be read
            ("documents-read", Always()),
        ],
    },
    "ENABLED": True,
}
