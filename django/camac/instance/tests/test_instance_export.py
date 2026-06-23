import datetime
import pathlib

import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import status

from camac.conftest import parse_xlsx_response
from camac.instance.export.views import (
    BabStatisticsExportView,
    InstanceExportView,
    generate_bab_statistics_export_file,
)
from camac.instance.models import Instance
from camac.tests.form_utils import FormUtils


@pytest.fixture
def data_for_bab_statistics_export(
    ur_instance,
    form_utils: FormUtils,
    service,
    ur_work_item_list_settings,
    ur_distribution_settings,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_form_factory,
):
    ur_instance.case.meta["dossier-number"] = "1201-01-123"
    ur_instance.case.save()

    ur_instance.case.document.form.name = "Baugesuch"
    ur_instance.case.document.form.save()

    caluma_work_item_factory(
        task_id="init-distribution",
        case=ur_instance.case,
        status=WorkItem.STATUS_COMPLETED,
        closed_at=timezone.make_aware(datetime.datetime(2025, 6, 16, 0, 0)),
    )

    bab_work_item = caluma_work_item_factory(
        task_id="bab",
        case=ur_instance.case,
        document=caluma_document_factory(form=Form.objects.get(slug="bab")),
    )

    caluma_form_factory(slug="bab-lage-flaechenbedarf-form")
    caluma_form_factory(slug="bab-versiegelte-entsiegelte-flaechen-form")

    # instance answers
    form_utils.add_municipality(ur_instance.case.document, "municipality", service)
    form_utils.add_table_answer(
        ur_instance.case.document,
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
    form_utils.add_answer(
        ur_instance.case.document, "proposal-description", "Einfamilienhaus"
    )

    # bab answers
    form_utils.add_answer(
        bab_work_item.document,
        "bab-art-der-massnahme",
        "bab-art-der-massnahme-neubau",
        "Neubau",
    )
    form_utils.add_answer(
        bab_work_item.document,
        "beschrieb-der-massnahme",
        "Beschrieb der Massnahme",
    )
    form_utils.add_answer(
        bab_work_item.document, "bab-objektart", "bab-objektart-wohnbaute", "Wohnbaute"
    )
    form_utils.add_answer(bab_work_item.document, "objektbeschrieb", "Objektbeschrieb")
    form_utils.add_answer(
        bab_work_item.document,
        "bab-nutzung-nach-rpg",
        "bab-nutzung-nach-rpg-zonenkonform",
        "Zonenkonform",
    )
    form_utils.add_answer(
        bab_work_item.document,
        "bab-bewilligungsgrund",
        "bab-bewilligungsgrund-innerhalb-bauzone",
        "Innerhalb Bauzone",
    )
    form_utils.add_answer(
        bab_work_item.document, "bab-entscheid", "bab-entscheid-positiv", "Positiv"
    )
    form_utils.add_answer(
        bab_work_item.document,
        "bab-typ-der-auftraggeber",
        "bab-typ-der-auftraggeber-privatpersonen",
        "Privatpersonen",
    )
    form_utils.add_table_answer(
        bab_work_item.document,
        "bab-lage-flaechenbedarf-tabelle",
        [
            {
                "bab-grundnutzung": {
                    "value": "bab-grundnutzung-landwirtschaftszone",
                    "options": [
                        ("bab-grundnutzung-landwirtschaftszone", "Landwirtschaftszone")
                    ],
                },
                "bab-flaechenbedarf-grundnutzung": 1000,
            }
        ],
        row_form_id="bab-lage-flaechenbedarf-form",
    )
    form_utils.add_answer(
        bab_work_item.document, "bab-flaechenbedarf-fruchtfolgeflaechen", 10
    )
    form_utils.add_answer(
        bab_work_item.document, "bab-kompensation-fruchtfolgeflaechen", 20
    )
    form_utils.add_answer(bab_work_item.document, "bab-neue-gebaeude", 3)
    form_utils.add_answer(bab_work_item.document, "bab-gebaeude-abbruch", 1)
    form_utils.add_answer(bab_work_item.document, "anzahl-gebaeude-unter-schutz", 2)
    form_utils.add_answer(
        bab_work_item.document,
        "versiegelt-oder-entsiegelt",
        "versiegelt-oder-entsiegelt-ja",
        "Ja",
    )
    form_utils.add_table_answer(
        bab_work_item.document,
        "versiegelte-entsiegelte-flaechen",
        [
            {
                "bab-art-versiegelung": {
                    "value": "bab-art-versiegelung-neu-versiegelt-gebaeude",
                    "options": [
                        (
                            "bab-art-versiegelung-neu-versiegelt-gebaeude",
                            "Neu versiegelte Gebäude",
                        )
                    ],
                },
                "bab-versiegelung-flaeche": 300,
                "bab-nutzung-versiegelte-flaeche": {
                    "value": "bab-nutzung-versiegelte-flaeche-andere",
                    "options": [("bab-nutzung-versiegelte-flaeche-andere", "Andere")],
                },
                "soemmerungsgebiet": {
                    "value": "soemmerungsgebiet-ja",
                    "options": [("soemmerungsgebiet-ja", "Ja")],
                },
                "bab-beschreibung-nutzung-flaeche-andere": {
                    "value": "bab-beschreibung-nutzung-flaeche-andere",
                    "options": [
                        (
                            "bab-beschreibung-nutzung-flaeche-andere",
                            "Beschreibung andere",
                        )
                    ],
                },
            }
        ],
        row_form_id="bab-versiegelte-entsiegelte-flaechen-form",
    )


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
@pytest.mark.django_db
def test_caluma_export_visibilities(
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
        ("Service", status.HTTP_200_OK, 1, 3),
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
@pytest.mark.django_db
def test_caluma_export_be(
    admin_client,
    be_instance,
    instance_service_factory,
    caluma_question_factory,
    instance_state_t_factory,
    responsible_service_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    active_inquiry_factory,
    caluma_forms_be,
    be_master_data_case,
    service,
    application_settings,
    settings,
    django_assert_num_queries,
    is_multilingual,
    role,
    expected_status,
    expected_count,
    expected_num_queries,
    snapshot,
    form_utils: FormUtils,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )
    application_settings["IS_MULTILINGUAL"] = is_multilingual

    # Ebau number
    be_instance.case.meta["ebau-number"] = "2025-1"
    be_instance.case.save()

    # Instance state
    be_instance.instance_state = instance_state_t_factory(
        name="In Zirkulation"
    ).instance_state
    be_instance.save()

    instance_service_factory(
        instance=be_instance, service=admin_client.user.groups.first().service
    )

    responsible_service_factory(
        responsible_user__name="John",
        responsible_user__surname="Doe",
        service=service,
        instance=be_instance,
    )

    # Decision date
    decision_work_item = caluma_work_item_factory(
        case=be_instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="decision"),
    )
    form_utils.add_answer(
        decision_work_item.document,
        "decision-date",
        datetime.date(2025, 5, 8),
    )

    # Inquiry
    active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2025, 1, 1)),
        closed_at=make_aware(datetime.datetime(2025, 1, 30)),
    )

    # Fill some interesting stuff in the form (BE:EBAU-1240)
    be_instance.case.document.answers.update_or_create(
        question_id="beschreibung-bauvorhaben",
        defaults={
            "value": "first page\fsecond page",
        },
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
        book = parse_xlsx_response(response)
        assert len(book.get_dict()["pyexcel sheet"]) - 1 == expected_count
        if expected_count:
            # Remove instance id from snapshot since it is always generated new
            del book.get_dict()["pyexcel sheet"][1][1]
            book.get_dict()["pyexcel sheet"][0].remove("Dossier-Nr.")

            data = book.get_dict()["pyexcel sheet"][1]
            snapshot.assert_match(data)


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
@pytest.mark.django_db
def test_caluma_export_sz(
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
    caluma_work_item_factory,
    caluma_document_factory,
    snapshot,
    has_overrides,
    role,
    expected_status,
    expected_count,
    expected_num_queries,
    settings,
    sz_distribution_settings,
    django_assert_num_queries,
    form_utils: FormUtils,
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
        value='Test "intent"',
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

    work_item = caluma_work_item_factory(
        task_id="building-authority", case=sz_instance.case
    )
    work_item.document = caluma_document_factory(form_id="bauverwaltung")
    work_item.save()
    form_utils.add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        make_aware(datetime.datetime(2023, 4, 1)),
    )
    form_utils.add_answer(
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
        book = parse_xlsx_response(response)
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


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.django_db
def test_caluma_export_ag(
    admin_client,
    ag_distribution_settings,
    ag_master_data_case,
    caluma_document_factory,
    caluma_work_item_factory,
    django_assert_num_queries,
    instance_state_t_factory,
    multilang,
    responsible_service_factory,
    service,
    settings,
    snapshot,
    form_utils: FormUtils,
    active_inquiry_factory,
):
    settings.APPLICATION_NAME = "kt_ag"

    # Instance state
    instance = ag_master_data_case.instance
    instance.instance_state = instance_state_t_factory(
        name="In Zirkulation"
    ).instance_state
    instance.save()

    # Responsible user
    responsible_service_factory(
        responsible_user__name="John",
        responsible_user__surname="Doe",
        service=service,
        instance=instance,
    )

    # Decision date
    decision_work_item = caluma_work_item_factory(
        case=instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="entscheid"),
    )
    form_utils.add_answer(
        decision_work_item.document,
        "entscheid-datum",
        datetime.date(2025, 5, 8),
    )

    # Inquiry
    active_inquiry_factory(
        for_instance=instance,
        addressed_service=service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2025, 1, 1)),
        closed_at=make_aware(datetime.datetime(2025, 1, 30)),
    )

    with django_assert_num_queries(3):
        response = admin_client.get(
            reverse("instance-export"), {"instance_id": instance.pk}
        )

    assert response.status_code == status.HTTP_200_OK

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["pyexcel sheet"]
    row = sheet[1]

    assert len(sheet) == 2  # one instance plus header row
    assert len(row) == 14  # number of expected columns

    assert ag_master_data_case.meta["dossier-number"] in row
    assert row == snapshot


