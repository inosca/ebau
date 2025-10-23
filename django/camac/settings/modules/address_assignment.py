from camac.settings.env import env

ADDRESS_ASSIGNMENT = {
    "default": {
        "EXAM_TASK": "formal-exam",
        "SUGGESTION_TASK": "address-assignment-make-suggestion",
        "CONFIRM_TASK": "address-assignment-confirm-suggestion",
        "MAIN_FORM_STREET_QUESTION_SLUG": "street-and-housenumber",
        "STREET_QUESTION_SLUG": "address-assignment-street",
        "REQUIRES_NEW_ADDRESS_QUESTION_SLUG": "neue-adresse-notwendig",
        "REQUIRES_NEW_ADDRESS_QUESTION_TRUE": "neue-adresse-notwendig-ja",
        "ADDRESS_VALID_QUESTION_SLUG": "address-assignment-valid",
        "ADDRESS_VALID_OPTION_SLUG": "address-assignment-valid-valid",
    },
    "kt_gr": {
        "ENABLED": env.bool("ADDRESS_ASSIGNMENT_ENABLED", default=False),
    },
}
