from datetime import timedelta

DISTRIBUTION = {
    "default": {
        "DEFAULT_DEADLINE_DELTA": timedelta(days=30),
        "DISTRIBUTION_WORKFLOW": "distribution",
        "DISTRIBUTION_TASK": "distribution",
        "DISTRIBUTION_INIT_TASK": "init-distribution",
        "DISTRIBUTION_COMPLETE_TASK": "complete-distribution",
        "INQUIRY_TASK": "inquiry",
        "INQUIRY_CREATE_TASK": "create-inquiry",
        "INQUIRY_CHECK_TASK": "check-inquiries",
        "INQUIRY_WORKFLOW": "inquiry",
        "INQUIRY_ANSWER_FORM": "inquiry-answer",
        "QUESTIONS": {
            "DEADLINE": "inquiry-deadline",
            "STATUS": "inquiry-answer-status",
            "STATEMENT": "inquiry-answer-statement",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
        },
    },
    "kt_bern": {"ENABLED": True},
    "kt_schwyz": {"ENABLED": True},
}
