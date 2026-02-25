from enum import Enum, StrEnum

from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_classes import (
    KtAargauDossier,
)

MUNICIPALITY_ID_AFB = "0001"

PERSON_VALUE_MAPPING = {
    "is_juristic_person": {
        True: "juristische-person-gesuchstellerin-ja",
        False: "juristische-person-gesuchstellerin-nein",
    }
}

PERSON_MAPPING = {
    "is_juristic_person": "juristische-person-gesuchstellerin",
    "company": "name-juristische-person-gesuchstellerin",
    "last_name": "name-gesuchstellerin",
    "first_name": "vorname-gesuchstellerin",
    "street": "strasse-gesuchstellerin",
    "street_number": "nummer-gesuchstellerin",
    "zip": "plz-gesuchstellerin",
    "town": "ort-gesuchstellerin",
    "phone": "telefon-oder-mobile-gesuchstellerin",
    "email": "e-mail-gesuchstellerin",
}

PLOT_DATA_MAPPING = {
    "number": "parzellennummer",
    "egrid": "e-grid-nr",
    "municipality": "gemeinde",
}

BUILDING_MAPPING = {
    "egid": "egid-nr",
    "insurance_number": "amtliche-gebaeudenummer",
}

SUBMISSION_REASON_MAP = {
    "Gesuch in Papierform": "erfassungsgrund-gesuch-in-papierform",
    "Bauen ohne Baubewilligung": "erfassungsgrund-bauen-ohne-baubewilligung",
    "Nacherfassung": "erfassungsgrund-nacherfassung",
    "Online Erfassung": "erfassungsgrund-online-erfassung",
}

APPLICATION_TYPE_MAPPING = {
    "Ordentlich": "verfahrensart-ordentliches-verfahren",
    "Vereinfacht": "verfahrensart-vereinfachtes-verfahren",
    "Direktentscheid": "vorlaeufige-pruefung-verfahrensart-verfahrensart-direktentscheid",
}


# enum values are property names from class DossierTypes
class DossierType(Enum):
    PGV = "pgv"
    UVP = "uvp"
    BAUGESUCH = "baugesuch"
    ANFRAGE = "anfrage"
    REKLAME = "reklamegesuch"
    VORENTSCHEID = "vorentscheid"
    RODUNG = "rodung"
    ABBRUCH = "abbruchgesuch"
    UMNUTZUNG = "umnutzung"


DOSSIER_TYPE_TO_FORM_MAPPING = {  # order is determining first match strategy
    DossierType.PGV.value: "pgv-migration",
    DossierType.UVP.value: "uvp-migration",
    DossierType.BAUGESUCH.value: "baugesuch-migration",
    DossierType.ANFRAGE.value: "anfrage-migration",
    DossierType.REKLAME.value: "reklame-migration",
    DossierType.VORENTSCHEID.value: "vorentscheid-migration",
    DossierType.RODUNG.value: "baugesuch-migration",
    DossierType.ABBRUCH.value: "baugesuch-migration",
    DossierType.UMNUTZUNG.value: "baugesuch-migration",
}

DOSSIER_TYPE_MAPPING = {
    DossierType.PGV.value: "art-des-gesuchs-pgv",
    DossierType.UVP.value: "art-des-gesuchs-umweltvertraeglichkeitspruefung-uvp",
    DossierType.BAUGESUCH.value: "art-des-gesuchs-baugesuch",
    DossierType.ANFRAGE.value: "art-des-gesuchs-anfrage",
    DossierType.REKLAME.value: "art-des-gesuchs-reklame",
    DossierType.VORENTSCHEID.value: "art-des-gesuchs-vorentscheid",
    DossierType.RODUNG.value: "art-des-gesuchs-rodung",
    DossierType.ABBRUCH.value: "art-des-gesuchs-abbruch",
    DossierType.UMNUTZUNG.value: "art-des-gesuchs-umnutzung",
}