@pytest.mark.parametrize("service__name", ["Altdorf"])
@pytest.mark.django_db
def test_bab_statistics_export_file(
    admin_client,
    ur_instance,
    data_for_bab_statistics_export,
):
    start_date = "2025-01-01T00:00:00Z"
    end_date = "2026-01-01T00:00:00Z"
    _, data = generate_bab_statistics_export_file(start_date, end_date)
    assert len(data) == 2
    data.sort()
    assert data[0] == [
        "Altdorf",
        "ACME AG, Max Mustermann, Teststrasse 123, 1233 Musterdorf",
        "Einfamilienhaus",
        "1201-01-123",
        str(ur_instance.pk),
        "Baugesuch",
        "Neubau",
        "Wohnbaute",
        "Objektbeschrieb",
        "Zonenkonform",
        "Innerhalb Bauzone",
        "Positiv",
        "Privatpersonen",
        "-",
        "-",
        "10",
        "20",
        "3",
        "1",
        "2",
        "Ja",
        "Neu versiegelte Gebäude",
        "300",
        "Andere",
        "Ja",
    ]
    assert data[1] == [
        "Altdorf",
        "ACME AG, Max Mustermann, Teststrasse 123, 1233 Musterdorf",
        "Einfamilienhaus",
        "1201-01-123",
        str(ur_instance.pk),
        "Baugesuch",
        "Neubau",
        "Wohnbaute",
        "Objektbeschrieb",
        "Zonenkonform",
        "Innerhalb Bauzone",
        "Positiv",
        "Privatpersonen",
        "Landwirtschaftszone",
        "1000",
        "10",
        "20",
        "3",
        "1",
        "2",
        "Ja",
        "-",
        "-",
        "-",
        "-",
    ]


