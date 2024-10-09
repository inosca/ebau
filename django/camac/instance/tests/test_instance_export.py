import datetime
import pathlib

import pyexcel
import pytest
from caluma.caluma_form import api as form_api, models as caluma_form_models
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status

from camac.instance.export.views import InstanceExportView
from camac.instance.models import Instance


@pytest.mark.parametrize(
    "role__name,method,has_access,expected_count",
    [
        ("Municipality", "get_queryset_for_municipality", True, 1),
        ("Service", "get_queryset_for_service", True, 1),
        ("Applicant", "_get_queryset_for_applicant", True, 0),
        ("Public", "get_queryset_for_public", True, 0),
        ("Municipality", "get_queryset_for_municipality", False, 0),
        ("Service", "get_queryset_for_service", False, 0),
        ("Applicant", "_get_queryset_for_applicant", False, 0),
        ("Public", "get_queryset_for_public", False, 0),
    ],
)
def test_caluma_export_visibilities(
    db,
    admin_client,
    instance,
    mocker,
    role,
    group,
    method,
    has_access,
    expected_count,
):
    is_public = role.name == "Public"
    mocker.patch(
        "camac.user.permissions.get_group", return_value=None if is_public else group
    )
    mocker.patch(
        f"camac.instance.mixins.InstanceQuerysetMixin.{method}",
        return_value=Instance.objects.filter(pk=instance.pk)
        if has_access
        else Instance.objects.none(),
    )

    view = InstanceExportView()
    assert view.get_queryset().count() == expected_count
    if expected_count:
        assert instance in view.get_queryset()


@pytest.mark.parametrize(
    "role__name,expected_status,expected_count,expected_num_queries",
    [
        ("Municipality", status.HTTP_200_OK, 1, 3),
        ("Service", status.HTTP_200_OK, 0, 3),
        ("Applicant", status.HTTP_200_OK, 0, 1),
        ("Public", status.HTTP_403_FORBIDDEN, 0, 0),
    ],
)
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
    role,
    expected_status,
    expected_count,
    expected_num_queries,
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
        caluma_form_models.Question.objects.get(pk="e-mail-gesuchstellerin"),
        row_doc,
        value="foo@bar.ch",
    )

    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="personalien-gesuchstellerin"),
        be_instance.case.document,
        value=[str(row_doc.pk)],
    )

    url = reverse("instance-export")

    with django_assert_num_queries(expected_num_queries):
        if role.name == "Public":
            response = admin_client.get(
                url, {"instance_id": be_instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
            )
        else:
            response = admin_client.get(url, {"instance_id": be_instance.pk})

    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
        assert len(book.get_dict()["pyexcel sheet"]) - 1 == expected_count
        if expected_count:
            assert be_instance.pk in book.get_dict()["pyexcel sheet"][1]


@pytest.mark.parametrize(
    "service__name,role__name,expected_status,expected_count,expected_num_queries",
    [
        ("Gemeinde Schwyz", "Municipality", status.HTTP_200_OK, 1, 3),
        ("Gemeinde Schwyz", "Service", status.HTTP_200_OK, 1, 3),
        (None, "Applicant", status.HTTP_200_OK, 0, 1),
        (None, "Public", status.HTTP_403_FORBIDDEN, 0, 0),
    ],
)
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
    role,
    expected_status,
    expected_count,
    expected_num_queries,
    settings,
    sz_distribution_settings,
    django_assert_num_queries,
    utils,
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
    utils.add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        make_aware(datetime.datetime(2023, 4, 1)),
    )
    utils.add_answer(
        work_item.document,
        "bewilligungsverfahren-datum-gesamtentscheid",
        make_aware(datetime.datetime(2023, 4, 3)),
    )

    url = reverse("instance-export")

    with django_assert_num_queries(expected_num_queries):
        if role.name == "Public":
            response = admin_client.get(
                url, {"instance_id": sz_instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
            )
        else:
            response = admin_client.get(url, {"instance_id": sz_instance.pk})

    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
        assert len(book.get_dict()["pyexcel sheet"]) - 1 == expected_count
        if expected_count:
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
