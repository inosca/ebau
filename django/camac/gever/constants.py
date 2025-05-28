"""
Define some useful constants.

These constants should be referenced by code to refer to objects (such as
templates) that reside in the database. That way, we reduce the risk of typos

"""

TEMPLATE_GESCHAEFT_EBAU_BG_GEMEINDE = "ebau-bg-gemeinde"
TEMPLATE_GESCHAEFT_EBAU_BG_RSTA = "ebau-bg-rsta"
TEMPLATE_GESCHAEFT_EBAU_VA_GEMEINDE = "ebau-va-gemeinde"
TEMPLATE_GESCHAEFT_EBAU_VA_RSTA = "ebau-va-rsta"

GESCHAEFT_TEMPLATES = [
    # TODO: Once (if really deemed necessary), we'll probably also
    # need to add the "Schiesslärm" templates
    TEMPLATE_GESCHAEFT_EBAU_BG_GEMEINDE,
    TEMPLATE_GESCHAEFT_EBAU_BG_RSTA,
    TEMPLATE_GESCHAEFT_EBAU_VA_GEMEINDE,
    TEMPLATE_GESCHAEFT_EBAU_VA_RSTA,
]

BETEILIGUNG_TEMPLATES = [
    # TODO: Once kown, we also need to have the templates for "Beteiligung".
    #  We don't have those yet, so we're still creating "naked" Geschaeft
    # objects for now
]

AUFGABE_TEMPLATES = [
    # TODO also: Once kown, we also need to have the templates for "Aufgabe".
    # We don't have those yet, so we're still creating "naked" Geschaeft
    # objects for now
]

VERFAHRENSSTAND_COMPLETED = "verfahrensstand-completed"
VERFAHRENSSTAND_OPEN = "verfahrensstand-open"

HERKUNFT_MUNICIPALITY = "herkunft-gemeinde"
HERKUNFT_RSTA = "herkunft-rsta"

# Service slugs
AGR_SERVICE_SLUG_BAUEN = "agr-bauen"
AGR_SERVICE_SLUG_SHOOTING_NOISE = "agr-schiesslaerm"
ALL_AGR_SERVICE_SLUGS = [AGR_SERVICE_SLUG_BAUEN, AGR_SERVICE_SLUG_SHOOTING_NOISE]

GEVER_TASK_SLUG = "gever"

INSTANCE_TYPE_SHORT = {
    "Einfache Vorabklärung": "VA",
    "Vollständige Vorabklärung": "VA",
    "Verlängerung Geltungsdauer": "VA",
    "Baugesuch": "BG",
    "Baugesuch mit UVP": "BG",
    "Baupolizeiliches Verfahren": "BG",
    "Voranfrage": "VA",
    "Projektänderung": "PÄ",
    "Hecken / Feldgehölze / Bäume": "BG",
    "Klärung Baubewilligungspflicht": "BG",
    "Meldung Benützung von öffentlichem Terrain": "BG",
    "Meldung Solaranlagen": "BG",
    "Meldung Wärmeerzeugerersatz": "BG",
    "Migriertes Dossier": "BG",
    "Zutrittsermächtigung": "VA",
}
