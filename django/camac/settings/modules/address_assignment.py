from camac.settings.env import env

ADDRESS_ASSIGNMENT = {
    "default": {
        "EXAM_TASK": "formal-exam",
        "SUGGESTION_TASK": "construction-step-adressvergabe",
        "CONFIRM_TASK": "construction-step-adressvergabe-confirm",
        "MAIN_FORM_STREET_QUESTION_SLUG": "street-and-housenumber",
        "STREET_QUESTION_SLUG": "construction-step-adressvergabe-street",
        "ADDRESS_VALID_QUESTION_SLUG": "construction-step-adressvergabe-is-approved",
        "ADDRESS_VALID_OPTION_SLUG": "construction-step-adressvergabe-is-approved-yes",
    },
    "kt_gr": {
        "ENABLED": env.bool("CONSTRUCTION_MONITORING_ENABLED", default=False),
    },
}
