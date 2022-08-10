import functools
import mimetypes
from datetime import datetime
from io import BytesIO

import pytest
from caluma.caluma_form.factories import AnswerFactory
from caluma.caluma_workflow.models import WorkItem
from django.core.management import call_command
from django.urls import reverse
from django.utils.timezone import make_aware
from docxtpl import DocxTemplate
from lxml import etree
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance.tests.test_master_data import add_answer, add_table_answer

from .data import django_file


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Service", 1), ("Municipality", 1)],
)
def test_template_list(admin_client, template, size):
    url = reverse("template-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size:
        assert json["data"][0]["id"] == str(template.pk)


@pytest.mark.parametrize("role__name", [("Canton")])
def test_template_detail(admin_client, template):
    url = reverse("template-detail", args=[template.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,status_code,template_path",
    [
        ("Canton", status.HTTP_201_CREATED, "template.docx"),
        ("Canton", status.HTTP_400_BAD_REQUEST, "multiple-pages.pdf"),
        ("Municipality", status.HTTP_201_CREATED, "template.docx"),
        ("Service", status.HTTP_201_CREATED, "template.docx"),
        ("Applicant", status.HTTP_403_FORBIDDEN, "template.docx"),
    ],
)
def test_template_create(admin_client, status_code, group, template_path):
    url = reverse("template-list")

    path = django_file(template_path)
    data = {"name": "test", "path": path.file, "group": group.pk}
    response = admin_client.post(url, data=data, format="multipart")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Canton", status.HTTP_200_OK),
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
        ("Applicant", status.HTTP_404_NOT_FOUND),
    ],
)
def test_template_update(admin_client, template, status_code):
    url = reverse("template-detail", args=[template.pk])

    data = {"name": "new"}
    response = admin_client.patch(url, data=data, format="multipart")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_404_NOT_FOUND),
    ],
)
def test_template_destroy(admin_client, template, status_code):
    url = reverse("template-detail", args=[template.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.freeze_time("2018-05-28")
@pytest.mark.parametrize(
    "publication_entry__publication_date", [make_aware(datetime(2018, 5, 28))]
)
@pytest.mark.parametrize(
    "billing_entry__created,billing_entry__amount,billing_account__department,billing_account__name",
    [(make_aware(datetime(2018, 5, 28)), "99.66", "Allgemein", "Gebuehren")],
)
@pytest.mark.parametrize("service__name", ["Amt"])
@pytest.mark.parametrize("template__path", [django_file("template.docx")])
@pytest.mark.parametrize("form_field__name", ["testname"])
@pytest.mark.parametrize("location__name", ["Schwyz"])
@pytest.mark.parametrize(
    "instance__identifier,instance__group,instance__user",
    [
        (
            "11-18-011",
            LazyFixture(lambda group_factory: group_factory()),
            LazyFixture("user"),
        )
    ],
)
@pytest.mark.parametrize(
    "role__name,status_code,to_type",
    [
        ("Canton", status.HTTP_200_OK, "docx"),
        ("Canton", status.HTTP_200_OK, "pdf"),
        ("Canton", status.HTTP_400_BAD_REQUEST, "invalid"),
        # service is not assigned to instance so not allowed to build document
        ("Service", status.HTTP_400_BAD_REQUEST, "docx"),
    ],
)
def test_template_merge(
    admin_client,
    template,
    sz_instance,
    to_type,
    form_field,
    status_code,
    form_field_factory,
    active_inquiry_factory,
    billing_entry,
    publication_entry,
    work_item_factory,
    document_factory,
    snapshot,
    settings,
    unoconv_pdf_mock,
    unoconv_invalid_mock,
    service_group,
    service,
    service_factory,
    application_settings,
):
    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_schwyz/config/buildingauthority.json"),
        settings.ROOT_DIR("kt_schwyz/config/caluma_form.json"),
    )

    inquiry_service = service_factory(name="Fachstelle")

    application_settings["INTER_SERVICE_GROUP_VISIBILITIES"] = {
        service_group.pk: [inquiry_service.service_group.pk],
    }

    inquiry = active_inquiry_factory(
        addressed_service=inquiry_service,
        status=WorkItem.STATUS_COMPLETED,
        deadline=make_aware(datetime(2018, 4, 30)),
        closed_at=make_aware(datetime(2018, 4, 15)),
    )
    active_inquiry_factory(addressed_service=service_factory())

    # This can't be passed on creation but can only be update after the object
    # already exists since it's an auto field.
    inquiry.created_at = make_aware(datetime(2018, 3, 15))
    inquiry.save()

    AnswerFactory(
        document=inquiry.document,
        question_id="inquiry-remark",
        value="Grund",
    )
    AnswerFactory(
        document=inquiry.child_case.document,
        question_id="inquiry-answer-status",
        value="inquiry-answer-status-final",
    )
    AnswerFactory(
        document=inquiry.child_case.document,
        question_id="inquiry-answer-request",
        value="Inhalt Antrag!",
    )
    AnswerFactory(
        document=inquiry.child_case.document,
        question_id="inquiry-answer-hint",
        value="Inhalt Hinweis!",
    )

    add_field = functools.partial(form_field_factory, instance=sz_instance)
    add_address_field = functools.partial(
        add_field,
        value=[
            {
                "name": "Hans Muster",
                "firma": "Firma Muster",
                "strasse": "Beispiel Strasse",
                "ort": "0000 Ort",
                "email": "email@example.com",
                "tel": "000 000 00 00",
            },
            {"name": "Hans Beispiel", "firma": "Firma Beispiel"},
        ],
    )
    add_field(name="art-der-befestigten-flache", value="Lagerplatz")
    add_field(name="kategorie-des-vorhabens", value=["Anlage(n)", "Baute(n)"])
    add_address_field(name="grundeigentumerschaft")
    add_address_field(name="bauherrschaft")
    add_address_field(name="bauherrschaft-v2")
    add_address_field(name="projektverfasser-planer")
    add_address_field(name="projektverfasser-planer-v2")

    work_item = work_item_factory(task_id="building-authority", case=sz_instance.case)
    work_item.document = document_factory(form_id="bauverwaltung")
    work_item.save()
    add_answer(work_item.document, "bewilligungsverfahren-gr-sitzung-nummer", 12)
    add_table_answer(
        work_item.document,
        "bewilligungsverfahren-sitzung-baukommission",
        [
            {
                "bewilligungsverfahren-sitzung-baukommission-nr": 78,
                "bewilligungsverfahren-sitzung-baukommission-bemerkung": "Foo Bar",
            }
        ],
    )

    url = reverse("template-merge", args=[template.pk])
    response = admin_client.get(url, data={"instance": sz_instance.pk, "type": to_type})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert (
            response["Content-Type"] == mimetypes.guess_type("filename." + to_type)[0]
        )
        if to_type == "docx":
            docx = DocxTemplate(BytesIO(response.content)).get_docx()
            xml = etree.tostring(
                docx._element.body, encoding="unicode", pretty_print=True
            )
            try:
                snapshot.assert_match(xml)
            except AssertionError:  # pragma: no cover
                with open("/tmp/camacng_template_result.docx", "wb") as output:
                    output.write(response.content)
                print("Template output changed. Check file at %s" % output.name)
                raise


@pytest.mark.parametrize(
    "role__name,template__path",
    [
        (
            "Municipality",
            django_file("template.docx"),
        )
    ],
)
def test_template_download(
    snapshot,
    admin_client,
    template,
):
    url = reverse("template-download", args=[template.pk])
    response = admin_client.get(url)
    docx = DocxTemplate(BytesIO(response.content)).get_docx()
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    snapshot.assert_match(xml)
