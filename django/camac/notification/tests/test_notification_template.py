import functools
import re
from datetime import datetime

import pytest
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_form.factories import QuestionFactory
from caluma.caluma_workflow import (
    api as workflow_api,
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.conftest import CALUMA_FORM_TYPES_SLUGS, FakeRequest
from camac.instance.models import HistoryEntry
from camac.instance.tests.test_master_data import add_answer, add_table_answer
from camac.notification import serializers
from camac.notification.serializers import (
    InstanceMergeSerializer,
    PermissionlessNotificationTemplateSendmailSerializer,
)


@pytest.mark.parametrize(
    "role__name,num_queries,size,notification_template__type,notification_template__service",
    [
        ("Applicant", 1, 0, "email", LazyFixture("service")),
        ("Service", 2, 1, "email", LazyFixture("service")),
        ("Municipality", 2, 1, "email", None),
        ("Canton", 2, 1, "textcomponent", None),
        ("Service", 2, 1, "textcomponent", LazyFixture("service")),
        ("Geometer", 2, 1, "textcomponent", LazyFixture("service")),
    ],
)
def test_notification_template_list(
    admin_client, notification_template, num_queries, django_assert_num_queries, size
):
    url = reverse("notificationtemplate-list")
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    if size > 0:
        json = response.json()
        assert len(json["data"]) == size
        assert json["data"][0]["id"] == str(notification_template.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
        ("Geometer", status.HTTP_200_OK),
    ],
)
def test_notification_template_update(admin_client, notification_template, status_code):
    url = reverse("notificationtemplate-detail", args=[notification_template.pk])
    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_201_CREATED),
        ("Service", status.HTTP_201_CREATED),
        ("Municipality", status.HTTP_201_CREATED),
        ("Geometer", status.HTTP_201_CREATED),
    ],
)
def test_notification_template_create(admin_client, notification_template, status_code):
    url = reverse("notificationtemplate-list")

    data = {
        "data": {
            "type": "notification-templates",
            "id": None,
            "attributes": {
                "slug": "test",
                "body": "Test",
                "purpose": "Test",
                "notification-type": "textcomponent",
                "subject": "Test",
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["attributes"]["notification-type"] == "textcomponent"


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
        ("Geometer", status.HTTP_204_NO_CONTENT),
    ],
)
def test_notification_template_destroy(
    admin_client, notification_template, status_code
):
    url = reverse("notificationtemplate-detail", args=[notification_template.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,instance__identifier,notification_template__subject,status_code",
    [
        ("Canton", "identifier", "{{identifier}}", status.HTTP_200_OK),
        ("Canton", "identifier", "{{$invalid}}", status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.freeze_time("2017-1-1")
def test_notification_template_merge(
    admin_client,
    sz_instance,
    notification_template,
    status_code,
    billing_entry,
    application_settings,
    form_field_factory,
    publication_entry,
    work_item_factory,
    document_factory,
    settings,
    snapshot,
):
    notification_template.body = """
        identifier: {{identifier}}
        answer_period_date: {{answer_period_date}}
        field_punkte: {{field_punkte}}
        field_bezeichnung: {{field_bezeichnung}}
        field_durchmesser_der_bohrung: {{field_durchmesser_der_bohrung}}
        billing_entries:{% for b in billing_entries %}
            - {{b.service}}: {{b.amount}} CHF, erstellt am {{b.created}} auf Kostenstelle {{b.account}} (Nr. {{b.account_number}}){% endfor %}
        bauverwaltung:
            - beschwerdeverfahren_weiterzug_durch: {{bauverwaltung.beschwerdeverfahren_weiterzug_durch}}
            - bewilligungsverfahren_gr_sitzung_beschluss: {{bauverwaltung.bewilligungsverfahren_gr_sitzung_beschluss}}
            - bewilligungsverfahren_gr_sitzung_datum: {{bauverwaltung.bewilligungsverfahren_gr_sitzung_datum}}
            - bewilligungsverfahren_gr_sitzung_bewilligungsdatum: {{bauverwaltung.bewilligungsverfahren_gr_sitzung_bewilligungsdatum}}
            - beschwerdeverfahren: {{bauverwaltung.beschwerdeverfahren}}
            - baukontrolle_realisierung_table: {{bauverwaltung.baukontrolle_realisierung_table}}
            - bewilligungsverfahren_sistierung: {{bauverwaltung.bewilligungsverfahren_sistierung}}
            - bewilligungsverfahren_sitzung_baukommission:{% for bv in bauverwaltung.bewilligungsverfahren_sitzung_baukommission %}
                - Bemerkung: {{bv.bewilligungsverfahren_sitzung_baukommission_bemerkung}}, Nr: {{bv.bewilligungsverfahren_sitzung_baukommission_nr}}{% endfor %}
        publications:{% for p in publications %}
            - {{p.date}} - {{p.end_date}} (W{{p.calendar_week}}){% endfor %}
    """
    notification_template.save()

    call_command(
        "loaddata", settings.ROOT_DIR("kt_schwyz/config/buildingauthority.json")
    )
    call_command("loaddata", settings.ROOT_DIR("kt_schwyz/config/caluma_form.json"))

    application_settings["COORDINATE_QUESTION"] = "punkte"
    application_settings["QUESTIONS_WITH_OVERRIDE"] = ["bezeichnung"]
    application_settings["LOCATION_NAME_QUESTION"] = "durchmesser-der-bohrung"
    application_settings["INSTANCE_MERGE_CONFIG"] = {
        "BAUVERWALTUNG": {
            "TASK_SLUG": "building-authority",
        }
    }

    work_item = work_item_factory(task_id="building-authority", case=sz_instance.case)
    work_item.document = document_factory(form_id="bauverwaltung")
    work_item.save()
    add_answer(work_item.document, "bewilligungsverfahren-gr-sitzung-beschluss", "foo")
    add_answer(
        work_item.document,
        "beschwerdeverfahren-weiterzug-durch",
        "beschwerdeverfahren-weiterzug-durch-beschwerdegegner",
    )
    add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-datum",
        timezone.now(),
        "date",
    )
    add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        timezone.now(),
    )
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

    add_field = functools.partial(form_field_factory, instance=sz_instance)
    add_field(
        name="punkte", value=[{"lat": 47.02433179952733, "lng": 8.634144559228435}]
    )
    add_field(name="bezeichnung", value="abc")
    add_field(name="bezeichnung-override", value="abc")
    add_field(name="durchmesser-der-bohrung", value=1)

    publication_entry.is_published = 1
    publication_entry.save()

    url = reverse("notificationtemplate-merge", args=[notification_template.pk])

    response = admin_client.get(url, data={"instance": sz_instance.pk})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["subject"] == sz_instance.identifier
        assert json["data"]["id"] == "{0}-{1}".format(
            notification_template.slug, sz_instance.pk
        )
        assert json["data"]["type"] == "notification-template-merges"

        snapshot.assert_match(json["data"]["attributes"]["body"])


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_notification_template_sendmail_exception_handling(
    db,
    admin_client,
    activation_factory,
    mocker,
    notification_template,
    be_instance,
    circulation,
    mailoutbox,
    service_factory,
    caplog,
    settings,
):
    settings.ADMINS = [("Admin", "admin@example.com")]
    original_send = EmailMessage.send

    def on_send(self, *args, **kwargs):
        if "not.an.email" in self.to:
            raise Exception("Invalid E-Mail")
        original_send(self, *args, **kwargs)

    mocker.patch("django.core.mail.EmailMessage.send", new=on_send)

    admin_service = admin_client.user.groups.first().service
    activation_factory(
        circulation=circulation,
        email_sent=0,
        service_parent=admin_service,
        service=service_factory(email="valid@example.com"),
    )
    activation_factory(
        circulation=circulation,
        email_sent=0,
        service_parent=admin_service,
        service=service_factory(email="not.an.email"),
    )
    activation_factory(
        circulation=circulation,
        email_sent=0,
        service_parent=admin_service,
        service=service_factory(email="fine@example.com"),
    )
    be_instance.case.document.answers.create(
        question_id="gemeinde", value=str(be_instance.responsible_service().pk)
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": [
                    "unnotified_service",
                ],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": be_instance.pk}},
                "circulation": {"data": {"type": "circulations", "id": circulation.pk}},
            },
        }
    }

    url = reverse("notificationtemplate-sendmail")

    admin_client.post(url, data=data)
    assert len(mailoutbox) == 3
    expected_subject = f"[eBau Test]: {notification_template.subject}"
    assert sorted([(m.to, m.subject) for m in mailoutbox]) == [
        (
            ["admin@example.com"],
            "[Django] ERROR: Failed to send 1 emails: to ['not.an.email'], cc []: Invalid E-Mail",
        ),
        (["fine@example.com"], expected_subject),
        (["valid@example.com"], expected_subject),
    ]


