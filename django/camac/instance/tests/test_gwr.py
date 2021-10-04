import functools

import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from camac.core.factories import WorkflowEntryFactory, WorkflowItemFactory


def test_gwr_data_ur(
    admin_client,
    user,
    instance,
    use_caluma_form,
    ur_instance,
    caluma_forms_ur,
    caluma_admin_user,
    application_settings,
    workflow_item_factory,
    workflow_entry_factory,
    question_factory,
    answer_factory,
    form_factory,
    location_factory,
    snapshot,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_uri"]["MASTER_DATA"]

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

    # Municipality
    caluma_form_factories.AnswerFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        value="1",
    )
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
        question__type=caluma_form_models.Question.TYPE_CHOICE,
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
        value=123456789,
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
        value=123,
        document=applicant_row,
    )
    caluma_form_factories.AnswerFactory(
        question__slug="zip",
        value=1233,
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
        value="category-hochbaute",
        document=ur_instance.case.document,
    )

    # WorkflowEntry
    WorkflowEntryFactory(
        instance=ur_instance,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
        workflow_item=WorkflowItemFactory(workflow_item_id=12),
    )

    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("has_client", [True, False])
def test_instance_gwr_data_sz(
    admin_client,
    user,
    sz_instance,
    application_settings,
    form_field_factory,
    has_client,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_schwyz"][
        "MASTER_DATA"
    ]
    url = reverse("instance-gwr-data", args=[sz_instance.pk])

    add_field = functools.partial(form_field_factory, instance=sz_instance)
    add_field(name="bezeichnung", value="Bezeichnung")
    if has_client:
        add_field(
            name="bauherrschaft",
            value=[
                {
                    "name": "Muster",
                    "vorname": "Hans",
                    "ort": "Musterhausen",
                    "plz": 1234,
                    "strasse": "Musterstrasse",
                }
            ],
        )

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["constructionProjectDescription"] == "Bezeichnung"
    assert data["totalCostsOfProject"] is None

    if has_client:
        assert data["client"]["address"]["town"] == "Musterhausen"
        assert (
            data["client"]["identification"]["personIdentification"]["officialName"]
            == "Muster"
        )
    else:
        assert data["client"] is None
