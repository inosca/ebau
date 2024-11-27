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
    },
    "kt_ag": {
        "ENABLED": True,
    },
    "kt_gr": {
        "ENABLED": True,
        "MARK_VISIBILITY": {
            "SENSITIVE": ["sensitive"],
        },
    },
    "kt_so": {
        "ENABLED": True,
        "TAG_VISIBILITY": "service-subservice",
        "MARK_VISIBILITY": {
            "APPLICANT": ["objection"],
            "SENSITIVE": ["sensitive"],
        },
    },
    "test": {
        "ENABLED": True,
    },
}
