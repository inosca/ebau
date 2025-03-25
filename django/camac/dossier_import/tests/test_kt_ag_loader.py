from camac.dossier_import.config.kt_ag.dossier_loader import KtAargauDossierLoader
from camac.dossier_import.dossier_classes import Dossier


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
            "STANDORTE": [
                {
                    "STRASSE": "Musterstrasse",
                    "STRASNR": "1",
                    "KOORDB": "1300000",
                    "KOORDL": "2480000",
                    "POSTAL_CODE": "4663",
                    "CITY": "Möhlin",
                }
            ],
        }
    )

    snapshot.assert_match(result)


def test_missing_fields():
    result: Dossier = KtAargauDossierLoader.map_data({})
    assert result
    assert result.id is None
    assert result._meta.target_state is None
    assert len(result.applicant) == 0
    assert len(result.landowner) == 0
    assert len(result.project_author) == 0


def test_mapping_for_multiple_locations(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "CITY": "Möhlin",
            "STANDORTE": [
                {
                    "STRASSE": "Andere Strasse",
                    "STRASNR": "5",
                    "CITY": "Aarburg",
                },
                {
                    "STRASSE": "Musterstrasse",
                    "STRASNR": "1",
                    "CITY": "Möhlin",
                },
                {
                    "STRASSE": "Nicht gematchte Strasse",
                    "STRASNR": "11",
                    "CITY": "Möhlin",
                },
            ],
        }
    )

    snapshot.assert_match(result)


def test_mapping_of_nested_lists(snapshot):
    result: Dossier = KtAargauDossierLoader.map_data(
        {
            "GESUCH_ID": "EBPA-0001-6924",
            "TXT30": "Verfügung erstellt",
            "BTITEL": "EFH Muster",
            "GEMEINDE_BG": "2021-344",
            "BVUAFBNR": "BVUAFB.21.104",
            "EINDAT": "20210629",
            "CITY": "Aarau",
            "STANDORTE": [
                {
                    "STRASSE": "Aarburg-Mapping-Str. 5",
                    "STRASNR": "",
                    "EGID": "",
                    "KOORDB": "1111",
                    "KOORDL": "1111",
                    "CITY": "Aarburg",
                },
                {
                    "STRASSE": "Aarau-Mapping-Str. 1",
                    "STRASNR": "",
                    "EGID": "",
                    "KOORDB": "2635136",
                    "KOORDL": "1240872",
                    "CITY": "Aarau",
                },
            ],
            "PARZELLEN": [
                {
                    "SGUID": "e1a5f3d1-7126-4a7d-b355-b3ac8ad9",
                    "PGUID": "f32b7723-87ed-4010-8c2a-38ad3e09",
                    "PARZNR": "123123",
                    "PARZM2": "",
                    "CITY": "Aarburg",
                },
                {
                    "SGUID": "3ed4fbbd-e6a5-4daf-a5dc-177fc47e",
                    "PGUID": "6e0dbfb8-62f0-4f86-a597-d9e0edc5",
                    "PARZNR": "234234",
                    "PARZM2": "",
                    "CITY": "Aarau",
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
            ],
        }
    )

    snapshot.assert_match(result)
