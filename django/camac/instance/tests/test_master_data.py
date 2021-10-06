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


def _question(slug):
    return (
        {"question_id": slug}
        if caluma_form_models.Question.objects.filter(pk=slug).exists()
        else {"question__pk": slug}
    )


def add_answer(
    document,
    question,
    value,
    value_key="value",
    label=None,
):
    answer = caluma_form_factories.AnswerFactory(
        document=document, **{value_key: value, **_question(question)}
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


def add_table_answer(document, question, rows):
    answer = add_answer(document, question, None)

    for i, row in enumerate(reversed(rows)):
        row_document = caluma_form_factories.DocumentFactory()
        for column, value in row.items():
            add_answer(row_document, column, value)

        caluma_form_factories.AnswerDocumentFactory(
            document=row_document, answer=answer, sort=i
        )

    return answer


def test_master_data_exceptions(
    db,
    application_settings,
):
    application_settings["MASTER_DATA"] = {
        "bar": ("unconfigured", "bar"),
        "baz": ("case_meta", "baz", {"value_parser": "boolean"}),
    }

    master_data = MasterData(caluma_workflow_factories.CaseFactory(meta={"baz": True}))

    with pytest.raises(AttributeError) as e:
        assert master_data.foo

    assert (
        str(e.value)
        == "Key 'foo' is not configured in master data config. Available keys are: bar, baz"
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


def test_master_data_parsers(
    db,
    application_settings,
    snapshot,
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
    }

    case = caluma_workflow_factories.CaseFactory(
        meta={"my-date": "2021-08-18", "my-datetime": "2021-08-18T06:58:08.397Z"}
    )

    add_answer(case.document, "my-success", "my-success-yes")
    add_answer(
        case.document, "multiple-choice", ["multiple-choice-yes", "multiple-choice-no"]
    )

    master_data = MasterData(case)

    snapshot.assert_match(
        {
            key: getattr(master_data, key)
            for key in application_settings["MASTER_DATA"].keys()
        }
    )


@pytest.fixture
def be_master_data_case(
    db,
    be_instance,
):
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
    add_answer(document, "schuetzenswert", "schuetzenswert-ja", label="Ja")
    add_answer(document, "erhaltenswert", "erhaltenswert-nein", label="Nein")
    add_answer(document, "k-objekt", "k-objekt-nein", label="Nein")
    add_answer(
        document, "baugruppe-bauinventar", "baugruppe-bauinventar-nein", label="Nein"
    )
    add_answer(document, "rrb", "rrb-ja", label="Ja")
    add_answer(document, "vertrag", "vertrag-ja", label="Ja")

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

    return be_instance.case


@pytest.fixture
def ur_master_data_case(db, ur_instance, workflow_entry_factory):
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

    # Municipality
    add_answer(document, "municipality", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Altdorf"},
    )

    # Plot
    add_table_answer(
        document,
        "parcels",
        [
            {
                "parcel-number": 123456789,
                "e-grid": "CH123456789",
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

    return ur_instance.case


@pytest.fixture
def sz_master_data_case(db, sz_instance, form_field_factory, workflow_entry_factory):
    # Simple data
    form_field_factory(instance=sz_instance, name="bezeichnung", value="Grosses Haus")
    form_field_factory(instance=sz_instance, name="baukosten", value=129000)

    # Applicant
    form_field_factory(
        instance=sz_instance,
        name="bauherrschaft",
        value=[
            {
                "vorname": "Max",
                "name": "Mustermann",
                "strasse": "Teststrasse",
                "plz": 1233,
                "ort": "Musterdorf",
            }
        ],
    )

    # Submit date
    workflow_entry_factory(
        instance=sz_instance,
        workflow_date="2021-07-16 08:00:06+00",
        workflow_item__pk=10,
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
            ],
            # 1. Query for fetching case
            # 2. Query for prefetching direct answers on case.document
            # 3. Query for prefetching questions of answers
            # 4. Query for prefetching options for questions
            # 5. Query for prefetching row document relation tables
            # 6. Query for prefetching row documents
            # 7. Query for prefetching answer on previously prefetched row documents
            # 8. Query for prefetching dynamic options
            8,
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
            ],
            8,
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
            ],
            # 1. Query for fetching case
            # 2. Query for prefetching direct answers on case.document
            # 3. Query for prefetching row document relation tables
            # 4. Query for prefetching row documents
            # 5. Query for prefetching answer on previously prefetched row documents
            # 6. Query for prefetching dynamic options
            # 7. Query for prefetching workflow entries
            7,
        ),
        (
            "kt_schwyz",
            "de",
            pytest.lazy_fixture("sz_master_data_case"),
            ["instance"],
            ["instance__fields", "instance__workflowentry_set"],
            # 1. Query for fetching case
            # 2. Query for prefetching fields
            # 3. Query for prefetching workflow entries
            3,
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
