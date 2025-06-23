APPLICANT = "applicant"

MUNICIPALITY = "municipality-lead"
MUNICIPALITY_READ = "municipality-read"
MUNICIPALITY_SUB = "subservice"

AFB = "afb-trusted-service-lead"
AFB_READ = "afb-trusted-service-read"
AFB_SUB = "afb-subservice"

INTERNAL = "cantonal-trusted-service-lead"
INTERNAL_READ = "cantonal-trusted-service-read"
INTERNE_SUB = "cantonal-subservice"

EXTERNAL = "external-service-lead"
EXTERNAL_SUB = "external-subservice"

SUPPORT = "support"


METADATA_FIELDS = ["title", "description", "date"]

DECISION_STATES = [
    "rejected",
    "finished",
    "to-finish",
    "construction-monitoring",
    "decided",
]
# VISIBILITY
VISIBILITY_ALL = {"visibility": "all"}
VISIBILITY_SERVICE_AND_SUBSERVICE = {"visibility": "service-and-subservice"}

# CONDITIONS

UNTIL_DECISION_CONDITION = {"~InstanceState": DECISION_STATES}
UNTIL_DECISION_WITH_PAPER_CONDITION = {
    "PaperInstance": True,
    "~InstanceState": DECISION_STATES,
}

NO_DECISION_MARK_CONDITION = {
    "~HasAnyMark": "decision",
}

HAS_DECISION_MARK_BEFORE_DECISION_CONDITION = {
    "HasAnyMark": "decision",
    "~InstanceState": DECISION_STATES,
}


UNTIL_SUBMIT_CONDITION = {"InstanceState": "new"}
UNTIL_SUBMIT_WITH_PAPER_CONDITION = {
    "PaperInstance": True,
    "InstanceState": "new",
}

OPEN_ADDITIONAL_DEMAND_CONDITION = {"ReadyWorkItem": "fill-additional-demand"}

ALL_UNTIL_DECISION = {
    "scope": "All",
    "condition": UNTIL_DECISION_CONDITION,
}
OWN_UNTIL_DECISION = {
    "scope": "Service",
    "condition": UNTIL_DECISION_CONDITION,
}

# PERMISSIONS

ALL_PERMISSIONS = {
    **VISIBILITY_ALL,
    "permissions": [
        {"permission": "create"},
        {"scope": "All", "permission": "update"},
        {"scope": "All", "permission": "delete"},
    ],
}


CREATE_UNRESTRICTED = {"permission": "create"}

CREATE_UNTIL_DECISION = {
    "condition": UNTIL_DECISION_CONDITION,
    "permission": "create",
}

CREATE_DURING_ADDITIONAL_DEMAND = {
    "fields": ["metainfo", "title", "category", "files"],
    "condition": OPEN_ADDITIONAL_DEMAND_CONDITION,
    "permission": "create",
}

UPDATE_ALL_TAGS = {
    "scope": "All",
    "fields": ["tags"],
    "permission": "update",
}

UPDATE_OWN_METADATA_UNRESTRICTED = {
    "scope": "Service",
    "fields": [*METADATA_FIELDS, "metainfo", "files"],
    "permission": "update",
}

UPDATE_ALL_MARKS_UNTIL_DECISION = {
    **ALL_UNTIL_DECISION,
    "fields": ["marks"],
    "permission": "update",
}

UPDATE_ALL_METADATA_UNTIL_DECISION = {
    **ALL_UNTIL_DECISION,
    "fields": METADATA_FIELDS,
    "permission": "update",
}

UPDATE_OWN_METADATA_UNTIL_DECISION = {
    **OWN_UNTIL_DECISION,
    "fields": METADATA_FIELDS,
    "permission": "update",
}

MOVE_OWN_UNRESTRICTED = {
    "scope": "Service",
    "fields": ["category"],
    "permission": "update",
}

MOVE_OWN_UNTIL_DECISION = {
    **OWN_UNTIL_DECISION,
    "fields": ["category"],
    "permission": "update",
}

MOVE_ALL_UNTIL_DECISION = {
    **ALL_UNTIL_DECISION,
    "fields": ["category"],
    "permission": "update",
}

MOVE_ALL_PAPER_UNTIL_DECISION = {
    "scope": "All",
    "fields": ["category"],
    "condition": UNTIL_DECISION_WITH_PAPER_CONDITION,
    "permission": "update",
}

DELETE_OWN_UNRESTRICTED = {
    "scope": "Service",
    "permission": "delete",
}

