import base64
from dataclasses import dataclass, field
from enum import StrEnum

from dataclasses_json import LetterCase, dataclass_json


class RapagStatus(StrEnum):
    """RAPAG status codes and their descriptions."""

    INITIAL = "10"  # Debtor not yet defined
    DEBTOR_DEFINED = "20"  # Debtor defined
    SALES_ORDER_CREATED = "30"  # Sales order created
    INVOICE_CREATED = "40"  # Invoice created (Final status)
    INVOICE_CANCELLED = "50"  # Invoice cancelled
    ERROR = "99"  # Erroneous (Validation failed)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RapagSalesOrderPos:
    auftr_pos: str
    matnr: str
    ktext: str
    menge: float
    meins: str
    preis: float
    waers: str
    ltext: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RapagSalesOrder:
    ext_aufnr: str
    name: str
    vorname: str
    strasse: str
    haus_nr: str
    plz: str
    ort: str
    land: str
    email: str
    email_re_empf: str
    mail_vers: str
    tel_nr: str
    bes_betr: float
    waerk: str
    debitor_nr_import: str
    file_name: str
    bin_data: bytes = field(
        metadata={
            "dataclasses_json": {
                "encoder": lambda x: base64.b64encode(x).decode("utf-8") if x else None
            }
        }
    )
    pos: list[RapagSalesOrderPos] = field(default_factory=list)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RapagSalesOrderResponse:
    state: RapagStatus | str | None = None
    error: str | None = None
    message: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RapagSalesOrderGetItem:
    bus_case: str | None = None
    eing_datum: str | None = None
    auftr_key: str | None = None
    ext_aufnr: str | None = None
    bukrs: str | None = None
    status: RapagStatus | str | None = None
    aedat: str | None = None
    kunnr: str | None = None
    kdaufnr: str | None = None
    faktnr: str | None = None
    sap_faktura_url: str | None = None


class RapagOrderNumberSequence:  # pragma: no cover
    """Sequence for RAPAG auftrKey (6-digit number)."""

    @classmethod
    def get_next(cls) -> str:
        """Atomically get the next 6-digit number, formatted as a string."""
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT nextval('ag_rapag_order_number_seq')")
            row = cursor.fetchone()
            val = row[0]
            # Ensure it's 6 digits and wraps around if it exceeds 999999
            # Postgres sequences can be defined with MAXVALUE 999999 and CYCLE
            return f"{val:06d}"
