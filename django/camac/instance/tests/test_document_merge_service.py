from pathlib import Path

import pytest
from caluma.caluma_form.models import Document, DynamicOption
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSHandler, DMSVisitor
from .test_master_data import add_answer, add_table_answer


@pytest.fixture
def caluma_form_fixture(db):
    kt_bern_path = Path(settings.ROOT_DIR) / "kt_bern"
    paths = [
        "caluma_form_common.json",
        "caluma_dossier_import_form.json",
        "caluma_form.json",
        "caluma_form_v2.json",
        "caluma_form_sb2.json",
        "caluma_audit_form.json",
        "caluma_publication_form.json",
        "caluma_information_of_neighbors_form.json",
        "caluma_workflow.json",
    ]

    # for path in sorted((kt_bern_path / "config").glob("caluma_*.json")):
    for path in paths:
        call_command("loaddata", kt_bern_path / "config" / path)

    call_command("loaddata", kt_bern_path / "data" / "caluma_form.json")


@pytest.fixture
def dms_settings(application_settings):
    application_settings["DOCUMENT_MERGE_SERVICE"] = settings.APPLICATIONS["kt_bern"][
        "DOCUMENT_MERGE_SERVICE"
    ]
    application_settings["DOCUMENT_MERGE_SERVICE"]["FORM"]["baugesuch"]["forms"].append(
        "main-form"
    )


@pytest.mark.parametrize(
    "form_slug",
    [
        ("baugesuch"),
        ("sb1"),
        ("sb2"),
        ("mp-form"),
    ],
)
def test_document_merge_service_snapshot(
    db,
    snapshot,
    service_factory,
    service_t_factory,
    service_group_factory,
    caluma_form_fixture,
    form_slug,
    dms_settings,
    document_factory,
    answer_factory,
):
    cache.clear()
    municipality = service_factory(
        pk=2,
        service_group=service_group_factory(name="municipality"),
    )
    service_t_factory(service=municipality, name="Leitbehörde Burgdorf", language="de")
    service_t_factory(service=municipality, name="Municipalité Burgdorf", language="fr")

    if form_slug == "mp-form":
        document = document_factory(form_id="mp-form")

    root_document = Document.objects.filter(form_id=form_slug).first()

    if form_slug == "mp-form":
        questions = [
            ("mp-nutzungsart", "choice", "mp-nutzungsart-nein"),
            ("mp-nutzungsart-bemerkungen", "textarea", "Test Nutzungsart"),
            ("mp-bepflanzung", "choice", "mp-bepflanzung-ja"),
            (
                "mp-bepflanzung-ergebnis",
                "choice",
                "mp-bepflanzung-ergebnis-eingehalten",
            ),
            ("mp-bepflanzung-bemerkungen", "textarea", "Test Bepflanzung"),
            (
                "mp-erforderliche-beilagen-vorhanden",
                "choice",
                "mp-erforderliche-beilagen-vorhanden",
            ),
            ("mp-welche-beilagen-fehlen", "textarea", "Alle"),
        ]
        for question_slug, question_type, value in questions:
            if value:
                answer_factory(
                    question_id=question_slug,
                    value=value,
                    document_id=document.pk,
                )

    visitor = DMSVisitor()
    snapshot.assert_match(visitor.visit(root_document))


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
            }
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

    snapshot.assert_match(
        DMSHandler().get_meta_data(
            be_instance, be_instance.case.document, group.service
        )
    )


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
