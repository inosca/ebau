from .alexandria_config.kt_ag import CONFIG as AG_CONFIG

ALEXANDRIA = {
    "default": {
        "ENABLED": False,
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
    },
    "kt_ag": {
        "ENABLED": True,
        "CUSTOM_ROLE_MAPPINGS": {
            "service-afb": "afb",
            "service-cantonal": "cantonal",
            "service-external": "external",
        },
        "APPEND_ROLE_TO_CUSTOM_ROLE_MAPPING": True,
        "PERMISSIONS_CONFIG": AG_CONFIG,
    },
    "kt_gr": {
        "ENABLED": True,
        "MARK_VISIBILITY": {
            "SENSITIVE": ["sensitive"],
        },
        "CUSTOM_ROLE_MAPPINGS": {"authority-bab": "are"},
        "INSTANCE_COPY_CATEGORIES": ["beilagen-zum-gesuch", "nachforderung", "system"],
    },
    "kt_so": {
        "ENABLED": True,
        "TAG_VISIBILITY": "service-subservice",
        "MARK_VISIBILITY": {
            "APPLICANT": ["objection"],
            "SENSITIVE": ["sensitive"],
        },
        "CUSTOM_ROLE_MAPPINGS": {
            "service-bab": "cantonal",
            "service-cantonal": "cantonal",
            "service-extra-cantonal": "extra-cantonal",
        },
        "APPEND_ROLE_TO_CUSTOM_ROLE_MAPPING": True,
    },
    "test": {
        "ENABLED": True,
    },
}