@pytest.mark.django_db
def test_bab_statistics_request(
    admin_client,
    data_for_bab_statistics_export,
):
    start_date = "2024-01-01T00:00:00Z"
    end_date = "2026-01-01T00:00:00Z"
    url = reverse("bab-statistics-export")
    response = admin_client.post(
        url, data={"data": "instances", "from": start_date, "to": end_date}
    )

    assert response.status_code == status.HTTP_200_OK

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["pyexcel sheet"]
    row = sheet[1]

    assert len(sheet) == 3  # two instance because of two table rows plus header row
    assert len(row) == 25  # number of expected columns


@pytest.mark.parametrize(
    "role__name,method,has_access,expected_count",
    [
        ("Municipality", "get_queryset_for_municipality", False, 0),
        ("Service", "get_queryset_for_service", True, 1),
        ("Applicant", "_get_queryset_for_applicant", False, 0),
        ("Public", "get_queryset_for_public", False, 0),
        ("Municipality", "get_queryset_for_municipality", False, 0),
        ("Applicant", "_get_queryset_for_applicant", False, 0),
        ("Public", "get_queryset_for_public", False, 0),
    ],
)
@pytest.mark.django_db
def test_bab_statistics_export_visibility(
    method, has_access, expected_count, mocker, role, group, instance
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

    view = BabStatisticsExportView()
    assert view.get_queryset().count() == expected_count
    if expected_count:
        assert instance in view.get_queryset()


@pytest.mark.parametrize("role__name", [("Municipality")])
def test_caluma_export_gr(
    db,
    admin_client,
    gr_distribution_settings,
    gr_master_data_case,
    keyword_factory,
    caluma_document_factory,
    caluma_work_item_factory,
    django_assert_num_queries,
    instance_state_t_factory,
    multilang,
    responsible_service_factory,
    service,
    settings,
    snapshot,
    form_utils: FormUtils,
    active_inquiry_factory,
):
    settings.APPLICATION_NAME = "kt_gr"

    # Instance state
    instance = gr_master_data_case.instance
    instance.instance_state = instance_state_t_factory(
        name="In Zirkulation"
    ).instance_state
    instance.save()

    # Responsible user
    responsible_service_factory(
        responsible_user__name="John",
        responsible_user__surname="Doe",
        service=service,
        instance=instance,
    )

    # Form answers
    form_utils.add_answer(
        gr_master_data_case.document,
        "voraussichtlicher-baubeginn",
        datetime.date(2025, 5, day=5),
    )
    form_utils.add_answer(
        gr_master_data_case.document,
        "voraussichtliche-fertigstellung",
        datetime.date(2025, 5, day=15),
    )
    form_utils.add_answer(
        gr_master_data_case.document,
        "gis-map",
        '{"markers": [{"x": 2569941.12345, "y": 1298923.12345}], "center": {"x": 2609995.12345,"y": 1271340.12345} }',
    )

    # Keywords
    kw = keyword_factory(service=service)
    kw.instances.set([instance])
    kw.save()

    # Decision date
    decision_work_item = caluma_work_item_factory(
        case=instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="decision"),
    )
    form_utils.add_answer(
        decision_work_item.document,
        "decision-date",
        datetime.date(2025, 5, 8),
    )
    form_utils.add_answer(
        decision_work_item.document,
        "decision-decision",
        "decision-decision-approved",
        options=[("decision-decision-approved", "Bewilligt")],
    )

    # Inquiry
    active_inquiry_factory(
        for_instance=instance,
        addressed_service=service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2025, 1, 1)),
        closed_at=make_aware(datetime.datetime(2025, 1, 30)),
    )

    with django_assert_num_queries(3):
        response = admin_client.get(
            reverse("instance-export"), {"instance_id": instance.pk}
        )

    assert response.status_code == status.HTTP_200_OK

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["pyexcel sheet"]
    row = sheet[1]

    assert len(sheet) == 2  # one instance plus header row
    assert len(row) == 18  # number of expected columns

    assert gr_master_data_case.meta["dossier-number"] in row
    assert row == snapshot
