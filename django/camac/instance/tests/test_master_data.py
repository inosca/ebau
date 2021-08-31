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

from camac.core.factories import WorkflowEntryFactory, WorkflowItemFactory

from ..master_data import MasterData


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

    caluma_form_factories.AnswerFactory(
        question__slug="my-success", value="my-success-yes", document=case.document
    )

    caluma_form_factories.AnswerFactory(
        question__slug="multiple-choice",
        value=["multiple-choice-yes", "multiple-choice-no"],
        document=case.document,
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

    # Simple data
    caluma_form_factories.AnswerFactory(
        question_id="is-paper",
        document=be_instance.case.document,
        value="is-paper-no",
    )
    caluma_form_factories.AnswerFactory(
        question_id="beschreibung-bauvorhaben",
        document=be_instance.case.document,
        value="Grosses Haus",
    )
    caluma_form_factories.AnswerFactory(
        question__slug="beschreibung-projektaenderung",
        document=be_instance.case.document,
        value="Doch eher kleines Haus",
    )
    caluma_form_factories.AnswerFactory(
        question__slug="strasse-flurname",
        document=be_instance.case.document,
        value="Musterstrasse",
    )
    caluma_form_factories.AnswerFactory(
        question__slug="nr",
        document=be_instance.case.document,
        value=4,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="baukosten-in-chf",
        document=be_instance.case.document,
        value=199000,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="ort-grundstueck",
        document=be_instance.case.document,
        value="Musterhausen",
    )

    # Municipality
    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
    )

    # Plot
    row_form = caluma_form_factories.FormFactory(slug="parzelle-tabelle")
    table_answer_plot = caluma_form_factories.AnswerFactory(
        question__slug="parzelle",
        question__type=caluma_form_models.Question.TYPE_TEXT,
        document=be_instance.case.document,
    )
    caluma_form_factories.FormQuestionFactory(
        form=row_form,
        question__slug="parzellennummer",
        question__type=caluma_form_models.Question.TYPE_CHOICE,
    )
    caluma_form_factories.FormQuestionFactory(
        form=row_form,
        question__slug="e-grid-nr",
        question__type=caluma_form_models.Question.TYPE_CHOICE,
    )
    plot_row = caluma_form_factories.DocumentFactory(form=row_form)
    table_answer_plot.documents.add(plot_row)
    caluma_form_factories.AnswerFactory(
        question_id="parzellennummer",
        value="123456789",
        document=plot_row,
    )
    caluma_form_factories.AnswerFactory(
        question_id="e-grid-nr",
        value="CH123456789",
        document=plot_row,
    )

    # Applicant
    table_answer_applicant = caluma_form_factories.AnswerFactory(
        question_id="personalien-gesuchstellerin", document=be_instance.case.document
    )
    applicant_row = caluma_form_factories.DocumentFactory(form_id="personalien-tabelle")
    table_answer_applicant.documents.add(applicant_row)
    caluma_form_factories.AnswerFactory(
        question_id="vorname-gesuchstellerin",
        value="Max",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question_id="name-gesuchstellerin",
        value="Mustermann",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="juristische-person-gesuchstellerin",
        value="juristische-person-gesuchstellerin-ja",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="name-juristische-person-gesuchstellerin",
        value="ACME AG",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="strasse-gesuchstellerin",
        value="Teststrasse",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="nummer-gesuchstellerin",
        value=123,
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="ort-gesuchstellerin",
        value="Testhausen",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="plz-gesuchstellerin",
        value=1234,
        document=applicant_row,
    )

    return be_instance.case


