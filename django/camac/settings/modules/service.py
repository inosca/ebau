SERVICE = {
    "default": {
        "CREATE_GROUPS_IN_ADMIN": False,
        "UPDATE_GROUP_NAME_IN_ADMIN": False,
        "ROLES_FOR_SERVICE_GROUP": {},
    },
    "kt_so": {
        "ENABLED": True,
        "CREATE_GROUPS_IN_ADMIN": True,
        "UPDATE_GROUP_NAME_IN_ADMIN": True,
        "ROLES_FOR_SERVICE_GROUP": {
            "municipality": [
                "municipality-admin",
                "municipality-lead",
                "municipality-read",
            ],
            "canton": ["municipality-admin", "municipality-lead", "municipality-read"],
            "service-cantonal": ["service-admin", "service-lead"],
            "service-extra-cantonal": ["service-admin", "service-lead"],
            "service-bab": ["service-admin", "service-lead"],
        },
    },
}
