from datetime import date, datetime
from unittest.mock import Mock

import faker
import pytest
from alexandria.core.factories import (
    CategoryFactory,
    DocumentFactory as AlexandriaDocumentFactory,
    FileFactory,
    MarkFactory,
    TagFactory,
)
from caluma.caluma_form import api as form_api, models as caluma_form_models
from caluma.caluma_form.factories import AnswerFactory, DocumentFactory
from caluma.caluma_form.models import Option, Question
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.translation import gettext_noop as _, override
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.instance.placeholders.fields import MasterDataField
from camac.instance.placeholders.serializers import DMSPlaceholdersSerializer
from camac.instance.placeholders.utils import (
    format_gis_center_coordinates,
    get_tel_and_email,
    get_yes_no,
    human_readable_date,
)
from camac.tests.data import (
    ag_personal_row_factory,
    so_fill_cantonal_exam,
    so_personal_row_factory,
)
from camac.tests.form_utils import FormUtils


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
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize("service_group__name", ["municipality"])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_gr(
    db,
    admin_user,
    admin_client,
    application_settings,
    gr_master_data_case,  # noqa
    settings,
    gr_instance,
    snapshot,
    gr_distribution_settings,
    service_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_question_factory,
    caluma_form_question_factory,
    keyword_factory,
    active_inquiry_factory,
    set_application_gr,
    gr_placeholders_settings,
    gr_dms_settings,
    gr_publication_settings,
    instance_service_factory,
    group,
    user_factory,
    responsible_service_factory,
    form_utils: FormUtils,
    gr_master_data_settings,
):
    instance_service_factory(instance=gr_instance, service=group.service, active=1)
    gr_instance.refresh_from_db()

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
    MarkFactory(slug="decision")
    tag = TagFactory(name="Secret")
    alexandria_category = CategoryFactory(
        metainfo={"access": {"municipality-lead": {"visibility": "all"}}}
    )
    alexandria_document = AlexandriaDocumentFactory(
        title="Grundriss",
        category=alexandria_category,
        metainfo={"camac-instance-id": str(gr_instance.pk)},
        marks=["decision"],
        tags=[tag],
        created_by_user=admin_client.user.pk,
        modified_by_user=admin_client.user.pk,
    )
    FileFactory(name="Situationsplan", document=alexandria_document, variant="original")

    # publication
    document = DocumentFactory()

    form_utils.add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    form_utils.add_answer(document, "publikation-text", "Text")
    form_utils.add_answer(
        document, "beginn-publikationsorgan-gemeinde", date(2021, 8, 20)
    )
    form_utils.add_answer(
        document, "ende-publikationsorgan-gemeinde", date(2021, 8, 21)
    )
    form_utils.add_answer(
        document, "beginn-publikation-kantonsamtsblatt", date(2021, 8, 22)
    )
    form_utils.add_answer(
        document, "ende-publikation-kantonsamtsblatt", date(2021, 8, 23)
    )

    form_utils.add_answer(document, "oeffentliche-auflage", ["oeffentliche-auflage-ja"])

    WorkItemFactory(
        case=gr_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(group.service_id)],
        document=document,
        meta={"is-published": True},
    )

    # shelter form
    form_utils.add_answer(
        gr_instance.case.document,
        "gebaeudeart",
        [
            "gebaeudeart-wohn-oder-ferienhaus",
            "gebaeudeart-spital-oder-heim",
            "gebaeudeart-andere",
        ],
        options=[
            ("gebaeudeart-wohn-oder-ferienhaus", "Wohn- oder Ferienhaus"),
            ("gebaeudeart-spital-oder-heim", "Spital oder Heim"),
            ("gebaeudeart-andere", "Andere"),
        ],
    )
    form_utils.add_answer(gr_instance.case.document, "wohnhaus-anzahl-zimmer", 100)
    form_utils.add_answer(
        gr_instance.case.document, "anzahl-schutzplaetze-wohnhaus", 50
    )
    form_utils.add_answer(gr_instance.case.document, "spital-anzahl-betten", 10)
    form_utils.add_answer(
        gr_instance.case.document, "flaeche-projektierte-schutzraeume", 20
    )
    form_utils.add_answer(
        gr_instance.case.document, "volumen-projektierte-schutzraeume", 30
    )
    form_utils.add_answer(
        gr_instance.case.document, "bemerkungen-schutzplaetze", "Foo bar baz"
    )

    # zones
    form_utils.add_answer(gr_instance.case.document, "zonenplan", "Rebwirtschaftszone")
    form_utils.add_answer(
        gr_instance.case.document, "genereller-gestaltungsplan", "Historischer Weg"
    )
    form_utils.add_answer(
        gr_instance.case.document,
        "genereller-erschliessungsplan",
        "Fuss- / Spazierweg, Parkierung Gebiete D",
    )
    form_utils.add_answer(
        gr_instance.case.document, "folgeplanung", "Baulinie allgemein"
    )

    # gis
    form_utils.add_answer(
        gr_instance.case.document,
        "gis-map",
        '{"markers": [{"x": 2569941.12345, "y": 1298923.12345}], "center": {"x": 2609995.12345,"y": 1271340.12345} }',
    )

    # Prepare project modification
    form_utils.add_answer(
        gr_instance.case.document, "beschreibung-projektaenderung", "Projektänderung"
    )

    # decision
    decision_work_item = caluma_work_item_factory(
        case=gr_instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="decision"),
    )
    decision_question = caluma_question_factory(
        slug="decision-decision", type=Question.TYPE_CHOICE
    )
    decision_date_question = caluma_question_factory(
        slug="decision-date", type=Question.TYPE_DATE
    )
    Option.objects.create(slug="decision-decision-approved", label="Bewilligt")
    caluma_form_question_factory(form_id="decision", question=decision_question)
    caluma_form_question_factory(form_id="decision", question=decision_date_question)
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
            value=f"Stellungnahme {i + 1}",
        )
        AnswerFactory(
            document=inquiry.child_case.document,
            question=nebenbestimmungen_question,
            value=f"Nebenbestimmungen {i + 1}",
        )

    form_utils.add_answer(
        gr_instance.case.document, "voraussichtliche-fertigstellung", date(2022, 12, 31)
    )

    admin_service = admin_user.groups.first().service
    kw_current1 = keyword_factory(name="keyword3", service=admin_service)
    kw_current2 = keyword_factory(name="keyword2", service=admin_service)
    kw_other1 = keyword_factory(name="keyword1", service=service_factory())
    gr_instance.keywords.set([kw_current1, kw_current2, kw_other1])

    url = reverse("instance-dms-placeholders", args=[gr_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.freeze_time("2024-01-18 13:37")
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_so(
    db,
    admin_client,
    billing_v2_entry_factory,
    group_factory,
    group,
    snapshot,
    set_application_so,
    so_distribution_settings,
    so_dms_settings,
    so_placeholders_settings,
    so_instance,
    service_factory,
    caluma_work_item_factory,
    caluma_dynamic_option_factory,
    mocker,
    multilang,
    form_utils: FormUtils,
    caluma_document_factory,
    active_inquiry_factory,
    master_data_is_visible_mock,
):
    # Authority
    authority = service_factory(
        trans__name="Test Leitbehörde",
        address="Teststrasse 13",
        zip="3000",
        website="https://leitbehoerde.ch",
        trans__city="Musterhausen",
        service_group__name="municipality",
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=authority
    )

    # Current service
    group.service.website = "https://meine-organisation.ch"
    group.service.save()

    # Municipality
    municipality = service_factory(website="https://gemeinde.ch")
    form_utils.add_answer(so_instance.case.document, "gemeinde", str(municipality.pk))
    caluma_dynamic_option_factory(
        slug=str(municipality.pk),
        question_id="gemeinde",
        document=so_instance.case.document,
    )

    # Land use
    form_utils.add_answer(
        so_instance.case.document,
        "nutzungsplanung-grundnutzung",
        "Wohnzone 3 - AZ 0.6",
    )
    form_utils.add_answer(
        so_instance.case.document,
        "nutzungsplanung-grundnutzung-kanton",
        "N112_Wohnzone_3_G",
    )

    # Billing
    billing_v2_entry_factory.create_batch(2, group=group, instance=so_instance)
    billing_v2_entry_factory.create_batch(
        2,
        group=group_factory(),
        instance=so_instance,
        legal_basis=None,
        cost_center=None,
    )

    # Builder
    form_utils.add_table_answer(
        so_instance.case.document,
        "bauherrin",
        [
            so_personal_row_factory(False, True),
            so_personal_row_factory(True),
            so_personal_row_factory(False, True, True),
        ],
        row_form_id="personalien-tabelle",
    )

    # Invoice recipients
    form_utils.add_table_answer(
        so_instance.case.document,
        "rechnungsempfaengerin",
        [so_personal_row_factory(), so_personal_row_factory(True)],
        row_form_id="personalien-tabelle",
    )

    # Objection
    objections_work_item = caluma_work_item_factory(
        task__pk="einsprachen",
        document__form_id="einsprachen",
        case=so_instance.case,
    )

    table_answer = form_utils.add_table_answer(
        objections_work_item.document,
        "einsprachen",
        [
            {"einsprache-datum": date(2023, 12, 12)},
            {"einsprache-datum": date(2023, 12, 22)},
        ],
        row_form_id="einsprache",
    )

    objections = table_answer.answerdocument_set.order_by("-sort")

    form_utils.add_table_answer(
        objections.first().document,
        "einsprache-einsprechende",
        [
            so_personal_row_factory(),
            so_personal_row_factory(),
        ],
        row_form_id="personalien-tabelle",
    )

    form_utils.add_table_answer(
        objections.last().document,
        "einsprache-einsprechende",
        [so_personal_row_factory(True)],
        row_form_id="personalien-tabelle",
    )

    # Publication
    publication_work_item = caluma_work_item_factory(
        case=so_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(service_factory().pk)],
        meta={"is-published": True},
    )

    form_utils.add_answer(
        publication_work_item.document, "publikation-start", date(2023, 12, 1)
    )
    form_utils.add_answer(
        publication_work_item.document, "publikation-ende", date(2023, 12, 15)
    )
    form_utils.add_answer(
        publication_work_item.document, "publikation-anzeiger", date(2023, 11, 28)
    )
    form_utils.add_answer(
        publication_work_item.document, "publikation-amtsblatt", date(2023, 11, 29)
    )
    form_utils.add_answer(
        publication_work_item.document,
        "publikation-organ",
        ["publikation-organ-amtsblatt", "publikation-organ-azeiger"],
        options=[
            ("publikation-organ-amtsblatt", "Amtsblatt"),
            ("publikation-organ-azeiger", "Azeiger"),
        ],
    )
    Option.objects.filter(pk="publikation-organ-amtsblatt").update(
        meta={"email": "amtsblatt@example.com"}
    )
    Option.objects.filter(pk="publikation-organ-azeiger").update(
        meta={"email": "azeiger@example.com"}
    )

    # Documents
    MarkFactory(slug="decision")

    FileFactory(
        document=AlexandriaDocumentFactory(
            title="Ausnahmebewilligung",
            category=CategoryFactory(
                slug="beilagen-zum-gesuch",
                metainfo={"access": {"Municipality": {"visibility": "all"}}},
            ),
            metainfo={"camac-instance-id": str(so_instance.pk)},
            created_by_user=admin_client.user.pk,
            modified_by_user=admin_client.user.pk,
        ),
        variant="original",
    )
    FileFactory(
        document=AlexandriaDocumentFactory(
            title="Situationsplan",
            category=CategoryFactory(
                slug="beilagen-zum-gesuch-projektplaene-projektbeschrieb",
                parent_id="beilagen-zum-gesuch",
                metainfo={"access": {"Municipality": {"visibility": "all"}}},
            ),
            metainfo={"camac-instance-id": str(so_instance.pk)},
            created_by_user=admin_client.user.pk,
            modified_by_user=admin_client.user.pk,
        ),
        variant="original",
    )
    FileFactory(
        document=AlexandriaDocumentFactory(
            title="Entscheid",
            category=CategoryFactory(
                slug="beteiligte-behoerden",
                metainfo={"access": {"Municipality": {"visibility": "all"}}},
            ),
            metainfo={"camac-instance-id": str(so_instance.pk)},
            marks=["decision"],
            created_by_user=admin_client.user.pk,
            modified_by_user=admin_client.user.pk,
        ),
        variant="original",
    )

    # Decision
    decision_work_item = caluma_work_item_factory(
        case=so_instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="entscheid"),
    )
    form_utils.add_answer(
        decision_work_item.document, "entscheid-datum", date(2024, 4, 18)
    )

    # General data
    form_utils.add_answer(so_instance.case.document, "ort", "Rüttenen")

    # Distribution
    inquiry = active_inquiry_factory(
        so_instance,
        service_factory(
            trans__name="Solothurnische Gebäudeversicherung (SGV)",
            service_group__name="service-cantonal",
        ),
        status=WorkItem.STATUS_COMPLETED,
        closed_at=make_aware(faker.Faker().date_time()),
    )

    # Draft inquiry
    active_inquiry_factory(
        so_instance,
        service_factory(
            trans__name="Amt für Umwelt (AfU)",
            service_group__name="service-cantonal",
        ),
        status=WorkItem.STATUS_SUSPENDED,
    )

    form_utils.add_answer(inquiry.document, "inquiry-remark", "Bemerkungen")

    for q, v in [
        ("inquiry-answer-status", "inquiry-answer-status-positive"),
        ("inquiry-answer-positive-assessments", "Zustimmend"),
        ("inquiry-answer-negative-assessments", "Ablehnend"),
        ("inquiry-answer-rejection-additional-demand", "Nachforderung"),
        ("inquiry-answer-objections", "Einsprachen"),
        ("inquiry-answer-notices-for-applicant", "Hinweis Gesuchsteller/in"),
        ("inquiry-answer-notices-for-authority", "Hinweis LB"),
        ("inquiry-answer-notices-for-authority-arp", "Hinweis ARP"),
        ("inquiry-answer-forward", "Weiterleiten an SGV"),
    ]:
        form_utils.add_answer(inquiry.child_case.document, q, v)

    inquiry.case.parent_work_item.closed_at = make_aware(faker.Faker().date_time())
    inquiry.case.parent_work_item.status = WorkItem.STATUS_COMPLETED
    inquiry.case.parent_work_item.save()

    # Cantonal exam
    cantonal_exam = caluma_work_item_factory(
        task_id="material-exam-bab", case=so_instance.case
    )
    so_fill_cantonal_exam(cantonal_exam.document, form_utils)

    url = reverse("instance-dms-placeholders", args=[so_instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


@pytest.mark.freeze_time("2021-08-30", tick=True)
@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_be(
    db,
    active_inquiry_factory,
    admin_client,
    settings,
    set_application_be,
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
    be_dms_settings,
    be_placeholders_settings,
    be_decision_settings,
    be_master_data_settings,
    be_publication_settings,
    form_utils: FormUtils,
):
    # publication
    document = DocumentFactory()

    form_utils.add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    form_utils.add_answer(document, "publikation-text", "Text")
    form_utils.add_answer(
        document,
        "publikation-1-publikation-anzeiger",
        date(2021, 8, 30),
    )
    form_utils.add_answer(
        document,
        "publikation-2-publikation-anzeiger",
        date(2021, 8, 20),
    )
    form_utils.add_answer(
        document,
        "publikation-amtsblatt",
        date(2021, 8, 10),
    )
    form_utils.add_answer(
        document,
        "publikation-startdatum",
        date(2021, 9, 1),
    )
    form_utils.add_answer(
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
    form_utils.add_answer(
        document, "beschreibung-projektaenderung", "Umbau Haus in Garage"
    )

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
    form_utils.add_table_answer(
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

    table_answer = form_utils.add_table_answer(
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

    form_utils.add_table_answer(
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

    form_utils.add_table_answer(
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

    form_utils.add_table_answer(
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
            value=f"Stellungnahme {i + 1}",
        )
        AnswerFactory(
            document=inquiry.child_case.document,
            question=nebenbestimmungen_question,
            value=f"Nebenbestimmungen {i + 1}",
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

    url = reverse("instance-dms-placeholders", args=[be_instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.freeze_time("2021-08-30")
@pytest.mark.parametrize(
    "role__name,app_instance,any_application",
    [
        pytest.param(
            "municipality-admin",
            lf("be_instance"),
            "kt_bern",
            id="Municipality",
        ),
    ],
    indirect=["any_application"],
)
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_empty(
    db,
    admin_client,
    application_settings,
    settings,
    any_application,
    app_instance,
    snapshot,
    mocker,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=None
    )

    response = admin_client.get(
        reverse("instance-dms-placeholders", args=[app_instance.pk])
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


def test_dms_placeholders_docs(
    admin_client, snapshot, any_application, try_get_fixture
):
    try_get_fixture("placeholders_settings", any_application)

    response = admin_client.get(reverse("dms-placeholders-docs"))
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize(
    "app",
    [
        lf("set_application_ag"),
        lf("set_application_be"),
        lf("set_application_gr"),
        lf("set_application_so"),
        lf("set_application_sz"),
    ],
)
def test_dms_placeholders_docs_available_placeholders(
    admin_client, snapshot, app, try_get_fixture
):
    try_get_fixture("dms_settings", app)
    try_get_fixture("placeholders_settings", app)
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


@pytest.mark.freeze_time("2024-01-18 13:37", tick=True)
@pytest.mark.parametrize("role__name", ["Sekretariat der Gemeindebaubehörde"])
def test_dms_placeholders_ur(
    db,
    snapshot,
    set_application_ur,
    ur_placeholders_settings,
    ur_dms_settings,
    ur_permissions_settings,
    admin_client,
    ur_instance,
    ur_distribution_settings,
    caluma_dynamic_option_factory,
    service_factory,
    group_factory,
    location_factory,
    ur_master_data_case,
    caluma_question_factory,
    caluma_answer_factory,
    caluma_document_factory,
    publication_entry_factory,
    caluma_work_item_factory,
    active_inquiry_factory,
):
    # Municipality
    municipality = service_factory(
        website="https://gemeinde.ch",
        service_group__name="Sekretariate Gemeindebaubehörden",
    )
    location = location_factory(communal_federal_number=1)
    group = group_factory()
    group.locations.set([location])
    municipality.groups.set([group])

    form_api.save_answer(
        caluma_form_models.Question.objects.get(pk="municipality"),
        ur_master_data_case.document,
        value="1",
    )
    complete_check_work_item = WorkItemFactory(
        task_id="complete-check",
        case=ur_instance.case,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="complete-check"),
    )
    caluma_answer_factory(
        document=complete_check_work_item.document,
        question__slug="complete-check-vollstaendigkeitspruefung",
        value="complete-check-vollstaendigkeitspruefung-complete",
    )
    publication_entry_factory(
        instance=ur_instance,
        publication_date=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        publication_end_date=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        is_published=True,
    )
    work_item = WorkItemFactory(
        task_id="instance-management",
        case=ur_instance.case,
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        document=work_item.document,
        question__slug="pruefung-durch-gemeinde",
        date=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
    )

    # Inquiriy
    active_inquiry_factory(
        ur_instance,
        status=WorkItem.STATUS_COMPLETED,
        closed_at=make_aware(faker.Faker().date_time()),
    )

    url = reverse("instance-dms-placeholders", args=[ur_instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    checked_keys = [
        "GEMEINDE",
        "ZONE",
        "HAUSNUMMER",
        "PUBLIKATIONSDATUM",
        "DATUM_PRUEFUNG_DURCH_GEMEINDE",
        "DATUM_DOSSIER_VOLLSTAENDIG",
    ]

    assert {
        key: value for key, value in response.json().items() if key in checked_keys
    } == snapshot


@pytest.mark.freeze_time("2016-06-06 13:37", tick=True)
@pytest.mark.parametrize(
    "role__name,service_group__name", [("municipality-lead", "municipality")]
)
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_dms_placeholders_ag(
    db,
    admin_client,
    admin_user,
    set_application_ag,
    ag_distribution_settings,
    ag_dms_settings,
    ag_placeholders_settings,
    ag_master_data_case,
    ag_publication_settings,
    billing_v2_entry_factory,
    create_caluma_publication,
    group,
    multilang,
    responsible_service_factory,
    service,
    snapshot,
    form_utils: FormUtils,
):
    ag_instance = ag_master_data_case.instance

    # GIS
    form_utils.add_answer(
        ag_instance.case.document,
        "gis-map",
        '{"markers": [{"x": 2569941.12345, "y": 1298923.12345}, {"x": 2609995.12345,"y": 1271340.12345}] }',
    )

    # Current service
    service_t = service.trans.first()
    service_t.department = "Departement Bau, Verkehr und Umwelt"
    service_t.save()

    # Responsible user
    responsible_service_factory(
        instance=ag_instance,
        service=service,
        responsible_user__name="John",
        responsible_user__surname="Doe",
        responsible_user__email="john.doe@acme.com",
        responsible_user__phone="012 345 67 89",
        responsible_user__title="Master of Science",
        responsible_user__position="Projektleiter",
        responsible_user__mobile="079 345 67 89",
    )

    # Publication
    publication = create_caluma_publication(
        ag_instance,
        module_settings=ag_publication_settings,
        addressed_groups=[str(service.pk)],
        end=date(2025, 7, 1),
    )
    form_utils.add_answer(
        publication.document, "publikation-text", "Text zur Publikation"
    )
    form_utils.add_answer(
        publication.document, "ende-publikation-kantonsamtsblatt", date(2025, 8, 1)
    )

    # Information of neighbors
    information_of_neighbors = create_caluma_publication(
        ag_instance,
        publication_type="NEIGHBORS",
        module_settings=ag_publication_settings,
        addressed_groups=[str(service.pk)],
        document__pk="878109fb-24c4-43e8-a00f-76999ca0f531",
    )
    form_utils.add_table_answer(
        information_of_neighbors.document,
        "nachbarschaftsorientierung-auswaertige-anstoesser",
        [ag_personal_row_factory(), ag_personal_row_factory(True)],
    )

    # Billing
    billing_v2_entry_factory(
        text="Nutzungsbewilligung",
        final_rate=200,
        remark="Nr. 1234",
        group=group,
        instance=ag_instance,
    )

    # Current user
    admin_user.mobile = "+41 79 012 34 56"
    admin_user.phone = "+41 31 012 34 56"
    admin_user.title = "Master of Science"
    admin_user.position = "Project manager"
    admin_user.save()

    url = reverse("instance-dms-placeholders", args=[ag_instance.pk])

    response = admin_client.get(url)
    result = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert result == snapshot

    # Remove invoice recipient
    ag_instance.case.document.answers.filter(
        question_id="personalien-rechnungsempfaenger"
    ).delete()

    fallback_response = admin_client.get(url)
    fallback_result = fallback_response.json()
    assert fallback_response.status_code == status.HTTP_200_OK

    for a_prop, ir_prop in [
        ("GESUCHSTELLER", "RECHNUNGSEMPFAENGER"),
        ("GESUCHSTELLER_ADRESSE_1", "RECHNUNGSEMPFAENGER_ADRESSE_1"),
        ("GESUCHSTELLER_ADRESSE_2", "RECHNUNGSEMPFAENGER_ADRESSE_2"),
    ]:
        # Make sure fallback is not used if invoice recipient is available
        assert result[ir_prop] != result[a_prop]
        # Make sure fallback is used if invoice recipient is not available
        assert fallback_result[ir_prop] == fallback_result[a_prop]


# Currently failing, but once it's configured properly, we need to revisit this
# test and fix it (thus, strict=True)
@pytest.mark.xfail(reason="SZ has no dms settings right now", strict=True)
@pytest.mark.parametrize("role__name", ["Gemeinde"])
def test_dms_placeholders_sz(
    db,
    admin_client,
    sz_master_data_case,
    sz_instance,
    sz_dms_settings,
    sz_placeholders_settings,
    snapshot,
):  # pragma: no cover
    response = admin_client.get(
        reverse("instance-dms-placeholders", args=[sz_instance.pk])
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot
    case_fn = getattr(str, sz_placeholders_settings["PLACEHOLDER_CASE"])
    for key in response.json().keys():
        assert key == case_fn(key)


@pytest.mark.parametrize(
    "options,expected",
    [
        ([False, True], "Ja"),
        ([False, False], "Nein"),
        (True, "Ja"),
        (False, "Nein"),
    ],
)
def test_yes_no(options, expected):
    assert get_yes_no(options) == expected


@pytest.mark.parametrize(
    "available_data,expected",
    [
        # ignore empty/invalid date
        (None, None),
        ("", None),
        ("{invalid-json}", None),
        (
            '{"valid-no-center": {"x": 2760558.123, "y": 1170288.456}}',
            None,
        ),
        # use center if provided
        (
            '{"center": {"x": 2760558.123, "y": 1170288.456}}',
            "2'760'558 / 1'170'288",
        ),
        # fallback to first marker if no center is provided
        (
            '{"markers": [{"x": 2760558.123, "y": 1170288.456}, {"x": 2609995.123, "y": 1271340.456}]}',
            "2'760'558 / 1'170'288",
        ),
        # ignore markers if valid center is provided
        (
            '{"markers": [{"x": 2569941.123, "y": 1298923.123}, {"x": 2609995.123, "y": 1271340.456}], "center": {"x": 2760558.123, "y": 1170288.456}}',
            "2'760'558 / 1'170'288",
        ),
    ],
)
def test_format_gis_center_coordinates(
    available_data,
    expected,
):
    assert format_gis_center_coordinates(available_data) == expected


@pytest.mark.parametrize(
    "coord_east,coord_north,expected",
    [
        # no rounding
        (2760558.123, 1170288.456, "2’760’558 / 1’170’288"),
        # rounded up
        (2760558.567, 1170288.899, "2’760’559 / 1’170’289"),
        (2701783.599, 1171109.999, "2’701’784 / 1’171’110"),
    ],
)
def test_get_koordinaten(coord_east, coord_north, expected, mocker):
    master_data_mock = Mock()
    master_data_mock.plot_data = [
        {"coord_east": coord_east, "coord_north": coord_north}
    ]

    instance_mock = Mock()
    mocker.patch(
        "camac.instance.master_data.MasterData.from_case_id",
        return_value=master_data_mock,
    )

    assert (
        DMSPlaceholdersSerializer(instance_mock).get_koordinaten(instance_mock)
        == expected
    )


@pytest.mark.parametrize(
    "is_collection",
    [
        pytest.param(True, id="is_collection: append [] to placholder name"),
        pytest.param(
            False,
            id="~is_collection: no [] appended to placeholder name, unless nested_aliases given",
        ),
    ],
)
def test_aliased_placeholder_field(
    db,
    fake_request,
    service_group,
    request_mock,
    sz_master_data_case,
    is_collection,
    snapshot,
):
    testfields = ["test_literal_field", "test_list_field", "test_nested_field"]

    class PlaceholderTestSerializer(DMSPlaceholdersSerializer):
        test_literal_field = MasterDataField(aliases=[_("TEST_CAT"), _("TEST_BAT")])
        test_list_field = MasterDataField(
            aliases=[_("TEST_LIST_CATS"), _("TEST_LIST_BATS")],
            is_collection=is_collection,
        )
        test_nested_field = MasterDataField(
            aliases=[_("TEST_CAT_OBJECTS"), _("TEST_BAT_OBJECTS")],
            is_collection=is_collection,
            nested_aliases={"NAME": [_("TEST_CAT")], "NESTED.NAME": [_("TEST_BAT")]},
        )

        class Meta:
            # ignore BaseClass' declared fields
            exclude = list(DMSPlaceholdersSerializer._declared_fields.keys())

    serializer = PlaceholderTestSerializer(
        instance=sz_master_data_case.instance, context={"request": fake_request}
    )

    for field_name in testfields:
        field = serializer.fields[field_name]
        assert field.get_docs() == snapshot
        assert field.make_placeholders() == snapshot
