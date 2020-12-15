from dataclasses import dataclass, field
from datetime import datetime
from functools import partial, reduce
from typing import List

from dataclasses_json import config, dataclass_json
from marshmallow import fields

# NOTE: no map for gebaudeeigentumerin, sb, weitere-personen
BETEILIGTER_TYPE_MAP = {
    "Gesuchsteller": {
        "tablequestion": "personalien-gesuchstellerin",
        "suffix": "gesuchstellerin",
    },
    "Projektverfasser": {
        "tablequestion": "personalien-projektverfasserin",
        "suffix": "projektverfasserin",
        "weitere-personen": "weitere-personen-projektverfasserin",
    },
    "Grundeigentümer": {
        "tablequestion": "personalien-grundeigentumerin",
        "suffix": "grundeigentuemerin",
        "weitere-personen": "weitere-personen-grundeigentumerin",
    },
    "Vertreter": {
        "tablequestion": "personalien-vertreterin-mit-vollmacht",
        "suffix": "vertreterin",
        "weitere-personen": "weitere-personen-vertreterin-mit-vollmacht",
    },
}

BETEILIGTER_QUESTION_MAP = {
    "aName": {"slug": "name", "len": 30},
    "aVorname": {"slug": "vorname", "len": 30},
    "aStrasse": {"slug": "strasse", "len": 60},
    "_aPlz": {"slug": "plz"},
    "aOrt": {"slug": "ort", "len": 40},
    "aMail": {"slug": "e-mail"},
    "phone": {"slug": "telefon-oder-mobile"},
    "aFirma": {"slug": "name-juristische-person"},
}

MANDANT_MAP = {
    300: 20021,  # Bern-Mittelland
    400: 20023,  # Emmental
    410: 20027,  # Oberaargau
    500: 20024,  # Frutigen-Niedersimmental
    510: 20025,  # Interlaken-Oberhasli
    520: 20028,  # Obersimmental-Saanen
    530: 20030,  # Thun
    600: 20022,  # Biel-Bienne
    610: 20029,  # Seeland
    620: 20026,  # Berner-Jura
}

