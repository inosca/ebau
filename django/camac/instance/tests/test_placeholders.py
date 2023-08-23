import pathlib
from datetime import date

import faker
import pytest
from caluma.caluma_form.factories import AnswerFactory, DocumentFactory
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.translation import override
from rest_framework import status

from camac.constants.kt_bern import (
    DECISION_TYPE_OVERALL_BUILDING_PERMIT,
    VORABKLAERUNG_DECISIONS_BEWILLIGT,
)
from camac.instance.placeholders.utils import get_tel_and_email, human_readable_date

from .test_master_data import add_answer, add_table_answer, be_master_data_case  # noqa


@pytest.fixture
def be_dms_config(settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name) for code, name in settings.LANGUAGES if code in ["de", "fr"]
    ]
    settings.APPLICATION_NAME = "kt_bern"
    settings.INTERNAL_BASE_URL = "http://ebau.local"
    settings.INTERNAL_INSTANCE_URL_TEMPLATE = "http://ebau.local/index/redirect-to-instance-resource/instance-id/{instance_id}"
    yield
    settings.LANGUAGES = original_languages


@pytest.fixture
def status_question(be_distribution_settings):
    return Question.objects.get(pk=be_distribution_settings["QUESTIONS"]["STATUS"])


@pytest.fixture
def stellungnahme_question(be_distribution_settings):
    return Question.objects.get(pk=be_distribution_settings["QUESTIONS"]["STATEMENT"])


@pytest.fixture
def nebenbestimmungen_question(be_distribution_settings):
    return Question.objects.get(
        pk=be_distribution_settings["QUESTIONS"]["ANCILLARY_CLAUSES"]
    )


