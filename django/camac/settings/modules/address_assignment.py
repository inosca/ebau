from camac.settings.env import env

ADDRESS_ASSIGNMENT = {
    "default": {
        "EXAM_TASK": "formal-exam",
        "SUGGESTION_TASK": "address-assignment-make-suggestion",
        "CONFIRM_TASK": "address-assignment-confirm-suggestion",
        "MAIN_FORM_STREET_QUESTION_SLUG": "street-and-housenumber",
        "STREET_QUESTION_SLUG": "construction-step-adressvergabe-street",
        "REQUIRES_NEW_ADDRESS_QUESTION_SLUG": "neue-adresse-notwendig",
        "REQUIRES_NEW_ADDRESS_QUESTION_TRUE": "neue-adresse-notwendig-ja",
        "ADDRESS_VALID_QUESTION_SLUG": "construction-step-adressvergabe-is-approved",
        "ADDRESS_VALID_OPTION_SLUG": "construction-step-adressvergabe-is-approved-yes",
    },
    "kt_gr": {
        "ENABLED": env.bool("CONSTRUCTION_MONITORING_ENABLED", default=False),
    },
}
