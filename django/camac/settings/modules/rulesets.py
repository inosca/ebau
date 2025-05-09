RULESETS = {
    "default": {
        "RESPONSIBLE_USER_RULE": {
            "AUTOMATICALLY_ASSIGN": True,
            "ALLOWED_ROLES": [],
        }
    },
    "kt_ag": {
        "ENABLED": True,
        "RESPONSIBLE_USER_RULE": {
            "ALLOWED_ROLES": [
                "municipality-admin",
                "service-admin",
                "trusted-service-admin",
            ]
        },
    },
}
