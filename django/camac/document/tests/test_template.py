import functools
import mimetypes
from datetime import datetime
from io import BytesIO

import pytest
import pytz
from django.urls import reverse
from docxtpl import DocxTemplate
from lxml import etree
from pytest_factoryboy import LazyFixture
from rest_framework import status

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
    "publication_entry__publication_date", [datetime(2018, 5, 28, tzinfo=pytz.UTC)]
)
@pytest.mark.parametrize(
    "billing_entry__created", [datetime(2018, 5, 28, tzinfo=pytz.UTC)]
)
@pytest.mark.parametrize(
    "activation__start_date", [datetime(2018, 3, 15, tzinfo=pytz.UTC)]
)
@pytest.mark.parametrize(
    "activation__end_date", [datetime(2018, 4, 15, tzinfo=pytz.UTC)]
)
@pytest.mark.parametrize(
    "activation__deadline_date", [datetime(2018, 4, 30, tzinfo=pytz.UTC)]
)
@pytest.mark.parametrize("billing_entry__amount", ["99.66"])
@pytest.mark.parametrize(
    "role__name,template__path,instance__user,status_code,to_type",
    [
        (
            "Canton",
            django_file("template.docx"),
            LazyFixture("user"),
            status.HTTP_200_OK,
            "docx",
        ),
        (
            "Canton",
            django_file("template.docx"),
            LazyFixture("user"),
            status.HTTP_200_OK,
            "pdf",
        ),
        (
            "Canton",
            django_file("template.docx"),
            LazyFixture("user"),
            status.HTTP_400_BAD_REQUEST,
            "invalid",
        ),
        # service is not assigned to instance so not allowed to build document
        (
            "Service",
            django_file("template.docx"),
            LazyFixture("user"),
            status.HTTP_400_BAD_REQUEST,
            "docx",
        ),
    ],
)
@pytest.mark.parametrize(
    "service__name,billing_account__department,billing_account__name",
    [("Amt", "Allgemein", "Gebuehren")],
)
@pytest.mark.parametrize(
    "activation__reason,circulation_state__name,circulation_answer__name",
    [("Grund", "OK", "Antwort")],
)
@pytest.mark.parametrize(
    "form_field__name,instance__identifier,location__name,activation__service",
    [
        (
            "testname",
            "11-18-011",
            "Schwyz",
            LazyFixture(lambda service_factory: service_factory(name="Fachstelle")),
        )
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
    activation,
    billing_entry,
    publication_entry,
    notice_factory,
    notice_type_factory,
    snapshot,
    settings,
    unoconv_pdf_mock,
    unoconv_invalid_mock,
):
    notice_type_application = notice_type_factory(name="Antrag")
    notice_type_hint = notice_type_factory(name="Hinweis")

    notice_factory(
        activation=activation,
        notice_type=notice_type_application,
        content="Inhalt Antrag!",
    )
    notice_factory(
        activation=activation, notice_type=notice_type_hint, content="Inhalt Hinweis!"
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

    url = reverse("template-merge", args=[template.pk])
    response = admin_client.get(url, data={"instance": sz_instance.pk, "type": to_type})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert (
            response["Content-Type"] == mimetypes.guess_type("filename." + to_type)[0]
        )
        if to_type == "docx":
            docx = DocxTemplate(BytesIO(response.content))
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
    docx = DocxTemplate(BytesIO(response.content))
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    snapshot.assert_match(xml)