GEMEINDE_MAP = {
    # 300 Bern-Mittelland
    "Arni (BE)": "Arni BE",
    "Deisswil": "Stettlen",
    "Kirchdorf": "Kirchdorf (BE)",
    "Schulgemeinde Mühlethurnen-Lohnstorf": "Thurnen",
    "Verwaltungskreis Bern-Mittelland": "Bern",
    "Wald (Zimmerwald)": "Wald BE",
    "(inaktiv) Aeschlen": "Oberdiessbach",
    "(Inaktiv) Albligen": "Schwarzenburg",
    "(Inaktiv) Amtsbezirk Bern": "Bern",
    "(Inaktiv) Amtsbezirk Konolfingen": "Konolfingen",
    "(Inaktiv) Amtsbezirk Laupen": "Laupen",
    "(Inaktiv) Englisberg": "Wald BE",
    "(Inaktiv) Kirchenthurnen": "Kirchenthurnen",
    "(Inaktiv) Lohnstorf": "Lohnstorf",
    "(Inaktiv) Mühlethurnen": "Thurnen",
    "(Inaktiv) Niederwichtrach": "Wichtrach",
    "(Inaktiv) Oberwichtrach": "Wichtrach",
    "(Inaktiv) Rüti bei Riggisberg": "Riggisberg",
    "(Inaktiv) Schönbühl-Urtenen": "Urtenen-Schönbühl",
    "(Inaktiv) Wahlern": "Schwarzenburg",
    "(inaktiv) Belpberg": "Belp",
    "(inaktiv) Bleiken bei Oberdiessbach": "Oberdiessbach",
    "(inaktiv) Büren zum Hof": "Fraubrunnen",
    "(inaktiv) Etzelkofen": "Fraubrunnen",
    "(inaktiv) Gelterfingen": "Kirchdorf (BE)",
    "(inaktiv) Golaten": "Kallnach",
    "(inaktiv) Grafenried": "Fraubrunnen",
    "(inaktiv) Limpach": "Fraubrunnen",
    "(inaktiv) Mühledorf (BE)": "Kirchdorf (BE)",
    "(inaktiv) Mülchi": "Fraubrunnen",
    "(inaktiv) Münchringen": "Jegenstorf",
    "(inaktiv) Noflen": "Kirchdorf (BE)",
    "(inaktiv) Schalunen": "Fraubrunnen",
    "(inaktiv) Scheunen": "Jegenstorf",
    "(inaktiv) Schlosswil": "Grosshöchstetten",
    "(inaktiv) Trimstein": "Münsingen",
    "(inaktiv) Tägertschi": "Münsingen",
    "(inaktiv) Zauggenried": "Fraubrunnen",
    # 400 Emmental
    "Kirchberg": "Kirchberg (BE)",
    "Röthenbach i. E.": "Röthenbach im Emmental",
    "Verwaltungskreis Emmental": "Langnau im Emmental",
    "(Inaktiv) Amtsbezirk Signau": "Signau",
    "(Inaktiv) Amtsbezirk Trachselwald": "Trachselwald",
    "(inaktiv) Niederösch": "Ersigen",
    "(inaktiv) Oberösch": "Ersigen",
    # 410 Oberaargau
    "Roggwil": "Roggwil (BE)",
    "Verwaltungskreis Oberaargau": "Wangen an der Aare",
    "Walterswil": "Walterswil (BE)",
    "(Inaktiv) Gutenburg": "Madiswil",
    "(Inaktiv) Wolfisberg": "Wolfisberg",
    "(inaktiv) Bollodingen": "Bettenhausen",
    "(inaktiv) Hermiswil": "Seeberg",
    "(inaktiv) Kleindietwil": "Madiswil",
    "(inaktiv) Leimiswil": "Madiswil",
    "(inaktiv) Oberönz": "Herzogenbuchsee",
    "(inaktiv) Röthenbach bei Herzogenbuchsee": "Heimenhausen",
    "(inaktiv) Untersteckholz": "Langenthal",
    "(inaktiv) Wanzwil": "Heimenhausen",
    # 500 Frutigen-Niedersimmental
    "Aeschi": "Aeschi bei Spiez",
    "Erlenbach": "Erlenbach im Simmental",
    "Oberwil i.S.": "Oberwil im Simmental",
    "Reichenbach": "Reichenbach im Kandertal",
    "Verwaltungskreis Frutigen-Niedersimmental": "Frutigen",
    # 510 Interlaken
    "Brienz (BE)": "Brienz",
    "Niederried bei Interlaken": "Niederried b. Interlaken",
    "Verwaltungskreis Interlaken-Oberhasli": "Interlaken",
    "(inaktiv) Gadmen": "Innertkirchen",
    # 520 Obersimmental-Saanen
    "Gsteig": "Gsteig b. Gstaad",
    "St Stephan": "St. Stephan",
    "(Inaktiv) Amtsbezirk Obersimmental": "Saanen",
    # 530 Thun
    "(Inaktiv) Amtsbezirk Thun": "Thun",
    "(Inaktiv) Forst": "Forst-Längenbühl",
    "(Inaktiv) Längenbühl": "Forst-Längenbühl",
    "(inaktiv) Höfen": "Stocken-Höfen",
    "(inaktiv) Kienersrüti": "Uttigen",
    "(inaktiv) Niederstocken": "Stocken-Höfen",
    "(inaktiv) Oberstocken": "Stocken-Höfen",
    "(inaktiv) Schwendibach": "Steffisburg",
    "Oberhofen": "Oberhofen am Thunersee",
    "Teuffenthal": "Teuffenthal (BE)",
    "Verwaltungskreis Thun": "Thun",
    # 600 Biel-Bienne
    "(Inaktiv) Nidau Amtsbezirk": "Nidau",
    "(Inaktiv) Twann": "Twann-Tüscherz",
    "(Inaktiv) Tüscherz-Alfermée": "Twann-Tüscherz",
    "Gemeindeverwaltung Evilard-Leubringen": "Leubringen Evilard",
    "Stadtverwaltung Biel-Bienne": "Biel / Bienne",
    "Verwaltungskreis Biel-Bienne": "Biel / Bienne",
    # 610 Seeland
    "(inaktiv) Bangerten": "Rapperswil (BE)",
    "(inaktiv) Busswil bei Büren": "Lyss",
    "(inaktiv) Niederried": "Kallnach",
    "(inaktiv) Ruppoldsried": "Rapperswil (BE)",
    "Bargen": "Bargen (BE)",
    "Rapperswil": "Rapperswil (BE)",
    "Seedorf": "Seedorf (BE)",
    "Studen": "Studen (BE)",
    "Verwaltungskreis Seeland": "Aarberg",
    # 620 Berner-Jura
    "(inactif) Bévilard": "Valbirse",
    "(inactif) Châtelat": "Petit-Val",
    "(inactif) Diesse": "Plateau de Diesse",
    "(inactif) District de La Neuveville": "La Neuveville",
    "(inactif) La Heutte": "Péry-La Heutte",
    "(inactif) Lamboing": "Plateau de Diesse",
    "(inactif) Malleray": "Valbirse",
    "(inactif) Monible": "Petit-Val",
    "(inactif) Plagne": "Sauge",
    "(inactif) Pontenet": "Valbirse",
    "(inactif) Prêles": "Plateau de Diesse",
    "(inactif) Péry": "Péry-La Heutte",
    "(inactif) Sornetan": "Petit-Val",
    "(inactif) Souboz": "Petit-Val",
    "(inactif) Vauffelin": "Sauge",
    "Commune de Saules": "Saules (BE)",
    "Elay": "Elay Seehof",
    "La Scheulte": "La Scheulte Schelten",
    "Péry - La Heutte": "Péry-La Heutte",
    "Renan": "Renan (BE)",
    "Romont": "Romont (BE)",
}