OLD_MUNICIPALITIES = {
    "4323": "4324",  # Bad Zurzach -> Zurzach
    "4308": "4324",  # Kaiserstuhl -> Zurzach
    "4317": "4324",  # Rümikon -> Zurzach
    "4133": "4139",  # Burg (AG) -> Menziken
    "4113": "4104",  # Scherz -> Lupfig
    "4042": "4021",  # Turgi -> Baden
    "4179": "4186",  # Ueken -> Herznach-Ueken
    "4167": "4186",  # Herznach -> Herznach-Ueken
    "4321": "4305",  # Unterendingen -> Endingen
    "4094": "4185",  # Bözen -> Böztal
    "4114": "4095",  # Schinznach-Bad -> Brugg
}

EBAU_MUNICIPALITIES = {
    "Aarburg": "4271",
    "Arni": "4061",
    "Aarau": "4001",
    "Biberstein": "4002",
    "Dietwil": "4231",
    "Endingen": "4305",
    "Freienwil": "4028",
    "Fischbach-Göslikon": "4067",
    "Hellikon": "4251",
    "Lengnau": "4312",
    "Meisterschwanden": "4202",
    "Menziken": "4139",
    "Mettauertal": "4184",
    "Möhlin": "4254",
    "Mülligen": "4107",
    "Obermumpf": "4256",
    "Oberwil-Lieli": "4074",
    "Olsberg": "4257",
    "Riniken": "4111",
    "Suhr": "4012",
    "Tägerig": "4077",
    "Tegerfelden": "4320",
    "Wallbach": "4261",
    "Würenlingen": "4047",
    "Zuzgen": "4264",
}


class DossierState(Enum):
    FINISHED = "finished"
    CONSTRUCTION_MONITORING = "construction-monitoring"
    DECISION = "decision"
    CIRCULATION = "circulation"
    FORMAL_EXAM = "subm"


class CantonalState(StrEnum):
    NEW = "Neues Gesuch"
    SPECIALIST_TASK_OPEN = "Fachstelle Aufgabe offen"
    AFB_PROCESSING = "Weiterbearbeitung AfB"
    RELEASE_PROCESS = "Freigabeverfahren"
    SUSPENDED = "Sistiert"
    REJECTED = "Zurückgewiesen"
    PROVISIONAL_COMPLETION = "Vorläufiger Abschluss"
    DEFINITIVE_COMPLETION = "Definitiver Abschluss"


def contains_any(actions, checked_actions):
    return not actions.isdisjoint(checked_actions)


def _map_ebau_state(dossier) -> DossierState:
    actions = set([p.action for p in dossier.procedural_status])
    status = dossier.municipal_status
    canton_status = dossier.cantonal_status

    # 1 - Abgeschlossen
    if status in [
        "Gesuch archiviert",
        "Gesuch zurückgezogen",
        "Gesuch abgeschrieben",
        "Gesuch storniert",
    ]:
        return DossierState.FINISHED

    # 2 - Baubegleitung
    if status == "Verfügung erstellt":
        return DossierState.CONSTRUCTION_MONITORING

    # 3 - Entscheid ausstehend
    # 4 - Entscheid ausstehend
    if contains_any(
        actions, ["Materielle Prüfung gestartet", "Materielle Prüfung abgeschlossen"]
    ):
        return DossierState.DECISION

    # 5 - In Zirkulation
    if status in [
        "Gesuch in Bearbeitung",
        "Anfrage / Stellungnahme offen",
        "In öffentlicher Auflage",
    ] and contains_any(
        actions,
        [
            "Stellungnahmen eingefordert",
            "Stellungnahme akzteptiert",
            "Stellungnahme eingetroffen",
            "Stellungnahme abgelehnt",
            "Ergänzung / Überarbeitung vom Kanton eingefordert",
            "Gesuch an Kanton senden",
        ],
    ):
        return DossierState.CIRCULATION

    # 5a - In Zirkulation
    if contains_any(
        actions,
        [
            "Vorprüfung durchführen",
            "Vorprüfung abgeschlossen (ohne Unterlagenergänzung)",
        ],
    ):
        return DossierState.CIRCULATION

    # 5b - In Zirkulation, independent from further states, if we are here and there is a cantonal involvement
    #                      we are in circulation
    if canton_status:  # pragma: no cover
        return DossierState.CIRCULATION

    # 6 Vorläufige Prüfung
    if status in [
        "Gesuch in Bearbeitung",
        "Anfrage / Stellungnahme offen",
        "In öffentlicher Auflage",
    ] and contains_any(
        actions,
        [
            "Ergänzung / Überarbeitung eingefordert",
            "Ergänzung / Überarbeitung eingereicht",
        ],
    ):
        return DossierState.FORMAL_EXAM

    # 7 Vorläufige Prüfung
    if status == "Gesuch in Bearbeitung" and contains_any(
        actions, ["Eingangsbestätigung versandt"]
    ):
        return DossierState.FORMAL_EXAM

    # 8 Vorläufige Prüfung
    if status == "Gesuch übermittelt":
        return DossierState.FORMAL_EXAM

    # 9 fallback
    return DossierState.CIRCULATION


