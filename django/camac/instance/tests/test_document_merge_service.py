import locale
from datetime import datetime
from pathlib import Path

import faker
import pytest
from alexandria.core.factories import CategoryFactory, DocumentFactory, FileFactory
from caluma.caluma_form.models import DynamicOption, Question
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _
from rest_framework import exceptions, status

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSHandler, DMSVisitor


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
        "config/caluma_form_v4.json",
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
        "config/caluma_geometer_form.json",
        "data/caluma_form.json",
        "data/caluma_workflow.json",
        "data/user.json",
        "data/instance.json",
    ]

    call_command("loaddata", *[kt_bern_path / path for path in paths])


@pytest.fixture
def ch_locale():
    locale.setlocale(locale.LC_ALL, "de_CH.utf8")
    yield locale.getlocale()
    locale.setlocale(locale.LC_ALL, "")


@pytest.mark.freeze_time("2023-01-06 16:10")
def test_document_merge_service_snapshot(
    db,
    application_settings,
    caluma_form_fixture,
    django_assert_num_queries,
    be_dms_settings,
    service,
    snapshot,
    be_master_data_settings,
):
    cache.clear()

    for kwargs, expected_queries in [
        ({"instance_id": 1}, 21),
        ({"instance_id": 3, "form_slug": "sb1"}, 27),
        ({"instance_id": 3, "form_slug": "sb2"}, 27),
        ({"instance_id": 3, "document_id": "da618b68-b4a8-414f-9d5e-50e0fda43cde"}, 25),
    ]:
        with django_assert_num_queries(expected_queries):
            handler = DMSHandler()
            instance, root_document = handler.get_instance_and_document(**kwargs)

            snapshot.assert_match(
                handler.get_meta_data(instance, root_document, service)
            )

            visitor = DMSVisitor(root_document, instance, BaseUser())
            snapshot.assert_match(visitor.visit(root_document))


def test_document_merge_service_is_valid(db, caluma_form_fixture, be_dms_settings):
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
    be_dms_settings,
    service_factory,
    tag_factory,
    be_instance,
    group,
    user_factory,
    snapshot,
    application_settings,
    master_data_is_visible_mock,
    freezer,
    be_master_data_settings,
    utils,
):
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
    utils.add_table_answer(
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
    utils.add_table_answer(
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
    utils.add_answer(be_instance.case.document, "strasse-flurname", "Bahnhofstrasse")
    utils.add_answer(be_instance.case.document, "nr", "2")
    utils.add_answer(be_instance.case.document, "ort-grundstueck", "Testhausen")

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
    utils.add_answer(
        be_instance.case.document, "beschreibung-projektaenderung", "Anbau Haus"
    )

    # Prepare proposal
    utils.add_answer(
        be_instance.case.document, "beschreibung-bauvorhaben", "Bau Einfamilienhaus"
    )

    # Municipality
    utils.add_answer(be_instance.case.document, "gemeinde", "1")
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
    be_dms_settings,
    be_instance,
    group,
    snapshot,
    application_settings,
    be_master_data_settings,
):
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
    gr_dms_settings,
    settings,
    gr_instance,
    service_factory,
    group,
    snapshot,
    freezer,
    application_settings,
    master_data_is_visible_mock,
    utils,
    gr_master_data_settings,
):
    settings.APPLICATION_NAME = "kt_gr"
    application_settings["DOCUMENT_BACKEND"] = "alexandria"

    gr_instance.case.meta = {
        "camac-instance-id": gr_instance.pk,
        "submit-date": "2021-01-01",
        "paper-submit-date": "2021-01-02",
    }
    gr_instance.case.save()

    municipality = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Chur",
        logo=None,
    )
    group.service = municipality
    group.save()

    alexandria_category = CategoryFactory()

    # In the test we use "main-form" as form
    gr_dms_settings["FORM"]["baugesuch"]["forms"].append("main-form")
    gr_dms_settings["ALEXANDRIA_DOCUMENT_CATEGORIES"] = [alexandria_category.pk]

    FileFactory(
        document=DocumentFactory(
            title="Lageplan.pdf",
            category=alexandria_category,
            metainfo={"camac-instance-id": gr_instance.pk},
        ),
        checksum=f"sha256:{faker.Faker().sha256()}",
    )

    # Prepare plot answer
    utils.add_table_answer(
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
    utils.add_table_answer(
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
    utils.add_table_answer(
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
    utils.add_table_answer(
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

    # Prepare project modification
    utils.add_answer(
        gr_instance.case.document, "projektaenderung", "projektaenderung-ja"
    )
    utils.add_answer(
        gr_instance.case.document, "beschreibung-projektaenderung", "Projekt Änderung"
    )

    # Prepare plot address
    utils.add_answer(
        gr_instance.case.document, "street-and-housenumber", "Bahnhofstrasse 2"
    )
    utils.add_answer(gr_instance.case.document, "ort-grundstueck", "Testhausen")

    # Prepare authority
    gr_instance.instance_services.all().delete()
    gr_instance.instance_services.create(service=municipality, active=1)

    # Prepare proposal
    utils.add_answer(
        gr_instance.case.document, "beschreibung-bauvorhaben", "Bau Einfamilienhaus"
    )

    # Municipality
    utils.add_answer(gr_instance.case.document, "gemeinde", "1")
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
        DMSHandler().get_data(
            gr_instance, gr_instance.case.document, BaseUser(), group.service
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


@pytest.mark.parametrize("use_number_separator", [True, False])
def test_number_separator(
    db,
    ch_locale,
    dms_settings,
    form_question_factory,
    so_instance,
    use_number_separator,
    utils,
):
    dms_settings["FORM"] = {"baugesuch": {"forms": ["main-form"]}}
    dms_settings["USE_NUMBER_SEPARATOR"] = use_number_separator

    form_question_factory(
        form_id="main-form",
        question__slug="integer",
        question__type=Question.TYPE_INTEGER,
    )
    form_question_factory(
        form_id="main-form",
        question__slug="float",
        question__type=Question.TYPE_FLOAT,
    )

    utils.add_answer(so_instance.case.document, "integer", 57000000)
    utils.add_answer(so_instance.case.document, "float", 1304.12)

    visitor = DMSVisitor(so_instance.case.document, so_instance, BaseUser())

    data = {
        item["slug"]: item.get("value")
        for item in visitor.visit(so_instance.case.document)
    }

    if use_number_separator:
        assert data["integer"] == "57’000’000"
        assert data["float"] == "1’304.12"
    else:
        assert data["integer"] == 57000000
        assert data["float"] == 1304.12
