# form version
BAUGESUCH_FORMS = [
    "baugesuch",
    "baugesuch-mit-uvp",
    "baugesuch-v2",
    "baugesuch-mit-uvp-v2",
]

PGV_GAS_FORMS = [
    "plangenehmigungsverfahren-gas",
    "plangenehmigungsverfahren-gas-v2",
]

PGV_BUND_FORMS = [
    "plangenehmigungsverfahren-bund",
    "plangenehmigungsverfahren-bund-v2",
]

PGV_FORMS = [
    *PGV_GAS_FORMS,
    *PGV_BUND_FORMS,
]

ANFRAGE_INTERN_FORMS = [
    "anfrage-intern",
    "anfrage-intern-v2",
]

VORENTSCHEID_FORMS = [
    "vorentscheid",
    "vorentscheid-v2",
]

VERSIONED_MAIN_FORMS = [
    *BAUGESUCH_FORMS,
    *PGV_FORMS,
    *ANFRAGE_INTERN_FORMS,
    *VORENTSCHEID_FORMS,
]
