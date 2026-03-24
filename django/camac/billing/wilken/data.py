from datetime import datetime

from camac.billing.models import Invoice, LineItem
from camac.billing.utils import stringify_price


class WilkenRow:
    EEI_KEY1: str  # Schluessel
    EII_OBJ: str = "FBE"  # Objekttyp
    EII_CHAR00: str = "P"  # Konzern
    EII_CHAR01: str = "01"  # Mandant
    EII_CHAR02: str = "N4"  # Werk
    EII_CHAR57: str = "eBau"  # Datenherkunft
    EEI_CHAR20_01: str  # Belegnummer

    def to_row(self) -> tuple[str, ...]:
        return tuple(getattr(self, field, "") for field in self.Meta.HEADERS)

    def __init__(self, now: datetime, row_index: int, invoice_index: int):
        now_str: str = now.strftime("%Y%m%d%H%M%S")
        self.EII_KEY1 = f"EBAU{now_str}{row_index:05}"
        self.EII_CHAR20_01 = f"AUTO{invoice_index:02}"

    class Meta:
        HEADERS: tuple[str, ...] = (
            "EII_KEY1",
            "EII_OBJ",
            "EII_CHAR00",
            "EII_CHAR01",
            "EII_CHAR02",
            "EII_CHAR57",
            "EII_CHAR59",
            "EII_CHAR20_01",
            "EII_CHAR04",
            "EII_CHAR05",
            "EII_CHAR06",
            "EII_CHAR07",
            "EII_CHAR08",
            "EII_CHAR09",
            "EII_CHAR10_01",
            "EII_CHAR10_02",
            "EII_CHAR10_03",
            "EII_CHAR10_04",
            "EII_CHAR10_05",
            "EII_CHAR10_06",
            "EII_CHAR10_07",
            "EII_CHAR10_08",
            "EII_CHAR10_09",
            "EII_CHAR10_10",
            "EII_CHAR10_11",
            "EII_CHAR10_12",
            "EII_CHAR10_13",
            "EII_CHAR10_14",
            "EII_CHAR10_15",
            "EII_CHAR10_16",
            "EII_CHAR10_17",
            "EII_CHAR10_18",
            "EII_CHAR10_19",
            "EII_CHAR10_20",
            "EII_CHAR10_21",
            "EII_CHAR10_22",
            "EII_CHAR10_23",
            "EII_CHAR10_24",
            "EII_CHAR10_25",
            "EII_CHAR10_26",
            "EII_CHAR10_27",
            "EII_CHAR10_28",
            "EII_CHAR10_29",
            "EII_CHAR10_30",
            "EII_CHAR10_31",
            "EII_CHAR10_32",
            "EII_CHAR10_33",
            "EII_CHAR10_34",
            "EII_CHAR10_35",
            "EII_CHAR10_36",
            "EII_CHAR10_37",
            "EII_CHAR10_38",
            "EII_CHAR10_39",
            "EII_CHAR10_40",
            "EII_CHAR100_1",
            "EII_CHAR11",
            "EII_CHAR12",
            "EII_CHAR14",
            "EII_CHAR15",
            "EII_CHAR150",
            "EII_CHAR16",
            "EII_CHAR17",
            "EII_CHAR18",
            "EII_CHAR19",
            "EII_CHAR20",
            "EII_CHAR20_02",
            "EII_CHAR20_03",
            "EII_CHAR20_04",
            "EII_CHAR20_05",
            "EII_CHAR20_06",
            "EII_CHAR20_07",
            "EII_CHAR20_08",
            "EII_CHAR20_09",
            "EII_CHAR20_10",
            "EII_CHAR20_11",
            "EII_CHAR20_12",
            "EII_CHAR20_13",
            "EII_CHAR20_14",
            "EII_CHAR20_17",
            "EII_CHAR20_20",
            "EII_CHAR20_21",
            "EII_CHAR20_22",
            "EII_CHAR20_23",
            "EII_CHAR20_24",
            "EII_CHAR20_25",
            "EII_CHAR20_26",
            "EII_CHAR20_27",
            "EII_CHAR20_29",
            "EII_CHAR20_30",
            "EII_CHAR20_31",
            "EII_CHAR20_32",
            "EII_CHAR20_33",
            "EII_CHAR20_34",
            "EII_CHAR20_35",
            "EII_CHAR20_36",
            "EII_CHAR20_37",
            "EII_CHAR20_38",
            "EII_CHAR20_39",
            "EII_CHAR20_40",
            "EII_CHAR20_41",
            "EII_CHAR20_42",
            "EII_CHAR20_43",
            "EII_CHAR20_44",
            "EII_CHAR20_45",
            "EII_CHAR20_46",
            "EII_CHAR20_47",
            "EII_CHAR20_49",
            "EII_CHAR20_50",
            "EII_CHAR21",
            "EII_CHAR22",
            "EII_CHAR23",
            "EII_CHAR24",
            "EII_CHAR25",
            "EII_CHAR250_1",
            "EII_CHAR26",
            "EII_CHAR27",
            "EII_CHAR28",
            "EII_CHAR29",
            "EII_CHAR34",
            "EII_CHAR35",
            "EII_CHAR36",
            "EII_CHAR37",
            "EII_CHAR38",
            "EII_CHAR39",
            "EII_CHAR40",
            "EII_CHAR40_01",
            "EII_CHAR40_02",
            "EII_CHAR40_03",
            "EII_CHAR40_04",
            "EII_CHAR40_05",
            "EII_CHAR40_06",
            "EII_CHAR40_07",
            "EII_CHAR40_08",
            "EII_CHAR40_09",
            "EII_CHAR40_11",
            "EII_CHAR40_12",
            "EII_CHAR40_13",
            "EII_CHAR40_14",
            "EII_CHAR40_15",
            "EII_CHAR40_16",
            "EII_CHAR40_17",
            "EII_CHAR40_18",
            "EII_CHAR40_19",
            "EII_CHAR40_20",
            "EII_CHAR41",
            "EII_CHAR42",
            "EII_CHAR43",
            "EII_CHAR44",
            "EII_CHAR45",
            "EII_CHAR46",
            "EII_CHAR47",
            "EII_CHAR48",
            "EII_CHAR49",
            "EII_CHAR50",
            "EII_CHAR51",
            "EII_CHAR512",
            "EII_CHAR52",
            "EII_CHAR53",
            "EII_CHAR54",
        )


