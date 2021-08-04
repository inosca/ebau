import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from rest_framework import status


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
    question_factory,
):

    application_settings["GWR"]["ANSWER_SLUGS"] = {
        "projectAnnouncementDate": ("submit_date_from_task", "submit"),
        "constructionProjectDescription": ("answer", None),
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )
    workitem = case.work_items.get(task_id="submit")
    workitem.closed_at = "2021-07-15 08:00:06+00"
    workitem.save()

    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["projectAnnouncementDate"] == "2021-07-15T08:00:06Z"
    assert data["constructionProjectDescription"] is None


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
        "typeOfConstructionProject": (
            "answer",
            "category",
            {
                "category-hochbaute": 6011,
            },
        ),
        "officialConstructionProjectFileNo": (
            "case_meta",
            "dossier-number",
        ),
        "client": (
            "client",
            "applicant",
            {
                "address_town": "city",
                "address_swissZipCode": "zip",
                "address_street": "street",
                "address_houseNumber": "street-number",
                "address_country": "country",
                "identification_personIdentification_officialName": "last-name",
                "identification_personIdentification_firstName": "first-name",
                "identification_isOrganisation": (
                    "is-juristic-person",
                    {
                        "is-juristic-person-no": False,
                        "is-juristic-person-yes": True,
                    },
                ),
                "identification_organisationIdentification_organisationName": "juristic-person-name",
            },
        ),
        "client_identification_isOrganisation": "is-juristic-person",
        "constructionLocalisation_municipalityName": ("location", "municipality"),
        "projectAnnouncementDate": ("submit_date_from_workflow", [10, 12]),
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
        "typeOfConstruction": (
            "location",
            None,
        ),
    }

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk, "dossier-number": "1200-00-00"},
        user=caluma_admin_user,
    )
    workflow_item_factory(pk=10, name="Dossiereingang")
    workflow_entry_factory(
        instance=instance,
        workflow_item_id=10,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
    )

    category_question = caluma_form_models.Question.objects.create(
        slug="category", type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
    )
    description_question = caluma_form_models.Question.objects.create(
        slug="proposal-description", type=caluma_form_models.Question.TYPE_TEXT
    )
    case.document.answers.create(
        question=category_question, value=["category-hochbaute"]
    )
    case.document.answers.create(question=description_question, value="Neues Haus")
    location_factory(pk=1, name="Musterhausen")
    case.document.answers.create(question_id="municipality", value=1)

    applicant_question = caluma_form_models.Question.objects.create(
        slug="applicant", type=caluma_form_models.Question.TYPE_TABLE
    )
    parcel_question = caluma_form_models.Question.objects.create(
        slug="parcels", type=caluma_form_models.Question.TYPE_TABLE
    )

    table_answer_applicant = case.document.answers.create(question=applicant_question)
    table_answer_parcel = case.document.answers.create(question=parcel_question)

    table_form_applicant = caluma_form_models.Form.objects.create(
        slug="personal-data-table"
    )
    table_form_parcel = caluma_form_models.Form.objects.create(slug="parcel-table")

    applicant_row = caluma_form_factories.DocumentFactory(form=table_form_applicant)
    parcel_row = caluma_form_factories.DocumentFactory(form=table_form_parcel)

    table_answer_applicant.documents.add(applicant_row)
    table_answer_parcel.documents.add(parcel_row)

    is_organisation_question = caluma_form_models.Question.objects.create(
        slug="is-juristic-person", type=caluma_form_models.Question.TYPE_CHOICE
    )
    egrid_nr_question = caluma_form_models.Question.objects.create(
        slug="e-grid", type=caluma_form_models.Question.TYPE_TEXT
    )

    applicant_row.answers.create(
        question=is_organisation_question, value="is-juristic-person-yes"
    )
    parcel_row.answers.create(question=egrid_nr_question, value="12345")
    url = reverse("instance-gwr-data", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["typeOfConstructionProject"] == 6011
    assert data["constructionLocalisation"]["municipalityName"] == "Musterhausen"
    assert data["officialConstructionProjectFileNo"] == "1200-00-00"
    assert data["client"]["identification"]["isOrganisation"] is True
    assert data["projectAnnouncementDate"] == "2021-07-16"
    assert data["constructionProjectDescription"] == "Neues Haus"