DELETE_DURING_ADDITIONAL_DEMAND = {
    "scope": "All",
    "condition": OPEN_ADDITIONAL_DEMAND_CONDITION,
    "permission": "delete",
}

DELETE_OWN_UNTIL_DECISION = {
    "scope": "Service",
    "condition": UNTIL_DECISION_CONDITION,
    "permission": "delete",
}
DELETE_OWN_WITH_NO_DECISION_MARK = {
    "scope": "Service",
    "condition": NO_DECISION_MARK_CONDITION,
    "permission": "delete",
}
DELETE_OWN_UNTIL_DECISION_WITH_DECISION_MARK = {
    "scope": "Service",
    "condition": HAS_DECISION_MARK_BEFORE_DECISION_CONDITION,
    "permission": "delete",
}

# PERMISSION COLLECTIONS

CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS = [
    CREATE_UNRESTRICTED,
    MOVE_ALL_UNTIL_DECISION,
    UPDATE_ALL_MARKS_UNTIL_DECISION,
    UPDATE_ALL_METADATA_UNTIL_DECISION,
    UPDATE_ALL_TAGS,
    DELETE_OWN_WITH_NO_DECISION_MARK,
    DELETE_OWN_UNTIL_DECISION_WITH_DECISION_MARK,
]


CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS = [
    CREATE_UNRESTRICTED,
    UPDATE_ALL_TAGS,
    UPDATE_OWN_METADATA_UNTIL_DECISION,
    MOVE_OWN_UNTIL_DECISION,
    DELETE_OWN_WITH_NO_DECISION_MARK,
    DELETE_OWN_UNTIL_DECISION_WITH_DECISION_MARK,
]

CATEGORY_ALL_CANTON_SUBSERVICE_PERMISSIONS = [
    CREATE_UNRESTRICTED,
    MOVE_OWN_UNTIL_DECISION,
    UPDATE_ALL_TAGS,
    UPDATE_OWN_METADATA_UNTIL_DECISION,
]

CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS = {
    **VISIBILITY_SERVICE_AND_SUBSERVICE,
    "permissions": [
        CREATE_UNRESTRICTED,
        UPDATE_OWN_METADATA_UNRESTRICTED,
        MOVE_OWN_UNRESTRICTED,
        UPDATE_ALL_TAGS,
        DELETE_OWN_UNRESTRICTED,
    ],
}


