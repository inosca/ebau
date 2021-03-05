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

QUESTION_MAP_BAUGESUCH = [
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
    # Chapter 2: Generell
    ("c21q91i1", "parzellen-oder-baurechtsnummer", Transform.none),
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
    ("c21q91i1", "parcels.*.parcel-number", Transform.none),
    ("c21q93i1", "parcels.*.parcel-street", Transform.none),
    ("c21q98i1", "proposal-description", Transform.append_text("; ")),
    ("c21q102i1", "construction-cost", Transform.extract_number),
    ("c21q22i1", "grundnutzung", Transform.join_multi_values_grundnutzung("; ")),
    # (
    #     # Vorhaben -> Vorhaben
    #     "c21q97i1",
    #     "proposal-description",
    #     # TODO should be prepended - how to do priorities?
    #     Transform.append_text("; "),
    # ),
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
    (
        "c21q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_multi_values_ueberlagerte_nutzung("; "),
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
        Transform.join_multi_values_orientierende_nutzung("; "),
    ),
    (
        # Orientierende Nutzungsplaninhalt
        "c101q95i1",
        "ueberlagerte-nutzungen",
        Transform.join_multi_values_orientierende_nutzung("; "),
    ),
    (
        # Orientierende Nutzungsplaninhalt
        "c102q95i1",
        "ueberlagerte-nutzungen",
        Transform.join_multi_values_orientierende_nutzung("; "),
    ),
    # Chapter 22: Objektdaten
    (
        "c22q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_multi_values_ueberlagerte_nutzung("; "),
    ),  # Überlagerte Nutzungsplaninhalte
    # Chapter 101: Objektdaten
    (
        "c101q22i1",
        "grundnutzung",
        Transform.join_multi_values_grundnutzung("; "),
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
        Transform.join_multi_values_ueberlagerte_nutzung("; "),
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
        Transform.join_multi_values_grundnutzung("; "),
    ),  # Grundnutzungen
    ("c102q92i1", "parcels.*.building-law-number", Transform.none),  # Baurechtsnummer
    (
        "c102q94i1",
        "ueberlagerte-nutzungen",
        Transform.join_multi_values_ueberlagerte_nutzung("; "),
    ),  # Überlagerte Nutzungsplaninhalte
]

IGNORE_QUESTIONS = {
    # temporarily ignoring for future analysis
    #
    # Chapter 1: baugesuch / personendaten / gesuchsteller
    "c1q68i1",  # Rechnungsadresse identisch GesuchstellerIn: TODO: if set, copy primary data to invoice data
    "c1q79i1",  # ProjektverfasserIn identisch GesuchstellerIn: TODO: if set, copy primary data to requestor data
    "c1q80i1",  # GrundeigentümerIn identisch GesuchstellerIn: TODO: if set, copy primary data to landowner data
    "c1q69i1",  # Rechnungsadresse - TODO no matching field?
    "c1q70i1",  # 2 ProjektverfasserIn
    "c1q81i1",  # 3 GrundeigentümerIn
    # Chapter 2: Generell
    "c2q3i1",  # Es werden keine physischen Unterlagen zugestellt
    "c2q251i1",  # Prüfungshinweise Gemeindebaubehörde
    "c2q260i1",  # Gesuch nachträglich eingereicht
    "c2q1i1",  # Mitteilungen der Gemeinde
    "c2q181i1",  # Mitteilungen der zuständigen Koordinationsstelle
    "c2q4i1",  # Die Gemeindebaubehörde wünscht, dass das vorliegende Gesuch hinsichtlich folgender Fachbereiche durch die zuständigen kantonalen Fachstellen geprüft wird
    "c2q256i1",  # Mitteilung an Bürger
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
    "c21q101i1",  # Umbauter Raum nach SIA 416 - TODO: in versteckte frage migrieren
    "c21q100i1",  # Andere Nutzung
    "c21q270i1",  # Parzellenstandort (Gemeinde)
    # Chapter 101: Objektdaten
    # Chapter 102: Objektdaten (veranstaltung?)
    "c102q255i1",  # Detailangaben zum Nutzungsplan
    "c102q247i1",  # Art der Nutzung
    "c102q250i1",  # Bemerkungen
    "c102q245i1",  # Datum / Zeit
    "c102q246i1",  # Dauer (von - bis)
    "c102q249i1",  # Beanspruchte Fläche in m2
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
]


def create_question_map(slugs):
    return filter(lambda mapping: mapping[1] not in slugs, QUESTION_MAP_BAUGESUCH)


QUESTION_MAP_VORABKLAERUNG = QUESTION_MAP_BAUGESUCH

QUESTION_MAP_REKLAME = create_question_map(slugs_to_ignore)

QUESTION_MAP_MELDUNG_VORHABEN = create_question_map(slugs_to_ignore)

QUESTION_MAP_MELDUNG_SOLARANLAGE = create_question_map(slugs_to_ignore)

QUESTION_MAP_MITBERICHT_KANTON = create_question_map(slugs_to_ignore + ["leitbehoerde"])

QUESTION_MAP_MITBERICHT_BUND = create_question_map(slugs_to_ignore + ["leitbehoerde"])

QUESTION_MAP_OEREB_VERFAHREN = create_question_map(slugs_to_ignore)

QUESTION_MAP_BENUETZUNG_KANTONSGEBIET = create_question_map(slugs_to_ignore)

QUESTION_MAP_BUNDESVERFAHREN = QUESTION_MAP_BAUGESUCH

IGNORE_CHAPTERS = {
    "c00000000000000",
}