class InvoiceLine(WilkenRow):
    EII_CHAR59: str = "RECHN"


class HeaderLine(WilkenRow):
    EII_CHAR59: str = "RKOPF"
    EII_CHAR10_03: str = "00000"  # AV30_interneLaufendeNummer
    EII_CHAR10_04: str = "000"  # V30_Sortierung
    EII_CHAR10_05: str  # V30_Erstelldatum Datum YYYYMMDD
    EII_CHAR10_07: str = "NORM"  # V30_Rechnungsart
    EII_CHAR10_09: str = "D"  # V30_ArtDerKundennummerRechnung
    EII_CHAR10_11: str = "0"  # V30_KzAbwAdresseRechnung
    EII_CHAR10_14: str = "0"  # V30_KzAbwAdresseEndempf
    EII_CHAR10_17: str = "0"  # V30_KzAbwAdresseLieferung
    EII_CHAR10_20: str = "0"  # V30_KzAbwAdresseBonusempf
    EII_CHAR10_21: str = "D"  # V30_Sprache
    EII_CHAR10_22: str = "CHF"  # V30_Waehrung
    EII_CHAR10_23: str = "BASIS"  # V30_Preisbasis
    EII_CHAR10_24: str  # V30_Preisstand Datum YYYYMMDD
    EII_CHAR10_25: str = "006"  # V30_Skontolinie Skontolinie (i.d.R. 003 bei bestehenden Rechnungen) Zahlungsfrist
    EII_CHAR10_27: str = "A"  # V30_Rechnungsstatus
    EII_CHAR10_30: str = "0"  # V30_KzBonusJaNein
    EII_CHAR10_31: str = "0"  # V30_KzZuAbschlagJaNein
    EII_CHAR10_32: str = "0"  # V30_KzProvisionJaNein
    EII_CHAR10_35: str = "0"  # V30_DruckenInAbwMandWaehrung
    EII_CHAR10_36: str  # V30_BestelldatumDesKunden Datum YYYYMMDD
    EII_CHAR150: str  # V30_Kurzbezeichnung Rechnungsbezeichnung
    EII_CHAR20_02: str  # V30_UserIdErstellung Wilken User ID des Sachbearbeiters
    EII_CHAR20_04: str  # V30_KundennummerRechnung Kundennummer des Debitoren
    EII_CHAR20_29: str  # V30_Stoppdatum Datum YYYYMMDD
    EII_CHAR20_46: str  # V30_Buchungsdatum YYYYMMDD
    EII_CHAR20_24: str  # V30_SachbearbeiterVTAnmeldung Sachbearbeiter auf der Rechnung
    EII_CHAR20_27: str = "0"  # V30_KzNettokunde
    EII_CHAR48: str = "0"  # V30_KzCSV31SatzDa
    EII_CHAR49: str = "0"  # V30_KzCSV31SatzDa
    EII_CHAR50: str = "0"  # V30_KzCSV32SatzDa
    EII_CHAR51: str = "0"  # V30_KzCSV33SatzDa

    def __init__(
        self, now: datetime, row_index: int, invoice_index: int, invoice: Invoice
    ):
        super().__init__(now=now, row_index=row_index, invoice_index=invoice_index)
        today = now.strftime("%Y%m%d")
        self.EII_CHAR10_05 = today
        self.EII_CHAR10_24 = today
        self.EII_CHAR10_36 = today
        self.EII_CHAR20_29 = today
        self.EII_CHAR20_46 = today
        self.EII_CHAR150 = invoice.payment_purpose
        self.EII_CHAR20_02 = invoice.user_id
        self.EII_CHAR20_04 = invoice.customer_number
        self.EII_CHAR20_24 = invoice.clerk


