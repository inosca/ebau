# item, chapter, question
MAPPING_MUNICIPALITY = {
    "fp-gesuchsbewilligungsart": (1, 40089, 40468),
    "fp-gesuchsbewilligungsart-andere": (1, 40089, 40469),
    "fp-profile": (1, 40089, 40474),
    "fp-profile-bemerkungen": (1, 40089, 40475),
    "fp-formulare-vollstaendig": (1, 40089, 40476),
    "fp-formulare-vollstaendig-bemerkungen": (1, 40089, 40477),
    "fp-beilagen-vorhanden": (1, 40089, 40478),
    "fp-beilagen-vorhanden-bemerkungen": (1, 40089, 40479),
    "fp-begruendungen-fuer-ausnahmen": (1, 40089, 40480),
    "fp-begruendungen-fuer-ausnahmen-bemerkungen": (1, 40089, 40481),
    "fp-form-und-inhalt-des-situationsplanes": (1, 40089, 40482),
    "fp-form-und-inhalt-des-situationsplanes-bemerkungen": (1, 40089, 40483),
    "fp-projektplaene-vorhanden": (1, 40089, 40484),
    "fp-projektplaene-vorhanden-bemerkungen": (1, 40089, 40485),
    "fp-offenkundige-materielle-maengel": (1, 40089, 40486),
    "fp-zustaendige-baubewilligungsbehoerde": (1, 40089, 40487),
}

RSTA_TRIAGE_QUESTION = (1, 40089, 40487)

# item, chapter, question
MAPPING_RSTA = {
    "fp-gesuchsbewilligungsart": (1, 40091, 40492),
    "fp-gesuchsbewilligungsart-andere": (1, 40091, 40493),
    "fp-profile": (1, 40091, 40494),
    "fp-profile-bemerkungen": (1, 40091, 40495),
    "fp-formulare-vollstaendig": (1, 40091, 40496),
    "fp-formulare-vollstaendig-bemerkungen": (1, 40091, 40497),
    "fp-beilagen-vorhanden": (1, 40091, 40498),
    "fp-beilagen-vorhanden-bemerkungen": (1, 40091, 40499),
    "fp-begruendungen-fuer-ausnahmen": (1, 40091, 40500),
    "fp-begruendungen-fuer-ausnahmen-bemerkungen": (1, 40091, 40501),
    "fp-form-und-inhalt-des-situationsplanes": (1, 40091, 40502),
    "fp-form-und-inhalt-des-situationsplanes-bemerkungen": (1, 40091, 40503),
    "fp-projektplaene-vorhanden": (1, 40091, 40504),
    "fp-projektplaene-vorhanden-bemerkungen": (1, 40091, 40505),
    "fp-offenkundige-materielle-maengel": (1, 40091, 40506),
    "fp-zustaendige-baubewilligungsbehoerde": (1, 40091, 40507),
}

VALUE_MAPPING = {
    "fp-gesuchsbewilligungsart": {
        "ORD": "fp-gesuchsbewilligungsart-ordentliche-baubewilligung",
        "KLE": "fp-gesuchsbewilligungsart-kleine-baubewilligung",
        "TEI": "fp-gesuchsbewilligungsart-teilbaubewilligung",
        "GEN": "fp-gesuchsbewilligungsart-generelle-baubewilligung",
        "VOR": "fp-gesuchsbewilligungsart-vorzeitige-baubewilligung",
        "VOR2": "fp-gesuchsbewilligungsart-vorzeitiger-baubeginn",
        "VORZ": "fp-gesuchsbewilligungsart-vorzeitiger-baubeginn",
        "AND": "fp-gesuchsbewilligungsart-andere",
    },
    "fp-zustaendige-baubewilligungsbehoerde": {
        "GEM": "fp-zustaendige-baubewilligungsbehoerde-gemeinde",
        "REG": "fp-zustaendige-baubewilligungsbehoerde-regierungsstatthalteramt",
        "ZUS": "fp-zustaendige-baubewilligungsbehoerde-unklar",
    },
}
