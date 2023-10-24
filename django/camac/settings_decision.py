DECISION = {
    "default": {
        "TASK": "decision",
        "QUESTIONS": {
            "DECISION": "decision-decision",
            "DATE": "decision-date",
        },
        "ANSWERS": {
            "DECISION": {
                "APPROVED": "decision-decision-approved",
                "REJECTED": "decision-decision-rejected",
            },
        },
        "INSTANCE_STATE_AFTER_DECISION": "construction-monitoring",
        "TASKS_AFTER_BUILDING_PERMIT_DECISION": ["construction-monitoring"],
    },
    "kt_bern": {
        "ENABLED": True,
        "ENABLE_STATS": True,
        "QUESTIONS": {
            "DECISION": "decision-decision-assessment",
            "APPROVAL_TYPE": "decision-approval-type",
        },
        "ANSWERS": {
            "DECISION": {
                # Building permit
                "APPROVED": "decision-decision-assessment-accepted",
                "REJECTED": "decision-decision-assessment-denied",
                "DEPRECIATED": "decision-decision-assessment-depreciated",
                # Preliminary clarification
                "POSITIVE": "decision-decision-assessment-positive",
                "POSITIVE_WITH_RESERVATION": "decision-decision-assessment-positive-with-reservation",
                "NEGATIVE": "decision-decision-assessment-negative",
            },
            "APPROVAL_TYPE": {
                "CONSTRUCTION_TEE_WITH_RESTORATION": "decision-approval-type-construction-tee-with-restoration",
                "BUILDING_PERMIT": "decision-approval-type-building-permit",
                "BUILDING_PERMIT_FREE": "decision-approval-type-building-permit-free",
                "PARTIAL_PERMIT_WITH_PARTIAL_CONSTRUCTION_TEE_AND_PARTIAL_RESTORATION": "decision-approval-type-partial-building-permit-partial-construction-tee-partial-restoration",
                "OVERALL_BUILDING_PERMIT": "decision-approval-type-overall-building-permit",
                "UNKNOWN": "decision-approval-type-unknown",
            },
        },
        "INSTANCE_STATE_AFTER_DECISION": "sb1",
        "TASKS_AFTER_BUILDING_PERMIT_DECISION": [
            "sb1",
            "create-manual-workitems",
            "create-publication",
        ],
    },
    "kt_so": {
        "ENABLED": True,
        "QUESTIONS": {
            "CONSTRUCTION_TEE": "decision-construction-tee",
        },
        "ANSWERS": {
            "DECISION": {
                "REJECTED": "decision-decision-declined",
                "PARTIALLY_APPROVED": "decision-decision-partially-approved",
                "RETREAT": "decision-decision-retreat",
            },
            "CONSTRUCTION_TEE": {
                "WITH_RESTORATION": "decision-construction-tee-with-restoration",
                "WITHOUT_RESTORATION": "decision-construction-tee-without-restoration",
            },
        },
    },
    "kt_gr": {
        "ENABLED": True,
    },
    "test": {
        "ENABLED": True,
        "ENABLE_STATS": True,
    },
}
