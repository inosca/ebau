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


# match these to categories
FORM_SLUGS = [
    "baugesuch-reklamegesuch",
    "projektanderung",
    "vorentscheid-gemass-ss84-pbg",
    "baugesuch-reklamegesuch-v2",
    "projektanderung-v2",
    "vorentscheid-gemass-ss84-pbg-v2",
    "baugesuch-reklamegesuch-v3",
    "baugesuch-reklamegesuch-v4",
    "baugesuch-reklamegesuch-v5",
    "projektanderung-v3",
    "projektanderung-v4",
    "projektanderung-v5",
    "projektanderung-v6",
    "vorentscheid-gemass-ss84-pbg-v3",
    "vorentscheid-gemass-ss84-pbg-v4",
    "vorentscheid-gemass-ss84-pbg-v5",
    "vorabklarung",
    "vorabklarung-v2",
    "vorabklarung-v3",
    "vorabklarung-v4",
    "baumeldung-fur-geringfugiges-vorhaben",
    "baumeldung-fur-geringfugiges-vorhaben-v2",
    "baumeldung-fur-geringfugiges-vorhaben-v3",
    "baumeldung-fur-geringfugiges-vorhaben-v4",
    "technische-bewilligung",
    "technische-bewilligung-v2",
    "konzession-fur-wasserentnahme",
    "konzession-fur-wasserentnahme-v2",
    "konzession-fur-wasserentnahme-v3",
    "anlassbewilligungen-verkehrsbewilligungen",
    "anlassbewilligungen-verkehrsbewilligungen-v2",
    "anlassbewilligungen-verkehrsbewilligungen-v3",
    "plangenehmigungsgesuch",
    "plangenehmigungsgesuch-v2",
    "plangenehmigungsgesuch-v3",
    "projektgenehmigungsgesuch-gemass-ss15-strag",
    "projektgenehmigungsgesuch-gemass-ss15-strag-v2",
    "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
    "geschaeftskontrolle",
    "migriertes-dossier",
]
