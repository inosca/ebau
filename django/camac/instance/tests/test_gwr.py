import functools

import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from django.urls import reverse
from rest_framework import status


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
    case = ur_instance.case
    case.meta["dossier-number"] = "1200-00-00"
    case.save()

    workitem = case.work_items.first()
    workitem.closed_at = "2021-07-15 08:00:06+00"
    workitem.save()

    workflow_entry = workflow_entry_factory(
        instance=instance,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
    )

    application_settings["GWR_DATA"] = {
        "typeOfConstructionProject": (
            "answer",
            "category",
            {
                "category-hochbaute": 6011,
            },
        ),
        "officialConstructionProjectFileNo": ("case_meta", "dossier-number"),
        "client": (
            "applicant",
            "applicant",
            {
                "identification_isOrganisation": (
                    "is-juristic-person",
                    {
                        "is-juristic-person-no": False,
                        "is-juristic-person-yes": True,
                    },
                ),
            },
        ),
        "constructionLocalisation_municipalityName": ("location", "municipality"),
        "projectAnnouncementDate": (
            "submit_date_from_workflow_entry",
            [12, workflow_entry.workflow_item.pk],
        ),
        "realestateIdentification_number": ("submit_date_from_task", "placeholder"),
        "totalCostsOfProject": ("submit_date_from_workflow_entry", [12]),
        "constructionProjectDescription": (
            "answer",
            [
                "proposal-description",
                "beschreibung-zu-mbv",
                "bezeichnung",
                "vorhaben-proposal-description",
                "veranstaltung-beschrieb",
            ],
        ),
        "realestateIdentification_EGRID": ("answer", "parcels.e-grid"),
        "typeOfConstruction": ("location", "unanswered"),
    }

    category_question = question_factory(
        slug="category", type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
    )
    question_factory(slug="unanswered", type=caluma_form_models.Question.TYPE_TEXT)

    description_question = question_factory(
        slug="proposal-description", type=caluma_form_models.Question.TYPE_TEXT
    )
    answer_factory(
        question=category_question, document=case.document, value=["category-hochbaute"]
    )
    answer_factory(
        question=description_question, document=case.document, value="Neues Haus"
    )
    location = location_factory(name="Musterhausen")
    answer_factory(
        question_id="municipality", document=case.document, value=location.pk
    )

    applicant_question = question_factory(
        slug="applicant", type=caluma_form_models.Question.TYPE_TABLE
    )
    parcel_question = question_factory(
        slug="parcels", type=caluma_form_models.Question.TYPE_TABLE
    )

    table_answer_applicant = answer_factory(
        question=applicant_question, document=case.document
    )
    table_answer_parcel = answer_factory(
        question=parcel_question, document=case.document
    )

    table_form_applicant = caluma_form_factories.FormFactory(slug="personal-data-table")
    table_form_parcel = caluma_form_factories.FormFactory(slug="parcel-table")

    applicant_row = caluma_form_factories.DocumentFactory(form=table_form_applicant)
    parcel_row = caluma_form_factories.DocumentFactory(form=table_form_parcel)

    table_answer_applicant.documents.add(applicant_row)
    table_answer_parcel.documents.add(parcel_row)

    is_organisation_question = question_factory(
        slug="is-juristic-person", type=caluma_form_models.Question.TYPE_CHOICE
    )
    egrid_nr_question = question_factory(
        slug="e-grid", type=caluma_form_models.Question.TYPE_TEXT
    )
    answer_factory(
        question=is_organisation_question,
        value="is-juristic-person-yes",
        document=applicant_row,
    )
    answer_factory(question=egrid_nr_question, value="12345", document=parcel_row)
    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("has_client", [True, False])
def test_instance_gwr_data_sz(
    admin_client,
    user,
    instance,
    form_field_factory,
    django_assert_num_queries,
    has_client,
):
    url = reverse("instance-gwr-data", args=[instance.pk])

    add_field = functools.partial(form_field_factory, instance=instance)
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
