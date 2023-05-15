from datetime import datetime
from pathlib import Path

import pytest
from caluma.caluma_form.models import DynamicOption
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _
from rest_framework import exceptions, status

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSHandler, DMSVisitor
from .test_master_data import add_answer, add_table_answer


@pytest.fixture
def caluma_form_fixture(db):
    kt_bern_path = Path(settings.ROOT_DIR) / "kt_bern"
    paths = [
        "config/user.json",
        "config/instance.json",
        "config/caluma_form_common.json",
        "config/caluma_dossier_import_form.json",
        "config/caluma_form.json",
        "config/caluma_form_v2.json",
        "config/caluma_form_v3.json",
        "config/caluma_form_sb2.json",
        "config/caluma_audit_form.json",
        "config/caluma_publication_form.json",
        "config/caluma_information_of_neighbors_form.json",
        "config/caluma_ebau_number_form.json",
        "config/caluma_solar_plants_form.json",
        "config/caluma_heat_generator_form.json",
        "config/caluma_decision_form.json",
        "config/caluma_distribution.json",
        "config/caluma_workflow.json",
        "config/caluma_legal_submission_form.json",
        "config/caluma_appeal_form.json",
        "data/caluma_form.json",
        "data/caluma_workflow.json",
        "data/user.json",
        "data/instance.json",
    ]

    call_command("loaddata", *[kt_bern_path / path for path in paths])


@pytest.fixture
def dms_settings(application_settings):
    application_settings["DOCUMENT_MERGE_SERVICE"] = settings.APPLICATIONS["kt_bern"][
        "DOCUMENT_MERGE_SERVICE"
    ]
    application_settings["DOCUMENT_MERGE_SERVICE"]["FORM"]["baugesuch"]["forms"].append(
        "main-form"
    )


@pytest.mark.freeze_time("2023-01-06 16:10")
def test_document_merge_service_snapshot(
    db,
    application_settings,
    caluma_form_fixture,
    django_assert_num_queries,
    dms_settings,
    service,
    snapshot,
):
    cache.clear()

    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    for snapshot_name, kwargs, expected_queries in [
        (
            "baugesuch",
            {"instance_id": 1},
            21,
        ),
        (
            "sb1",
            {"instance_id": 3, "form_slug": "sb1"},
            27,
        ),
        (
            "sb2",
            {"instance_id": 3, "form_slug": "sb2"},
            27,
        ),
        (
            "mp-form",
            {"instance_id": 3, "document_id": "da618b68-b4a8-414f-9d5e-50e0fda43cde"},
            25,
        ),
    ]:
        with django_assert_num_queries(expected_queries):
            handler = DMSHandler()
            instance, root_document = handler.get_instance_and_document(**kwargs)

            snapshot.assert_match(
                handler.get_meta_data(instance, root_document, service),
                f"{snapshot_name}_header",
            )

            visitor = DMSVisitor(root_document, instance, BaseUser())
            snapshot.assert_match(visitor.visit(root_document), snapshot_name)


def test_document_merge_service_is_valid(db, caluma_form_fixture, dms_settings):
    cache.clear()

    instance, root_document = DMSHandler().get_instance_and_document(instance_id=1)

    assert DMSVisitor(root_document, instance, BaseUser()).is_valid()

    root_document.answers.all().delete()

    assert not DMSVisitor(root_document, instance, BaseUser()).is_valid()


def test_document_merge_service_client(db, requests_mock):
    template = "some-template"
    expected = b"foo\nNot a pdf"

    requests_mock.register_uri(
        "POST",
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            f"/template/{template}/merge",
            trailing=True,
        ),
        content=expected,
    )

    client = DMSClient("some token")
    result = client.merge({"foo": "some data"}, template)

    assert result == expected


@pytest.mark.freeze_time("2022-09-06 13:37")
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_document_merge_service_cover_sheet_with_header_values(
    db,
    dms_settings,
    service_factory,
    tag_factory,
    be_instance,
    group,
    user_factory,
    snapshot,
    application_settings,
    master_data_is_visible_mock,
    freezer,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]
    be_instance.case.meta = {
        "camac-instance-id": be_instance.pk,
        "ebau-number": "2021-99",
        "submit-date": "2021-01-01",
        "paper-submit-date": "2021-01-02",
    }
    be_instance.case.save()

    municipality = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Burgdorf",
    )
    group.service = municipality
    group.save()

    # Prepare plot answer
    add_table_answer(
        be_instance.case.document,
        "parzelle",
        [
            {
                "parzellennummer": "123",
            },
            {
                # This should be excluded since no parcel number is given
                "egrid": "CH908035124647",
            },
        ],
    )

    # Prepare applicant answer
    add_table_answer(
        be_instance.case.document,
        "personalien-gesuchstellerin",
        [
            {
                "vorname-gesuchstellerin": "Foo",
                "name-gesuchstellerin": "Bar",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Test AG",
            }
        ],
    )

    # Prepare plot address
    add_answer(be_instance.case.document, "strasse-flurname", "Bahnhofstrasse")
    add_answer(be_instance.case.document, "nr", "2")
    add_answer(be_instance.case.document, "ort-grundstueck", "Testhausen")

    # Prepare tags
    tag_factory(name="some tag", instance=be_instance, service=municipality)

    # Prepare authority
    be_instance.instance_services.all().delete()
    be_instance.instance_services.create(service=municipality, active=1)

    # Prepare responsible
    be_instance.responsible_services.create(
        service=municipality,
        responsible_user=user_factory(name="testuser"),
    )

    # Prepare modification
    add_answer(be_instance.case.document, "beschreibung-projektaenderung", "Anbau Haus")

    # Prepare proposal
    add_answer(
        be_instance.case.document, "beschreibung-bauvorhaben", "Bau Einfamilienhaus"
    )

    # Municipality
    add_answer(be_instance.case.document, "gemeinde", "1")
    DynamicOption.objects.create(
        document=be_instance.case.document,
        question_id="gemeinde",
        slug="1",
        label="Testhausen",
    )

    be_instance.case.document.created_at = make_aware(datetime(2022, 8, 3, 9, 19))
    be_instance.case.document.save()

    freezer.move_to("2022-09-07 12:01")

    snapshot.assert_match(
        DMSHandler().get_meta_data(
            be_instance, be_instance.case.document, group.service
        )
    )