@pytest.mark.parametrize(
    "user__email,service__email",
    [("user@example.com", "service@example.com, service2@example.com")],
)
@pytest.mark.parametrize(
    "notification_template__subject,instance__identifier",
    [("{{identifier}}", "identifer")],
)
@pytest.mark.parametrize("new_responsible_model", [True, False])
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_400_BAD_REQUEST),
        ("Coordination", status.HTTP_204_NO_CONTENT),
    ],
)
def test_notification_template_sendmail(
    db,
    admin_client,
    be_instance,
    responsible_service_factory,
    instance_responsibility_factory,
    notification_template,
    status_code,
    mailoutbox,
    activation,
    new_responsible_model,
    settings,
):
    url = reverse("notificationtemplate-sendmail")
    if new_responsible_model:
        responsible = instance_responsibility_factory(
            instance=be_instance, service=be_instance.responsible_service()
        )
        responsible_email = responsible.user.email
    else:
        responsible = responsible_service_factory(
            instance=be_instance, service=be_instance.responsible_service()
        )
        responsible_email = responsible.responsible_user.email

    be_instance.case.document.answers.create(
        question_id="gemeinde", value=str(be_instance.responsible_service().pk)
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": [
                    "applicant",
                    "municipality",
                    "leitbehoerde",
                    "unnotified_service",
                    "activation_service_parent",
                    "caluma_municipality",
                ],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": be_instance.pk}},
                "activation": {"data": {"type": "activations", "id": activation.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_204_NO_CONTENT:
        assert len(mailoutbox) == 5

        # recipient types are sorted alphabetically
        assert [(m.to, m.cc) for m in mailoutbox] == [
            (
                [responsible_email],
                ["service@example.com", "service2@example.com"],
            ),  # activation parent service
            (["user@example.com"], []),  # applicant
            (
                [responsible_email],
                ["service@example.com", "service2@example.com"],
            ),  # caluma municipality
            (
                [responsible_email],
                ["service@example.com", "service2@example.com"],
            ),  # leitbehoerde
            (
                [responsible_email],
                ["service@example.com", "service2@example.com"],
            ),  # municipality
        ]
        assert (
            mailoutbox[0].subject
            == settings.EMAIL_PREFIX_SUBJECT + be_instance.identifier
        )
        assert mailoutbox[0].body == settings.EMAIL_PREFIX_BODY + "Test body"


@pytest.mark.parametrize(
    "form_name,expected_recipients",
    [
        ("baugesuch", ["info@aib.gr.ch"]),
        ("solaranlage", ["info@aib.gr.ch"]),
        ("bauanzeige", ["info@aib.gr.ch"]),
        ("vorlaeufige-beurteilung", []),
    ],
)
@pytest.mark.parametrize(
    "role__name",
    ["Municipality"],
)
def test_notification_template_construction_acceptance(
    caluma_admin_user,
    gr_instance,
    caluma_workflow_config_gr,
    settings,
    form_name,
    mailoutbox,
    expected_recipients,
    application_settings,
    instance_state_factory,
    notification_template_factory,
    gr_decision_settings,
):
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"]["construction-acceptance"][
        "notification"
    ]["conditions"] = {"forms": ["baugesuch", "bauanzeige", "solaranlage"]}
    instance_state_factory(name="finished")
    instance_state_factory(name="construction-acceptance")
    notification_template_factory(slug="bauabnahme")

    gr_instance.case.document.form = caluma_form_models.Form.objects.create(
        pk=form_name
    )
    gr_instance.case.document.save()

    for task_id in [
        "submit",
        "formal-exam",
        "distribution",
        "decision",
    ]:
        if task_id == "decision":
            QuestionFactory(slug="decision-decision")
            gr_instance.case.work_items.get(task_id=task_id).document.answers.create(
                question_id="decision-decision", value="decision-decision-approved"
            )
        workflow_api.skip_work_item(
            work_item=gr_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    workflow_api.complete_work_item(
        work_item=gr_instance.case.work_items.get(task_id="construction-acceptance"),
        user=caluma_admin_user,
    )

    assert len(mailoutbox) == len(expected_recipients)

    if form_name != "vorlaeufige-beurteilung":
        assert mailoutbox[0].recipients() == expected_recipients


@pytest.mark.parametrize(
    "notification_template__subject,instance__identifier",
    [("{{identifier}}", "identifer")],
)
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_204_NO_CONTENT),
    ],
)
def test_notification_template_gvg(
    admin_client,
    notification_template,
    gr_instance,
    status_code,
    mailoutbox,
):
    url = reverse("notificationtemplate-sendmail")

    gr_instance.case.document.save()

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": [
                    "gvg",
                ],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": gr_instance.pk}},
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    assert len(mailoutbox) == 1
    assert mailoutbox[0].recipients() == ["versicherung@gvg.gr.ch"]


