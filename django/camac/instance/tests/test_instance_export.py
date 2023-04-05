import datetime
import pathlib

import pyexcel
import pytest
from caluma.caluma_form import api as form_api, models as caluma_form_models
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status

from .test_master_data import add_answer


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
@pytest.mark.parametrize("service__name", ["Gemeinde Schwyz"])
@pytest.mark.parametrize("has_overrides", [False, True])
def test_caluma_export_sz(
    db,
    admin_client,
    sz_instance,
    form,
    location,
    instance_state_factory,
    form_field_factory,
    workflow_entry_factory,
    workflow_item_factory,
    form_factory,
    location_factory,
    work_item_factory,
    document_factory,
    snapshot,
    has_overrides,
    settings,
    sz_distribution_settings,
    django_assert_num_queries,
):
    settings.APPLICATION_NAME = "kt_schwyz"
    settings.SHORT_DATE_FORMAT = "%d.%m.%Y"
    sz_instance.identifier = "123-45-77"
    sz_instance.form = form_factory(description="Test form")
    sz_instance.location = location_factory(name="Test location")
    sz_instance.instance_state = instance_state_factory(
        description="Test instance state"
    )
    sz_instance.save()

    workflow_entry_factory(
        workflow_item=workflow_item_factory(pk=10),
        workflow_date=make_aware(datetime.datetime(2023, 3, 3)),
        instance=sz_instance,
    )

    form_field_factory(
        name="bauherrschaft-v3",
        value=[
            {
                "vorname": "Yellow",
                "firma": "Smoothie-licious Inc.",
                "name": "Banana",
                "plz": 8670,
            },
            {
                "vorname": "Red",
                "name": "Apple",
                "plz": 8670,
            },
        ],
        instance=sz_instance,
    )

    form_field_factory(
        name="bezeichnung",
        value="Test intent",
        instance=sz_instance,
    )

    form_field_factory(
        name="standort-ort",
        value="Test location",
        instance=sz_instance,
    )

    if has_overrides:
        form_field_factory(
            name="bauherrschaft-override",
            value=[
                {
                    "vorname": "Yellow",
                    "firma": "Smoothie-not-so-licious Inc.",
                    "name": "Banana",
                    "plz": 8670,
                },
                {
                    "vorname": "Red",
                    "name": "Apple",
                    "plz": 8670,
                },
            ],
            instance=sz_instance,
        )

        form_field_factory(
            name="bezeichnung-override",
            value="Test intent override",
            instance=sz_instance,
        )

        form_field_factory(
            name="ortsbezeichnung-des-vorhabens",
            value="Test address",
            instance=sz_instance,
        )

        form_field_factory(
            name="standort-spezialbezeichnung",
            value="Test special name",
            instance=sz_instance,
        )

    work_item = work_item_factory(task_id="building-authority", case=sz_instance.case)
    work_item.document = document_factory(form_id="bauverwaltung")
    work_item.save()
    add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        make_aware(datetime.datetime(2023, 4, 1)),
    )
    add_answer(
        work_item.document,
        "bewilligungsverfahren-datum-gesamtentscheid",
        make_aware(datetime.datetime(2023, 4, 3)),
    )

    url = reverse("instance-export")

    with django_assert_num_queries(2):
        response = admin_client.get(url, {"instance_id": sz_instance.pk})

    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    data = book.get_dict()["pyexcel sheet"][1]
    assert sz_instance.identifier in data

    snapshot.assert_match(data)


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
