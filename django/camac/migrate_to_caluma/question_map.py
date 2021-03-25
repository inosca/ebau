from .transforms import Transform

# Question mapping triplets:
# First:  CAMAC question identifier mapping(ch123q344)
# Second: Caluma question identifier
# Third: transform function

MUNICIPALITY_MAP = {
    "22": "22",  # Alle Gemeinden
    "1": "1",  # Altdorf
    "2": "2",  # Andermatt
    "3": "3",  # Attinghausen
    "5": "5",  # Bürglen
    "21": "21",  # Diverse Gemeinden
    "6": "6",  # Erstfeld
    "7": "7",  # Flüelen
    "9": "9",  # Gurtnellen
    "8": "8",  # Göschenen
    "10": "10",  # Hospental
    "11": "11",  # Isenthal
    "12": "12",  # Realp
    "13": "13",  # Schattdorf
    "14": "14",  # Seedorf
    "4": "4",  # Seedorf (Ortsteil Bauen)
    "15": "15",  # Seelisberg
    "16": "16",  # Silenen
    "17": "17",  # Sisikon
    "18": "18",  # Spiringen
    "19": "19",  # Unterschächen
    "20": "20",  # Wassen
}

GRUNDNUTZUNG_MAP = {
    "W1": "Wohnzone 1",  # Wohnzone 1
    "W2": "Wohnzone 2",  # Wohnzone 2
    "W3": "Wohnzone 3",  # Wohnzone 3
    "W4": "Wohnzone 4",  # Wohnzone 4
    "GE": "Gewerbezone",  # Gewerbezone
    "I": "Industriezone",  # Industriezone
    "WG2": "Wohn- und Gewerbezone 2",  # Wohn- und Gewerbezone 2
    "WG3": "Wohn- und Gewerbezone 3",  # Wohn- und Gewerbezone 3
    "WG4": "Wohn- und Gewerbezone 4",  # Wohn- und Gewerbezone 4
    "K1": "Kernzone 1",  # Kernzone 1
    "K3": "Kernzone 3",  # Kernzone 3
    "BZ": "Bahnhofzone",  # Bahnhofzone
    "OE": "Zone für öffentliche Bauten und Anlagen",  # Zone für öffentliche Bauten und Anlagen
    "FZ": "Freihaltezone",  # Freihaltezone
    "TZ": "Tourismuszone",  # Tourismuszone
    "SF": "Zone für Sport- und Freizeitanlagen",  # Zone für Sport- und Freizeitanlagen
    "VF": "Verkehrsfläche innerhalb Bauzonen",  # Verkehrsfläche innerhalb Bauzonen
    "AB": "Zone für besondere Anlagen und Betriebsstätten",  # Zone für besondere Anlagen und Betriebsstätten
    "L": "Landwirtschaftszone",  # Landwirtschaftszone
    "SL": "Speziallandwirtschaftszone",  # Speziallandwirtschaftszone
    "RB": "Rebbauzone",  # Rebbauzone
    "NSl": "Naturschutzzone lokal",  # Naturschutzzone lokal
    "FZaB": "Freihaltezone ausserhalb Bauzonen",  # Freihaltezone ausserhalb Bauzonen
    "GR": "Gewässerraumzone",  # Gewässerraumzone
    "Ge": "Gewässer",  # Gewässer
    "WZ": "Weilerzone",  # Weilerzone
    "VFaB": "Verkehrsfläche ausserhalb Bauzonen",  # Verkehrsfläche ausserhalb Bauzonen
    "RZ": "Reservezone",  # Reservezone
    "Wa": "Wald",  # Wald
    "D": "Deponiezone",  # Deponiezone
    "A": "Abbauzone",  # Abbauzone
    "AD": "Abbau- und Deponiezone",  # Abbau- und Deponiezone
    "SFG": "Zone für Sport- und Freizeitanlagen Golf",  # Zone für Sport- und Freizeitanlagen Golf
    "RZu": "Reservezone, unproduktiv",  # Reservezone, unproduktiv
    "W2K": "Wohnzone 2 Kirchhügel",  # Wohnzone 2 Kirchhügel
    "W2a": "Wohnzone 2a",  # Wohnzone 2a
    "W2b": "Wohnzone 2b",  # Wohnzone 2b
    "W2c": "Wohnzone 2c",  # Wohnzone 2c
    "WE": "Wohnzone Eggberge",  # Wohnzone Eggberge
    "WL": "Wohnzone im Landschaftsgebiet",  # Wohnzone im Landschaftsgebiet
    "WK": "Wohnzone Kolonie",  # Wohnzone Kolonie
    "WSRütli": "Sonderwohnzone Rütli",  # Sonderwohnzone Rütli
    "WGE": "Wohn- und Gewerbezone Eggberge",  # Wohn- und Gewerbezone Eggberge
    "K2": "Kernzone 2",  # Kernzone 2
    "K4": "Kernzone 4",  # Kernzone 4
    "I1": "Industriezone 1",  # Industriezone 1
    "I2": "Industriezone 2",  # Industriezone 2
    "ABEC": "Zone für besondere Anlage und Betriebsstätte Event-Center",  # Zone für besondere Anlage und Betriebsstätte Event-Center
    "WS": "Sonderwohnzone",  # Sonderwohnzone
    "BZB": "BZ Brüsti",  # BZ Brüsti
    "Eh": "Erholungszone",  # Erholungszone
    "FPZ": "Flugplatzzone",  # Flugplatzzone
    "ABE": "Gewerbesonderzone Eielen",  # Gewerbesonderzone Eielen
    "ABH": "Gewerbesonderzone Harder",  # Gewerbesonderzone Harder
    "ABN": "Niederhofen",  # Niederhofen
    "ABSH": "Sondernutzungszone Holzheizwerk",  # Sondernutzungszone Holzheizwerk
    "SZB": "Sonderzone Baugruppen",  # Sonderzone Baugruppen
    "G1": "Gewerbezone 1",  # Gewerbezone 1
    "G2": "Gewerbezone 2",  # Gewerbezone 2
    "W5": "Wohnzone 5+",  # Wohnzone 5+
    "WG5": "Wohn- und Gewerbezone 5+",  # Wohn- und Gewerbezone 5+
    "K": "Kernzone",  # Kernzone
    "KZE": "Kernzone - Zentrum",  # Kernzone - Zentrum
    "LW": None,  # Value not in answerlist
    "R": None,  # Value not in answerlist
    "W": None,  # Value not in answerlist
    "KZ": None,  # Value not in answerlist
    "KS": None,  # Value not in answerlist
    "ViB": None,  # Value not in answerlist
    "T": None,  # Value not in answerlist
    "G": None,  # Value not in answerlist
    "O": None,  # Value not in answerlist
    "VaB": None,  # Value not in answerlist
    "F": None,  # Value not in answerlist
    "FaB": None,  # Value not in answerlist
    "B": None,  # Value not in answerlist
    "U": None,  # Value not in answerlist
    "": None,  # Empty value in answerslist
}

