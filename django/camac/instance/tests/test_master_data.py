import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import (
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.conf import settings
from django.utils.translation import override

from ..master_data import MasterData


def _question(slug, question_label=None):
    return (
        {"question_id": slug}
        if caluma_form_models.Question.objects.filter(pk=slug).exists()
        else {
            "question__pk": slug,
            **({"question__label": question_label} if question_label else {}),
        }
    )


def add_answer(
    document,
    question,
    value,
    value_key="value",
    label=None,
    question_label=None,
):
    answer = caluma_form_factories.AnswerFactory(
        document=document, **{value_key: value, **_question(question, question_label)}
    )

    if label:
        if not isinstance(label, list):
            label = [label]

        if not isinstance(value, list):
            value = [value]

        for val, lab in zip(value, label):
            if not isinstance(lab, dict):
                lab = {"de": lab, "fr": lab}

            caluma_form_factories.QuestionOptionFactory(
                question_id=question, option__slug=val, option__label=lab
            )

    return answer


def add_table_answer(document, question, rows, table_answer=None):
    answer = add_answer(document, question, None) if not table_answer else table_answer

    for i, row in enumerate(reversed(rows)):
        row_document = caluma_form_factories.DocumentFactory(family=document)
        for column, value in row.items():
            add_answer(row_document, column, value)

        caluma_form_factories.AnswerDocumentFactory(
            document=row_document, answer=answer, sort=i
        )

    return answer


def test_master_data_exceptions(
    db,
    instance,
    instance_with_case,
    application_settings,
):
    application_settings["MASTER_DATA"] = {
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
):
    application_settings["MASTER_DATA"] = {
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

    add_answer(case.document, "my-success", "my-success-yes")
    add_answer(
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
            for key in application_settings["MASTER_DATA"].keys()
        }
    )


@pytest.fixture
def be_master_data_case(db, be_instance, group, master_data_is_visible_mock):
    be_instance.case.meta = {
        "ebau-number": "2021-1",
        "submit-date": "2021-03-31T13:17:08+0000",
        "paper-submit-date": "2021-03-20T13:17:08+0000",
    }
    be_instance.case.save()

    document = be_instance.case.document

    # Simple data
    add_answer(document, "is-paper", "is-paper-no")
    add_answer(document, "beschreibung-bauvorhaben", "Grosses Haus")
    add_answer(document, "beschreibung-projektaenderung", "Doch eher kleines Haus")
    add_answer(document, "strasse-flurname", "Musterstrasse")
    add_answer(document, "nr", 4)
    add_answer(document, "baukosten-in-chf", 199000)
    add_answer(document, "ort-grundstueck", "Musterhausen")
    add_answer(document, "baubeschrieb", "baubeschrieb-neubau", label="Neubau")
    add_answer(
        document,
        "gewaesserschutzbereich-v2",
        ["gewaesserschutzbereich-v2-au"],
        label=[{"de": "Aᵤ", "fr": "Aᵤ"}],
    )
    add_answer(
        document,
        "nutzungsart",
        ["nutzungsart-wohnen"],
        label=[{"de": "Wohnen", "fr": "Vivre"}],
    )
    add_answer(document, "nutzungszone", "Wohnzone W2")
    add_answer(document, "ueberbauungsordnung", "Überbauung XY")
    add_answer(document, "sachverhalt", "Sachverhalt Test")
    add_answer(
        document,
        "grundwasserschutzzonen",
        ["grundwasserschutzzonen-s1"],
        label=[{"de": "S1", "fr": "S1"}],
    )
    add_answer(
        document,
        "grundwasserschutzzonen-v2",
        ["grundwasserschutzzonen-v2-s1"],
        label=[{"de": "S1", "fr": "S1"}],
    )
    add_answer(
        document, "oeffentlichkeit", "oeffentlichkeit-oeffentlich", label="Öffentlich"
    )
    add_answer(document, "alkoholausschank", "alkoholausschank-ja", label="Ja")
    add_answer(document, "sitzplaetze-garten", 20)

    # Municipality
    add_answer(document, "gemeinde", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
    )

    # Table data
    add_table_answer(
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
    add_table_answer(
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
    add_table_answer(
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
    add_table_answer(
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
    add_table_answer(
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
    add_table_answer(
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
    add_table_answer(
        document, "ausschankraeume", [{"sitzplaetze": 20}, {"sitzplaetze": 15}]
    )

    return be_instance.case


@pytest.fixture
def ur_master_data_case(
    db,
    ur_instance,
    workflow_entry_factory,
    camac_answer_factory,
    master_data_is_visible_mock,
):
    ur_instance.case.meta = {"dossier-number": "1201-21-003"}
    ur_instance.case.save()

    document = ur_instance.case.document

    # Simple data
    add_answer(document, "proposal-description", "Grosses Haus")
    add_answer(document, "parcel-street", "Musterstrasse")
    add_answer(document, "parcel-street-number", 4)
    add_answer(document, "construction-cost", 129000)
    add_answer(document, "parcel-city", "Musterdorf")
    add_answer(document, "category", ["category-hochbaute", "category-tiefbaute"])
    add_answer(document, "veranstaltung-art", ["veranstaltung-art-umbau"])
    add_answer(document, "oereb-thema", ["oereb-thema-knp"])
    add_answer(document, "form-type", ["form-type-oereb"])
    add_answer(document, "typ-des-verfahrens", ["typ-des-verfahrens-genehmigung"])

    # Municipality
    add_answer(document, "municipality", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Altdorf"},
    )

    # Authority
    add_answer(document, "leitbehoerde", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="leitbehoerde",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Leitbehörde Altdorf"},
    )

    # Plot
    add_table_answer(
        document,
        "parcels",
        [
            {
                "parcel-number": 123456789,
                "e-grid": "CH123456789",
                "coordinates-east": 2690970.9,
                "coordinates-north": 1192891.9,
            }
        ],
    )

    # Applicant
    add_table_answer(
        document,
        "applicant",
        [
            {
                "first-name": "Max",
                "last-name": "Mustermann",
                "is-juristic-person": "is-juristic-person-yes",
                "juristic-person-name": "ACME AG",
                "street": "Teststrasse",
                "street-number": 123,
                "zip": 1233,
                "city": "Musterdorf",
                "country": "Schweiz",
            }
        ],
    )

    # Submit date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
        workflow_item__pk=12,
    )

    # Decision date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-20 08:00:06+00",
        group=1,
        workflow_item__pk=47,
    )

    # Construction start date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-25 08:00:06+00",
        group=1,
        workflow_item__pk=55,
    )

    # Construction end date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-30 08:00:06+00",
        group=1,
        workflow_item__pk=67,
    )

    # Approval reason
    camac_answer_factory(answer=5031, question__question_id=264, instance=ur_instance)

    # Type of applicant
    camac_answer_factory(
        answer=6141,
        question__question_id=267,
        instance=ur_instance,
    )

    # Buildings
    add_table_answer(
        document,
        "gebaeude",
        [
            {
                "art-der-hochbaute": "art-der-hochbaute-parkhaus",
                "gebaeudenummer-bezeichnung": "Villa",
                "proposal": ["proposal-neubau"],
                "gebaeudekategorie": "gebaeudekategorie-ohne-wohnnutzung",
            }
        ],
    )

    # Dwellings
    add_table_answer(
        document,
        "wohnungen",
        [
            {
                "zugehoerigkeit": "Villa",
                "stockwerktyp": "stockwerktyp-obergeschoss",
                "stockwerknummer": "2",
                "lage": "Süd",
                "wohnungsgroesse": "20",
                "kocheinrichtung": "kocheinrichtung-kochnische-greater-4-m2",
                "flaeche-in-m2": "420",
                "mehrgeschossige-wohnung": "mehrgeschossige-wohnung-ja",
                "zwg": "zwg-keine",
            },
            {
                "zugehoerigkeit": "Villa",
                "stockwerktyp": "stockwerktyp-parterre",
                "lage": "Nord",
                "wohnungsgroesse": "10",
                "kocheinrichtung": "kocheinrichtung-keine-kocheinrichtung",
                "flaeche-in-m2": "72",
                "mehrgeschossige-wohnung": "mehrgeschossige-wohnung-nein",
                "zwg": "zwg-erstwohnung",
            },
        ],
    )

    # Energy devices
    add_table_answer(
        document,
        "haustechnik-tabelle",
        [
            {
                "gehoert-zu-gebaeudenummer": "Villa",
                "anlagetyp": "anlagetyp-hauptheizung",
                "heizsystem-art": "-hauptheizung",
                "hauptheizungsanlage": "hauptheizungsanlage-sonne-thermisch",
            },
        ],
    )

    return ur_instance.case


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
    "application_name,language,case,select_related,prefetch_related,num_queries",
    [
        (
            "kt_bern",
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
            9,
        ),
        (
            "kt_bern",
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
            9,
        ),
        (
            "kt_uri",
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
            "kt_schwyz",
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
            "kt_schwyz",
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
    application_settings,
    django_assert_num_queries,
    application_name,
    language,
    case,
    select_related,
    prefetch_related,
    num_queries,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS[application_name][
        "MASTER_DATA"
    ]

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
                for key in application_settings["MASTER_DATA"].keys()
            }
        )
