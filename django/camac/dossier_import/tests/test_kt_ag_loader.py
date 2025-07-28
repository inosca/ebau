from dataclasses import asdict
from datetime import datetime

import pytest
import pytz
from django.utils.timezone import make_aware

from camac.dossier_import.config.kt_ag.dossier_import.dossier_loader import (
    KtAargauDossierLoader,
    datetime_from_float,
)
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.tests.test_utils import to_sorted_json


def test_datetime_from_float():
    assert datetime_from_float(20250415082103.53) == make_aware(
        datetime(2025, 4, 15, 8, 21, 3)
    )
    assert datetime_from_float(20250415082103) == make_aware(
        datetime(2025, 4, 15, 8, 21, 3)
    )
    assert datetime_from_float(0) is None
    assert datetime_from_float(None) is None


def test_simple_mapping(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "GESUCH_ID": "EBPA-0001-6924",
            "TXT30": "Verfügung erstellt",
            "BTITEL": "EFH Muster",
            "GEMEINDE_BG": "2021-344",
            "BVUAFBNR": "BVUAFB.21.104",
            "EINDAT": "20210629",
            "CITY": "Möhlin",
            "CITY_ID": "4254",
            "PROFIL_KTR": "00000000",
            "STANDORTE": [
                {
                    "STRASSE": "Musterstrasse",
                    "STRASNR": "1",
                    "KOORDB": "1300000",
                    "KOORDL": "2480000",
                    "POSTAL_CODE": "4663",
                    "CITY": "Möhlin",
                    "CITY_ID": "4254",
                }
            ],
        }
    )

    snapshot.assert_match(to_sorted_json(asdict(result)))


def test_empty_string(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "ERDSND_KNZ": "",
        }
    )

    snapshot.assert_match(to_sorted_json(asdict(result)))


def test_missing_fields():
    result: Dossier = KtAargauDossierLoader.map_data({})
    assert result
    assert result.id is None
    assert len(result.applicant) == 0
    assert len(result.landowner) == 0
    assert len(result.project_author) == 0


def test_mapping_for_multiple_locations(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "CITY": "Möhlin",
            "CITY_ID": "4254",
            "STANDORTE": [
                {
                    "STRASSE": "Andere Strasse",
                    "STRASNR": "5",
                    "CITY": "Aarburg",
                    "CITY_ID": "4271",
                },
                {
                    "STRASSE": "Musterstrasse",
                    "STRASNR": "1",
                    "CITY": "Möhlin",
                    "CITY_ID": "4254",
                },
                {
                    "STRASSE": "Nicht gematchte Strasse",
                    "STRASNR": "11",
                    "CITY": "Möhlin",
                    "CITY_ID": "4254",
                },
            ],
        }
    )

    snapshot.assert_match(to_sorted_json(asdict(result)))