@pytest.mark.parametrize(
    "user__email,service__email",
    [("user@example.com", "service@example.com, service2@example.com")],
)
@pytest.mark.parametrize(
    "role__name",
    ["Service"],
)
@pytest.mark.parametrize(
    "form_slug",
    [
        "baupolizeiliches-verfahren",
        "hecken-feldgehoelze-baeume",
        "klaerung-baubewilligungspflicht",
        "zutrittsermaechtigung",
    ],
)
def test_notification_template_sendmail_rsta_forms(
    admin_client,
    instance_service,
    instance_with_case,
    notification_template,
    mailoutbox,
    activation,
    settings,
    caluma_workflow_config_be,
    form_slug,
):
    url = reverse("notificationtemplate-sendmail")

    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    instance_with_case(instance_service.instance, workflow="internal", form=form_slug)

    instance_service.instance.case.document.answers.create(
        question_id="gemeinde", value=str(instance_service.service.pk)
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": ["leitbehoerde"],
            },
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": instance_service.instance.pk}
                },
                "activation": {"data": {"type": "activations", "id": activation.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert (
        mailoutbox[0].body
        == settings.EMAIL_PREFIX_BODY
        + settings.EMAIL_PREFIX_BODY_SPECIAL_FORMS
        + "Test body"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    "use_forbidden_state,status_code",
    [(True, status.HTTP_400_BAD_REQUEST), (False, status.HTTP_204_NO_CONTENT)],
)
@pytest.mark.parametrize("role__name", [("Coordination")])
def test_notification_template_sendmail_koor(
    mocker,
    admin_client,
    notification_template,
    status_code,
    mailoutbox,
    activation,
    ur_instance,
    settings,
    instance_state_factory,
    use_forbidden_state,
    application_settings,
):
    """Test notification permissions for KOOR roles.

    KOOR is special in that they have more complicated rules than other
    roles in Kanton Uri: Full access is granted for the following cases
    * They've created an instance themselves
    * The instance is not in a "hidden" state (which mostly
      excludes instances being edited before submission)
    """
    if use_forbidden_state:
        forbidden_states = [ur_instance.instance_state.name]
    else:
        forbidden_states = [instance_state_factory().name]

    application_settings["INSTANCE_HIDDEN_STATES"] = {"coordination": forbidden_states}

    url = reverse("notificationtemplate-sendmail")
    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": ["municipality"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": ur_instance.pk}},
                "activation": {"data": {"type": "activations", "id": activation.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "user__email,role__name,notification_template__body",
    [
        (
            "user@example.com",
            "Municipality",
            """
                REGISTRATION_LINK: {{registration_link}}
                DATE_DOSSIERVOLLSTANDIG: {{date_dossiervollstandig}}
                DATE_DOSSIEREINGANG: {{date_dossiereingang}}
                DATE_START_ZIRKULATION: {{date_start_zirkulation}}
                DATE_BAU_EINSPRACHEENTSCHEID: {{date_bau_einspracheentscheid}}
                BILLING_TOTAL_KOMMUNAL: {{billing_total_kommunal}}
                BILLING_TOTAL_KANTON: {{billing_total_kanton}}
                BILLING_TOTAL: {{billing_total}}
                CURRENT_SERVICE_DESCRIPTION: {{current_service_description}}
                OBJECTIONS: {{objections}}
                BILLING_TOTAL_UNCHARGED: {{billing_total_uncharged}}
                BILLING_TOTAL_UNCHARGED_KOMMUNAL: {{billing_total_uncharged_kommunal}}
                BILLING_TOTAL_UNCHARGED_KANTON: {{billing_total_uncharged_kanton}}
            """,
        )
    ],
)
def test_notification_placeholders(
    admin_client,
    admin_user,
    sz_instance,
    notification_template,
    mailoutbox,
    activation,
    settings,
    workflow_entry_factory,
    billing_v2_entry_factory,
    objection,
    objection_participant_factory,
    work_item_factory,
    distribution_settings,
):
    settings.APPLICATION["WORKFLOW_ITEMS"]["SUBMIT"] = workflow_entry_factory(
        instance=sz_instance,
        workflow_date=timezone.make_aware(datetime(2019, 7, 22, 10)),
    ).workflow_item.pk
    settings.APPLICATION["WORKFLOW_ITEMS"][
        "INSTANCE_COMPLETE"
    ] = workflow_entry_factory(
        instance=sz_instance,
        workflow_date=timezone.make_aware(datetime(2019, 8, 23, 10)),
    ).workflow_item.pk
    settings.APPLICATION["WORKFLOW_ITEMS"]["START_CIRC"] = workflow_entry_factory(
        instance=sz_instance,
        workflow_date=timezone.make_aware(datetime(2019, 9, 24, 10)),
    ).workflow_item.pk

    work_item_factory(
        case=sz_instance.case,
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
        task_id=distribution_settings["DISTRIBUTION_INIT_TASK"],
        closed_at=timezone.make_aware(datetime(2019, 9, 24, 10)),
    )

    building_authority_work_item = work_item_factory(
        case=sz_instance.case,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        task_id="building-authority",
    )
    add_answer(
        building_authority_work_item.document,
        "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
        timezone.make_aware(datetime(2019, 10, 24, 10)),
    )

    kommunal_amount = billing_v2_entry_factory(
        instance=sz_instance, organization="municipal", date_charged="2023-04-13"
    ).final_rate
    kanton_amount = billing_v2_entry_factory(
        instance=sz_instance, organization="cantonal", date_charged="2023-04-13"
    ).final_rate
    uncharged_amount_kommunal = billing_v2_entry_factory(
        instance=sz_instance, organization="municipal", date_charged=None
    ).final_rate
    uncharged_amount_kantonal = billing_v2_entry_factory(
        instance=sz_instance, organization="cantonal", date_charged=None
    ).final_rate

    objection_participant_factory(objection=objection, representative=1)

    url = reverse("notificationtemplate-sendmail")

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": ["applicant"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": sz_instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(mailoutbox) == 1

    mail = mailoutbox[0]

    admin_svc = admin_user.get_default_group().service

    assert [
        placeholder.strip()
        for placeholder in mail.body.replace(settings.EMAIL_PREFIX_BODY, "")
        .strip()
        .split("\n")
    ] == [
        f"REGISTRATION_LINK: {settings.REGISTRATION_URL}",
        "DATE_DOSSIERVOLLSTANDIG: 23.08.2019",
        "DATE_DOSSIEREINGANG: 22.07.2019",
        "DATE_START_ZIRKULATION: 24.09.2019",
        "DATE_BAU_EINSPRACHEENTSCHEID: 24.10.2019",
        f"BILLING_TOTAL_KOMMUNAL: {kommunal_amount + uncharged_amount_kommunal}",
        f"BILLING_TOTAL_KANTON: {kanton_amount + uncharged_amount_kantonal}",
        f"BILLING_TOTAL: {kommunal_amount + kanton_amount + uncharged_amount_kantonal + uncharged_amount_kommunal}",
        f"CURRENT_SERVICE_DESCRIPTION: {admin_svc.description}",
        f"OBJECTIONS: <QuerySet [<Objection: Objection object ({objection.id})>]>",
        f"BILLING_TOTAL_UNCHARGED: {uncharged_amount_kommunal + uncharged_amount_kantonal}",
        f"BILLING_TOTAL_UNCHARGED_KOMMUNAL: {uncharged_amount_kommunal}",
        f"BILLING_TOTAL_UNCHARGED_KANTON: {uncharged_amount_kantonal}",
    ]


@pytest.mark.parametrize(
    "user__email,role__name", [("user@example.com", "Municipality")]
)
@pytest.mark.parametrize("total_inquiries,done_inquiries", [(2, 2), (2, 1)])
@pytest.mark.parametrize("with_inquiry", [True, False])
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_notification_caluma_placeholders(
    db,
    application_settings,
    settings,
    active_inquiry_factory,
    admin_client,
    be_instance,
    distribution_settings,
    done_inquiries,
    mailoutbox,
    multilang,
    notification_template,
    service,
    service_t_factory,
    snapshot,
    total_inquiries,
    with_inquiry,
    decision_factory,
    be_decision_settings,
):
    # make sure that tests also run locally when INTERNAL_BASE_URL might be something else
    application_settings["INTERNAL_FRONTEND"] = "camac"
    settings.INTERNAL_BASE_URL = "http://ebau.local"
    notification_template.body = """
        BASE_URL: {{BASE_URL}}
        EBAU_NUMBER: {{EBAU_NUMBER}}
        FORM_NAME_DE: {{FORM_NAME_DE}}
        FORM_NAME_FR: {{FORM_NAME_FR}}
        MUNICIPALITY_DE: {{MUNICIPALITY_DE}}
        MUNICIPALITY_FR: {{MUNICIPALITY_FR}}
        INSTANCE_ID: {{INSTANCE_ID}}
        LEITBEHOERDE_NAME_DE: {{LEITBEHOERDE_NAME_DE}}
        LEITBEHOERDE_NAME_FR: {{LEITBEHOERDE_NAME_FR}}
        INTERNAL_DOSSIER_LINK: {{INTERNAL_DOSSIER_LINK}}
        PUBLIC_DOSSIER_LINK: {{PUBLIC_DOSSIER_LINK}}
        DISTRIBUTION_STATUS_DE: {{DISTRIBUTION_STATUS_DE}}
        DISTRIBUTION_STATUS_FR: {{DISTRIBUTION_STATUS_FR}}
        INQUIRY_ANSWER_DE: {{INQUIRY_ANSWER_DE}}
        INQUIRY_ANSWER_FR: {{INQUIRY_ANSWER_FR}}
        INQUIRY_REMARK: {{INQUIRY_REMARK}}
        INQUIRY_LINK: {{INQUIRY_LINK}}
        CURRENT_SERVICE: {{CURRENT_SERVICE}}
        CURRENT_SERVICE_DE: {{CURRENT_SERVICE_DE}}
        CURRENT_SERVICE_FR: {{CURRENT_SERVICE_FR}}
        CURRENT_USER_NAME: {{CURRENT_USER_NAME}}
        WORK_ITEM_NAME_DE: {{WORK_ITEM_NAME_DE}}
        WORK_ITEM_NAME_FR: {{WORK_ITEM_NAME_FR}}
        DECISION_DE: {{DECISION_DE}}
        DECISION_FR: {{DECISION_FR}}
        REJECTION_FEEDBACK: {{REJECTION_FEEDBACK}}
    """
    notification_template.save()

    decision_factory()

    caluma_form_factories.AnswerFactory(
        document=be_instance.case.document, question_id="gemeinde", value="1"
    )

    caluma_form_factories.DynamicOptionFactory(
        question_id="gemeinde",
        document=be_instance.case.document,
        slug="1",
        label={"de": "Bern", "fr": "Berne"},
    )

    service.trans.all().delete()
    service_t_factory(language="de", service=service, name="Leitbehörde Bern")
    service_t_factory(language="fr", service=service, name="Municipalité Berne")

    inquiries = [
        *[
            active_inquiry_factory(
                status=caluma_workflow_models.WorkItem.STATUS_COMPLETED
            )
            for _ in range(done_inquiries)
        ],
        *[active_inquiry_factory() for _ in range(total_inquiries - done_inquiries)],
    ]

    be_instance.rejection_feedback = "Grund für die Rückweisung"
    be_instance.save()

    be_instance.case.meta["ebau-number"] = "2019-01"
    be_instance.case.save()

    submit_work_item = be_instance.case.work_items.filter(task_id="submit").first()

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": ["applicant"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": be_instance.pk}},
                "work-item": {
                    "data": {"type": "work-items", "id": submit_work_item.pk}
                },
            },
        }
    }

    if with_inquiry:
        inquiry = inquiries[0]

        document = caluma_form_factories.DocumentFactory()
        status_option = caluma_form_factories.OptionFactory(
            label={
                "de": "Nicht betroffen / nicht zuständig",
                "fr": "Non concerné/e / non compétent/e",
            }
        )
        answer = caluma_form_factories.AnswerFactory(
            document=document,
            value=status_option.slug,
            question__type=caluma_form_models.Question.TYPE_CHOICE,
        )
        answer.question.options.add(status_option)
        answer.question.save()

        caluma_form_factories.AnswerFactory(
            document=inquiry.document,
            question_id="inquiry-remark",
            value="Bemerkung Anfrage",
            question__type=caluma_form_models.Question.TYPE_TEXT,
        )

        distribution_settings["QUESTIONS"]["STATUS"] = answer.question_id

        inquiry.child_case = caluma_workflow_factories.CaseFactory(document=document)
        inquiry.save()

        data["data"]["relationships"]["inquiry"] = {
            "data": {"type": "work-items", "id": inquiry.pk}
        }

    response = admin_client.post(reverse("notificationtemplate-sendmail"), data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(mailoutbox) == 1

    body = mailoutbox[0].body
    body = re.sub(r"(distribution\/).{36}(\/)", r"\1DISTRIBUTION_UUID\2", body)
    body = re.sub(r"(from\/\d+\/to\/\d+\/).{36}(\/answer)", r"\1INQUIRY_UUID\2", body)

    snapshot.assert_match(body)


@pytest.mark.parametrize("use_static_user", [True, False])
def test_notification_template_merge_without_context(
    db,
    be_instance,
    notification_template,
    system_operation_user,
    application_settings,
    use_static_user,
):
    """Test sendmail without request context.

    When sending a notification through a batch job we can't provide a
    request context to the serializer. The request context is required to
    determine the user of the related history entry which gets automatically
    created.

    In this case the history entry should be sent in the name of the system
    operation user.
    """
    if use_static_user:
        application_settings["SYSTEM_USER"] = system_operation_user.username

    data = {
        "recipient_types": ["leitbehoerde"],
        "notification_template": {
            "type": "notification-templates",
            "id": notification_template.pk,
        },
        "instance": {"id": be_instance.pk, "type": "instances"},
    }

    sendmail_serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data=data
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    entry = HistoryEntry.objects.latest("created_at")
    assert entry.instance == be_instance
    assert entry.user == system_operation_user


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_notification_validate_slug_update(admin_client, notification_template):
    url = reverse("notificationtemplate-detail", args=[notification_template.pk])
    data = {
        "data": {
            "type": "notification-templates",
            "id": notification_template.pk,
            "attributes": {
                "slug": "test",
                "body": "Test",
                "purpose": "Test",
                "notification-type": "textcomponent",
                "subject": "Test",
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0]["detail"] == "Updating a slug is not allowed!"


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_notification_validate_slug_create(admin_client, notification_template):
    url = reverse("notificationtemplate-list")
    data = {
        "data": {
            "type": "notification-templates",
            "id": None,
            "attributes": {
                "slug": notification_template.slug,
                "body": "Test",
                "purpose": "Test",
                "notification-type": "textcomponent",
                "subject": "Test",
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data[0]["detail"]
        == "Vorlage für Benachrichtigung mit diesem slug existiert bereits."
    )


@pytest.mark.parametrize("service__email", [None, "", "foo@example.org"])
@pytest.mark.parametrize("instance__location", [LazyFixture("location")])
def test_recipient_type_municipality_users(
    db, instance, location, location_factory, service, role, mocker, group_location
):
    mocker.patch("camac.constants.kt_uri.ROLE_MUNICIPALITY", role.pk)

    serializer = serializers.NotificationTemplateSendmailSerializer()
    res = serializer._get_recipients_municipality_users(instance)

    if service.email:
        assert res == [{"to": "foo@example.org"}]
    else:
        assert res == []


def test_recipient_type_work_item_addressed(
    db, be_instance, service, work_item_factory, notification_template, user_group
):
    work_item = work_item_factory(
        addressed_groups=[str(service.pk)],
        # controlling_groups=[str(service.pk)],
    )
    be_instance.responsible_services.create(
        service=service, responsible_user=user_group.user
    )

    serializer = serializers.NotificationTemplateSendmailSerializer(
        data={
            "template_slug": notification_template.slug,
            "recipient_types": ["work_item_addressed"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"type": "instances", "id": be_instance.pk},
            "work_item": {"type": "work-items", "id": work_item.pk},
        },
        context={"request": FakeRequest(group=user_group.group, user=user_group.user)},
    )
    serializer.is_valid()
    assert not serializer.errors

    assert serializer._get_recipients_work_item_addressed(be_instance) == [
        {"cc": service.email, "to": user_group.user.email}
    ]


def test_recipient_type_work_item_controlling(
    db, be_instance, service, work_item_factory, notification_template, user_group
):
    be_instance.responsible_services.create(
        service=service, responsible_user=user_group.user
    )

    serializer = serializers.NotificationTemplateSendmailSerializer(
        data={
            "template_slug": notification_template.slug,
            "recipient_types": ["work_item_controlling"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"type": "instances", "id": be_instance.pk},
        },
        context={"request": FakeRequest(group=user_group.group, user=user_group.user)},
    )
    serializer.is_valid()
    assert not serializer.errors

    assert serializer._get_responsible(be_instance, service) == [
        {"cc": service.email, "to": user_group.user.email}
    ]


@pytest.mark.parametrize("service__email", [None, "", "foo@example.org"])
def test_recipient_type_unnotified_service_users(
    db, ur_instance, activation, user_group, mocker, notification_template, service
):
    mocker.patch(
        "camac.constants.kt_uri.CIRCULATION_STATE_IDLE", activation.circulation_state_id
    )

    # Setup the serializer fully, as the recipient type depends on
    # some of the request data
    serializer = serializers.NotificationTemplateSendmailSerializer(
        data={
            "template_slug": notification_template.slug,
            "body": "Test body",
            "recipient_types": [],
            "circulation": {"type": "circulations", "id": activation.circulation.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"type": "instances", "id": ur_instance.pk},
        },
        context={"request": FakeRequest(group=user_group.group, user=user_group.user)},
    )
    serializer.is_valid()
    assert not serializer.errors
    res = serializer._get_recipients_unnotified_service_users(ur_instance)

    if service.email:
        assert res == [{"to": "foo@example.org"}]
    else:
        assert res == []


def test_recipient_type_koor_users(
    db, instance_factory, mocker, user_group, service_factory, form_factory
):
    koor_bg = service_factory()
    koor_np = service_factory()
    instance_bg = instance_factory()
    instance_np = instance_factory()

    mocker.patch("camac.constants.kt_uri.KOOR_BG_SERVICE_ID", koor_bg.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_NP_SERVICE_ID", koor_np.pk)
    mocker.patch(
        "camac.constants.kt_uri.RESPONSIBLE_KOORS",
        {koor_bg.pk: [instance_bg.form.pk], koor_np.pk: [instance_np.form.pk]},
    )

    serializer = serializers.NotificationTemplateSendmailSerializer()

    # instance / form doesn't matter
    bg_recipients = serializer._get_recipients_koor_bg_users(instance_bg)
    np_recipients = serializer._get_recipients_koor_np_users(instance_bg)

    # instance / form matters
    responsible_recipients_bg = serializer._get_recipients_responsible_koor(instance_bg)
    responsible_recipients_np = serializer._get_recipients_responsible_koor(instance_np)

    assert bg_recipients == [{"to": koor_bg.email}]
    assert np_recipients == [{"to": koor_np.email}]
    assert responsible_recipients_bg == [{"to": koor_bg.email}]
    assert responsible_recipients_np == [{"to": koor_np.email}]


@pytest.mark.parametrize("group__name", ["Lisag"])
def test_recipient_type_lisag(db, instance, group):
    serializer = serializers.NotificationTemplateSendmailSerializer()
    res = serializer._get_recipients_lisag(instance)
    assert res == [{"to": group.email}]


@pytest.mark.parametrize(
    "service_group__name,expected",
    [("district", [{"to": "bauen@example.ch"}]), ("municipality", [])],
)
def test_recipient_inactive_municipality(
    db,
    be_instance,
    service_group,
    expected,
    service_factory,
):
    municipality = service_factory(email="bauen@example.ch")

    be_instance.case.document.answers.create(
        value=str(municipality.pk), question_id="gemeinde"
    )

    serializer = serializers.NotificationTemplateSendmailSerializer()

    assert serializer._get_recipients_inactive_municipality(be_instance) == expected


@pytest.mark.parametrize(
    "has_geometer,expected",
    [(True, [{"to": "geometer@example.ch"}]), (False, [])],
)
def test_recipient_geometer_acl_services(
    db,
    be_instance,
    has_geometer,
    expected,
    service_factory,
    instance_acl_factory,
    access_level_factory,
    permissions_settings,
):
    if has_geometer:
        geometer_service = service_factory(email="geometer@example.ch")
        instance_acl_factory(
            instance=be_instance,
            access_level=access_level_factory(slug="geometer"),
            service=geometer_service,
            metainfo={"disable-notification-on-creation": True},
        )
        permissions_settings["geometer"] = [("foo", ["*"])]

    serializer = serializers.NotificationTemplateSendmailSerializer()

    assert serializer._get_recipients_geometer_acl_services(be_instance) == expected


@pytest.mark.parametrize("service__email", ["test@example.com"])
@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize("has_parcel_filled", [True, False])
@pytest.mark.parametrize(
    "notification_template__body",
    ["parz={{parzelle}}, gs={{GESUCHSTELLER}}, vorhaben={{vorhaben}}"],
)
def test_ur_placeholders(
    admin_client,
    db,
    ur_instance,
    camac_answer_factory,
    instance_service,
    mocker,
    notification_template,
    caluma_workflow_config_ur,
    caluma_admin_user,
    mailoutbox,
    settings,
    has_parcel_filled,
):
    caluma_form_models.Question.objects.create(
        slug="proposal-description",
        type=caluma_form_models.Question.TYPE_TEXT,
    )
    parcel_form = caluma_form_models.Form.objects.create(slug="parcel-form")
    parcel_question = caluma_form_models.Question.objects.create(
        slug="parcel-number",
        type=caluma_form_models.Question.TYPE_TEXT,
    )
    caluma_form_models.FormQuestion.objects.create(
        form=parcel_form, question=parcel_question
    )

    caluma_form_models.Question.objects.create(
        slug="parcels",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=parcel_form,
    )

    personal_data_form = caluma_form_models.Form.objects.create(
        slug="personal-data-form"
    )
    personal_questions = [
        caluma_form_models.Question.objects.create(
            slug=slug,
            type=caluma_form_models.Question.TYPE_TEXT,
        )
        for slug in [
            "first-name",
            "last-name",
            "juristic-person-name",
            "street",
            "street-number",
            "zip",
            "city",
        ]
    ]
    is_juristic_person_question = caluma_form_models.Question.objects.create(
        slug="is-juristic-person",
        type=caluma_form_models.Question.TYPE_CHOICE,
    )

    [
        caluma_form_models.FormQuestion.objects.create(
            form=personal_data_form, question=question
        )
        for question in personal_questions + [is_juristic_person_question]
    ]

    applicant_question = caluma_form_models.Question.objects.create(
        slug="applicant",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=personal_data_form,
    )
    main_form = caluma_form_models.Form.objects.get(pk="main-form")
    caluma_form_models.FormQuestion.objects.create(
        form=main_form, question=applicant_question
    )

    ur_instance.case.document.answers.create(
        value="my description", question_id="proposal-description"
    )
    parcel_row_doc = caluma_form_models.Document.objects.create(form=parcel_form)
    if has_parcel_filled:
        parcel_row_doc.answers.create(value="123", question=parcel_question)

    parcel_table_answer = ur_instance.case.document.answers.create(
        question_id="parcels"
    )
    parcel_table_answer.documents.add(parcel_row_doc)
    parcel_table_answer.save()

    applicant_row_doc = caluma_form_models.Document.objects.create(
        form=personal_data_form
    )
    [
        applicant_row_doc.answers.create(value=question.slug, question=question)
        for question in personal_questions[:-1]  # test for missing answers as well
    ]
    applicant_row_doc.answers.create(
        value="is-juristic-person-yes", question=is_juristic_person_question
    )

    table_answer = ur_instance.case.document.answers.create(question_id="applicant")
    table_answer.documents.add(applicant_row_doc)
    table_answer.save()

    sendmail_serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["leitbehoerde"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"id": ur_instance.pk, "type": "instances"},
        }
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    assert len(mailoutbox) == 1

    expected_parcel = "123" if has_parcel_filled else ""

    assert (
        mailoutbox[0].body
        == f"{settings.EMAIL_PREFIX_BODY}parz={expected_parcel}, gs=juristic-person-name, first-name last-name, street street-number, zip, vorhaben=my description"
    )


def test_notification_template_update_purposes(admin_client, notification_template):
    url = reverse("notificationtemplate-update-purposes")

    admin_client.get(
        url, {"current": notification_template.purpose, "new": "NewPurpose"}
    )

    notification_template.refresh_from_db()

    assert notification_template.purpose == "NewPurpose"

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_notification_template_delete_by_purpose(admin_client, notification_template):
    url = reverse("notificationtemplate-delete-by-purpose")

    admin_client.delete(url + "?purpose=" + notification_template.purpose)

    with pytest.raises(ObjectDoesNotExist):
        notification_template.refresh_from_db()

    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "service__email,service__notification,role__name",
    [("test@example.com", 0, "support")],
)
def test_notification_template_service_no_notification(
    db,
    be_instance,
    notification_template,
    settings,
    mailoutbox,
):
    # No need to test this here.
    settings.EMAIL_PREFIX_BODY = ""

    sendmail_serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["leitbehoerde"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"id": be_instance.pk, "type": "instances"},
        }
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    assert len(mailoutbox) == 0


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_unnotified_services(
    activation_factory,
    admin_client,
    be_instance,
    circulation,
    db,
    mailoutbox,
    notification_template,
    service_factory,
    service,
):
    activation_factory(
        circulation=circulation,
        email_sent=0,
        service_parent=service,
        service=service_factory(email="valid@example.com"),
    )
    activation_factory(
        circulation=circulation,
        email_sent=0,
        service_parent=service,
        service=service_factory(email="dontsend@example.com", notification=0),
    )
    be_instance.case.document.answers.create(
        question_id="gemeinde", value=str(be_instance.responsible_service().pk)
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": [
                    "unnotified_service",
                ],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": be_instance.pk}},
                "circulation": {"data": {"type": "circulations", "id": circulation.pk}},
            },
        }
    }

    url = reverse("notificationtemplate-sendmail")
    admin_client.post(url, data=data)

    assert len(mailoutbox) == 1
    assert circulation.activations.filter(email_sent=1).count() == 2


