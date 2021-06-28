from pathlib import Path

import pytest
from caluma.caluma_form.models import Document
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSVisitor


@pytest.fixture
def caluma_form_fixture(db, form_question_factory, question_factory):
    kt_bern_path = Path(settings.ROOT_DIR) / "kt_bern"
    paths = [
        "caluma_form.json",
        "caluma_form_v2.json",
        "caluma_form_sb2.json",
        "caluma_audit_form.json",
        "caluma_publication_form.json",
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
    form_question_factory,
    question_factory,
    document_factory,
    camac_answer_factory,
    instance_factory,
    answer_factory,
    multilang,
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