@pytest.mark.parametrize("language", ["de", "fr"])
def test_master_data_be(
    db,
    be_master_data_case,
    snapshot,
    application_settings,
    django_assert_num_queries,
    language,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    # This should never trigger more than 5 queries on the DB:
    # 1. Query for fetching case
    # 2. Query for prefetching direct answers on case.document
    # 3. Query for prefetching row documents
    # 4. Query for prefetching answer on previously prefetched row documents
    # 5. Query for prefetching dynamic options
    with django_assert_num_queries(5), override(language):
        case = (
            caluma_workflow_models.Case.objects.filter(pk=be_master_data_case.pk)
            .select_related("document")
            .prefetch_related(
                "document__answers",
                "document__answers__documents__answers",
                "document__dynamicoption_set",
            )
            .first()
        )

        master_data = MasterData(case)

        snapshot.assert_match(
            {
                key: getattr(master_data, key)
                for key in application_settings["MASTER_DATA"].keys()
            }
        )


@pytest.fixture
def ur_master_data_case(
    db,
    ur_instance,
):
    ur_instance.case.meta = {"dossier-number": "1201-21-003"}
    ur_instance.case.save()

    # Simple data
    caluma_form_factories.AnswerFactory(
        question__slug="proposal-description",
        document=ur_instance.case.document,
        value="Grosses Haus",
    )
    caluma_form_factories.AnswerFactory(
        question__slug="parcel-street",
        document=ur_instance.case.document,
        value="Musterstrasse",
    )
    caluma_form_factories.AnswerFactory(
        question__slug="parcel-street-number",
        document=ur_instance.case.document,
        value=4,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="construction-cost",
        document=ur_instance.case.document,
        value=129000,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="parcel-city",
        document=ur_instance.case.document,
        value="Musterdorf",
    )

    # Municipality
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Altdorf"},
    )

    # Plot
    row_form = caluma_form_factories.FormFactory(slug="parcels")
    table_answer_plot = caluma_form_factories.AnswerFactory(
        question__slug="parcels",
        question__type=caluma_form_models.Question.TYPE_TEXT,
        document=ur_instance.case.document,
    )
    caluma_form_factories.FormQuestionFactory(
        form=row_form,
        question__slug="parcel-number",
        question__type=caluma_form_models.Question.TYPE_INTEGER,
    )
    caluma_form_factories.FormQuestionFactory(
        form=row_form,
        question__slug="e-grid",
        question__type=caluma_form_models.Question.TYPE_TEXT,
    )
    plot_row = caluma_form_factories.DocumentFactory(form=row_form)
    table_answer_plot.documents.add(plot_row)
    caluma_form_factories.AnswerFactory(
        question_id="parcel-number",
        value="123456789",
        document=plot_row,
    )
    caluma_form_factories.AnswerFactory(
        question_id="e-grid",
        value="CH123456789",
        document=plot_row,
    )

    # Applicant
    table_answer_applicant = caluma_form_factories.AnswerFactory(
        question__slug="applicant", document=ur_instance.case.document
    )
    applicant_row = caluma_form_factories.DocumentFactory(form__slug="personal-table")
    table_answer_applicant.documents.add(applicant_row)
    caluma_form_factories.AnswerFactory(
        question__slug="first-name",
        value="Max",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="last-name",
        value="Mustermann",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="is-juristic-person",
        value="is-juristic-person-yes",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="juristic-person-name",
        value="ACME AG",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="street",
        value="Teststrasse",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="street-number",
        value="123",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="zip",
        value="1233",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="city",
        value="Musterdorf",
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="country",
        value="Schweiz",
        document=applicant_row,
    )

    # Category
    caluma_form_factories.AnswerFactory(
        question__slug="category",
        value=["category-hochbaute", "category-tiefbaute"],
        document=ur_instance.case.document,
    )

    # WorkflowEntry
    WorkflowEntryFactory(
        instance=ur_instance,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
        workflow_item=WorkflowItemFactory(workflow_item_id=12),
    )

    return ur_instance.case


def test_master_data_ur(
    db,
    ur_master_data_case,
    snapshot,
    application_settings,
    django_assert_num_queries,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_uri"]["MASTER_DATA"]

    # This should never trigger more than 6 queries on the DB:
    # 1. Query for fetching case
    # 2. Query for prefetching direct answers on case.document
    # 3. Query for prefetching row documents
    # 4. Query for prefetching answer on previously prefetched row documents
    # 5. Query for prefetching dynamic options
    # 6. Query for prefetching workflow entries
    with django_assert_num_queries(6):
        case = (
            caluma_workflow_models.Case.objects.filter(pk=ur_master_data_case.pk)
            .select_related("document", "instance")
            .prefetch_related(
                "document__answers",
                "document__answers__documents__answers",
                "document__dynamicoption_set",
                "instance__workflowentry_set",
            )
            .first()
        )

        master_data = MasterData(case)

        snapshot.assert_match(
            {
                key: getattr(master_data, key)
                for key in application_settings["MASTER_DATA"].keys()
            }
        )
