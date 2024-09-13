import pathlib
from datetime import date

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
from django.utils.timezone import make_aware
from django.utils.translation import override
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.instance.placeholders.utils import get_tel_and_email, human_readable_date
from camac.tests.data import so_personal_row_factory

from .test_master_data import be_master_data_case, gr_master_data_case  # noqa


@pytest.fixture
def be_dms_config(settings, be_placeholders_settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name) for code, name in settings.LANGUAGES if code in ["de", "fr"]
    ]
    settings.APPLICATION_NAME = "kt_bern"
    settings.INTERNAL_BASE_URL = "http://ebau.local"
    yield
    settings.LANGUAGES = original_languages


@pytest.fixture
def gr_dms_config(settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name) for code, name in settings.LANGUAGES if code in ["de", "it"]
    ]
    settings.APPLICATION_NAME = "kt_gr"
    settings.INTERNAL_BASE_URL = "http://ember-ebau.local"
    yield
    settings.LANGUAGES = original_languages


@pytest.fixture
def so_dms_config(settings, application_settings, so_placeholders_settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name) for code, name in settings.LANGUAGES if code in ["de"]
    ]
    settings.APPLICATION_NAME = "kt_so"
    settings.INTERNAL_BASE_URL = "http://ember-ebau.local"
    application_settings["SHORT_NAME"] = "so"
    yield
    settings.LANGUAGES = original_languages


