import pathlib

import pyexcel
import pytest
from caluma.caluma_form import api as form_api, models as caluma_form_models
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("service__name", ["Leitbehörde Burgdorf"])
@pytest.mark.parametrize(
    "is_multilingual",
    [
        False,
        # TODO: True,
    ],
)
def test_caluma_export_be(
    db,
    admin_client,
    be_instance,
    instance_service_factory,
    service,
    application_settings,
    settings,
    django_assert_num_queries,
    is_multilingual,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )
    application_settings["IS_MULTILINGUAL"] = is_multilingual

    instance_service_factory(
        instance=be_instance, service=admin_client.user.groups.first().service
    )

    be_instance.case.document.answers.create(
        value=str(service.pk), question_id="gemeinde"
    )

    row_doc = form_api.save_document(
        caluma_form_models.Form.objects.get(pk="personalien-tabelle")
    )
    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="vorname-gesuchstellerin"),
        row_doc,
        value="Max",
    )
    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="name-gesuchstellerin"),
        row_doc,
        value="Muster",
    )

    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="personalien-gesuchstellerin"),
        be_instance.case.document,
        value=[str(row_doc.pk)],
    )

    url = reverse("instance-export")

    with django_assert_num_queries(2):
        response = admin_client.get(url, {"instance_id": be_instance.pk})

    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    assert be_instance.pk in book.get_dict()["pyexcel sheet"][1]


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("service__name", ["Leitbehörde Schwyz"])
def test_caluma_export_sz(
    db,
    admin_client,
    sz_instance,
    service,
    settings,
    sz_distribution_settings,
    django_assert_num_queries,
):
    settings.APPLICATION_NAME = "kt_schwyz"
    sz_instance.identifier = "123-45-77"
    sz_instance.save()

    # TODO: Update test to reflect exported data

    url = reverse("instance-export")

    with django_assert_num_queries(2):
        response = admin_client.get(url, {"instance_id": sz_instance.pk})

    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    assert sz_instance.identifier in book.get_dict()["pyexcel sheet"][1]


@pytest.mark.parametrize(
    "query",
    [
        {},
        {"foo": "bar"},
        {"instance_id": ""},
        {"instance_id": ",".join(str(i) for i in range(10000, 11001))},
    ],
)
def test_caluma_export_bad_request(admin_client, query):
    url = reverse("instance-export")
    resp = admin_client.get(url, query)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
