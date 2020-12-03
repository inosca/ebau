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
        MAP = {
            "Brienz (BE)": "Brienz",
            "(inaktiv) Gadmen": "Innertkirchen",
            "Niederried bei Interlaken": "Niederried b. Interlaken",
            "Verwaltungskreis Interlaken-Oberhasli": "Interlaken",
        }
        name = MAP.get(self.gdBez, self.gdBez)
        return f"Leitbehörde {name}"


@dataclass_json
@dataclass(frozen=True)
class Mandant:
    mNr: int
    mAmtstypD: str
    mAmtstypF: str

    @property
    def service(self):
        # TODO extend with additional rstas
        # * 20025 = Regierungsstatthalteramt Interlaken-Oberhasli
        MAP = {510: 20025}
        return MAP[self.mNr]


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

        # TODO nummer?
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
        # pruefung-bewilligungspflicht
        MAP = {
            "bg": "baubewilligungsverfahren",
            "bgam": "amtsbericht",
            "bgv": "vorabklaerung",
            "bgz": "anfrage-zustaendigkeit",
            "bpv": "baupolizeiliches-verfahren",
            "nhs": "entfernen-von-hecken-und-feldgeholzen",
            "nhsb": "baubewilligungsverfahren",
        }

        return f"geschaeftstyp-{MAP[self.cgCode]}"

    @property
    def submit_date(self):
        eingang = [akt for akt in self.Aktivitaeten if akt.sCodeS == 1]

        # TODO this is has to be logged
        if not eingang:
            return self.Aktivitaeten[0].sDatum1.date().isoformat()

        eingang = eingang[0]

        if all([eingang.sDatum1, eingang.sDatum2]):
            return sorted([eingang.sDatum1, eingang.sDatum2])[0].date().isoformat()
        elif eingang.sDatum1 is not None:
            return eingang.sDatum1.date().isoformat()
        elif eingang.sDatum2 is not None:
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
