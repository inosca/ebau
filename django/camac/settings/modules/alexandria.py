from .alexandria_config.kt_ag import CONFIG as AG_CONFIG

ALEXANDRIA = {
    "default": {
        "ENABLED": False,
        "LOG_MARKS_IN_HISTORY": False,
        "EXCLUSIVE_MARKS": ["void"],
        "MARK_VISIBILITY": {
            "APPLICANT": ["decision"],
            "PUBLIC": ["publication"],
        },
        "PUBLIC_MARKS": ["publication", "void"],
        "RESTRICTED_FIELDS": {
            "title",
            "description",
            "date",
            "metainfo",
            "category",
            "tags",
            "marks",
            "files",
        },
        "TAG_VISIBILITY": "all",
        "INSTANCE_COPY_CATEGORIES": ["beilagen-zum-gesuch", "nachforderung"],
        "PERMISSIONS_CONFIG": {},
        "USE_V2_PERMISSIONS": False,
        "V2_BASE_PERMISSION": "documents-write",
        "PERMISSION_KEY": {
            # Optional mapping between service group slug and custom key
            "SERVICE_GROUP_MAPPING": {},
            # Whether to append the role name to custom keys configured above
            "SERVICE_GROUP_APPEND_ROLE": False,
            # Whether to use mapped role names as configured in
            # `settings.APPLICATION["ROLE_PERMISSIONS"]`
            "USE_ROLE_PERMISSIONS_MAPPING": False,
        },
    },
    "kt_ag": {
        "ENABLED": True,
        "PERMISSION_KEY": {
            "SERVICE_GROUP_MAPPING": {
                "service-afb": "afb",
                "service-cantonal": "cantonal",
                "service-external": "external",
            },
            "SERVICE_GROUP_APPEND_ROLE": True,
        },
        "PERMISSIONS_CONFIG": AG_CONFIG,
    },
    "kt_gr": {
        "ENABLED": True,
        "MARK_VISIBILITY": {
            "SENSITIVE": ["sensitive"],
        },
        "PERMISSION_KEY": {
            "SERVICE_GROUP_MAPPING": {"authority-bab": "are"},
        },
        "INSTANCE_COPY_CATEGORIES": ["beilagen-zum-gesuch", "nachforderung", "system"],
    },
    "kt_so": {
        "ENABLED": True,
        "LOG_MARKS_IN_HISTORY": True,
        "TAG_VISIBILITY": "service-subservice",
        "MARK_VISIBILITY": {
            "APPLICANT": ["objection"],
            "SENSITIVE": ["sensitive"],
        },
        "PERMISSION_KEY": {
            "SERVICE_GROUP_MAPPING": {
                "service-bab": "cantonal",
                "service-cantonal": "cantonal",
                "service-extra-cantonal": "extra-cantonal",
            },
            "SERVICE_GROUP_APPEND_ROLE": True,
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "USE_V2_PERMISSIONS": True,
        # This base permission from the top-level permission module is required in order
        # to do any write actions in alexandria. We explicitly don't use
        # "documents-write" that already exists in order to avoid collisions
        # with the permission checks of the legacy documents module in the
        # transition / migration period.
        "V2_BASE_PERMISSION": "alexandria-write",
        "PERMISSION_KEY": {
            "USE_ROLE_PERMISSIONS_MAPPING": True,
        },
        "MARK_VISIBILITY": {
            "GEOMETER": ["geometer"],
        },
    },
    "kt_uri": {
        # Initial minimum configuration
        "ENABLED": True,
        "USE_V2_PERMISSIONS": True,
        # This base permission from the top-level permission module is required in order
        # to do any write actions in alexandria. We explicitly don't use
        # "documents-write" that already exists in order to avoid collisions
        # with the permission checks of the legacy documents module in the
        # transition / migration period.
        "V2_BASE_PERMISSION": "alexandria-write",
        "PERMISSION_KEY": {
            "USE_ROLE_PERMISSIONS_MAPPING": True,
        },
    },
    "kt_schwyz": {
        # Initial minimum configuration
        "ENABLED": True,
        "USE_V2_PERMISSIONS": True,
        # This base permission from the top-level permission module is required in order
        # to do any write actions in alexandria. We explicitly don't use
        # "documents-write" that already exists in order to avoid collisions
        # with the permission checks of the legacy documents module in the
        # transition / migration period.
        "V2_BASE_PERMISSION": "alexandria-write",
        "PERMISSION_KEY": {
            "USE_ROLE_PERMISSIONS_MAPPING": True,
        },
    },
    "kt_sg": {
        "ENABLED": True,
        "USE_V2_PERMISSIONS": True,
        "PERMISSION_KEY": {
            "USE_ROLE_PERMISSIONS_MAPPING": True,
        },
    },
    "test": {
        "ENABLED": True,
    },
}
