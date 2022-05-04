# decisions
DECISIONS_BEWILLIGT = "accepted"
DECISIONS_ABGELEHNT = "denied"
DECISIONS_ABGESCHRIEBEN = "writtenOff"
VORABKLAERUNG_DECISIONS_BEWILLIGT = "positive"
VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT = "conditionallyPositive"
VORABKLAERUNG_DECISIONS_NEGATIVE = "negative"

DECISION_JUDGEMENT = {
    DECISIONS_BEWILLIGT: 1,
    DECISIONS_ABGELEHNT: 3,
    VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT: 2,
    VORABKLAERUNG_DECISIONS_NEGATIVE: 4,
}


# The different forms (e. g. -v2 ...) are categorized by their description
FORM_DESCRIPTIONS = [
    "Baugesuch",
    "Projektänderung zu bewilligtem Baugesuch",
    "Vorabklärung",
    "Vorentscheid gemäss § 84 PBG",
    "Projektgenehmigungsgesuch gemäss § 15 StraG",
    "Migriertes Dossier",
]
