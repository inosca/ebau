TRIAGE_QUESTION = (1, 40095, 40519)

# item, chapter, question
MAPPING = {
    "bab-streusiedlungsgebiet": (1, 40095, 40520),
    "bab-erwerbsmaessigen-landwirtschaft": (1, 40095, 40522),
    "bab-01-07-1972-um-und-ausgebaut": (1, 40095, 40523),
    "bab-lanat-vorgeprueft": (1, 40095, 40524),
    "bab-lanat-vorgeprueft-bemerkungen": (1, 40095, 40525),
    "bab-naehe-von-schutzenswerten-gebaeuden": (1, 40095, 120001),
    "bab-ortsschutzperimeter": (1, 40095, 40526),
    "bab-ortsschutzperimeter-bemerkungen": (1, 40095, 40527),
    "bab-anzahl-wohnungen-01-07-1972": (1, 40096, 40528),
    "bab-nutzung-01-07-1972": (1, 40097, 40529),
    "bab-bgf-01-07-1972": (1, 40098, 40530),
    "bab-bgf-heute": (1, 40098, 40531),
    "bab-bgf-nach-ausbau": (1, 40098, 40532),
    "bab-nnf-01-07-1972": (1, 40099, 40533),
    "bab-nnf-heute": (1, 40099, 40534),
    "bab-nnf-nach-ausbau": (1, 40099, 40535),
    "bab-bemerkungen": (1, 40100, 40536),
}

VALUE_MAPPING = {
    "bab-nutzung-01-07-1972": {
        "WOH": "bab-nutzung-01-07-1972-wohnen",
        "LAG": "bab-nutzung-01-07-1972-lager",
        "IND": "bab-nutzung-01-07-1972-industrie",
        "GEW": "bab-nutzung-01-07-1972-gewerbe",
        "DIE": "bab-nutzung-01-07-1972-dienstleistung",
        "VER": "bab-nutzung-01-07-1972-verkauf",
        "LAN": "bab-nutzung-01-07-1972-landwirtschaft",
        "GAS": "bab-nutzung-01-07-1972-gastgewerbe",
        "AND": "bab-nutzung-01-07-1972-andere",
    }
}