@pytest.mark.freeze_time("2021-08-30", tick=True)
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders(
    db,
    active_inquiry_factory,
    admin_client,
    application_settings,
    settings,
    be_instance,
    be_master_data_case,  # noqa
    billing_v2_entry_factory,
    group,
    instance_service,
    multilang,
    notice_factory,
    notice_type_factory,
    responsible_service_factory,
    service_factory,
    snapshot,
    tag_factory,
    objection,
    objection_participant_factory,
    decision_factory,
    status_question,
    stellungnahme_question,
    nebenbestimmungen_question,
    be_dms_config,
):
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    # publication
    document = DocumentFactory()

    add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    add_answer(document, "publikation-text", "Text")
    add_answer(
        document,
        "publikation-1-publikation-anzeiger",
        date(2021, 8, 30),
    )
    add_answer(
        document,
        "publikation-2-publikation-anzeiger",
        date(2021, 8, 20),
    )
    add_answer(
        document,
        "publikation-amtsblatt",
        date(2021, 8, 10),
    )
    add_answer(
        document,
        "publikation-startdatum",
        date(2021, 9, 1),
    )
    add_answer(
        document,
        "publikation-ablaufdatum",
        date(2021, 9, 15),
    )

    WorkItemFactory(
        case=be_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(group.service_id)],
        document=document,
        meta={"is-published": True},
    )

    # Modification
    add_answer(document, "beschreibung-projektaenderung", "Umbau Haus in Garage")

    # Neighbors
    information_of_neighbors_document = DocumentFactory(
        pk="5a498238-6af4-472b-bc3c-83a4848ed6cc"
    )
    WorkItemFactory(
        task_id="information-of-neighbors",
        document=information_of_neighbors_document,
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(group.service_id)],
        case=be_instance.case,
        meta={"is-published": True},
    )
    add_table_answer(
        information_of_neighbors_document,
        "information-of-neighbors-neighbors",
        [
            {
                "vorname-gesuchstellerin": "Karl",
                "name-gesuchstellerin": "Nachbarsson",
                "strasse-gesuchstellerin": "Teststrasse",
                "nummer-gesuchstellerin": 124,
                "ort-gesuchstellerin": "Testhausen",
                "plz-gesuchstellerin": 1234,
            },
        ],
    )

    # Legal submission
    legal_submission = WorkItemFactory(
        task_id="legal-submission",
        document__form_id="legal-submission",
        case=be_instance.case,
    )

    table_answer = add_table_answer(
        legal_submission.document,
        "legal-submission-table",
        [
            {
                "legal-submission-type": ["legal-submission-type-objection"],
                "legal-submission-document-date": date(2022, 12, 1),
                "legal-submission-receipt-date": date(2022, 12, 2),
                "legal-submission-reprimands": "Test E 1\nTest E 2",
                "legal-submission-title": "Test Einsprache",
            },
            {
                "legal-submission-type": ["legal-submission-type-legal-custody"],
                "legal-submission-document-date": date(2022, 11, 1),
                "legal-submission-receipt-date": date(2022, 11, 2),
                "legal-submission-request-legal-custody": "Test RV 1\nTest RV 2",
                "legal-submission-title": "Test Rechtsverwahrung",
            },
            {
                "legal-submission-type": [
                    "legal-submission-type-load-compensation-request"
                ],
                "legal-submission-document-date": date(2022, 10, 1),
                "legal-submission-receipt-date": date(2022, 10, 2),
                "legal-submission-request-load-compensation-request": "Test LAB 1\nTest LAB 2",
                "legal-submission-title": "Test Lastenausgleichsbegehren",
            },
        ],
        row_form_id="legal-submission-form",
    )

    objection = table_answer.documents.get(
        answers__value=["legal-submission-type-objection"]
    )
    legal_custody = table_answer.documents.get(
        answers__value=["legal-submission-type-legal-custody"]
    )
    load_compensation = table_answer.documents.get(
        answers__value=["legal-submission-type-load-compensation-request"]
    )

    add_table_answer(
        objection,
        "legal-submission-legal-claimants-table-question",
        [
            {
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-nein",
                "vorname-gesuchstellerin": "Heinz",
                "name-gesuchstellerin": "Einsprachenmann",
                "strasse-gesuchstellerin": "Beispielstrasse",
                "nummer-gesuchstellerin": 1,
                "ort-gesuchstellerin": "Beispieldorf",
                "plz-gesuchstellerin": 4321,
            }
        ],
        row_form_id="personalien-tabelle",
    )

    add_table_answer(
        legal_custody,
        "legal-submission-legal-claimants-table-question",
        [
            {
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-nein",
                "vorname-gesuchstellerin": "Martha",
                "name-gesuchstellerin": "Rechstverwahrungsson",
                "strasse-gesuchstellerin": "Beispielstrasse",
                "nummer-gesuchstellerin": 2,
                "ort-gesuchstellerin": "Beispieldorf",
                "plz-gesuchstellerin": 4321,
            }
        ],
        row_form_id="personalien-tabelle",
    )

    add_table_answer(
        load_compensation,
        "legal-submission-legal-claimants-table-question",
        [
            {
                "juristische-person-gesuchstellerin": "juristische-person-gesuchstellerin-ja",
                "name-juristische-person-gesuchstellerin": "Lastenausgleichsbegehren4you AG",
                "strasse-gesuchstellerin": "Beispielstrasse",
                "nummer-gesuchstellerin": 3,
                "ort-gesuchstellerin": "Beispieldorf",
                "plz-gesuchstellerin": 4321,
            }
        ],
        row_form_id="personalien-tabelle",
    )

    municipality = service_factory(
        trans__name="Burgdorf",
    )
    be_master_data_case.document.answers.filter(question_id="gemeinde").update(
        value=str(municipality.pk)
    )
    be_master_data_case.document.dynamicoption_set.update(slug=str(municipality.pk))

    district_inquiries = [
        active_inquiry_factory(be_instance, svc)
        for svc in service_factory.create_batch(2, service_group__name="district")
    ]
    municipalities_inquiries = [
        active_inquiry_factory(be_instance, svc)
        for svc in service_factory.create_batch(2, service_group__name="municipality")
    ]
    service_inquiries = [
        active_inquiry_factory(
            be_instance,
            svc,
            status=WorkItem.STATUS_COMPLETED,
            closed_at=make_aware(faker.Faker().date_time()),
        )
        for svc in service_factory.create_batch(2, service_group__name="service")
    ]

    inquiries = [*district_inquiries, *municipalities_inquiries, *service_inquiries]

    for i, inquiry in enumerate(inquiries):
        # add stellungnahme and nebenbestimmungen
        AnswerFactory(
            document=inquiry.child_case.document,
            question=stellungnahme_question,
            value=f"Stellungnahme {i+1}",
        )
        AnswerFactory(
            document=inquiry.child_case.document,
            question=nebenbestimmungen_question,
            value=f"Nebenbestimmungen {i+1}",
        )

    for service_inquiry in service_inquiries:
        # add status
        AnswerFactory(
            document=service_inquiry.child_case.document,
            question=status_question,
            value=faker.Faker().word(
                ext_word_list=status_question.options.values_list("pk", flat=True)
            ),
        )

    inquiries[0].addressed_groups = [str(group.service.pk)]
    inquiries[0].save()

    # Add an inquiry in draft
    draft_inquiry = active_inquiry_factory(
        be_instance,
        group.service,
        status=WorkItem.STATUS_SUSPENDED,
    )
    draft_inquiry.child_case = None
    # This should not happen anymore but should still be tested
    draft_inquiry.deadline = None
    draft_inquiry.save()

    tag_factory.create_batch(5, service=group.service, instance=be_instance)
    responsible_service_factory(instance=be_instance, service=group.service)
    decision = decision_factory(
        decision=VORABKLAERUNG_DECISIONS_BEWILLIGT,
        decision_type=DECISION_TYPE_OVERALL_BUILDING_PERMIT,
    )
    decision.status = WorkItem.STATUS_COMPLETED
    decision.save()
    billing_v2_entry_factory.create_batch(2, instance=be_instance)
    billing_v2_entry_factory.create_batch(2, instance=be_instance, group=group)

    # Inventar
    add_answer(
        be_instance.case.document,
        "schuetzenswert",
        "schuetzenswert-ja",
        question_label="Schützenswert",
    )
    add_answer(
        be_instance.case.document,
        "erhaltenswert",
        "erhaltenswert-nein",
        question_label="Erhaltenswert",
    )
    add_answer(
        be_instance.case.document, "k-objekt", "k-objekt-ja", question_label="K-Objekt"
    )
    add_answer(
        be_instance.case.document,
        "baugruppe-bauinventar",
        "baugruppe-bauinventar-ja",
        question_label="Baugruppe Bauinventar",
    )
    add_answer(be_instance.case.document, "bezeichnung-baugruppe", "Test Baugruppe")
    add_answer(be_instance.case.document, "rrb", "rrb-ja")
    add_answer(
        be_instance.case.document,
        "rrb-vom",
        date(2022, 1, 1),
        question_label="RRB vom",
    )
    add_answer(be_instance.case.document, "vertrag", "vertrag-ja")
    add_answer(
        be_instance.case.document,
        "vertrag-vom",
        date(2022, 2, 1),
        question_label="Vertrag vom",
    )

    url = reverse("instance-dms-placeholders", args=[be_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.freeze_time("2021-08-30")
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_empty(
    db,
    admin_client,
    application_settings,
    settings,
    be_instance,
    snapshot,
    be_dms_config,
):
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_bern"][
        "MASTER_DATA"
    ]

    response = admin_client.get(
        reverse("instance-dms-placeholders", args=[be_instance.pk])
    )
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.freeze_time("2023-01-24")
@pytest.mark.parametrize(
    "language,expected",
    [("de", "24. Januar 2023"), ("fr", "24 janvier 2023"), ("en", "January 24, 2023")],
)
def test_human_readable_date(language, expected):
    with override(language):
        assert human_readable_date(date.today()) == expected


def test_dms_placeholders_docs(admin_client, snapshot, be_dms_config):
    response = admin_client.get(reverse("dms-placeholders-docs"))
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


def test_dms_placeholders_docs_available_placeholders(
    admin_client, snapshot, be_dms_config
):
    response = admin_client.get(
        reverse("dms-placeholders-docs"), data={"available_placeholders": True}
    )
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


def test_get_tel_and_email():
    assert (
        get_tel_and_email({"tel": "0311234567", "email": "foo@bar.com"})
        == "0311234567, foo@bar.com"
    )