@pytest.mark.timezone(pytz.FixedOffset(120))
def test_all_mappings(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "GESUCH_ID": "EBPA-0001-6924",
            "BTITEL": "EFH Muster",
            "BSGUID_TXT": "Dies ist eine detaillierte Beschreibung",
            "BVUAFBNR": "BVUAFB.21.104",
            "GEMEINDE_BG": "2021-344",
            "EINDAT": "20210629",
            "CITY": "Aarau",
            "CITY_ID": "4001",
            "ERFGRND": "Nacherfassung",
            "VERFTYP": "Ordentlich",
            "GEMEINDE_STATUS": "Verfügung erstellt",
            "KANTONS_STATUS": "Neues Gesuch",
            "PROFIL_KNZ": "1",
            "PROFIL_DAT": "20240213",
            "PRGUID": "",
            "PROFIL_KTR": "20250501",
            "PROFIL_OK": "",
            "GESART": [
                {
                    "MANDT": "600",
                    "GESUCH_ID": "EBPA-6929-6843",
                    "GESART": "Baugesuch",
                    "FFIRST": "",
                },
                {
                    "MANDT": "600",
                    "GESUCH_ID": "EBPA-6929-6843",
                    "GESART": "Umweltvertr\u00e4glichkeitspr\u00fcfung (UVP)",
                    "FFIRST": "",
                },
            ],
            "PARZELLEN": [
                {
                    "SGUID": "e1a5f3d1-7126-4a7d-b355-b3ac8ad9",
                    "PGUID": "f32b7723-87ed-4010-8c2a-38ad3e09",
                    "PARZNR": "123123",
                    "PARZM2": "",
                    "CITY": "Aarburg",
                    "CITY_ID": "4271",
                },
                {
                    "SGUID": "3ed4fbbd-e6a5-4daf-a5dc-177fc47e",
                    "PGUID": "6e0dbfb8-62f0-4f86-a597-d9e0edc5",
                    "PARZNR": "234234",
                    "PARZM2": "",
                    "CITY": "Aarau",
                    "CITY_ID": "4001",
                },
            ],
            "STANDORTE": [
                {
                    "STRASSE": "Aarburg-Mapping-Str. 5",
                    "STRASNR": "",
                    "ASSEKNR": "1234",
                    "EGID": "2345",
                    "KOORDB": "1111",
                    "KOORDL": "1111",
                    "CITY": "Aarburg",
                    "CITY_ID": "4271",
                },
                {
                    "STRASSE": "Aarau-Mapping-Str. 1",
                    "STRASNR": "",
                    "ASSEKNR": "3456",
                    "EGID": "4567",
                    "KOORDB": "2635136",
                    "KOORDL": "1240872",
                    "CITY": "Aarau",
                    "CITY_ID": "4001",
                },
            ],
            "KONTAKTE": [
                {
                    "PTROL": "BH",
                    "FIRMA": "",
                    "NAME": "Mapper",
                    "VNAM": "Manfred",
                    "STRASSE": "Mappingstr.",
                    "STRASNR": "777",
                    "PLZ": "7777",
                    "ORT": "Mappingen",
                    "TELMOBI": "076 331 9446",
                    "TELFEST": "061 511 3600",
                    "EMAIL": "manfred@mapper.ch",
                },
                {
                    "PTROL": "GE",
                    "FIRMA": "Grundbesitzer AG",
                    "VNAM": "Gero",
                    "NAME": "Grund",
                    "STRASSE": "Gundeldingerstr.",
                    "STRASNR": "1",
                    "PLZ": "4000",
                    "ORT": "Basel",
                    "TELMOBI": "",
                    "TELFEST": "+41 61 228 9400",
                    "EMAIL": "gero.grund@grundbesitz.com",
                },
                {
                    "PTROL": "PV",
                    "FIRMA": "Architekturbüro Bauschön",
                    "NAME": "Schön",
                    "VNAM": "Benno",
                    "STRASSE": "Im schönen Ort",
                    "STRASNR": "3",
                    "PLZ": "1234",
                    "ORT": "Belair",
                    "TELMOBI": "076 123 23456",
                    "TELFEST": "",
                    "EMAIL": "schoen@bauschoen.ar",
                },
                {
                    "PTROL": "BH",
                    "FIRMA": "",
                    "NAME": "Mapper",
                    "VNAM": "Manuela",
                    "STRASSE": "Mappingstr.",
                    "STRASNR": "777",
                    "PLZ": "7777",
                    "ORT": "Mappingen",
                    "TELMOBI": "",
                    "TELFEST": "",
                    "EMAIL": "manu@mapper.ch",
                },
                {
                    "PTROL": "GV",
                    "FIRMA": "",
                    "NAME": "Vertreter",
                    "VNAM": "Gesetzlicher",
                    "STRASSE": "Mappingstr.",
                    "STRASNR": "777",
                    "PLZ": "7777",
                    "ORT": "Mappingen",
                    "TELMOBI": "",
                    "TELFEST": "",
                    "EMAIL": "legal@repr.ch",
                },
                {
                    "PTROL": "RE",
                    "FIRMA": "",
                    "NAME": "Recipient",
                    "VNAM": "Invoice",
                    "STRASSE": "Mappingstr.",
                    "STRASNR": "777",
                    "PLZ": "7777",
                    "ORT": "Mappingen",
                    "TELMOBI": "",
                    "TELFEST": "",
                    "EMAIL": "invoices@mapper.ch",
                },
            ],
            "WOHNUTZ": [
                {
                    "ANZ_WHG": "2",
                    "ANZ_ZIM": "2",
                    "ANZ_ZWHG": "1",
                },
                {
                    "ANZ_WHG": "3",
                    "ANZ_ZIM": "3",
                    "ANZ_ZWHG": "1",
                },
                {
                    "ANZ_WHG": "2",
                    "ANZ_ZIM": "",
                    "ANZ_ZWHG": "",
                },
            ],
            # Zweckbestimmung
            "WHNTZ_KNZ": "X",
            "GINTZ_KNZ": "X",
            "GINTZ_ART": "Gewerbe",
            "GIBRANCHE": "Telekommunikation",
            "LWNTZ_KNZ": "X",
            "LWNTZ_EL": "10000",
            "LWNTZ_PL": "20000",
            "LWNTZ_TBB": "50",
            "LWNTZ_TBN": "75",
            "ABNTZ_KNZ": "X",
            "ABNTZ_BEZ": "Garage",
            "ABNTZ_ART": "Privat",
            # Gebäudehülle
            "AWND_BART": "Schiefer",
            "AWND_COL": "dunkelgrau",
            "DBEL_MAT": "Beton",
            "DBEL_COL": "gr\u00fcn",
            # Parkplätze
            "PARK_KNZ": "X",
            "ANZ_OPARK": "1",
            "ANZ_OPARK_P": "2",
            "ANZ_OPARK_NP": "3",
            "ANZ_NPARK": "4",
            "ANZ_NPARK_P": "5",
            "ANZ_NPARK_NP": "6",
            # Gebäudeheizung und Energie
            "GHNO_KNZ": "X",
            "GHIS_KNZ": "X",
            "GHNW_KNZ": "X",
            "GHNW_KW": "2000",
            "GHES_KNZ": "X",
            "GHES_KW": "1000",
            "GHUK_KNZ": "X",
            "GHGUID_TXT": "Some text here",
            "BA_OEL_KNZ": "X",
            "BA_OEN_KNZ": "1",
            "BA_GAS": "X",
            "BA_HLZ": "X",
            "BA_ELK": "X",
            "BA_FRN": "X",
            "BA_WAP": "X",
            "BA_WAB": "X",
            "BA_LUF": "X",
            "BA_OTH": "X",
            "BA_OTB": "was ganz anderes",
            # Kanalisationsanschluss, Dach- und Sickerwasser
            "KA_LGS_KNZ": "X",
            "KA_LGN_KNZ": "bestehend",
            "KA_BAU_KNZ": "X",
            "KA_BAN_KNZ": "nicht angeschlossen",
            "DS_VSK_KNZ": "X",
            "DS_VSN_KNZ": "0",
            "DS_OGW_KNZ": "X",
            "DS_OGN_KNZ": "0",
            "DS_KNL_KNZ": "X",
            "DS_KNN_KNZ": "0",
            "DS_EIG_KNZ": "X",
            # Bauzonen
            "BAU_ZON": "innerhalb rechtskr\u00e4ftiger Bauzone",
            "NTZ_ZON": "Nuzungszone",
            "UBL_ZON": "\u00dcberlagerte Zone",
            "SND_PLN": "Sondernutzungsplanung",
            # Dichteziffern
            "ASN_ZIF_ZOD": "10.0",
            "ASN_ZIF_BPJ": "9.1",
            "BMS_ZIF_ZOD": "8.2",
            "BMS_ZIF_BPJ": "7.3",
            "GFL_ZIF_ZOD": "4.6",
            "GFL_ZIF_BPJ": "5.5",
            "GSF_ZIF_ZOD": "6.4",
            "GSF_ZIF_BPJ": "3.7",
            "UEB_ZIF_ZOD": "2.8",
            "UEB_ZIF_BPJ": "1.9",
            # Bauzonen - weitere Angaben
            "GWS_AU_KNZ": "X",
            "GWS_UB_KNZ": "X",
            "GWS_QB_KNZ": "X",
            "HWG_KNZ": "1",
            "EKE_ERF": "nicht erforderlich",
            "EMP_STF": "4",
            # Umweltrechtliche Angaben
            "ERDSND_KNZ": "X",
            "SDBOHR_KNZ": "X",
            "SOLAR_KNZ": "X",
            "ALTLAST_KNZ": "X",
            "GWABSNK_KNZ": "X",
            "BODEIN_KNZ": "X",
            "LSMERF_KNZ": "X",
            "MATABB_KNZ": "X",
            "KANAL_KNZ": "X",
            "ENERGIE_KNZ": "X",
            # Angaben zur Sicherheit
            "BS_KANT_KNZ": "X",
            "BSFKANT_KNZ": "X",
            "BS_KOMM_KNZ": "X",
            "BETRIEB_KNZ": "X",
            "STOER_KNZ": "X",
            "HWGEFHR_KNZ": "X",
            "SRBAUPF_KNZ": "X",
            # Kantonsstrasse, Wald
            "KANTSTR_KNZ": "X",
            "BAULINE_KNZ": "X",
            "ERSCHLS_KNZ": "X",
            "REKLAME_KNZ": "X",
            "BLGUID_TXT": "Grund der Unterschreitung",
            "MAWALD_KNZ": "X",
            "BVWALD_KNZ": "X",
            "MAGUID_TXT": "Grund der Unterschreitung",
            # Bauen ausserhalb der Bauzone
            "LWBETR_KNZ": "X",
            "BSTAND_KNZ": "X",
            "BVBZON_KNZ": "X",
            "TVBZON_KNZ": "X",
            # Weitere Angaben, Gewässer, ...
            "OEFFGW_KNZ": "X",
            "OEFFGW_NAM": "Bodensee",
            "OEFFGW_ABS": "X",
            "GWGUID_TXT": "Ich habe nah am Wasser gebaut",
            "OEFFGW_EIN": "X",
            "DENKMAL_KNZ": "X",
            "LFHIND_KNZ": "X",
            # Baukosten
            "BKOLND": 1700000,
            "BKUMGB": 40000,
            "BKTOTAL": 1740000,
            # Weitere Angaben - Bemerkungen
            "BKGUID_TXT": "Famous last words",
            "VERFSTAND": [
                {
                    "MANDT": "600",
                    "PROCESS_ID": "ZEBP",
                    "EXTERN_ID": "EBPA-0219-7779",
                    "VGUID": "005056ABB4351EDD92DB92C8A93BF8A2",
                    "VORIGIN": "S",
                    "ACTION": "Gesuch an Kanton senden",
                    "STEP": "Gesuch an Kanton gesendet",
                    "TSTAMPL": 20221013095122.074,
                    "WHOTXT": "Testautomatisierung EBP",
                    "KOMMENTAR": "Gesuch EBPA-0219-7779 wurde an den Kanton gesendet.",
                    "VFSTD_ID": "1500",
                    "DOC_ID": "0000000000000000000000000",
                },
                {
                    "MANDT": "600",
                    "PROCESS_ID": "ZEBP",
                    "EXTERN_ID": "EBPA-0219-7779",
                    "VGUID": "005056ABB4351EDD949070992C1CD8A2",
                    "VORIGIN": "S",
                    "ACTION": "Dokumente an Kanton senden",
                    "STEP": "Dokumente an Kanton gesendet",
                    "TSTAMPL": 20221020142900.65,
                    "WHOTXT": "EB2_AFB_02",
                    "KOMMENTAR": "Dokumente vom Gesuch EBPA-0219-7779 wurden an den Kanton gesendet.",
                    "VFSTD_ID": "1510",
                    "DOC_ID": "0000000000000000000000000",
                },
            ],
            "KOMMENTARE": [
                {
                    "MANDT": "600",
                    "GESUCH_ID": "EBPA-4406-5058",
                    "GUID": "005056ABB4351FD092F1938B54F778C1",
                    "SACHB": "EB2_AFB_01",
                    "KOMMENTAR": "Kommentar aus eBau AG",
                    "CREATED_AT": 20250617150613,
                    "SACHB_FIRSTNAME": "Markus Test",
                    "SACHB_LASTNAME": "Krause Test",
                }
            ],
        }
    )

    snapshot.assert_match(to_sorted_json(asdict(result)))
