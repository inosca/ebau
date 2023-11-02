import pathlib
from datetime import date

import faker
import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory as AlexandriaDocumentFactory,
    FileFactory,
    TagFactory,
)
from caluma.caluma_form.factories import AnswerFactory, DocumentFactory
from caluma.caluma_form.models import Option, Question
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.translation import override
from rest_framework import status

from camac.instance.placeholders.utils import get_tel_and_email, human_readable_date

from .test_master_data import (  # noqa
    add_answer,
    add_table_answer,
    be_master_data_case,
    gr_master_data_case,
)


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
def gr_dms_config(settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name)
        for code, name in settings.LANGUAGES
        if code in ["de"]  # TODO: add IT
    ]
    settings.APPLICATION_NAME = "kt_gr"
    settings.INTERNAL_BASE_URL = "http://ember-ebau.local"
    settings.INTERNAL_INSTANCE_URL_TEMPLATE = (
        "http://ember-ebau.local/cases/{instance_id}"
    )
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
def test_dms_placeholders_gr(
    db,
    admin_client,
    application_settings,
    gr_master_data_case,  # noqa
    settings,
    gr_instance,
    snapshot,
    gr_distribution_settings,
    service_factory,
    work_item_factory,
    document_factory,
    question_factory,
    form_question_factory,
    active_inquiry_factory,
    gr_dms_config,
    group,
    user_factory,
    responsible_service_factory,
):
    settings.DISTRIBUTION["QUESTIONS"]["STATEMENT"] = "inquiry-answer-statement"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_gr",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )
    application_settings["MASTER_DATA"] = settings.APPLICATIONS["kt_gr"]["MASTER_DATA"]

    responsible_service = gr_instance.responsible_service()
    responsible_service.address = "Teststrasse 1, 1234 Testdorf"
    responsible_service.city = "Testdorf"
    responsible_service.phone = "032163546546"
    responsible_service.zip = "1234"
    responsible_service.website = "www.example.com"
    responsible_service.save()

    # responsible user
    responsible_user = user_factory()
    responsible_service_factory(
        instance=gr_instance,
        service=responsible_service,
        responsible_user=responsible_user,
    )

    # alexandria document
    TagFactory(slug="decision")
    alexandria_category = CategoryFactory()
    alexandria_document = AlexandriaDocumentFactory(
        title="Grundriss",
        category=alexandria_category,
        metainfo={"camac-instance-id": str(gr_instance.pk)},
        tags=["decision"],
        created_by_user=admin_client.user.username,
    )
    FileFactory(name="Situationsplan", document=alexandria_document, variant="original")

    # publication
    document = DocumentFactory()

    add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    add_answer(document, "publikation-text", "Text")
    add_answer(document, "beginn-publikationsorgan-gemeinde", date(2021, 8, 20))
    add_answer(document, "ende-publikationsorgan-gemeinde", date(2021, 8, 21))
    add_answer(document, "beginn-publikation-kantonsamtsblatt", date(2021, 8, 22))
    add_answer(document, "ende-publikation-kantonsamtsblatt", date(2021, 8, 23))

    WorkItemFactory(
        case=gr_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(group.service_id)],
        document=document,
        meta={"is-published": True},
    )

    # zones
    add_answer(gr_instance.case.document, "zonenplan", "Rebwirtschaftszone")
    add_answer(
        gr_instance.case.document, "genereller-gestaltungsplan", "Historischer Weg"
    )
    add_answer(
        gr_instance.case.document,
        "genereller-erschliessungsplan",
        "Fuss- / Spazierweg, Parkierung Gebiete D",
    )
    add_answer(gr_instance.case.document, "folgeplanung", "Baulinie allgemein")

    # gis
    add_answer(
        gr_instance.case.document,
        "gis-map",
        '{"markers": [{"x": 2569941.12345, "y": 1298923.12345}, {"x": 2609995.12345,"y": 1271340.12345}] }',
    )

    # Prepare project modification
    add_answer(
        gr_instance.case.document, "beschreibung-projektaenderung", "Projektänderung"
    )

    # decision
    decision_work_item = work_item_factory(
        case=gr_instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form_id="decision"),
    )
    decision_question = question_factory(
        slug="decision-decision", type=Question.TYPE_CHOICE
    )
    decision_date_question = question_factory(
        slug="decision-date", type=Question.TYPE_DATE
    )
    Option.objects.create(slug="decision-decision-approved", label="Bewilligt")
    form_question_factory(form_id="decision", question=decision_question)
    form_question_factory(form_id="decision", question=decision_date_question)
    decision_work_item.document.answers.create(
        question_id="decision-decision",
        value="decision-decision-approved",
    )
    decision_work_item.document.answers.create(
        question_id="decision-date", date=date.today()
    )

    # municipality
    municipality = service_factory(
        trans__name="Chur",
    )
    gr_master_data_case.document.answers.filter(question_id="gemeinde").update(
        value=str(municipality.pk)
    )
    gr_master_data_case.document.dynamicoption_set.update(slug=str(municipality.pk))

    # inquiry
    nebenbestimmungen_question = Question.objects.get(
        pk=gr_distribution_settings["QUESTIONS"]["ANCILLARY_CLAUSES"]
    )
    stellungnahme_question = Question.objects.get(
        pk=gr_distribution_settings["QUESTIONS"]["STATEMENT"]
    )
    district_inquiries = [
        active_inquiry_factory(gr_instance, svc)
        for svc in service_factory.create_batch(2, service_group__name="district")
    ]
    municipalities_inquiries = [
        active_inquiry_factory(gr_instance, svc)
        for svc in service_factory.create_batch(2, service_group__name="municipality")
    ]
    service_inquiries = [
        active_inquiry_factory(
            gr_instance,
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

    url = reverse("instance-dms-placeholders", args=[gr_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


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
    be_decision_settings,
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
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][
            "OVERALL_BUILDING_PERMIT"
        ],
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
