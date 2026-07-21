ARE_SERVICE_GROUP = "authority-bab"
CANTON_SERVICE_GROUP = "service"
MUNICIPALITY_SERVICE_GROUP = "municipality"

# Services that receive "special" notifications after decision / acceptance
ARE_SERVICE_SLUG = "are"
GVG_SERVICE_SLUG = "gvg"
AIB_SERVICE_SLUG = "aib"

BAUBEITRAGSWESEN_FORM_INVESTITIONSANMELDUNG = "baubeitragswesen-investitionsanmeldung"
BAUBEITRAGSWESEN_FORM_PHASE_1 = "baubeitragswesen-phase-1"
BAUBEITRAGSWESEN_FORM_PHASE_2 = "baubeitragswesen-phase-2"
BAUBEITRAGSWESEN_FORM_TEILZAHLUNGEN = "baubeitragswesen-teilzahlungen"
BAUBEITRAGSWESEN_FORM_BAUABRECHNUNG = "baubeitragswesen-bauabrechnung"

# Form versions
BAUGESUCH_FORMS = [
    "baugesuch",
    "baugesuch-v2",
    "baugesuch-v3",
    "baugesuch-v4",
    "baugesuch-v5",
    "baugesuch-v6",
]
BAUANZEIGE_FORMS = [
    "bauanzeige",
    "bauanzeige-v3",
]
VORLAEUFIGE_BEURTEILUNG_FORMS = [
    "vorlaeufige-beurteilung",
    "vorlaeufige-beurteilung-v3",
    "vorlaeufige-beurteilung-v4",
    "vorlaeufige-beurteilung-v6",
]
SOLARANLAGE_FORMS = [
    "solaranlage",
    "solaranlage-v2",
    "solaranlage-v6",
    "solaranlage-andere",
]

BAUBEITRAGSWESEN_FORMS = [
    BAUBEITRAGSWESEN_FORM_INVESTITIONSANMELDUNG,
    BAUBEITRAGSWESEN_FORM_PHASE_1,
    BAUBEITRAGSWESEN_FORM_PHASE_2,
    BAUBEITRAGSWESEN_FORM_TEILZAHLUNGEN,
    BAUBEITRAGSWESEN_FORM_BAUABRECHNUNG,
]


MIGRATED_INSTANCE_FORMS = ["migriertes-dossier"]

PUBLIC_INSTANCES_URL_PREFIXES = {
    "de": "/oeffentliche-auflage",
    "it": "/esposizione-pubblica",
}
