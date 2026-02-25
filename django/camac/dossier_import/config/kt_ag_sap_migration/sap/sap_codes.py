from typing import Dict, Union

FIELD_CODES: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
    "ERFGRND": {
        "1": "Gesuch in Papierform",
        "2": "Bauen ohne Baubewilligung",
        "3": "Nacherfassung",
        "4": "Online Erfassung",
    },
    "VERFTYP": {"1": "Ordentlich", "2": "Vereinfacht", "3": "Direktentscheid"},
    "GINTZ_ART": {"01": "Dienstleistung", "02": "Gewerbe", "03": "Industrie"},
    "KA_LGN_KNZ": {
        "0": "bestehend",
        "1": "neu",
        "2": "nicht angeschlossen",
    },
    "KA_BAN_KNZ": {
        "0": "bestehend",
        "1": "neu",
        "2": "nicht angeschlossen",
    },
    "BAU_ZON": {
        "1": "innerhalb rechtskräftiger Bauzone",
        "2": "ausserhalb rechtskräftiger Bauzone",
        "3": "teilweise innerhalb / teilweise ausserhalb Bauzone",
        "4": "übriges Gebiet",
    },
    "EKE_ERF": {
        "1": "nicht erforderlich",
        "2": "erforderlich und liegt bei",
        "3": "erforderlich und wird vor Baubeginn eingereicht",
    },
    "GESART": {
        "GESART": {
            "1": "Anfrage",
            "2": "Baugesuch",
            "3": "Umweltverträglichkeitsprüfung (UVP)",
            "4": "Umnutzung",
            "5": "Vorentscheid",
            "6": "Rodung",
            "7": "Reklame",
            "8": "Abbruch",
            "9": "PGV",
            "10": "Anhörung",
        },
    },
    "DWFLOW": {
        "DWTYP": {
            "ABS": "Abschreibung",
            "EIN": "Einsicht",
            "ERG": "Ergänzung",
            "RBS": "Rückbau bestätigen",
            "RVL": "Nachbesserung Rückbau verlange",
            "STG": "Stellungnahme Gesuch",
            "STI": "Stellungnahme intern",
            "AUF": "Auflagen",
            "KNE": "Ergänzung des Kantons",
        },
        "DWSTAT": {
            "": "",
            "000": "initial",
            "005": "offen",
            "010": "eingegangen",
            "015": "erledigt",
            "020": "abgelehnt",
            "025": "akzeptiert",
            "030": "geschlossen",
        },
    },
    "DWFLOW_DOC": {
        "DOCTYPE": {
            "DTO": "Dokumente zur Prüfung",
            "DTE": "Dokumente zur Begutachtung",
            "RBS": "Rückbau akzeptieren",
            "RVL": "Rückbau verlangen",
            "SEF": "Stellungnahme einfordern",
            "SEW": "Stellungnahme Einwendung",
            "VDF": "Vorprüfung durchführen",
            "EUE": "Ergänzung überarbeiten",
        },
    },
    "DWFLOW_REC": {
        "ANTRAG": {
            "TZA": "Teilweise Zustimmung mit Auflage(n)",
            "ABT": "Abweisung mit Tolerierung",
            "": "",
            "ZUA": "Zustimmung mit Auflage(n)",
            "ABW": "Abweisung",
            "ERG": "Unterlagenergänzung",
            "SON": "Sonstiges",
            "TZU": "Teilweise Zustimmung",
            "ZUS": "Zustimmung",
        },
        "REASON": {
            "TZA": "Teilweise Zustimmung mit Auflage(n)",
            "ABT": "Abweisung mit Tolerierung",
            "": "",
            "ZUA": "Zustimmung mit Auflage(n)",
            "ABW": "Abweisung",
            "ERG": "Unterlagenergänzung",
            "SON": "Sonstiges",
            "TZU": "Teilweise Zustimmung",
            "ZUS": "Zustimmung",
        },
        "RCSTAT": {
            "OFF": "Offen",
            "": "",
            "ABG": "Abgelehnt",
            "AKZ": "Akzeptiert",
            "EIN": "Eingegangen",
        },
    },
    "DATES": {
        "TRMTYP": {
            "ABS": "Abschreibung",
            "AFL": "Auflagefrist",
            "FRS": "Frist",
            "SIS": "Sistierung",
            "VEF": "Verfügung",
        }
    },
    "ENTSCHEID": {
        "ART_ID": {
            "BE": "Bewilligung",
            "AS": "Abschreibung",
            "NE": "Nichteintreten",
            "AW": "Abweisung",
            "TW": "Teilabweisung",
            "AA": "Antwort auf Anfrage",
        }
    },
    "KANTON_KANALISATION": {
        "0": "Keine",
        "1": "Bestehend",
        "2": "Neu",
        "3": "Nicht angeschlossen",
    },
}
