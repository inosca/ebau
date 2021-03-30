from pathlib import Path

import pytest
from caluma.caluma_form.models import Document, Form
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command

from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSVisitor


@pytest.fixture
def caluma_form_fixture(db, form_question_factory, question_factory):
    # load caluma config
    path = Path(settings.ROOT_DIR) / "kt_bern" / "config" / "caluma_form.json"
    call_command("loaddata", path)

    # load custom caluma data (includes sb1 and sb2)
    path = Path(__file__).parent / "fixtures" / "data-caluma.json"
    call_command("loaddata", path)


@pytest.fixture
def dms_settings(application_settings):
    application_settings["DOCUMENT_MERGE_SERVICE"] = settings.APPLICATIONS["kt_bern"][
        "DOCUMENT_MERGE_SERVICE"
    ]


@pytest.mark.parametrize(
    "instance_id,form_slug",
    [
        (1, "baugesuch"),
        (1, "sb1"),
        (1, "sb2"),
        (3, None),
        (2, "mp-form"),
    ],
)
def test_document_merge_service_snapshot(
    db,
    snapshot,
    service_factory,
    service_t_factory,
    service_group_factory,
    caluma_form_fixture,
    instance_id,
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

    _filter = {"meta__camac-instance-id": instance_id}

    if form_slug:
        _filter["form__slug"] = form_slug

    if form_slug == "mp-form":
        form = Form.objects.create(slug="mp-form")
        document = document_factory(form=form)
        _filter = {"id": document.id}

    root_document = Document.objects.get(**_filter)

    if form_slug == "baugesuch":
        archived_q = question_factory(
            pk="verpflichtung-bei-handaenderung", is_archived=True
        )
        form_question_factory(form=root_document.form, question=archived_q)

    if form_slug == "mp-form":
        questions = [
            ("mp-nutzungsart", "choice", "mp-nutzungsart-nein"),
            ("mp-nutzungsart-ergebnis", "choice", None),
            ("mp-nutzungsart-bemerkungen", "textarea", "Test Nutzungsart"),
            ("mp-bepflanzung", "choice", "mp-bepflanzung-ja"),
            (
                "mp-bepflanzung-ergebnis",
                "choice",
                "mp-bepflanzung-ergebnis-eingehalten",
            ),
            ("mp-bepflanzung-bemerkungen", "textarea", "Test Bepflanzung"),
            ("mp-eigene-pruefgegenstaende", "table", None),
            (
                "mp-erforderliche-beilagen-vorhanden",
                "choice",
                "mp-erforderliche-beilagen-vorhanden",
            ),
            ("mp-welche-beilagen-fehlen", "textarea", "Alle"),
        ]
        for i, (question_slug, question_type, value) in enumerate(reversed(questions)):
            question = question_factory(slug=question_slug, type=question_type)
            form_question_factory(form=root_document.form, question=question, sort=i)
            if value:
                answer_factory(
                    question_id=question.pk,
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