@pytest.mark.parametrize(
    "user__email,role__name,notification_template__body",
    [
        (
            "user@example.com",
            "Municipality",
            """
                BAUVERWALTUNG:
                {{bauverwaltung.bewilligungsverfahren_sitzung_baukommission[0].bewilligungsverfahren_sitzung_baukommission_bemerkung}}
                {{bauverwaltung.bewilligungsverfahren_sitzung_baukommission[0].bewilligungsverfahren_sitzung_baukommission_nr}}
                {{bauverwaltung.bewilligungsverfahren_gr_sitzung_datum}}
            """,
        )
    ],
)
def test_notification_bauverwaltung_placeholders(
    admin_client,
    sz_instance,
    notification_template,
    application_settings,
    work_item_factory,
    document_factory,
    settings,
):
    call_command(
        "loaddata", settings.ROOT_DIR("kt_schwyz/config/buildingauthority.json")
    )
    call_command("loaddata", settings.ROOT_DIR("kt_schwyz/config/caluma_form.json"))

    application_settings["INSTANCE_MERGE_CONFIG"] = {
        "BAUVERWALTUNG": {
            "TASK_SLUG": "building-authority",
        }
    }

    work_item = work_item_factory(task_id="building-authority", case=sz_instance.case)
    work_item.document = document_factory(form_id="bauverwaltung")
    work_item.save()
    add_answer(work_item.document, "bewilligungsverfahren-gr-sitzung-beschluss", "foo")
    add_answer(
        work_item.document,
        "beschwerdeverfahren-weiterzug-durch",
        "beschwerdeverfahren-weiterzug-durch-beschwerdegegner",
    )
    date = timezone.now()
    add_answer(
        work_item.document,
        "bewilligungsverfahren-gr-sitzung-datum",
        date,
        "date",
    )
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

    url = reverse("notificationtemplate-merge", args=[notification_template.pk])
    response = admin_client.get(url, data={"instance": sz_instance.pk})

    assert response.status_code == status.HTTP_200_OK

    assert [
        placeholder.strip()
        for placeholder in response.json()["data"]["attributes"]["body"]
        .strip()
        .split("\n")
    ] == [
        "BAUVERWALTUNG:",
        "Foo Bar",
        "78",
        f"{date.strftime(settings.MERGE_DATE_FORMAT)}",
    ]


