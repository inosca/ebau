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
        },
    },
    "test": {
        "ENABLED": True,
    },
}