def iso_decoder(*args, **kwargs):
    try:
        return datetime.fromisoformat(*args, **kwargs)
    except ValueError:
        return None


iso_date_field = partial(
    field,
    default=None,
    metadata=config(
        encoder=datetime.isoformat,
        decoder=iso_decoder,
        mm_field=fields.DateTime(format="iso"),
    ),
)


@dataclass_json
@dataclass(frozen=True)
class Gemeinde:
    gGemeindeNr: int
    gdBez: str
    gdName: str
    gdPlz: str
    gdOrt: str

    @property
    def service_name(self):
        name = GEMEINDE_MAP.get(self.gdBez, self.gdBez)
        return f"Leitbehörde {name}"


@dataclass_json
@dataclass(frozen=True)
class Mandant:
    mNr: int
    mAmtstypD: str
    mAmtstypF: str

    @property
    def service(self):
        return MANDANT_MAP[self.mNr]


@dataclass_json
@dataclass(frozen=True)
class Aktivitaet:
    sText: str
    sCodeS: int
    sCodeSBezD: str
    sCodeSBezF: str
    sDatum1BezD: str
    sDatum1BezF: str
    sDatum2BezD: str
    sDatum2BezF: str
    sDatum3BezD: str
    sDatum3BezF: str
    sText1: str
    sText1BezD: str
    sText1BezF: str
    sText2: str
    sText2BezD: str
    sText2BezF: str
    sZahl1: str
    sZahl1BezD: str
    sZahl1BezF: str
    sCodeS1: str
    sCodeS1BezD: str
    sCodeS1BezF: str
    sCodeS2: str
    sCodeS2BezD: str
    sCodeS2BezF: str
    sCodeS3: str
    sCodeS3BezD: str
    sCodeS3BezF: str
    sDatum1: datetime = iso_date_field()
    sDatum2: datetime = iso_date_field()
    sDatum3: datetime = iso_date_field()
    sMutdat: datetime = iso_date_field()

    @property
    def journal_date(self):
        return self.sDatum1 or self.sDatum2 or self.sMutdat

    @property
    def journal_text(self):
        def field(attr):
            val = getattr(self, attr)
            if val:
                bezD, bezF = [getattr(self, f"{attr}Bez{lang}") for lang in ["D", "F"]]
                return f"\n{bezD} | {bezF}: " + (
                    f"{val:%d.%m.%Y}" if isinstance(val, datetime) else f"{val}"
                )

            return ""

        text = f"{self.sCodeSBezD} | {self.sCodeSBezD}"
        if self.sText:
            text += f"\nText: {self.sText}"

        test = reduce(
            lambda x, y: x + field(y),
            [
                "sDatum1",
                "sDatum2",
                "sText1",
                "sText2",
                "sZahl1",
                "sCodeS1",
                "sCodeS2",
                "sCodeS3",
            ],
            text,
        )

        return test


@dataclass_json
@dataclass(frozen=True)
class Adresse:
    aFirma: str
    aName: str
    aVorname: str
    aStrasse: str
    aPlz: int
    aOrt: str
    aMobile: str
    aTelWork: str
    aTelHome: str
    aMail: str
    aLandCode: str

    @property
    def _aPlz(self):
        try:
            return int(self.aPlz)
        except ValueError:
            # TODO log this
            return 0

    @property
    def phone(self):
        return self.aMobile or self.aTelWork or self.aTelHome or ""

    def __str__(self):
        ret = ""
        if self.aFirma:
            ret += f"\n{self.aFirma}"
        if self.aVorname and self.aName:
            ret += f"\n{self.aVorname} {self.aName}"
        if self.aStrasse:
            ret += f"\n{self.aStrasse}"
        if self.aPlz and self.aOrt:
            ret += f"\n{self.aPlz} {self.aOrt}"
        if self.aLandCode:
            ret += f"\n{self.aLandCode}"
        if self.phone:
            ret += f"\n{self.phone}"
        if self.aMail:
            ret += f"\n{self.aMail}"
        return ret