UEBERLAGERTE_NUTZUNG_MAP = {
    "OS": "Ortsbildschutzzone",  # Ortsbildschutzzone
    "SOK": "Schutzobjekt in Kernzonen",  # Schutzobjekt in Kernzonen
    "Arch": "Archäologisches Funderwartungsgebiet",  # Archäologisches Funderwartungsgebiet
    "NSlü": "Naturschutzzone lokal, überlagert",  # Naturschutzzone lokal, überlagert
    "LSl": "Landschaftsschutzzone lokal",  # Landschaftsschutzzone lokal
    "LpB": "Gebiet mit landschaftsprägenden Bauten",  # Gebiet mit landschaftsprägenden Bauten
    "TrS": "Gebiet mit traditioneller Streubauweise",  # Gebiet mit traditioneller Streubauweise
    "GRü": "Gewässerraumzone, überlagert",  # Gewässerraumzone, überlagert
    "GZr": "Gefahrenzone rot",  # Gefahrenzone rot
    "GZb": "Gefahrenzone blau",  # Gefahrenzone blau
    "GZg": "Gefahrenzone gelb",  # Gefahrenzone gelb
    "ZW": "Zone für Wintersport",  # Zone für Wintersport
    "Dü": "Deponiezone, überlagert",  # Deponiezone, überlagert
    "Aü": "Abbauzone, überlagert",  # Abbauzone, überlagert
    "ABü": "Zone für besondere Anlagen und Betriebsstätten, überlagert",  # Zone für besondere Anlagen und Betriebsstätten, überlagert
    "ZBG": "Zone für Bauten in Gewässern",  # Zone für Bauten in Gewässern
    "SFü": "Zone für Sport- und Freizeitanlagen, überlagert",  # Zone für Sport- und Freizeitanlagen, überlagert
    "QPr": "Bereich rechtsgültiger Quartierplan",  # Bereich rechtsgültiger Quartierplan
    "QGPr": "Bereich rechtsgültiger Quartiergestaltungsplan",  # Bereich rechtsgültiger Quartiergestaltungsplan
    "QPp": "Zone mit Quartierplanpflicht",  # Zone mit Quartierplanpflicht
    "QGPp": "Zone mit Quartiergestaltungsplanpflicht",  # Zone mit Quartiergestaltungsplanpflicht
    "NvI": "Nutzungsvorbehalt Immissionsschutz",  # Nutzungsvorbehalt Immissionsschutz
    "GvRR": "Genehmigungsvorbehalt RR",  # Genehmigungsvorbehalt RR
    "wfF": "weitere flächenbezogene Festlegung",  # weitere flächenbezogene Festlegung
    "BLS": "Baulinie Strasse",  # Baulinie Strasse
    "BLG": "Baulinie Gewässer",  # Baulinie Gewässer
    "BLI": "Baulinie Immissionsschutz",  # Baulinie Immissionsschutz
    "BL": "weitere Baulinie (gem. Art. 49 PBG)",  # weitere Baulinie (gem. Art. 49 PBG)
    "NOll": "Naturobjekt lokal, linear",  # Naturobjekt lokal, linear
    "KOll": "Kulturobjekt lokal, linear",  # Kulturobjekt lokal, linear
    "NOl": "Naturobjekt lokal",  # Naturobjekt lokal
    "KOl": "Kulturobjekt lokal",  # Kulturobjekt lokal
    "EO": "Einzelobjekt in Kern- und Schutzzonen",  # Einzelobjekt in Kern- und Schutzzonen
    "KOIIGM": "Geschützte Mauer",  # Geschützte Mauer
    "NOIEB": "Einzelbaum",  # Einzelbaum
    "EOSG": "Schutzwürdige Gebäude",  # Schutzwürdige Gebäude
    "VB": "Gebiet mit verdichteter Bauweise",  # Gebiet mit verdichteter Bauweise
    "QRPr": "Bereich rechtsgültiger Quartierrichtplan",  # Bereich rechtsgültiger Quartierrichtplan
    "AR": "Abfahrtsrouten",  # Abfahrtsrouten
    "F": "Fernsprenganlagen",  # Fernsprenganlagen
    "PA": "Parkanlagen",  # Parkanlagen
    "SUB": "Seeuferbereich, überlagert",  # Seeuferbereich, überlagert
    "E": "Schutzbereich",  # Schutzbereich
    "KOIIwG": "wichtige Gasse",  # wichtige Gasse
    "QRPp": "Zone mit Quartierrichtplanpflicht",  # Zone mit Quartierrichtplanpflicht
    "ABüH": "Gewerbesonderzone Harder, überlagert",  # Gewerbesonderzone Harder, überlagert
    "PB": "Projektierungsbereich",  # Projektierungsbereich
    "GSZ": "Grundwasserschutzzone",
    "GSZp": "Grundwasserschutzzonen provisorisch",
    "GSA": "Grundwasserschutzareale",
    "GSAp": "Grundwasserschutzareale provisorisch",
    "GG": "Gefahrengebiet",
    "WRZ": "Wildruhezone",
    "WR": "Waldreservat",
    "NSrn": "Naturschutzzone regional / national",
    "FM": "Flachmoor",
    "LSrn": "Landschaftsschutzzone regional / national",
    "GmsB": "Gebiete mit schützenswerter Bausubstanz",
    "NOrnl": "Naturobjekt regional / national, linear",
    "NOrn": "Naturobjekt regional / national, punktförmig",
    "KOrnl": "Kulturobjekt regional / national, linear",
    "KOrn": "Kulturobjekt regional / national, punktförmig",
    "FFF": "Fruchtfolgefläche",
    "GRu": None,  # Value not in answerlist
    "WS": None,  # Value not in answerlist
    "NSlu": None,  # Value not in answerlist
    "SFu": None,  # Value not in answerlist
    "": None,  # Empty value in answerslist
}


