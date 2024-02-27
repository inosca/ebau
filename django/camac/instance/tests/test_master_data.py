from datetime import date

import pytest
from caluma.caluma_form import factories as caluma_form_factories
from caluma.caluma_workflow import (
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.utils.translation import override

from ..master_data import MasterData


def test_master_data_exceptions(
    db,
    instance,
    instance_with_case,
    master_data_settings,
):
    master_data_settings["CONFIG"] = {
        "bar": ("unconfigured", "bar"),
        "baz": ("case_meta", "baz", {"value_parser": "boolean"}),
        "an_instance_property": ("instance_property", "case__form"),
    }
    instance.case = caluma_workflow_factories.CaseFactory(meta={"baz": True})
    instance.save()
    master_data = MasterData(instance.case)

    with pytest.raises(AttributeError) as e:
        assert master_data.foo

    assert (
        str(e.value)
        == "Key 'foo' is not configured in master data config. Available keys are: bar, baz, an_instance_property"
    )

    with pytest.raises(AttributeError) as e:
        assert master_data.bar

    assert (
        str(e.value)
        == "Resolver 'unconfigured' used in key 'bar' is not defined in master data class"
    )

    with pytest.raises(AttributeError) as e:
        assert master_data.baz

    assert str(e.value) == "Parser 'boolean' is not defined in master data class"

    with pytest.raises(AttributeError) as e:
        assert master_data.an_instance_property

    assert (
        str(e.value)
        == "Instance property lookup failed for lookup `case__form` with 'Case' object has no attribute 'form'."
    )


def test_master_data_parsers(
    db,
    application_settings,
    snapshot,
    form_field_factory,
    instance,
    master_data_is_visible_mock,
    master_data_settings,
    utils,
):
    master_data_settings["CONFIG"] = {
        "date": ("case_meta", "my-date", {"value_parser": "date"}),
        "datetime": ("case_meta", "my-datetime", {"value_parser": "datetime"}),
        "success": (
            "answer",
            "my-success",
            {
                "value_parser": (
                    "value_mapping",
                    {"mapping": {"my-success-yes": True, "my-success-no": False}},
                )
            },
            "multiple-choice",
            {
                "value_parser": (
                    "value_mapping",
                    {
                        "mapping": {
                            "multiple-choice-yes": True,
                            "multiple-choice-no": False,
                        }
                    },
                )
            },
        ),
        "static_value": ("static", "some-value"),
        "my_values": (
            "ng_table",
            ["values-v1", "values-v2"],
            {
                "column_mapping": {
                    "my_static_value": ("static", 3.14),
                    "my_value": "value-single",
                    "my_list": (
                        "list-values",
                        {
                            "value_parser": (
                                "list_mapping",
                                {
                                    "mapping": {
                                        "my_list_value": "value-list",
                                    }
                                },
                            )
                        },
                    ),
                }
            },
        ),
    }

    case = caluma_workflow_factories.CaseFactory(
        meta={"my-date": "2021-08-18", "my-datetime": "2021-08-18T06:58:08.397Z"},
        instance=instance,
    )

    utils.add_answer(case.document, "my-success", "my-success-yes")
    utils.add_answer(
        case.document, "multiple-choice", ["multiple-choice-yes", "multiple-choice-no"]
    )

    form_field_factory(
        instance=instance,
        name="values-v1",
        value=[
            {
                "value-single": 0,
                "list-values": [
                    {"value-list": 1},
                    {"value-list": 2},
                ],
            }
        ],
    )
    form_field_factory(
        instance=instance,
        name="values-v2",
        value=[
            {
                "value-single": 10,
                "list-values": [
                    {"value-list": 11},
                    {"value-list": 12},
                ],
            }
        ],
    )

    master_data = MasterData(case)

    snapshot.assert_match(
        {
            key: getattr(master_data, key)
            for key in master_data_settings["CONFIG"].keys()
        }
    )


@pytest.fixture
def be_master_data_case(db, be_instance, group, master_data_is_visible_mock, utils):
    be_instance.case.meta = {
        "ebau-number": "2021-1",
        "submit-date": "2021-03-31T13:17:08+0000",
        "paper-submit-date": "2021-03-20T13:17:08+0000",
    }
    be_instance.case.save()

    document = be_instance.case.document

    # Simple data
    utils.add_answer(document, "is-paper", "is-paper-no")
    utils.add_answer(document, "beschreibung-bauvorhaben", "Grosses Haus")
    utils.add_answer(
        document, "beschreibung-projektaenderung", "Doch eher kleines Haus"
    )
    utils.add_answer(document, "strasse-flurname", "Musterstrasse")
    utils.add_answer(document, "nr", 4)
    utils.add_answer(document, "baukosten-in-chf", 199000)
    utils.add_answer(document, "plz-grundstueck-v3", 3000)
    utils.add_answer(document, "ort-grundstueck", "Musterhausen")
    utils.add_answer(document, "baubeschrieb", "baubeschrieb-neubau", label="Neubau")
    utils.add_answer(
        document,
        "gewaesserschutzbereich-v2",
        ["gewaesserschutzbereich-v2-au"],
        label=[{"de": "Aᵤ", "fr": "Aᵤ"}],
    )
    utils.add_answer(
        document,
        "nutzungsart",
        ["nutzungsart-wohnen"],
        label=[{"de": "Wohnen", "fr": "Vivre"}],
    )
    utils.add_answer(document, "nutzungszone", "Wohnzone W2")
    utils.add_answer(document, "ueberbauungsordnung", "Überbauung XY")
    utils.add_answer(document, "sachverhalt", "Sachverhalt Test")
    utils.add_answer(
        document,
        "grundwasserschutzzonen",
        ["grundwasserschutzzonen-s1"],
        label=[{"de": "S1", "fr": "S1"}],
    )
    utils.add_answer(
        document,
        "grundwasserschutzzonen-v2",
        ["grundwasserschutzzonen-v2-s1"],
        label=[{"de": "S1", "fr": "S1"}],
    )
    utils.add_answer(
        document, "oeffentlichkeit", "oeffentlichkeit-oeffentlich", label="Öffentlich"
    )
    utils.add_answer(document, "alkoholausschank", "alkoholausschank-ja", label="Ja")
    utils.add_answer(
        document,
        "schuetzenswert",
        "schuetzenswert-ja",
        question_label="Schützenswert",
        label="Ja",
    )
    utils.add_answer(
        document,
        "erhaltenswert",
        "erhaltenswert-nein",
        question_label="Erhaltenswert",
        label="Nein",
    )
    utils.add_answer(
        document, "k-objekt", "k-objekt-ja", question_label="K-Objekt", label="Ja"
    )
    utils.add_answer(
        document,
        "baugruppe-bauinventar",
        "baugruppe-bauinventar-ja",
        question_label="Baugruppe Bauinventar",
        label="Ja",
    )
    utils.add_answer(document, "bezeichnung-baugruppe", "Test Baugruppe")
    utils.add_answer(document, "rrb", "rrb-ja", label="Ja")
    utils.add_answer(
        document,
        "rrb-vom",
        date(2022, 1, 1),
        question_label="RRB vom",
    )
    utils.add_answer(document, "vertrag", "vertrag-ja", label="Ja")

    utils.add_answer(
        document,
        "vertrag-vom",
        date(2022, 2, 1),
        question_label="Vertrag vom",
    )
    utils.add_answer(document, "sitzplaetze-garten", 20)

    # Municipality
    utils.add_answer(document, "gemeinde", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
    )

    # Table data
    utils.add_table_answer(
        document,
        "parzelle",
        [
            {
                "parzellennummer": 473,
                "e-grid-nr": "CH334687350542",
                "lagekoordinaten-ost": 2599941,
                "lagekoordinaten-nord": 1198923,
            },
            {
                "parzellennummer": 2592,
                "e-grid-nr": "CH913553467614",
                "lagekoordinaten-ost": 2601995,
                "lagekoordinaten-nord": 1201340,
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-gesuchstellerin",
        [
            {
                "vorname-gesuchstellerin": "Max",
                "name-gesuchstellerin": "Mustermann",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "ACME AG",
                "strasse-gesuchstellerin": "Teststrasse",
                "nummer-gesuchstellerin": 123,
                "ort-gesuchstellerin": "Testhausen",
                "plz-gesuchstellerin": 1234,
            }
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-projektverfasserin",
        [
            {
                "vorname-projektverfasserin": "Hans",
                "name-projektverfasserin": "Müller",
                "strasse-projektverfasserin": "Einweg",
                "nummer-projektverfasserin": 9,
                "plz-projektverfasserin": 3000,
                "ort-projektverfasserin": "Bern",
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-gebaudeeigentumerin",
        [
            {
                "vorname-gebaeudeeigentuemerin": "Peter",
                "name-gebaeudeeigentuemerin": "Meier",
                "strasse-gebaeudeeigentuemerin": "Thunstrasse",
                "nummer-gebaeudeeigentuemerin": 88,
                "plz-gebaeudeeigentuemerin": 3002,
                "ort-gebaeudeeigentuemerin": "Bern",
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-grundeigentumerin",
        [
            {
                "vorname-grundeigentuemerin": "Sandra",
                "name-grundeigentuemerin": "Holzer",
                "strasse-grundeigentuemerin": "Bernweg",
                "nummer-grundeigentuemerin": 12,
                "plz-grundeigentuemerin": 3002,
                "ort-grundeigentuemerin": "Bern",
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-vertreterin-mit-vollmacht",
        [
            {
                "juristische-person-vertreterin": "juristische-person-vertreterin-ja",
                "name-juristische-person-vertreterin": "Mustermann und Söhne AG",
                "strasse-vertreterin": "Juristenweg",
                "nummer-vertreterin": 99,
                "plz-vertreterin": 3008,
                "ort-vertreterin": "Bern",
            },
        ],
    )
    utils.add_table_answer(
        document, "ausschankraeume", [{"sitzplaetze": 20}, {"sitzplaetze": 15}]
    )

    return be_instance.case


@pytest.fixture
def gr_master_data_case(db, gr_instance, group, master_data_is_visible_mock, utils):
    gr_instance.case.meta = {
        "dossier-number": "2023-1",
        "submit-date": "2021-03-31T13:17:08+0000",
    }
    gr_instance.case.save()

    document = gr_instance.case.document

    # Simple data
    utils.add_answer(document, "beschreibung-bauvorhaben", "Einfamilienhaus")
    utils.add_answer(document, "projektaenderung", "projektaenderung-ja")
    utils.add_answer(document, "street-and-housenumber", "Teststrasse 12")
    utils.add_answer(document, "plz-grundstueck-v3", 1234)
    utils.add_answer(document, "ort-grundstueck", "Testhausen")
    utils.add_answer(document, "baukosten", 4000)

    # Municipality
    utils.add_answer(document, "gemeinde", "18")
    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=gr_instance.case.document,
        slug="18",
        label={"de": "Chur", "fr": "Chur"},
    )

    # Table data
    utils.add_table_answer(
        document,
        "parzelle",
        [
            {
                "parzellennummer": 123465,
                "e-grid-nr": "CH334687150542",
                "lagekoordinaten-ost": 2569941,
                "lagekoordinaten-nord": 1298923,
            },
            {
                "parzellennummer": 789876,
                "e-grid-nr": "CH913545967614",
                "lagekoordinaten-ost": 2609995,
                "lagekoordinaten-nord": 1271340,
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-gesuchstellerin",
        [
            {
                "vorname-gesuchstellerin": "Esther",
                "name-gesuchstellerin": "Tester",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Test AG",
                "strasse-gesuchstellerin": "Testweg",
                "nummer-gesuchstellerin": 321,
                "ort-gesuchstellerin": "Testingen",
                "plz-gesuchstellerin": 4321,
            }
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-projektverfasserin",
        [
            {
                "vorname-gesuchstellerin": "Hans",
                "name-gesuchstellerin": "Muster",
                "strasse-gesuchstellerin": "Bahnhofstrasse",
                "nummer-gesuchstellerin": 3,
                "plz-gesuchstellerin": 3600,
                "ort-gesuchstellerin": "Thun",
            },
        ],
    )
    utils.add_table_answer(
        document,
        "personalien-grundeigentumerin",
        [
            {
                "vorname-gesuchstellerin": "Sandra",
                "name-gesuchstellerin": "Beispiel",
                "strasse-gesuchstellerin": "Beispielstrasse",
                "nummer-gesuchstellerin": 16,
                "plz-gesuchstellerin": 2222,
                "ort-gesuchstellerin": "Beispieldorf",
            },
        ],
    )
    utils.add_table_answer(
        document,
        "gebaeude-und-anlagen",
        [
            {
                "amtliche-gebaeudenummer": "4-116",
                # heating 1
                "waermeerzeuger-heizung": "waermeerzeuger-heizung-7430",
                "energie-waermequelle-heizung": "energie-waermequelle-heizung-7540",
                # heating 2
                "weitere-waermeerzeuger-heizung": "weitere-waermeerzeuger-heizung-7499",
                "weitere-energie-waermequelle-heizung": "weitere-energie-waermequelle-heizung-7530",
                # warm water 1
                "waermeerzeuger-warmwasser": "waermeerzeuger-warmwasser-7651",
                "energie-waermequelle-warmwasser": "energie-waermequelle-warmwasser-7510",
                # warm water 2
                "weitere-waermeerzeuger-warmwasser": "weitere-waermeerzeuger-warmwasser-7660",
                "weitere-energie-waermequelle-warmwasser": "weitere-energie-waermequelle-warmwasser-7512",
            },
        ],
    )

    return gr_instance.case


@pytest.fixture
def so_master_data_case(
    db,
    so_instance,
    workflow_entry_factory,
    camac_answer_factory,
    master_data_is_visible_mock,
    utils,
):
    so_instance.case.meta = {
        "dossier-number": "2024-1",
        "submit-date": "2024-02-22T13:17:08+0000",
    }
    so_instance.case.save()

    document = so_instance.case.document

    # Simple data
    utils.add_answer(document, "umschreibung-bauprojekt", "Grosses Haus")
    utils.add_answer(document, "strasse-flurname", "Musterstrasse")
    utils.add_answer(document, "strasse-nummer", 4)
    utils.add_answer(document, "gesamtkosten", 129000)
    utils.add_answer(document, "ort", "Musterdorf")
    utils.add_answer(
        document,
        "art-der-bauwerke",
        ["art-der-bauwerke-hochbaute", "art-der-bauwerke-tiefbaute"],
    )

    # Municipality
    utils.add_answer(document, "gemeinde", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=so_instance.case.document,
        slug="1",
        label={"de": "Solothurn"},
    )

    # Plot
    utils.add_table_answer(
        document,
        "parzellen",
        [
            {
                "parzellennummer": 123456789,
                "e-grid": "CH123456789",
                "lagekoordinaten-ost": 2690970.9,
                "lagekoordinaten-nord": 1192891.9,
            }
        ],
    )

    # Applicant
    utils.add_table_answer(
        document,
        "bauherrin",
        [
            {
                "vorname": "Max",
                "nachname": "Mustermann",
                "juristische-person": "juristische-person-ja",
                "juristische-person-name": "ACME AG",
                "strasse": "Teststrasse",
                "strasse-nummer": 123,
                "plz": 1233,
                "ort": "Musterdorf",
                "country": "Schweiz",
            }
        ],
    )

    # Buildings
    utils.add_table_answer(
        document,
        "gebaeude",
        [
            {
                "art-der-hochbaute": "art-der-hochbaute-parkhaus",
                "gebaeude-bezeichnung": "Villa",
                "proposal": ["proposal-neubau"],
                "gebaeudekategorie": "gebaeudekategorie-ohne-wohnnutzung",
            }
        ],
    )

    # Dwellings
    utils.add_table_answer(
        document,
        "wohnungen",
        [
            {
                "dazugehoeriges-gebaeude": "Villa",
                "stockwerktyp": "stockwerktyp-obergeschoss",
                "stockwerknummer": "2",
                "lage": "Süd",
                "anzahl-zimmer": "20",
                "kocheinrichtung": "kocheinrichtung-kochnische-greater-4-m2",
                "flaeche": "420",
                "maisonette": "maisonette-ja",
                "zwg": "zwg-keine",
            },
            {
                "dazugehoeriges-gebaeude": "Villa",
                "stockwerktyp": "stockwerktyp-parterre",
                "lage": "Nord",
                "anzahl-zimmer": "10",
                "kocheinrichtung": "kocheinrichtung-keine-kocheinrichtung",
                "flaeche": "72",
                "maisonette": "maisonette-nein",
                "zwg": "zwg-erstwohnung",
            },
        ],
    )

    # Energy devices
    utils.add_table_answer(
        document,
        "gebaeudetechnik",
        [
            {
                "bezeichnung-dazugehoeriges-gebaeude": "Villa",
                "anlagetyp": "anlagetyp-hauptheizung",
                "heizsystem-art": "-hauptheizung",
                "hauptheizungsanlage": "hauptheizungsanlage-sonne-thermisch",
            },
        ],
    )

    return so_instance.case


@pytest.fixture
def ur_master_data_case_gwr(
    ur_instance, ur_master_data_case, workflow_entry_factory, utils
):
    ur_master_data_case.meta = {"dossier-number": "1201-21-003"}
    ur_master_data_case.save()

    document = ur_master_data_case.document

    # Completed date
    # Assert that workflow entry of last group (phase) is selected
    workflow_entry = next(
        filter(
            lambda entry: entry.workflow_item_id == 67,
            ur_instance.workflowentry_set.all(),
        ),
        None,
    )

    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-08-05 08:00:06+00",
        group=2,
        workflow_item=workflow_entry.workflow_item,
    )

    # Energy devices
    # Check logic for heating / warmwater devices and
    # primary / secondary devices
    table_answer = document.answers.filter(question_id="haustechnik-tabelle").first()
    utils.add_table_answer(
        document,
        "haustechnik-tabelle",
        [
            {
                "gehoert-zu-gebaeudenummer": "Villa",
                "anlagetyp": "anlagetyp-warmwasser",
                "heizsystem-art": "-zusatzheizung",
                "hauptheizungsanlage": "hauptheizungsanlage-gas",
            }
        ],
        table_answer,
    )

    return ur_master_data_case


@pytest.fixture
def sz_master_data_case_gwr(sz_master_data_case, form_field_factory):
    sz_instance = sz_master_data_case.instance

    # GWR Form
    form_field_factory(
        instance=sz_instance,
        name="gwr",
        value=[
            {
                "kategorie": "Gebäude ohne Wohnnutzung",
                "heizungsart": "Einzelofenheizung",
                "energietrager-heizung": "Holz",
                "energietrager-warmwasser": "Elektrizität",
                "geschosse": 2,
                "wohnungen": [
                    {
                        "stockwerk": "1. OG",
                        "maisonette": "Ja",
                        "lage": "Nord",
                        "zimmer": 4,
                        "flache": 42,
                        "kuchenart": "Kochnische (unter 4m²)",
                    }
                ],
            }
        ],
    )

    return sz_instance.case


@pytest.fixture
def sz_master_data_case_gwr_v2(sz_master_data_case, form_field_factory):
    sz_instance = sz_master_data_case.instance

    # GWR Form v2
    form_field_factory(
        instance=sz_instance,
        name="gwr-v2",
        value=[
            {
                "gebaeudebezeichnung": "Grosses Haus",
                "kategorie": "Gebäude mit ausschliesslicher Wohnnutzung",
                "zivilschutzraum": "Ja",
                "heizungsart": "Wärmepumpe für mehrere Gebäude",
                "energietrager-heizung": "Erdwärme (generisch)",
                "waermeerzeuger-warmwasser": "Zentraler Elektroboiler",
                "energietrager-warmwasser": "Sonne (thermisch)",
                "geschosse": 4,
                "wohnraeume": 24,
                "wohnungen": [
                    {
                        "stockwerk": "Parterre",
                        "maisonette": "Nein",
                        "lage": "West",
                        "zimmer": 2,
                        "flache": 70,
                        "kocheinrichtung": "Ja",
                    },
                    {
                        "stockwerk": "2. UG",
                        "maisonette": "Nein",
                        "lage": "Ost",
                        "zimmer": 3,
                        "flache": 24,
                        "kocheinrichtung": "Nein",
                    },
                ],
            }
        ],
    )

    return sz_instance.case


@pytest.mark.parametrize(
    "canton_master_data_settings,language,case,select_related,prefetch_related,num_queries",
    [
        (
            pytest.lazy_fixture("be_master_data_settings"),
            "de",
            pytest.lazy_fixture("be_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            # 1. Query for fetching case
            # 2. Query for prefetching direct answers on case.document
            # 3. Query for prefetching questions of answers
            # 4. Query for prefetching options for questions
            # 5. Query for prefetching row document relation tables
            # 6. Query for prefetching row documents
            # 7. Query for prefetching answer on previously prefetched row documents
            # 8. Query for prefetching dynamic options
            # 9. Query for fetching main form
            # 10. ?
            10,
        ),
        (
            pytest.lazy_fixture("be_master_data_settings"),
            "fr",
            pytest.lazy_fixture("be_master_data_case"),
            ["document"],
            [
                "document__answers",
                "document__answers__question__options",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "work_items__document__answers",
                "work_items__document__answers__answerdocument_set",
                "work_items__document__answers__answerdocument_set__document__answers",
            ],
            10,
        ),
        (
            pytest.lazy_fixture("ur_master_data_settings"),
            "de",
            pytest.lazy_fixture("ur_master_data_case"),
            ["document", "instance"],
            [
                "document__answers",
                "document__answers__answerdocument_set",
                "document__answers__answerdocument_set__document__answers",
                "document__dynamicoption_set",
                "instance__workflowentry_set",
                "instance__answers",
            ],
            # 1. Query for fetching case
            # 2. Query for prefetching direct answers on case.document
            # 3. Query for prefetching row document relation tables
            # 4. Query for prefetching row documents
            # 5. Query for prefetching answer on previously prefetched row documents
            # 6. Query for prefetching dynamic options
            # 7. Query for prefetching workflow entries
            # 8. Query for prefetching camac core answers
            8,
        ),
        (
            pytest.lazy_fixture("sz_master_data_settings"),
            "de",
            pytest.lazy_fixture("sz_master_data_case_gwr"),
            ["instance", "instance__form"],
            ["instance__fields", "instance__workflowentry_set", "work_items"],
            # 1. Query for fetching case
            # 2. Query for prefetching fields
            # 3. Query for prefetching workflow entries
            # 4. Query for prefetching work_items
            # 5. Query for selecting form
            5,
        ),
        (
            pytest.lazy_fixture("sz_master_data_settings"),
            "de",
            pytest.lazy_fixture("sz_master_data_case_gwr_v2"),
            ["instance", "instance__form"],
            ["instance__fields", "instance__workflowentry_set", "work_items"],
            # 1. Query for fetching case
            # 2. Query for prefetching fields
            # 3. Query for prefetching workflow entries
            # 4. Query for prefetching work_items
            # 5. Query for selecting form
            5,
        ),
    ],
)
def test_master_data(
    db,
    snapshot,
    django_assert_num_queries,
    language,
    case,
    select_related,
    prefetch_related,
    num_queries,
    canton_master_data_settings,
):
    with django_assert_num_queries(num_queries), override(language):
        case = (
            caluma_workflow_models.Case.objects.filter(pk=case.pk)
            .select_related(*select_related)
            .prefetch_related(*prefetch_related)
            .first()
        )

        master_data = MasterData(case)

        snapshot.assert_match(
            {
                key: getattr(master_data, key)
                for key in canton_master_data_settings["CONFIG"].keys()
            }
        )