CONFIG = {
    "beilagen-zum-gesuch": {
        APPLICANT: {
            **VISIBILITY_ALL,
            "permissions": [
                {
                    "fields": ["metainfo", "title", "category", "files"],
                    "condition": UNTIL_SUBMIT_CONDITION,
                    "permission": "create",
                },
                {
                    "scope": "All",
                    "condition": UNTIL_SUBMIT_CONDITION,
                    "permission": "delete",
                },
            ],
        },
        MUNICIPALITY: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                MOVE_ALL_PAPER_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                UPDATE_ALL_MARKS_UNTIL_DECISION,
                UPDATE_ALL_METADATA_UNTIL_DECISION,
                DELETE_OWN_UNTIL_DECISION,
                {
                    "scope": "All",
                    "condition": UNTIL_SUBMIT_WITH_PAPER_CONDITION,
                    "permission": "delete",
                },
            ],
        },
        MUNICIPALITY_READ: VISIBILITY_ALL,
        MUNICIPALITY_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        AFB: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                UPDATE_ALL_MARKS_UNTIL_DECISION,
                UPDATE_ALL_METADATA_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                DELETE_OWN_UNTIL_DECISION,
            ],
        },
        AFB_READ: VISIBILITY_ALL,
        AFB_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        INTERNAL: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                DELETE_OWN_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                UPDATE_OWN_METADATA_UNTIL_DECISION,
            ],
        },
        INTERNAL_READ: VISIBILITY_ALL,
        INTERNE_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        EXTERNAL: VISIBILITY_ALL,
        EXTERNAL_SUB: VISIBILITY_ALL,
        SUPPORT: ALL_PERMISSIONS,
    },
    "unterlagenergaenzung": {
        APPLICANT: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_DURING_ADDITIONAL_DEMAND,
                DELETE_DURING_ADDITIONAL_DEMAND,
            ],
        },
        MUNICIPALITY: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                UPDATE_ALL_MARKS_UNTIL_DECISION,
                UPDATE_ALL_METADATA_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                DELETE_OWN_UNTIL_DECISION,
            ],
        },
        MUNICIPALITY_READ: VISIBILITY_ALL,
        MUNICIPALITY_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        AFB: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                UPDATE_ALL_MARKS_UNTIL_DECISION,
                UPDATE_ALL_METADATA_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                DELETE_OWN_UNTIL_DECISION,
            ],
        },
        AFB_READ: VISIBILITY_ALL,
        AFB_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        INTERNAL: {
            **VISIBILITY_ALL,
            "permissions": [
                CREATE_UNTIL_DECISION,
                MOVE_OWN_UNTIL_DECISION,
                UPDATE_OWN_METADATA_UNTIL_DECISION,
                UPDATE_ALL_TAGS,
                DELETE_OWN_UNTIL_DECISION,
            ],
        },
        INTERNAL_READ: VISIBILITY_ALL,
        INTERNE_SUB: {
            **VISIBILITY_ALL,
            "permissions": [UPDATE_ALL_TAGS],
        },
        EXTERNAL: VISIBILITY_ALL,
        EXTERNAL_SUB: VISIBILITY_ALL,
        SUPPORT: ALL_PERMISSIONS,
    },
    "alle-beteiligten": {
        APPLICANT: {
            **VISIBILITY_ALL,
        },
        MUNICIPALITY: {
            **VISIBILITY_ALL,
            "permissions": CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        MUNICIPALITY_READ: VISIBILITY_ALL,
        MUNICIPALITY_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        AFB: {
            **VISIBILITY_ALL,
            "permissions": CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        AFB_READ: VISIBILITY_ALL,
        AFB_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        INTERNAL: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        INTERNAL_READ: VISIBILITY_ALL,
        INTERNE_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        EXTERNAL: VISIBILITY_ALL,
        EXTERNAL_SUB: VISIBILITY_ALL,
        SUPPORT: ALL_PERMISSIONS,
    },
    "beteiligte-behörden": {
        MUNICIPALITY: {
            **VISIBILITY_ALL,
            "permissions": CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        MUNICIPALITY_READ: VISIBILITY_ALL,
        MUNICIPALITY_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        AFB: {
            **VISIBILITY_ALL,
            "permissions": CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        AFB_READ: VISIBILITY_ALL,
        AFB_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        INTERNAL: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        INTERNAL_READ: VISIBILITY_ALL,
        INTERNE_SUB: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        EXTERNAL: {
            **VISIBILITY_SERVICE_AND_SUBSERVICE,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        EXTERNAL_SUB: {
            **VISIBILITY_SERVICE_AND_SUBSERVICE,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        SUPPORT: ALL_PERMISSIONS,
    },
    "intern": {
        MUNICIPALITY: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        MUNICIPALITY_READ: VISIBILITY_SERVICE_AND_SUBSERVICE,
        MUNICIPALITY_SUB: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        AFB: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        AFB_READ: VISIBILITY_SERVICE_AND_SUBSERVICE,
        AFB_SUB: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        INTERNAL: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        INTERNAL_READ: VISIBILITY_SERVICE_AND_SUBSERVICE,
        INTERNE_SUB: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        EXTERNAL: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        EXTERNAL_SUB: CATEGORY_INTERNAL_VISIBILITY_AND_PERMISSIONS,
        SUPPORT: ALL_PERMISSIONS,
    },
    "alle-kanton": {
        AFB: {
            **VISIBILITY_ALL,
            "permissions": CRU_ALL_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        AFB_READ: VISIBILITY_ALL,
        AFB_SUB: {
            **VISIBILITY_ALL,
            "permissions": CATEGORY_ALL_CANTON_SUBSERVICE_PERMISSIONS,
        },
        INTERNAL: {
            **VISIBILITY_ALL,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        INTERNAL_READ: VISIBILITY_ALL,
        INTERNE_SUB: {
            **VISIBILITY_ALL,
            "permissions": CATEGORY_ALL_CANTON_SUBSERVICE_PERMISSIONS,
        },
        EXTERNAL: {
            **VISIBILITY_SERVICE_AND_SUBSERVICE,
            "permissions": CRU_OWN_UNTIL_DECISION_AND_DELETE_OWN_DECISION_MARK_CONDITIONS,
        },
        EXTERNAL_SUB: {
            **VISIBILITY_SERVICE_AND_SUBSERVICE,
            "permissions": CATEGORY_ALL_CANTON_SUBSERVICE_PERMISSIONS,
        },
        SUPPORT: ALL_PERMISSIONS,
    },
}