QUESTION_MAP_BAUGESUCH = [
    (
        "c2q260i1",
        "status-bauprojekt",
        Transform.static_if_present("status-bauprojekt-nachtraeglich"),
    ),
    (
        "c2q260i1",
        "stand-der-realisierung",
        Transform.join_checkbox(
            {
                "already_realized": "stand-der-realisierung-realisiert",
                "stopped": "stand-der-realisierung-realisierung-gestartet-baustopp-verfuegt",
            },
            "; ",
        ),
    ),
    # address / names
    # Chapter 1: baugesuch / personendaten / gesuchsteller
    # TODO: list/subform, different types of address?
    # sub part 1: Gesuchsteller
    (
        "c1q23i1",
        "applicant.*.first-name",
        Transform.extract_name_part("first"),
    ),  # Name / Vorname
    (
        "c1q23i1",
        "applicant.*.last-name",
        Transform.extract_name_part("last"),
    ),  # Name / Vorname
    ("c1q61i1", "applicant.*.street", Transform.none),  # Strasse/Nr.
    ("c1q62i1", "applicant.*.zip", Transform.extract_from_city("zip")),  # PLZ / Ort
    ("c1q62i1", "applicant.*.city", Transform.extract_from_city("city")),
    ("c1q64i1", "applicant.*.phone", Transform.append_text()),  # Telefon Privat
    ("c1q67i1", "applicant.*.phone", Transform.append_text()),  # Telefon Geschäft
    (
        "c1q65i1",
        "applicant.*.phone",
        Transform.append_text(),
    ),  # Telefon Mobile (again?)
    ("c1q66i1", "applicant.*.e-mail", Transform.none),  # Email
    ("c1q221i1", "applicant.*.juristic-person-name", Transform.none),  # Organisation
    (
        "c1q221i1",
        "applicant.*.is-juristic-person",
        Transform.yes_if_present("is-juristic-person"),
    ),  # Organisation
    # sub part 2: projektverfasserin
    ("c1q71i1", "project-author.*.first-name", Transform.extract_name_part("first")),
    (
        "c1q71i1",
        "project-author.*.last-name",
        Transform.extract_name_part("last"),
    ),  # Name / Vorname
    ("c1q72i1", "project-author.*.street", Transform.none),  # Strasse/Nr.
    ("c1q73i1", "project-author.*.zip", Transform.extract_from_city("zip")),
    ("c1q73i1", "project-author.*.city", Transform.extract_from_city("city")),
    ("c1q75i1", "project-author.*.phone", Transform.append_text()),  # Telefon Mobile
    (
        "c1q76i1",
        "project-author.*.phone",
        Transform.append_text(),
    ),  # Telefon Mobile - AGAIN?
    ("c1q78i1", "project-author.*.phone", Transform.none),
    ("c1q77i1", "project-author.*.e-mail", Transform.none),
    (
        "c1q222i1",
        "project-author.*.juristic-person-name",
        Transform.none,
    ),  # Organisation
    (
        "c1q222i1",
        "project-author.*.is-juristic-person",
        Transform.yes_if_present("is-juristic-person"),
    ),  # Organisation
    # sub part 3: Grundeigentümer
    (
        "c1q82i1",
        "landowner.*.first-name",
        Transform.extract_name_part("last"),
    ),  # nachname, vorname
    (
        "c1q82i1",
        "landowner.*.last-name",
        Transform.extract_name_part("first"),
    ),  # nachname, vorname
    ("c1q83i1", "landowner.*.street", Transform.none),  # Strasse/Nr.
    ("c1q84i1", "landowner.*.zip", Transform.extract_from_city("zip")),
    ("c1q84i1", "landowner.*.city", Transform.none),
    ("c1q86i1", "landowner.*.phone", Transform.append_text()),  # Telefon Privat
    ("c1q87i1", "landowner.*.phone", Transform.none),  # Telefon Mobile
    ("c1q89i1", "landowner.*.phone", Transform.append_text()),  # Telefon Geschäft
    ("c1q88i1", "landowner.*.e-mail", Transform.none),  # Email
    ("c1q223i1", "landowner.*.juristic-person-name", Transform.none),  # Organisation
    (
        "c1q223i1",
        "landowner.*.is-juristic-person",
        Transform.yes_if_present("is-juristic-person"),
    ),  # Organisation
    ("c1q69i1", "invoice-recipient.*.first-name", Transform.none),
    # Chapter 3: Erstellung
    (
        "c3q2i1",
        "municipality",
        Transform.select(MUNICIPALITY_MAP),
    ),
    ("c2q2i1", "municipality", Transform.select(MUNICIPALITY_MAP)),
    ("c3q5i1", "leitbehoerde", Transform.none),
    ("c2q5i1", "leitbehoerde", Transform.none),
    # Chapter 21: Objektdaten
    ("c21q93i1", "parcel-street", Transform.none),
    ("c102q93i1", "parcel-street", Transform.none),
    ("c21q91i1", "parcels.*.parcel-number", Transform.none),
    ("c21q93i1", "parcels.*.parcel-street", Transform.none),
    ("c21q98i1", "proposal-description", Transform.append_text("; ")),
    ("c21q97i1", "proposal-description", Transform.prepend_proposal()),
    ("c21q102i1", "construction-cost", Transform.extract_number),
    ("c21q22i1", "grundnutzung", Transform.join_checkbox(GRUNDNUTZUNG_MAP, "; ")),
    (
        # Vorhaben -> Vorhaben
        "c21q97i1",
        "proposal",
        Transform.checkbox(
            {
                "21": "proposal-neubau",
                "22": "proposal-umbau-erneuerung-sanierung",
                "24": "proposal-umbau-erneuerung-sanierung",
                "23": "proposal-umbau-erneuerung-sanierung",
                "26": "proposal-abbruch-rueckbau",
                "27": "proposal-neubau",
                "25": "proposal-umbau-erneuerung-sanierung",
                "28": "proposal-neubau",
                "29": "proposal-neubau",
                "30": "proposal-neubau",  # TODO: Prepend to "detailbeschreibung vorhaben"
                "31": "proposal-neubau",  # TODO korrekt?
                "32": "proposal-neubau",  # TODO korrekt?
                "33": "proposal-neubau",  # TODO korrekt?
                "34": "proposal-neubau",
                "35": "proposal-neubau",
                "36": "proposal-umbau-erneuerung-sanierung",
            }
        ),
    ),
    (
        # Vorhaben -> Vorhaben
        "c101q97i1",
        "proposal",
        Transform.checkbox(
            {
                "21": "proposal-neubau",
                "22": "proposal-umbau-erneuerung-sanierung",
                "24": "proposal-umbau-erneuerung-sanierung",
                "23": "proposal-umbau-erneuerung-sanierung",
                "26": "proposal-abbruch-rueckbau",
                "27": "proposal-neubau",
                "25": "proposal-umbau-erneuerung-sanierung",
                "28": "proposal-neubau",
                "29": "proposal-neubau",
                "30": "proposal-neubau",  # TODO: Prepend to "detailbeschreibung vorhaben"
                "31": "proposal-neubau",  # TODO korrekt?
                "32": "proposal-neubau",  # TODO korrekt?
                "33": "proposal-neubau",  # TODO korrekt?
                "34": "proposal-neubau",
                "35": "proposal-neubau",
                "36": "proposal-umbau-erneuerung-sanierung",
            }
        ),
    ),
    (
        # Vorhaben -> Vorhaben
        "c102q97i1",
        "proposal",
        Transform.checkbox(
            {
                "21": "proposal-neubau",
                "22": "proposal-umbau-erneuerung-sanierung",
                "24": "proposal-umbau-erneuerung-sanierung",
                "23": "proposal-umbau-erneuerung-sanierung",
                "26": "proposal-abbruch-rueckbau",
                "27": "proposal-neubau",
                "25": "proposal-umbau-erneuerung-sanierung",
                "28": "proposal-neubau",
                "29": "proposal-neubau",
                "30": "proposal-neubau",  # TODO: Prepend to "detailbeschreibung vorhaben"
                "31": "proposal-neubau",  # TODO korrekt?
                "32": "proposal-neubau",  # TODO korrekt?
                "33": "proposal-neubau",  # TODO korrekt?
                "34": "proposal-neubau",
                "35": "proposal-neubau",
                "36": "proposal-umbau-erneuerung-sanierung",
            }
        ),
    ),
    (
        # Vorhaben -> Category
        "c21q97i1",
        "category",
        Transform.checkbox(
            {
                "21": None,
                "22": None,
                "24": None,
                "23": None,
                "26": None,
                "27": None,
                "25": None,
                "28": "category-tiefbaute",
                "29": None,
                "30": None,
                "31": "category-hochbaute",
                "32": "category-hochbaute",
                "33": "category-hochbaute",
                "34": "category-hochbaute",
                "35": None,
                "36": "category-tiefbaute",
            }
        ),
    ),
    (
        # Vorhaben -> Category
        "c101q97i1",
        "category",
        Transform.checkbox(
            {
                "21": None,
                "22": None,
                "24": None,
                "23": None,
                "26": None,
                "27": None,
                "25": None,
                "28": "category-tiefbaute",
                "29": None,
                "30": None,
                "31": "category-hochbaute",
                "32": "category-hochbaute",
                "33": "category-hochbaute",
                "34": "category-hochbaute",
                "35": None,
                "36": "cateogry-tiefbaute",
            }
        ),
    ),
    (
        # Vorhaben -> Category
        "c102q97i1",
        "category",
        Transform.checkbox(
            {
                "21": None,
                "22": None,
                "24": None,
                "23": None,
                "26": None,
                "27": None,
                "25": None,
                "28": "category-tiefbaute",
                "29": None,
                "30": None,
                "31": "category-hochbaute",
                "32": "category-hochbaute",
                "33": "category-hochbaute",
                "34": "category-hochbaute",
                "35": None,
                "36": "category-tiefbaute",
            }
        ),
    ),
    (
        # Gebäude Tabelle -> art-der-hochbaute
        "c21q97i1",
        "gebaeude.*.art-der-hochbaute",
        Transform.checkbox(
            {
                "Neubau": None,
                "Umbau": None,
                "Zweckänderung": None,
                "An/Aufbau": None,
                "Abbruch": None,
                "Reklame": "art-der-hochbaute-reklamebauten",
                "Terrainveranderung": None,
                "Terrainveränderung": None,
                "Garage": "art-der-hochbaute-garage-oder-carport",
                "Solaranlage": None,
                "Fassadensanierung": None,
                "EFH": "art-der-hochbaute-wohn-und-geschaftshaus",
                "MFH": "art-der-hochbaute-wohn-und-geschaftshaus",
                "Geschäftshaus": "art-der-hochbaute-wohn-und-geschaftshaus",
                "Lagergebäude": "art-der-hochbaute-andere",
                "Lagergebaude": "art-der-hochbaute-andere",
                "Antennenanlage": None,
                "Unterkellerung": None,
            }
        ),
    ),
    ("c21q101i1", "umbauter-raum", Transform.extract_number),
    ("c21q100i1", "purpose-description", Transform.none),
    (
        "c21q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),
    ("c21q103i1", "remarks", Transform.append_text("; ")),  # Bemerkungen
    ("c21q92i1", "parcels.*.building-law-number", Transform.none),  # Baurechtsnummer
    (
        # Nutzung (alternate destination: 'grundnutzung')
        "c21q99i1",
        "purpose",
        Transform.checkbox(
            {
                "Industrie": "purpose-industrie",
                "Dienstleistung": "purpose-dienstleistung",
                "Büro": "purpose-gewerbe",
                "Wohnen": "purpose-wohnen",
                "Gewerbe": "purpose-gewerbe",
                "Lager": "purpose-lager",
                "Landwirtschaft": "purpose-landwirtschaft",
                "Produktion": "purpose-gewerbe",
            }
        ),
    ),
    (
        # Orientierende Nutzungsplaninhalt
        "c21q95i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),
    (
        # Orientierende Nutzungsplaninhalt
        "c101q95i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),
    (
        # Orientierende Nutzungsplaninhalt
        "c102q95i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),
    # Chapter 22: Objektdaten
    (
        "c22q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),  # Überlagerte Nutzungsplaninhalte
    # Chapter 101: Objektdaten
    (
        "c101q22i1",
        "grundnutzung",
        Transform.join_checkbox(GRUNDNUTZUNG_MAP, "; "),
    ),  # Grundnutzungen
    (
        "c101q91i1",
        "parcels.*.parcel-number",
        Transform.none,
    ),  # Parzellennummer (TODO: Table?)
    ("c101q93i1", "parcels.*.parcel-street", Transform.none),  # Strasse/Flurname
    (
        "c101q98i1",
        "proposal-description",
        Transform.append_text("; "),
    ),  # Vorhaben / Beschrieb
    ("c101q103i1", "remarks", Transform.append_text("; ")),  # Bemerkungen
    (
        "c101q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),  # Überlagerte Nutzungsplaninhalte
    # Chapter 102: Objektdaten
    ("c102q91i1", "parcels.*.parcel-number", Transform.none),  # Parzellennummer
    ("c102q93i1", "parcels.*.parcel-street", Transform.none),  # Strasse/Flurname
    (
        "c102q244i1",
        "proposal-description",
        Transform.append_text("; "),
    ),  # Vorhaben / Veranstaltung
    (
        "c102q22i1",
        "grundnutzung",
        Transform.join_checkbox(GRUNDNUTZUNG_MAP, "; "),
    ),  # Grundnutzungen
    ("c102q92i1", "parcels.*.building-law-number", Transform.none),  # Baurechtsnummer
    (
        "c102q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_checkbox(UEBERLAGERTE_NUTZUNG_MAP, "; "),
    ),  # Überlagerte Nutzungsplaninhalte
]

QUESTION_MAP_BEANSPRUCHUNG_KANTONSGEBIET = [
    ("c102q244i1", "veranstaltung-beschrieb", Transform.none),
    ("c102q247i1", "veranstaltung-andere-beschreibung", Transform.none),
    ("c102q249i1", "beanspruchte-flaeche-m2", Transform.extract_number),
    ("c102q250i1", "veranstaltung-begruendung", Transform.none),
    ("c102q245i1", "date-time-migrated", Transform.none),
    ("c102q246i1", "duration-migrated", Transform.none),
]

QUESTION_MAP_MITBERICHTSVERFAHREN = [
    ("c21q98i1", "beschreibung-zu-mbv", Transform.none),
    ("c21q103i1", "beschreibung-bemerkungen", Transform.none),
]

QUESTION_MAP_OEREB = [
    ("c21q98i1", "bezeichnung", Transform.none),
    ("c21q103i1", "bemerkungen-np", Transform.none),
]

QUESTION_MAP_MELDUNG = [
    ("c21q98i1", "vorhaben-proposal-description", Transform.none),
    ("c21q102i1", "vorhaben-gesamtkosten-chf", Transform.extract_number),
    ("c21q100i1", "bemerkungen-meldung", Transform.join_multiple_values()),
    ("c21q103i1", "bemerkungen-meldung", Transform.join_multiple_values()),
]

QUESTION_MAP_REKLAME_GESUCH = [
    ("c21q98i1", "bemerkungen-reklame", Transform.join_multiple_values()),
    ("c21q103i1", "bemerkungen-reklame", Transform.join_multiple_values()),
    ("c21q100i1", "bemerkungen-reklame", Transform.join_multiple_values()),
]

QUESTION_MAP_SOLAR = [
    ("c21q98i1", "bemerkungen-solaranlage", Transform.join_multiple_values()),
    ("c21q103i1", "bemerkungen-solaranlage", Transform.join_multiple_values()),
    ("c21q100i1", "bemerkungen-solaranlage", Transform.join_multiple_values()),
]

IGNORE_QUESTIONS = {
    # temporarily ignoring for future analysis
    #
    # Chapter 1: baugesuch / personendaten / gesuchsteller
    "c1q70i1",  # 2 ProjektverfasserIn
    "c1q81i1",  # 3 GrundeigentümerIn
    # Chapter 2: Generell
    "c2q3i1",  # Es werden keine physischen Unterlagen zugestellt
    "c2q251i1",  # Prüfungshinweise Gemeindebaubehörde
    "c2q260i1",  # Gesuch nachträglich eingereicht
    "c2q6i1",  # Dossiernummer
    "c2q272i1",  # Alte Dossier NR
    "c1q41i1",  # 1 Gesuchsteller
    # Chapter 3: Erstellung
    "c3q271i1",  # Dossier Erfassungsjahr
    # Chapter 21: Objektdaten
    "c21q90i1",  # 4 Bauplatz
    "c21q96i1",  # 5 Vorhaben
    "c21q253i1",  # Detailangaben zum Nutzungsplan
    "c21q254i1",  # Detailangaben zur Nutzung
    "c21q270i1",  # Parzellenstandort (Gemeinde)
    # Chapter 101: Objektdaten
    # Chapter 102: Objektdaten (veranstaltung?)
    "c102q255i1",  # Detailangaben zum Nutzungsplan
    "c102q245i1",  # Datum / Zeit
    "c102q246i1",  # Dauer (von - bis)
    "c102q270i1",  # Parzellenstandort (Gemeinde)
    # Chapter 103: Meta
    "c103q257i1",  # Dossier eingereicht von
    # Chapter 104: BaB Daten
    "c104q261i1",  # Art der Massnahme
    "c104q262i1",  # Objektart
    "c104q263i1",  # Nutzung nach RPG
    "c104q264i1",  # Bewilligungsgrund - Rechtliche Grundlage
    "c104q265i1",  # Entscheid
    "c104q267i1",  # Typ der Auftraggeber  - Gesuchsteller
    "c104q268i1",  # Flächenbedarf Fruchtfolgeflächen (m²)
    "c104q269i1",  # Kompensation Fruchtfolgeflächen (m²)
}

slugs_to_ignore = [
    "remarks",
    "proposal-description",
    "construction-cost",
    "proposal",
    "category",
    "gebaeude.*.art-der-hochbaute",
    "purpose",
    "purpose-description",
    "umbauter-raum",
    "status-bauprojekt",
    "stand-der-realisierung",
]


def create_question_map(slugs):
    return list(filter(lambda mapping: mapping[1] not in slugs, QUESTION_MAP_BAUGESUCH))


QUESTION_MAP_REKLAME = (
    create_question_map(slugs_to_ignore) + QUESTION_MAP_REKLAME_GESUCH
)

QUESTION_MAP_MELDUNG_SOLARANLAGE = (
    create_question_map(slugs_to_ignore) + QUESTION_MAP_SOLAR
)

QUESTION_MAP_MELDUNG_VORHABEN = (
    create_question_map(slugs_to_ignore) + QUESTION_MAP_MELDUNG
)

QUESTION_MAP_MITBERICHT_KANTON = (
    create_question_map(slugs_to_ignore + ["leitbehoerde"])
    + QUESTION_MAP_MITBERICHTSVERFAHREN
)

QUESTION_MAP_MITBERICHT_BUND = (
    create_question_map(slugs_to_ignore + ["leitbehoerde"])
    + QUESTION_MAP_MITBERICHTSVERFAHREN
)

QUESTION_MAP_OEREB_VERFAHREN = create_question_map(slugs_to_ignore) + QUESTION_MAP_OEREB

QUESTION_MAP_BENUETZUNG_KANTONSGEBIET = (
    create_question_map(slugs_to_ignore) + QUESTION_MAP_BEANSPRUCHUNG_KANTONSGEBIET
)

IGNORE_CHAPTERS = {
    "c00000000000000",
}
