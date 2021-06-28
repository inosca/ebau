import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from ..gwr_lookups import get_submit_date


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_instance_caluma_gwr_data_be(
    admin_client,
    user,
    instance,
    use_caluma_form,
    caluma_workflow_config_be,
    caluma_forms_be,
    caluma_admin_user,
    application_settings,
    workflow_item_factory,
    workflow_entry_factory,
    gwr_config_be,
    question_factory,
):

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )
    workitem = case.work_items.get(task_id="submit")
    workitem.closed_at = "2021-07-15 08:00:06+00"
    workitem.save()

    building_cost_question = caluma_form_models.Question.objects.create(
        slug="baukosten-in-chf", type=caluma_form_models.Question.TYPE_INTEGER
    )
    case.document.answers.create(question=building_cost_question, value="1200")
    case.document.answers.create(
        question_id="beschreibung-bauvorhaben", value="Bezeichnung"
    )
    table_answer = case.document.answers.create(
        question_id="personalien-gesuchstellerin"
    )
    row = caluma_form_factories.DocumentFactory(form_id="personalien-tabelle")
    table_answer.documents.add(row)
    zip_question = caluma_form_models.Question.objects.create(
        slug="plz-gesuchstellerin", type=caluma_form_models.Question.TYPE_INTEGER
    )
    city_question = caluma_form_models.Question.objects.create(
        slug="ort-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )
    street_question = caluma_form_models.Question.objects.create(
        slug="strasse-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )
    row.answers.create(question=city_question, value="Musterhausen")
    row.answers.create(question=zip_question, value=1234)
    row.answers.create(question=street_question, value="Musterstrasse")
    row.answers.create(question_id="name-gesuchstellerin", value="Muster")
    row.answers.create(question_id="vorname-gesuchstellerin", value="Max")

    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["constructionProjectDescription"] == "Bezeichnung"
    assert data["constructionLocalisation"]["municipalityName"] is None
    assert data["client"]["address"]["town"] == "Musterhausen"
    assert data["client"]["address"]["houseNumber"] is None
    assert data["client"]["address"]["country"] is None
    assert data["client"]["identification"]["isOrganisation"] == [None]
    assert (
        data["client"]["identification"]["organisationIdentification"][
            "organisationName"
        ]
        is None
    )
    assert (
        data["client"]["identification"]["personIdentification"]["officialName"]
        == "Muster"
    )
    assert data["typeOfConstructionProject"] is None
    assert data["officialConstructionProjectFileNo"] is None
    assert data["realestateIdentification"]["EGRID"] is None
    assert data["realestateIdentification"]["number"] is None
    assert data["projectAnnouncementDate"] == "2021-07-15T08:00:06Z"


def test_instance_caluma_gwr_data_ur(
    admin_client,
    user,
    instance,
    use_caluma_form,
    caluma_workflow_config_ur,
    caluma_forms_ur,
    caluma_admin_user,
    application_settings,
    workflow_item_factory,
    workflow_entry_factory,
    question_factory,
    location_factory,
):
    application_settings["GWR"]["ANSWER_SLUGS"] = {
        "typeOfConstructionProject": "category",
        "client_identification_isOrganisation": "is-juristic-person",
        "constructionLocalisation_municipalityName": "municipality",
    }
    application_settings["GWR"]["ANSWER_MAPPING"] = {
        "category-hochbaute": 6011,
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk, "dossier-number": "1200-00-00"},
        user=caluma_admin_user,
    )

    category_question = caluma_form_models.Question.objects.create(
        slug="category", type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
    )
    case.document.answers.create(
        question=category_question, value=["category-hochbaute"]
    )
    location_factory(pk=1, name="Musterhausen")
    case.document.answers.create(question_id="municipality", value=1)
    applicant_question = caluma_form_models.Question.objects.create(
        slug="applicant", type=caluma_form_models.Question.TYPE_TABLE
    )

    table_answer = case.document.answers.create(question=applicant_question)
    table_form = caluma_form_models.Form.objects.create(slug="personal-data-table")
    row = caluma_form_factories.DocumentFactory(form=table_form)
    table_answer.documents.add(row)
    is_organisation_question = caluma_form_models.Question.objects.create(
        slug="is-juristic-person", type=caluma_form_models.Question.TYPE_CHOICE
    )
    row.answers.create(
        question=is_organisation_question, value="is-juristic-person-yes"
    )
    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["typeOfConstructionProject"] == 6011
    assert data["constructionLocalisation"]["municipalityName"] == "Musterhausen"
    assert data["officialConstructionProjectFileNo"] == "1200-00-00"


def test_gwr_lookups_submit_date(
    caluma_admin_user,
    instance,
    gwr_config_ur,
    workflow_entry_factory,
    workflow_item_factory,
    caluma_workflow_config_ur,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk, "dossier-number": "1200-00-000"},
        user=caluma_admin_user,
    )
    workflow_item_factory(pk=10, name="Dossiereingang")
    workflow_entry_factory(
        instance=instance,
        workflow_item_id=10,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
    )

    answer_slugs = settings.APPLICATION["GWR"].get("ANSWER_SLUGS", {})

    assert get_submit_date(instance.pk, case, answer_slugs) == "2021-07-16"