@pytest.fixture
def ur_dms_config(settings, application_settings):
    original_languages = settings.LANGUAGES
    settings.LANGUAGES = [
        (code, name) for code, name in settings.LANGUAGES if code in ["de"]
    ]
    settings.APPLICATION_NAME = "kt_uri"
    settings.INTERNAL_BASE_URL = "http://ember.local"
    application_settings["SHORT_NAME"] = "ur"
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
@pytest.mark.parametrize("role__name", ["municipality-lead"])
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
    utils,
    gr_master_data_settings,
):
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_gr",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )

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

    utils.add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    utils.add_answer(document, "publikation-text", "Text")
    utils.add_answer(document, "beginn-publikationsorgan-gemeinde", date(2021, 8, 20))
    utils.add_answer(document, "ende-publikationsorgan-gemeinde", date(2021, 8, 21))
    utils.add_answer(document, "beginn-publikation-kantonsamtsblatt", date(2021, 8, 22))
    utils.add_answer(document, "ende-publikation-kantonsamtsblatt", date(2021, 8, 23))

    WorkItemFactory(
        case=gr_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(group.service_id)],
        document=document,
        meta={"is-published": True},
    )

    # shelter form
    utils.add_answer(
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
    utils.add_answer(gr_instance.case.document, "wohnhaus-anzahl-zimmer", 100)
    utils.add_answer(gr_instance.case.document, "anzahl-schutzplaetze-wohnhaus", 50)
    utils.add_answer(gr_instance.case.document, "spital-anzahl-betten", 10)
    utils.add_answer(gr_instance.case.document, "flaeche-projektierte-schutzraeume", 20)
    utils.add_answer(gr_instance.case.document, "volumen-projektierte-schutzraeume", 30)
    utils.add_answer(
        gr_instance.case.document, "bemerkungen-schutzplaetze", "Foo bar baz"
    )

    # zones
    utils.add_answer(gr_instance.case.document, "zonenplan", "Rebwirtschaftszone")
    utils.add_answer(
        gr_instance.case.document, "genereller-gestaltungsplan", "Historischer Weg"
    )
    utils.add_answer(
        gr_instance.case.document,
        "genereller-erschliessungsplan",
        "Fuss- / Spazierweg, Parkierung Gebiete D",
    )
    utils.add_answer(gr_instance.case.document, "folgeplanung", "Baulinie allgemein")

    # gis
    utils.add_answer(
        gr_instance.case.document,
        "gis-map",
        '{"markers": [{"x": 2569941.12345, "y": 1298923.12345}, {"x": 2609995.12345,"y": 1271340.12345}] }',
    )

    # Prepare project modification
    utils.add_answer(
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


@pytest.mark.freeze_time("2024-01-18 13:37", tick=True)
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_dms_placeholders_so(
    db,
    admin_client,
    billing_v2_entry_factory,
    group_factory,
    group,
    snapshot,
    so_distribution_settings,
    so_dms_config,
    so_instance,
    service_factory,
    work_item_factory,
    dynamic_option_factory,
    mocker,
    multilang,
    utils,
    document_factory,
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
    utils.add_answer(so_instance.case.document, "gemeinde", str(municipality.pk))
    dynamic_option_factory(
        slug=str(municipality.pk),
        question_id="gemeinde",
        document=so_instance.case.document,
    )
    mocker.patch(
        "camac.instance.master_data.MasterData._answer_is_visible", return_value=True
    )

    # Land use
    utils.add_answer(
        so_instance.case.document,
        "nutzungsplanung-grundnutzung",
        "Wohnzone 3 - AZ 0.6",
    )
    utils.add_answer(
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
    utils.add_table_answer(
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
    utils.add_table_answer(
        so_instance.case.document,
        "rechnungsempfaengerin",
        [so_personal_row_factory(), so_personal_row_factory(True)],
        row_form_id="personalien-tabelle",
    )

    # Objection
    objections_work_item = work_item_factory(
        task_id="einsprachen",
        document__form_id="einsprachen",
        case=so_instance.case,
    )

    table_answer = utils.add_table_answer(
        objections_work_item.document,
        "einsprachen",
        [
            {"einsprache-datum": date(2023, 12, 12)},
            {"einsprache-datum": date(2023, 12, 22)},
        ],
        row_form_id="einsprache",
    )

    objections = table_answer.answerdocument_set.order_by("-sort")

    utils.add_table_answer(
        objections.first().document,
        "einsprache-einsprechende",
        [
            so_personal_row_factory(),
            so_personal_row_factory(),
        ],
        row_form_id="personalien-tabelle",
    )

    utils.add_table_answer(
        objections.last().document,
        "einsprache-einsprechende",
        [so_personal_row_factory(True)],
        row_form_id="personalien-tabelle",
    )

    # Publication
    publication_work_item = work_item_factory(
        case=so_instance.case,
        task_id="fill-publication",
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(service_factory().pk)],
        meta={"is-published": True},
    )

    utils.add_answer(
        publication_work_item.document, "publikation-start", date(2023, 12, 1)
    )
    utils.add_answer(
        publication_work_item.document, "publikation-ende", date(2023, 12, 15)
    )
    utils.add_answer(
        publication_work_item.document, "publikation-anzeiger", date(2023, 11, 28)
    )
    utils.add_answer(
        publication_work_item.document, "publikation-amtsblatt", date(2023, 11, 29)
    )
    utils.add_answer(
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
    decision_work_item = work_item_factory(
        case=so_instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form_id="entscheid"),
    )
    utils.add_answer(decision_work_item.document, "entscheid-datum", date(2024, 4, 18))

    url = reverse("instance-dms-placeholders", args=[so_instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    checked_keys = [
        "ALLE_GESUCHSTELLER_LISTE",
        "ALLE_GESUCHSTELLER_VERTRETER_NAME_ADRESSE",
        "ALLE_GESUCHSTELLER_VERTRETER",
        "ALLE_GRUNDEIGENTUEMER_LISTE",
        "ALLE_PROJEKTVERFASSER_LISTE",
        "ALLE_RECHNUNGSEMPFAENGER_LISTE",
        "ALLE_RECHNUNGSEMPFAENGER_NAME_ADRESSE",
        "ALLE_RECHNUNGSEMPFAENGER",
        "ANGEMELDET_EMAIL",
        "ANGEMELDET_NAME",
        "BAUENTSCHEID_DATUM",
        "EIGENE_GEBUEHREN_TOTAL",
        "EIGENE_GEBUEHREN",
        "EINGEREICHTE_PLAENE",
        "EINGEREICHTE_UNTERLAGEN",
        "EINSPRACHEN",
        "ENTSCHEIDDOKUMENTE",
        "GEBUEHREN_TOTAL",
        "GEBUEHREN",
        "GEMEINDE_WEBSEITE",
        "GESUCHSTELLER_ANREDE",
        "GESUCHSTELLER_VERTRETER_ADRESSE_1",
        "GESUCHSTELLER_VERTRETER_ADRESSE_2",
        "GESUCHSTELLER_VERTRETER_NAME_ADRESSE",
        "GESUCHSTELLER_VERTRETER",
        "LEITBEHOERDE_NAME_ADRESSE",
        "LEITBEHOERDE_WEBSEITE",
        "MEINE_ORGANISATION_WEBSEITE",
        "NUTZUNGSPLANUNG_GRUNDNUTZUNG",
        "NUTZUNGSPLANUNG_GRUNDNUTZUNG_KANTON",
        "PUBLIKATION_AMTSBLATT",
        "PUBLIKATION_ANZEIGER",
        "PUBLIKATION_ENDE",
        "PUBLIKATION_ORGAN",
        "PUBLIKATION_START",
        "RECHNUNGSEMPFAENGER_ADRESSE_1",
        "RECHNUNGSEMPFAENGER_ADRESSE_2",
        "RECHNUNGSEMPFAENGER_NAME_ADRESSE",
        "RECHNUNGSEMPFAENGER",
    ]

    assert {
        key: value for key, value in response.json().items() if key in checked_keys
    } == snapshot


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
    be_master_data_settings,
    utils,
):
    application_settings["INTERNAL_FRONTEND"] = "camac"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )

    # publication
    document = DocumentFactory()

    utils.add_answer(document, "publikation-anzeiger-von", "Bärnerblatt")
    utils.add_answer(document, "publikation-text", "Text")
    utils.add_answer(
        document,
        "publikation-1-publikation-anzeiger",
        date(2021, 8, 30),
    )
    utils.add_answer(
        document,
        "publikation-2-publikation-anzeiger",
        date(2021, 8, 20),
    )
    utils.add_answer(
        document,
        "publikation-amtsblatt",
        date(2021, 8, 10),
    )
    utils.add_answer(
        document,
        "publikation-startdatum",
        date(2021, 9, 1),
    )
    utils.add_answer(
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
    utils.add_answer(document, "beschreibung-projektaenderung", "Umbau Haus in Garage")

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
    utils.add_table_answer(
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

    table_answer = utils.add_table_answer(
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

    utils.add_table_answer(
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

    utils.add_table_answer(
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

    utils.add_table_answer(
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
    be_master_data_settings,
):
    application_settings["INTERNAL_FRONTEND"] = "camac"
    application_settings["MUNICIPALITY_DATA_SHEET"] = settings.ROOT_DIR(
        "kt_bern",
        pathlib.Path(settings.APPLICATIONS["kt_bern"]["MUNICIPALITY_DATA_SHEET"]).name,
    )

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


@pytest.mark.parametrize(
    "dms_config",
    [
        lf("be_dms_config"),
        lf("gr_dms_config"),
        lf("so_dms_config"),
    ],
)
def test_dms_placeholders_docs(admin_client, snapshot, dms_config):
    response = admin_client.get(reverse("dms-placeholders-docs"))
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize(
    "dms_config",
    [
        lf("be_dms_config"),
        lf("gr_dms_config"),
        lf("so_dms_config"),
    ],
)
def test_dms_placeholders_docs_available_placeholders(
    admin_client, snapshot, dms_config
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


@pytest.mark.freeze_time("2024-01-18 13:37", tick=True)
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_dms_placeholders_ur(
    db,
    snapshot,
    ur_dms_config,
    admin_client,
    ur_instance,
    ur_distribution_settings,
    utils,
    dynamic_option_factory,
    service_factory,
    group_factory,
    location_factory,
    ur_master_data_case,
    question_factory,
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

    url = reverse("instance-dms-placeholders", args=[ur_instance.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    checked_keys = ["GEMEINDE", "ZONE"]

    assert {
        key: value for key, value in response.json().items() if key in checked_keys
    } == snapshot
