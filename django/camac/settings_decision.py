DECISION = {
    "default": {
        "QUESTION_SLUG": "decision-decision",
        "APPROVED": "decision-decision-approved",
        "REJECTED": "decision-decision-rejected",
        "INSTANCE_STATE_AFTER_DECISION": "construction-monitoring",
        "TASKS_AFTER_BUILDING_PERMIT_DECISION": ["construction-monitoring"],
    },
    "kt_bern": {
        "ENABLED": True,
        "QUESTION_SLUG": "decision-decision-assessment",
        "INSTANCE_STATE_AFTER_DECISION": "sb1",
        "TASKS_AFTER_BUILDING_PERMIT_DECISION": [
            "sb1",
            "create-manual-workitems",
            "create-publication",
        ],
    },
    "kt_gr": {
        "ENABLED": True,
    },
    "test": {
        "ENABLED": True,
    },
}
