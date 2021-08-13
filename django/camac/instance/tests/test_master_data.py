import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow.models import Case
from django.utils.translation import override

from ..master_data import MasterData


def test_master_data(
    db,
    be_instance,
    application_settings,
    question_factory,
    answer_factory,
    dynamic_option_factory,
    django_assert_num_queries,
):
    application_settings["MASTER_DATA"] = {
        "proposal": (
            "answer",
            "beschreibung-bauvorhaben",
        ),
        "construction_costs": ("answer", "baukosten-in-chf"),
        "ebau_number": (
            "case_meta",
            "ebau-number",
        ),
        "personal_data": (
            "table",
            "personalien-gesuchstellerin",
            {
                "country": None,
                "last_name": "name-gesuchstellerin",
                "first_name": "vorname-gesuchstellerin",
                "is_juristic_person": (
                    "juristische-person-gesuchstellerin",
                    {
                        "juristische-person-gesuchstellerin-ja": True,
                        "juristische-person-gesuchstellerin-nein": False,
                    },
                ),
            },
        ),
        "plot_data": (
            "table",
            "parzelle",
            {
                "plot_number": "parzellennummer",
                "e_grid_number": "e-grid-nr",
            },
        ),
        "submit_date": ("case_meta", "submit-date"),
        "paper_submit_date": ("case_meta", "paper-submit-date"),
        "municipality": ("dynamic_option", "gemeinde"),
        "unconfigured_resolver": ("unconfigured", "bar"),
    }

    answer_factory(
        question_id="beschreibung-bauvorhaben",
        document=be_instance.case.document,
        value="Grosses Haus",
    )
    be_instance.case.document.form.questions.add(
        caluma_form_models.Question.objects.get(slug="beschreibung-bauvorhaben")
    )
    be_instance.case.meta = {
        "ebau-number": "2021-1",
        "submit-date": "2021-03-31T13:17:08+0000",
        "paper-submit-date": "2021-03-20T13:17:08+0000",
    }
    be_instance.case.save()
    # Dynamic option
    dynamic_option_factory(
        question_id="gemeinde",
        document=be_instance.case.document,
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
    )
    # Parcel questions and answers
    plot_question = question_factory(
        slug="parzelle", type=caluma_form_models.Question.TYPE_TEXT
    )

    table_answer_plot = answer_factory(
        question=plot_question, document=be_instance.case.document
    )

    table_form_plot = caluma_form_factories.FormFactory(slug="parzelle-tabelle")

    plot_row = caluma_form_factories.DocumentFactory(form=table_form_plot)

    table_answer_plot.documents.add(plot_row)

    plot_number_question = question_factory(
        slug="parzellennummer", type=caluma_form_models.Question.TYPE_CHOICE
    )
    e_grid_number_question = question_factory(
        slug="e-grid-nr", type=caluma_form_models.Question.TYPE_CHOICE
    )

    answer_factory(
        question=plot_number_question,
        value="123456789",
        document=plot_row,
    )
    answer_factory(
        question=e_grid_number_question,
        value="CH123456789",
        document=plot_row,
    )

    # Applicant questions and answers
    applicant_question = caluma_form_models.Question.objects.get(
        slug="personalien-gesuchstellerin"
    )

    table_answer_applicant = answer_factory(
        question=applicant_question, document=be_instance.case.document
    )

    table_form_applicant = caluma_form_models.Form.objects.get(
        slug="personalien-tabelle"
    )

    applicant_row = caluma_form_factories.DocumentFactory(form=table_form_applicant)

    table_answer_applicant.documents.add(applicant_row)

    answer_factory(
        question_id="vorname-gesuchstellerin",
        value="Max",
        document=applicant_row,
    )
    answer_factory(
        question_id="name-gesuchstellerin",
        value="Muster",
        document=applicant_row,
    )
    answer_factory(
        question__slug="juristische-person-gesuchstellerin",
        value="juristische-person-gesuchstellerin-ja",
        document=applicant_row,
    )

    # This should never trigger more than 4 queries on the DB:
    # 1. Query for fetching case
    # 2. Query for prefetching direct answers on case.document
    # 3. Query for prefetching row documents
    # 4. Query for prefetching answer on previously prefetched row documents
    with django_assert_num_queries(5):
        case = (
            Case.objects.filter(pk=be_instance.case.pk)
            .select_related("document")
            .prefetch_related(
                "document__answers",
                "document__answers__documents__answers",
                "document__dynamicoption_set",
            )
            .first()
        )

        master_data = MasterData(case)

        assert master_data.proposal == "Grosses Haus"
        assert master_data.construction_costs is None
        assert master_data.ebau_number == "2021-1"
        assert master_data.personal_data == [
            {
                "country": None,
                "first_name": "Max",
                "last_name": "Muster",
                "is_juristic_person": True,
            },
        ]
        assert master_data.plot_data == [
            {"plot_number": "123456789", "e_grid_number": "CH123456789"}
        ]
        assert master_data.submit_date == "2021-03-31T13:17:08+0000"
        assert master_data.paper_submit_date == "2021-03-20T13:17:08+0000"
        with override("de"):
            assert master_data.municipality == {
                "label": "Bern",
                "slug": "1",
            }
        with override("fr"):
            assert master_data.municipality == {
                "label": "Berne",
                "slug": "1",
            }

        with pytest.raises(AttributeError) as e:
            assert master_data.unconfigured_property

        assert (
            str(e.value)
            == "Key 'unconfigured_property' is not configured in master data config"
        )

        with pytest.raises(AttributeError) as e:
            assert master_data.unconfigured_resolver

        assert (
            str(e.value)
            == "Resolver 'unconfigured' used in key 'unconfigured_resolver' is not defined in master data class"
        )