@pytest.mark.freeze_time("2022-09-06 13:37")
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_document_merge_service_cover_sheet_without_header_values(
    db,
    dms_settings,
    be_instance,
    group,
    snapshot,
    application_settings,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    be_instance.case.meta = {
        "camac-instance-id": be_instance.pk,
        "submit-date": "2021-01-01",
    }
    be_instance.case.save()

    be_instance.instance_services.all().delete()

    snapshot.assert_match(
        DMSHandler().get_meta_data(
            be_instance, be_instance.case.document, group.service
        )
    )


@pytest.mark.freeze_time("2022-09-06 13:37")
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_eingabebestaetigung_gr(
    db,
    dms_settings,
    settings,
    gr_instance,
    service_factory,
    group,
    snapshot,
    freezer,
    application_settings,
    master_data_is_visible_mock,
):
    settings.APPLICATION_NAME = "kt_gr"
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_gr"]["MASTER_DATA"]

    gr_instance.case.meta = {
        "camac-instance-id": gr_instance.pk,
        "ebau-number": "2021-99",
        "submit-date": "2021-01-01",
        "paper-submit-date": "2021-01-02",
    }
    gr_instance.case.save()

    municipality = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Chur",
    )
    group.service = municipality
    group.save()

    # Prepare plot answer
    add_table_answer(
        gr_instance.case.document,
        "parzelle",
        [
            {
                "parzellennummer": "123",
            },
            {
                # This should be excluded since no parcel number is given
                "egrid": "CH908035124647",
            },
        ],
    )

    # Prepare applicant answer
    add_table_answer(
        gr_instance.case.document,
        "personalien-gesuchstellerin",
        [
            {
                "vorname-gesuchstellerin": "Foo",
                "name-gesuchstellerin": "Bar",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Test AG",
            }
        ],
    )

    # Prepare landowner answer
    add_table_answer(
        gr_instance.case.document,
        "personalien-grundeigentumerin",
        [
            {
                "vorname-gesuchstellerin": "Grund",
                "name-gesuchstellerin": "Eigentümerin",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Eigentümer AG",
            }
        ],
    )

    # Prepare project author answer
    add_table_answer(
        gr_instance.case.document,
        "personalien-projektverfasserin",
        [
            {
                "vorname-gesuchstellerin": "Projekt",
                "name-gesuchstellerin": "Verfasserin",
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Projektverfasserin AG",
            }
        ],
    )

    # Prepare plot address
    add_answer(gr_instance.case.document, "strasse-flurname", "Bahnhofstrasse")
    add_answer(gr_instance.case.document, "nr", "2")
    add_answer(gr_instance.case.document, "ort-grundstueck", "Testhausen")

    # Prepare authority
    gr_instance.instance_services.all().delete()
    gr_instance.instance_services.create(service=municipality, active=1)

    # Prepare proposal
    add_answer(
        gr_instance.case.document, "beschreibung-bauvorhaben", "Bau Einfamilienhaus"
    )

    # Municipality
    add_answer(gr_instance.case.document, "gemeinde", "1")
    DynamicOption.objects.create(
        document=gr_instance.case.document,
        question_id="gemeinde",
        slug="1",
        label="Testhausen",
    )

    gr_instance.case.document.created_at = make_aware(datetime(2022, 8, 3, 9, 19))
    gr_instance.case.document.save()

    freezer.move_to("2022-09-07 12:01")

    snapshot.assert_match(
        DMSHandler().get_meta_data(
            gr_instance, gr_instance.case.document, group.service
        )
    )


def test_document_merge_service_unauthorized(db, requests_mock):
    template = "some-template"

    requests_mock.register_uri(
        "POST",
        build_url(
            settings.DOCUMENT_MERGE_SERVICE_URL,
            f"/template/{template}/merge",
            trailing=True,
        ),
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

    with pytest.raises(exceptions.AuthenticationFailed) as e:
        DMSClient("some token").merge({"foo": "some data"}, template)

    assert str(e.value.detail) == _("Signature has expired.")