class PositionLine(WilkenRow):
    EII_KEY1: str  #  Schluessel
    EII_CHAR59: str = "RPOSI"  # Satzkennung
    EII_CHAR20_01: str  #  Belegnummer
    EII_CHAR10_03: str  # V35_Positionsnummer
    EII_CHAR10_04: str = "500"  # V35_Sortierung Fix 500 an jeder Position
    EII_CHAR10_05: str  # V35_Erstelldatum
    EII_CHAR10_06: str  # V35_Aenderungsdatum
    EII_CHAR10_16: str = "0"  # V35_KzCSV36SatzDa
    EII_CHAR10_17: str = "0"  # V35_KennzeichenFrei1
    EII_CHAR10_18: str = "0"  # V35_KennzeichenFrei2
    EII_CHAR10_19: str = "0"  # V35_KennzeichenFrei3
    EII_CHAR10_20: str = "0"  # V35_KennzeichenFrei4
    EII_CHAR10_21: str = "0"  # V35_KennzeichenFrei5
    EII_CHAR10_24: str  # V35_Druckposition
    EII_CHAR10_25: str = "BASIS"  # V35_Preisbasis
    EII_CHAR10_26: str  # V35_Preisstand
    EII_CHAR10_27: str = "001"  # V35_Steuerschluessel
    EII_CHAR20_09: str = "1"  # V35_Auftragsmenge
    EII_CHAR20_17: str  # V35_Nettowarenwert
    EII_CHAR20_20: str = "0"  # V35_Produktgruppe#
    EII_CHAR20_24: str = "ANZ"  # V35_Preismengeneinheit
    EII_CHAR20_26: str = "1"  # TODO: Not in wilken documentation, what is this?
    EII_CHAR20_30: str = "1"  # V35_KzPreiseAenderbar
    EII_CHAR20_31: str = "0"  # V35_KzBezeichnungAenderbar
    EII_CHAR20_32: str = "0"  # V35_KzBonusJaNein
    EII_CHAR20_33: str = "0"  # V35_KzProvisionJaNein
    EII_CHAR20_34: str = "0"  # V35_KzSkontofaehig
    EII_CHAR20_35: str = "0"  # V35_KzZuAbschlagJaNein
    EII_CHAR20_36: str = "0"  # V35_Textkonstante1Texte
    EII_CHAR36: str  # V35_Bruttopreis
    EII_CHAR37: str  # V35_Basispreis
    EII_CHAR39: str  # V35_Nettopreis
    EII_CHAR40_01: str  #  V35_Produktnummer
    EII_CHAR40_03: str  # V35_Startdatum
    EII_CHAR40_05: str  # V35_DatumLetzteFaktura

    def __init__(
        self,
        now: datetime,
        row_index: int,
        invoice_index: int,
        line_item_index: int,
        invoice: Invoice,
        line_item: LineItem,
    ):
        super().__init__(now=now, row_index=row_index, invoice_index=invoice_index)
        today = now.strftime("%Y%m%d")
        self.EII_CHAR10_05 = today
        self.EII_CHAR10_06 = today
        self.EII_CHAR40_03 = today
        self.EII_CHAR40_05 = today
        self.EII_CHAR10_03 = f"{line_item_index:05}"
        self.EII_CHAR10_24 = f"{line_item_index:03}"
        self.EII_CHAR10_26 = today
        self.EII_CHAR20_17 = stringify_price(line_item.amount)
        self.EII_CHAR40_01 = line_item.product_number
        self.EII_CHAR36 = stringify_price(line_item.amount)
        self.EII_CHAR37 = stringify_price(line_item.amount)
        self.EII_CHAR39 = stringify_price(line_item.amount)


class HeaderTexts(WilkenRow):
    EII_KEY1: str  # Schluessel TYP+yyyymmdd+hhmmss+lfdNr.
    EII_CHAR59: str = "RKOPT"  # Satzkennung
    EII_CHAR20_01: str  # Belegnummer wie bei Rechnung
    EII_CHAR10_04: str = "050"  # V30_Sortierung 050 = Rechnungstext Anfang 060 = Rechnungstext Ende 070 = Rechnungskopf Notizen 080 = Rechnungsstornotext 560 = Rechnungspositionstext
    EII_CHAR10_05: str  # V30_Erstelldatum Datum YYYYMMDD
    EII_CHAR10_06: str  # V35_Aenderungsdatum
    EII_CHAR10_07: str = "D"  # R3K_Sprache Sprachkennzeichen  1-stellig
    EII_CHAR250_1: str  # R3K_Text Rechnungstext

    def __init__(
        self, now: datetime, row_index: int, invoice_index: int, invoice: Invoice
    ):
        super().__init__(now=now, row_index=row_index, invoice_index=invoice_index)
        today = now.strftime("%Y%m%d")
        self.EII_CHAR10_05 = today
        self.EII_CHAR10_06 = today
        self.EII_CHAR250_1 = invoice.invoice_text
