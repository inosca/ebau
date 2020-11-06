from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

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
        "weitere-personen": "weitere-personen-grundeigentumerin"
    },
    "Vertreter": {
        "tablequestion": "personalien-vertreterin-mit-vollmacht",
        "suffix": "vertreterin",
        "weitere-personen": "weitere-personen-vertreterin-mit-vollmacht",
    },
}

BETEILIGTER_QUESTION_MAP = {
    "aName": "name",
    "aVorname": "vorname",
    "aStrasse": "strasse",
    "_aPlz": "plz",
    "aOrt": "ort",
    "aMail": "e-mail",
    "nummer": "nummer",
    "aFirma": "name-juristische-person",
}


@dataclass_json
@dataclass(frozen=True)
class Gemeinde:
    gGemeindeNr: int
    gdBez: str
    gdName: str
    gdPlz: str
    gdOrt: str


@dataclass_json
@dataclass(frozen=True)
class Mandant:
    pass


@dataclass_json
@dataclass(frozen=True)
class Aktivitaet:
    pass


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

    @property
    def _aPlz(self):
        return int(self.aPlz)

    @property
    def nummer(self):
        return self.aMobile or self.aTelWork or self.aTelHome or ""


@dataclass_json
@dataclass(frozen=True)
class Beteiligter:
    bHauptbeteiligteFlag: int
    bVertreterCode: str
    bVertreterBezD: str
    bCodeB: str
    bCodeBBezD: str
    Adresse: Adresse

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
        aFirma: str
        ans = [
            {
                "question": f"{BETEILIGTER_QUESTION_MAP[field]}-{self.suffix}",
                "value": getattr(self.Adresse, field),
            }
            for field in BETEILIGTER_QUESTION_MAP
            if getattr(self.Adresse, field)
        ]

        q = f"juristische-person-{self.suffix}"
        ans.append(
            {"question": q, "value": f"{q}-ja" if self.Adresse.aFirma else f"{q}-nein"}
        )

        return ans

    @property
    def weitere_personen_option(self):
        return self.type.get("weitere-personen", None)



@dataclass_json
@dataclass(frozen=True)
class Detail:
    pass


@dataclass_json
@dataclass(frozen=True)
class Dokument:
    pass


@dataclass_json
@dataclass(frozen=True)
class Geschaeft:
    gMandant: int
    gNr: int
    gJahr: int
    gNrIntern: int
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

    @property
    def geschaefts_nr(self):
        return f"{self.cgCodeD}-{self.gNrIntern}-{self.gJahr}"

    @property
    def geschaefts_typ(self):
        # TODO missing values:
        # entfernen-von-hecken-und-feldgeholzen, pruefung-bewilligungspflicht
        MAP = {
            "bg": "baubewilligungsverfahren",
            "bgam": "amtsbericht",
            "bgv": "vorabklaerung",
            "bgz": "anfrage-zustaendigkeit",
            "bpv": "baupolizeiliches-verfahren",
        }

        return f"geschaeftstyp-{MAP[self.cgCode]}"
