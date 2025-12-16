ARE_SERVICE_GROUP = "authority-bab"
CANTON_SERVICE_GROUP = "service"
MUNICIPALITY_SERVICE_GROUP = "municipality"

# Services that receive "special" notifications after decision / acceptance
GVG_SERVICE_SLUG = "gvg"
AIB_SERVICE_SLUG = "aib"

# Form versions
BAUGESUCH_FORMS = [
    "baugesuch",
    "baugesuch-v2",
    "baugesuch-v3",
    "baugesuch-v4",
    "baugesuch-v5",
]
BAUANZEIGE_FORMS = [
    "bauanzeige",
    "bauanzeige-v3",
]
VORLAEUFIGE_BEURTEILUNG_FORMS = [
    "vorlaeufige-beurteilung",
    "vorlaeufige-beurteilung-v3",
    "vorlaeufige-beurteilung-v4",
]
SOLARANLAGE_FORMS = [
    "solaranlage",
    "solaranlage-v2",
    "solaranlage-andere",
]

PUBLIC_INSTANCES_URL_PREFIXES = {
    "de": "/oeffentliche-auflage",
    "it": "/esposizione-pubblica",
}