@pytest.mark.parametrize("use_multilang", [True, False])
@pytest.mark.parametrize(
    "role__name,notification_template__subject,notification_template__body",
    [("Support", "Subject", "Body")],
)
def test_notification_history_entry(
    db,
    be_instance,
    application_settings,
    use_multilang,
    notification_template,
    settings,
):
    application_settings["IS_MULTILINGUAL"] = use_multilang
    settings.EMAIL_PREFIX_BODY = ""
    settings.EMAIL_PREFIX_SUBJECT = ""

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["leitbehoerde"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"id": be_instance.pk, "type": "instances"},
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    service = be_instance.responsible_service(filter_type="municipality")
    history_entry = HistoryEntry.objects.filter(instance=be_instance).last()

    if use_multilang:
        assert (
            history_entry.get_trans_attr("title", "de")
            == f"Notifikation gesendet an {service.email} (Leitbehörde) (Subject)"
        )
        assert history_entry.get_trans_attr("body", "de") == "Body"
        assert (
            history_entry.get_trans_attr("title", "fr")
            == f"Notification envoyée à {service.email} (Autorité directrice) (Subject)"
        )
        assert history_entry.get_trans_attr("body", "fr") == "Body"
    else:
        assert (
            history_entry.title == f"Notifikation gesendet an {service.email} (Subject)"
        )
        assert history_entry.body == "Body"


def test_merge_serializer_used_placeholders(db, instance):
    serializer = InstanceMergeSerializer(
        instance=instance, used_placeholders=["base_url"]
    )

    assert list(serializer.data.keys()) == ["base_url"]


def test_notification_additional_demand(
    db,
    gr_instance,
    service,
    service_factory,
    case_factory,
    work_item_factory,
    notification_template,
    user_group,
    active_inquiry_factory,
    additional_demand_settings,
):
    inviter = service_factory()
    active_inquiry_factory(gr_instance, service, inviter)
    case = case_factory()
    work_item_factory(addressed_groups=[str(service.pk)], child_case=case)
    work_item = work_item_factory(case=case)

    serializer = serializers.NotificationTemplateSendmailSerializer(
        data={
            "template_slug": notification_template.slug,
            "recipient_types": ["work_item_addressed"],
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"type": "instances", "id": gr_instance.pk},
            "work_item": {"type": "work-items", "id": work_item.pk},
        },
        context={"request": FakeRequest(group=user_group.group, user=user_group.user)},
    )
    serializer.is_valid()
    assert not serializer.errors

    assert serializer._get_recipients_additional_demand_inviter(gr_instance) == [
        {"to": inviter.email}
    ]