def _map_non_ebau_state(dossier: KtAargauDossier) -> DossierState:
    if dossier.cantonal_status == "Definitiver Abschluss":
        return DossierState.FINISHED

    return DossierState.CIRCULATION


def map_target_state(dossier: KtAargauDossier):
    if is_ebau_municipality(dossier.responsible_municipality):
        dossier._meta.target_state = _map_ebau_state(dossier).value
    else:
        dossier._meta.target_state = _map_non_ebau_state(dossier).value


def is_ebau_municipality(municipality_bfs):
    return municipality_bfs in EBAU_MUNICIPALITIES.values()


# define task_id's to be skipped to reach instance state
FORMAL_EXAM = ["submit"]
DISTRIBUTION = FORMAL_EXAM + ["formal-exam"]
DECISION = DISTRIBUTION + ["distribution"]
CONSTRUCTION_MONITORING = DECISION + ["decision"]
FINISHED = CONSTRUCTION_MONITORING + [
    "init-construction-monitoring",
    "complete-instance",
]

PATH_TO_STATE = {
    DossierState.FORMAL_EXAM.value: FORMAL_EXAM,
    DossierState.CIRCULATION.value: DISTRIBUTION,
    DossierState.DECISION.value: DECISION,
    DossierState.CONSTRUCTION_MONITORING.value: CONSTRUCTION_MONITORING,
    DossierState.FINISHED.value: FINISHED,
}

