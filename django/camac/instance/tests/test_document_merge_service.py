from pathlib import Path

import pytest
from caluma.caluma_form.models import Document, DynamicOption, Form, Question
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command

from camac.responsible.models import ResponsibleService
from camac.tags.models import Tags
from camac.utils import build_url

from ..document_merge_service import DMSClient, DMSHandler, DMSVisitor


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


def test_document_merge_service_cover_sheet_with_header_values(
    db,
    dms_settings,
    service_factory,
    service_t_factory,
    service_group_factory,
    instance_service_factory,
    caluma_form_fixture,
    instance,
    rf,
    caluma_admin_user,
    group,
    mocker,
    form_question_factory,
    user_factory,
    snapshot,
    application_settings,
    answer_factory,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    municipality = service_factory(
        pk=2,
        service_group=service_group_factory(pk=2, name="gemeinde"),
    )
    service_t_factory(
        pk=2, service=municipality, name="Leitbehörde Burgdorf", language="de"
    )

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="baugesuch"),
        user=caluma_admin_user,
        meta={
            "camac-instance-id": instance.pk,
            "submit-date": "2021-01-01",
            "paper-submit-date": "2021-01-02",
        },
    )
    instance.case = case
    instance.save()

    # Prepare plot answer
    plot_table_form = Form.objects.get(slug="parzelle-tabelle")
    plot_question = Question.objects.get(slug="parzelle")
    plot_question.row_form = plot_table_form

    form_question_factory(
        form=case.document.form,
        question=plot_question,
    )
    plot_table = case.document.answers.create(question_id="parzelle")
    plot_row = Document.objects.create(form_id="parzelle-tabelle")
    plot_row.answers.create(question_id="parzellennummer", value="123")
    plot_table.documents.add(plot_row)

    # Prepare applicant answer
    applicant_table_form = Form.objects.get(slug="personalien")
    applicant_question = Question.objects.get(slug="personalien-gesuchstellerin")
    applicant_question.row_form = applicant_table_form

    form_question_factory(
        form=case.document.form,
        question=applicant_question,
    )
    applicant_table = case.document.answers.create(
        question_id="personalien-gesuchstellerin"
    )
    applicant_row = Document.objects.create(form_id="personalien-tabelle")
    applicant_row.answers.create(question_id="vorname-gesuchstellerin", value="Foo")
    applicant_row.answers.create(question_id="name-gesuchstellerin", value="Bar")
    applicant_row.answers.create(
        question_id="juristische-person-gesuchstellerin",
        value="juristische-person-gesuchstellerin-ja",
    )
    applicant_row.answers.create(
        question_id="name-juristische-person-gesuchstellerin", value="Test AG"
    )
    applicant_table.documents.add(applicant_row)

    # Prepare plot address
    answer_factory(
        question_id="strasse-flurname",
        value="Bahnhofstrasse",
        document=instance.case.document,
    )
    answer_factory(question_id="nr", value="2", document=instance.case.document)
    answer_factory(
        question_id="ort-grundstueck",
        value="Testhausen",
        document=instance.case.document,
    )

    # Prepare tags
    Tags.objects.create(name="some tag", instance=instance, service=municipality)

    # Prepare authority
    instance_service = instance_service_factory(
        instance=instance, service=municipality, active=1
    )
    instance.instance_services.add(instance_service)

    # Prepare responsible
    ResponsibleService.objects.create(
        instance=instance,
        service=municipality,
        responsible_user=user_factory(name="testuser"),
    )

    # Prepare modification
    answer_factory(
        question_id="beschreibung-projektaenderung",
        value="Anbau Haus",
        document=instance.case.document,
    )

    # Prepare proposal
    answer_factory(
        question_id="beschreibung-bauvorhaben",
        value="Bau Einfamilienhaus",
        document=instance.case.document,
    )

    # Municipality
    answer_factory(
        question_id="gemeinde",
        value="1",
        document=instance.case.document,
    )
    DynamicOption.objects.create(
        document=instance.case.document,
        question_id="gemeinde",
        slug="1",
        label="Testhausen",
    )

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token", X_CAMAC_GROUP=group.pk)

    client = mocker.patch(
        "camac.instance.document_merge_service.DMSClient"
    ).return_value
    client.merge.return_value = b"some binary data"

    handler = DMSHandler()
    handler.generate_pdf(instance.pk, request, None, instance.case.document.pk)

    merge_data, template = client.merge.call_args[0]

    assert template == "form"
    assert merge_data["addressHeaderLabel"]
    snapshot.assert_match(
        {k: v for k, v in client.merge.call_args[0][0].items() if "Header" in k}
    )


def test_document_merge_service_cover_sheet_without_header_values(
    db,
    dms_settings,
    caluma_form_fixture,
    instance,
    rf,
    caluma_admin_user,
    group,
    mocker,
    snapshot,
    application_settings,
):
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="baugesuch"),
        user=caluma_admin_user,
        meta={
            "camac-instance-id": instance.pk,
            "submit-date": "2021-01-01",
        },
    )
    instance.case = case
    instance.save()

    root_document = Document.objects.filter(case=case, form_id="baugesuch").first()

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token", X_CAMAC_GROUP=group.pk)

    client = mocker.patch(
        "camac.instance.document_merge_service.DMSClient"
    ).return_value
    client.merge.return_value = b"some binary data"

    handler = DMSHandler()
    handler.generate_pdf(instance.pk, request, None, root_document.pk)

    merge_data, template = client.merge.call_args[0]

    assert template == "form"
    assert merge_data["addressHeaderLabel"]
    snapshot.assert_match(
        {k: v for k, v in client.merge.call_args[0][0].items() if "Header" in k}
    )