@dataclass_json
@dataclass(frozen=True)
class Beteiligter:
    bHauptbeteiligteFlag: int
    bVertreterCode: str
    bVertreterBezD: str
    bVertreterBezF: str
    bCodeB: str
    bCodeBBezD: str
    bCodeBBezF: str
    Adresse: Adresse
    bMutdat: datetime = iso_date_field()

    @property
    def type(self):
        return BETEILIGTER_TYPE_MAP.get(self.bCodeBBezD, None)

    @property
    def is_main(self):
        return self.type is not None

    @property
    def tablequestion(self):
        if self.type:
            return self.type["tablequestion"]

    @property
    def suffix(self):
        if self.type:
            return self.type["suffix"]

    @property
    def answer_values(self):
        if self.Adresse.aLandCode != "CH":
            return []

        ans = [
            {
                "question": f"{BETEILIGTER_QUESTION_MAP[field]['slug']}-{self.suffix}",
                "value": getattr(self.Adresse, field),
                "len": BETEILIGTER_QUESTION_MAP[field].get("len", None),
            }
            for field in BETEILIGTER_QUESTION_MAP
            if getattr(self.Adresse, field)
        ]

        q = f"juristische-person-{self.suffix}"
        ans.append(
            {
                "question": q,
                "value": f"{q}-ja" if self.Adresse.aFirma else f"{q}-nein",
                "len": None,
            }
        )

        return ans

    @property
    def weitere_personen_option(self):
        return self.type.get("weitere-personen", None)

    @property
    def journal_text(self):
        return (
            f"{self.bCodeBBezD} | {self.bCodeBBezF}\n"
            f"{self.bVertreterBezD} | {self.bVertreterBezF}"
            f"{self.Adresse}"
        )


@dataclass_json
@dataclass(frozen=True)
class Detail:
    dNr: int
    dCodeD: str
    dCodeDBezD: str
    dCodeDBezF: str
    dCodeD1: str
    dCodeD1BezD: str
    dCodeD1BezF: str
    dText1: str
    dText1BezD: str
    dText1BezF: str
    dMutdat: datetime = iso_date_field()

    @property
    def is_main(self):
        return self.dCodeD in ["1", "2"]

    @property
    def question_slug(self):
        return {"1": "beschreibung-bauvorhaben", "2": "standort-migriert"}[self.dCodeD]

    @property
    def journal_text(self):
        return f"{self.dCodeDBezD} | {self.dCodeDBezF}\n{self.dText1}"


@dataclass_json
@dataclass(frozen=True)
class Dokument:
    gNr: int
    docSerialNr: int
    docFileType: str
    docFileName: str
    docName: str
    docComment: str
    docCreatedat: datetime = iso_date_field()

    @property
    def file_path(self):
        return f"{self.gNr}/{self.docFileName}"


@dataclass_json
@dataclass(frozen=True)
class Geschaeft:
    gMandant: int
    gNr: int
    gJahr: int
    gNrIntern: int
    gNrExtern: int
    gStatus: int
    gStatusBezD: str
    cgCode: str
    cgCodeD: str
    cgCodeBezD: str
    gZustaendig: str
    gMutuser: str

    Gemeinde: Gemeinde
    Mandant: Mandant
    Aktivitaeten: List[Aktivitaet]
    Beteiligte: List[Beteiligter]
    Details: List[Detail]
    Dokumente: List[Dokument]
    gMutdat: datetime = iso_date_field()

    @property
    def geschaefts_nr(self):
        return f"{self.cgCodeD}-{self.gNrIntern}-{self.gJahr}"

    @property
    def geschaefts_typ(self):
        # TODO missing values:
        # unknown nhsb: 'Ausnahmen von Schutzbeschlüssen'
        # pruefung-bewilligungspflicht -> zusammen mit "anfrage-zustaendigkeit"?
        MAP = {
            "bg": "baubewilligungsverfahren",
            "bgam": "amtsbericht",
            "bgv": "vorabklaerung",
            "bgz": "anfrage-zustaendigkeit",
            "bpv": "baupolizeiliches-verfahren",
            "nhs": "entfernen-von-hecken-und-feldgeholzen",
            "nhsb": "entfernen-von-hecken-und-feldgeholzen",
        }

        return f"geschaeftstyp-{MAP[self.cgCode]}"

    @property
    def submit_date(self):
        eingang = [akt for akt in self.Aktivitaeten if akt.sCodeS == 1]

        # TODO log this
        if not eingang:
            return self.Aktivitaeten[0].sDatum1.date().isoformat()

        eingang = eingang[0]

        if eingang.sDatum1:
            # Datum Eingang
            return eingang.sDatum1.date().isoformat()
        if eingang.sDatum2:
            # Datum Baugesuch
            return eingang.sDatum2.date().isoformat()

        # TODO log this.
        return ""

    @property
    def instance_state_name(self):
        # TODO hängig
        return {
            "eröffnet": "in_progress",
            "abgeschlossen": "finished",
            "hängig": "in_progress",
        }[self.gStatusBezD]