CANTON_APPLICATION_CODES = {
    "A01 / Art. 16 Ökologische Massnahmen, Biotope": "kantonale-pruefung-gesuchscodes-a01",
    "A02 / Art. 16a Landw. Wohnbauten, neue freistehende Gebäude": "kantonale-pruefung-gesuchscodes-a02",
    "A03 / Art. 16a Landw. Wohnbauten, An- und Umbauten": "kantonale-pruefung-gesuchscodes-a03",
    "A04 / Art. 16a Aussiedlungen (Kombination mit weiteren Codes)": "kantonale-pruefung-gesuchscodes-a04",
    "A05 / Art. 16a Landw. Remisen": "kantonale-pruefung-gesuchscodes-a05",
    "A06 / Art. 16a Landw. Tierställe": "kantonale-pruefung-gesuchscodes-a06",
    "A07 / Art. 16a Gemüsebau und produzierender Gartenbau": "kantonale-pruefung-gesuchscodes-a07",
    "A08 / Art. 16a Obstanlagen": "kantonale-pruefung-gesuchscodes-a08",
    "A09 / Art. 16a Rebanlagen, Rebhäuschen": "kantonale-pruefung-gesuchscodes-a09",
    "A10 / Art. 16a Übrige Spezialkulturen": "kantonale-pruefung-gesuchscodes-a10",
    "A11 / Art. 16a Terrainveränderungen": "kantonale-pruefung-gesuchscodes-a11",
    "A12 / Art. 16a Landw. Energiegewinnung": "kantonale-pruefung-gesuchscodes-a12",
    "A13 / Art. 16a_bis Landw. Pferdehaltung": "kantonale-pruefung-gesuchscodes-a13",
    "A14 / Art. 16a Abs. 3 Landw. Bauten in landw. Spezialzonen": "kantonale-pruefung-gesuchscodes-a14",
    "A15 / Art. 16a Übrige landw. Bauten": "kantonale-pruefung-gesuchscodes-a15",
    "A16 / Art. 18 Bauten in nichtlandw. Spezialzonen": "kantonale-pruefung-gesuchscodes-a16",
    "A17 / Art. 18a Solaranlagen": "kantonale-pruefung-gesuchscodes-a17",
    "A18 / Art. 24 Bienenhäuser": "kantonale-pruefung-gesuchscodes-a18",
    "A19 / Art. 24 Deponien": "kantonale-pruefung-gesuchscodes-a19",
    "A20 / Art. 24 Materialabbau": "kantonale-pruefung-gesuchscodes-a20",
    "A21 / Art. 24 Schiessanlagen": "kantonale-pruefung-gesuchscodes-a21",
    "A22 / Art. 24 Sendeanlagen": "kantonale-pruefung-gesuchscodes-a22",
    "A23 / Art. 24 Siedlungsentwässerung": "kantonale-pruefung-gesuchscodes-a23",
    "A24 / Art. 24 Erholungsnutzung / Tourismus": "kantonale-pruefung-gesuchscodes-a24",
    "A25 / Art. 24 Wasserversorgung": "kantonale-pruefung-gesuchscodes-a25",
    "A26 / Art. 24 Übrige standortgebundene Bauten": "kantonale-pruefung-gesuchscodes-a26",
    "A27 / Art. 24a Zweckänderung ohne bauliche Massnahmen": "kantonale-pruefung-gesuchscodes-a27",
    "A28 / Art. 24b Nichtlandw. Nebenbetrieb": "kantonale-pruefung-gesuchscodes-a28",
    "A29 / Art. 24c Besitzstandsgeschützte Bauten": "kantonale-pruefung-gesuchscodes-a29",
    "A30 / Art. 24c Besitzstandsgeschützte Bauten, Ersatzbau": "kantonale-pruefung-gesuchscodes-a30",
    "A31 / Art. 24d Neurechtliche Wohnbauten": "kantonale-pruefung-gesuchscodes-a31",
    "A32 / Art. 24d Geschützte Bauten": "kantonale-pruefung-gesuchscodes-a32",
    "A33 / Art. 24e Hobbymässige Tierhaltung": "kantonale-pruefung-gesuchscodes-a33",
    "A34 / Art. 37a Gewerbliche Bauten": "kantonale-pruefung-gesuchscodes-a34",
    "A35 / Strassen, Wege (Art. 16a und 24)": "kantonale-pruefung-gesuchscodes-a35",
    "A36 / Wald, zonenkonforme Bauten und Anlagen": "kantonale-pruefung-gesuchscodes-a36",
    "A37 / Wald, zonenfremde Bauten und Anlagen": "kantonale-pruefung-gesuchscodes-a37",
    "B01 / Landw. Bauten": "kantonale-pruefung-gesuchscodes-b01",
    "B02 / Materialabbau/Deponien": "kantonale-pruefung-gesuchscodes-b02",
    "B03 / Öffentliche Bauten": "kantonale-pruefung-gesuchscodes-b03",
    "B04 / Erschliessungen (Parkplätze)": "kantonale-pruefung-gesuchscodes-b04",
    "B05 / Erschliessungen (neuer Anschluss an Kantonsstrasse)": "kantonale-pruefung-gesuchscodes-b05",
    "B06 / Erschliessungen (Strassen / Wege)": "kantonale-pruefung-gesuchscodes-b06",
    "B07 / Leitungen (Kanalisation / Wasserleitungen / Gasleitungen)": "kantonale-pruefung-gesuchscodes-b07",
    "B08 / Sendeanlagen": "kantonale-pruefung-gesuchscodes-b08",
    "B09 / Weitere Bauten und Anlagen": "kantonale-pruefung-gesuchscodes-b09",
    "B10 / Wohnbauten": "kantonale-pruefung-gesuchscodes-b10",
    "B11 / Klein- und Nebenbauten": "kantonale-pruefung-gesuchscodes-b11",
    "B13 / Gewerbe unter Störfallverordnung (z.B. Chemie)": "kantonale-pruefung-gesuchscodes-b13",
    "B14 / Gewerbe-/Industriebauten (div)": "kantonale-pruefung-gesuchscodes-b14",
    "B15 / Restaurant / Hotel": "kantonale-pruefung-gesuchscodes-b15",
    "B16 / Garagen-/Tankstellen-Gewerbe": "kantonale-pruefung-gesuchscodes-b16",
    "B17 / Verkaufsgewerbe": "kantonale-pruefung-gesuchscodes-b17",
    "B18 / Reklamenanlagen": "kantonale-pruefung-gesuchscodes-b18",
    "B19 / Solaranlage": "kantonale-pruefung-gesuchscodes-b19",
    "C01 / EleG Anhörung PGV Transformatorenstation ordentlich": "kantonale-pruefung-gesuchscodes-c01",
    "C02 / EleG Anhörung PGV Transformatorenstation vereinfacht": "kantonale-pruefung-gesuchscodes-c02",
    "C03 / EleG Anhörung PGV 16kV-Leitung ordentlich": "kantonale-pruefung-gesuchscodes-c03",
    "C04 / EleG Anhörung PGV 16kV-Leitung vereinfacht": "kantonale-pruefung-gesuchscodes-c04",
    "C05 / EleG Anhörung PGV 50/110kV-Leitung ordentlich": "kantonale-pruefung-gesuchscodes-c05",
    "C06 / EleG Anhörung PGV 50/110kV-Leitung vereinfacht": "kantonale-pruefung-gesuchscodes-c06",
    "C07 / EleG Anhörung PGV 220/380kV-Leitung ordentlich": "kantonale-pruefung-gesuchscodes-c07",
    "C08 / EleG Anhörung PGV 220/380kV-Leitung vereinfacht": "kantonale-pruefung-gesuchscodes-c08",
    "C09 / EleG Anhörung PGV Niederspannung (BLN & LKB) ordentlich": "kantonale-pruefung-gesuchscodes-c09",
    "C10 / EleG Anhörung PGV Niederspannung (BLN & LKB) vereinfacht": "kantonale-pruefung-gesuchscodes-c10",
    "C11 / EleG Anhörung PGV weitere Bauten und Anlagen im Energiesektor": "kantonale-pruefung-gesuchscodes-c11",
    "D01 / EBG Anhörung PGV Eisenbahnen ordentlich": "kantonale-pruefung-gesuchscodes-d01",
    "D02 / EBG Anhörung PGV Eisenbahnen vereinfacht": "kantonale-pruefung-gesuchscodes-d02",
    "E01 / MG Anhörung PGV ordentlich": "kantonale-pruefung-gesuchscodes-e01",
    "E02 / MG Anhörung PGV vereinfacht": "kantonale-pruefung-gesuchscodes-e02",
    "F01 / RLG Anhörung PGV > 5bar- Leitung ordentlich": "kantonale-pruefung-gesuchscodes-f01",
    "F02 / RLG Anhörung PGV > 5bar- Leitung vereinfacht": "kantonale-pruefung-gesuchscodes-f02",
    "F03 / RLG Anhörung PGV Druckreduzier- und Messstationen (DRS/DRM)": "kantonale-pruefung-gesuchscodes-f03",
    "G02 / RLG PGV 1- 5bar- Leitung vereinfacht": "kantonale-pruefung-gesuchscodes-g02",
    "G03 / RLG PGV Druckreduzier- und Messstationen (DRS/DRM)": "kantonale-pruefung-gesuchscodes-g03",
    "G04 / RLG PGV weitere Bauten und Anlagen der Gasversorgung": "kantonale-pruefung-gesuchscodes-g04",
    "H02 / LFG Anhörung PGV vereinfacht": "kantonale-pruefung-gesuchscodes-h02",
    "I01 / NSG Anhörung PGV ordentlich": "kantonale-pruefung-gesuchscodes-i01",
    "I02 / NSG Anhörung PGV vereinfacht": "kantonale-pruefung-gesuchscodes-i02",
    "K01 / KEG Anhörung PGV ordentlich": "kantonale-pruefung-gesuchscodes-k01",
    "K02 / KEG Anhörung PGV ordentlich": "kantonale-pruefung-gesuchscodes-k02",
}
