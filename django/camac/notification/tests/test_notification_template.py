import functools
from datetime import date, datetime
from time import mktime

import pytest
from caluma.caluma_form import models as caluma_form_models
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import exceptions, status

from camac.conftest import CALUMA_FORM_TYPES_SLUGS, FakeRequest
from camac.instance.models import HistoryEntry
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
                "type": "textcomponent",
                "subject": "Test",
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["attributes"]["type"] == "textcomponent"


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
    ],
)
def test_notification_template_destroy(
    admin_client, notification_template, status_code
):
    url = reverse("notificationtemplate-detail", args=[notification_template.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "notification_template__body", ["{{identifier}} {{answer_period_date}}"]
)
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
    activation,
    billing_entry,
    application_settings,
    form_field_factory,
    notice_factory,
    publication_entry,
):
    notice_factory.create_batch(size=3, activation=activation)
    application_settings["COORDINATE_QUESTION"] = "punkte"
    application_settings["QUESTIONS_WITH_OVERRIDE"] = ["bezeichnung"]
    application_settings["LOCATION_NAME_QUESTION"] = "durchmesser-der-bohrung"

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
        assert json["data"]["attributes"]["body"] == "identifier 21.01.2017"
        assert json["data"]["id"] == "{0}-{1}".format(
            notification_template.slug, sz_instance.pk
        )
        assert json["data"]["type"] == "notification-template-merges"


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
                    "service",
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
        assert len(mailoutbox) == 6

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
            (
                [responsible_email],
                ["service@example.com", "service2@example.com"],
            ),  # service
        ]
        assert (
            mailoutbox[0].subject
            == settings.EMAIL_PREFIX_SUBJECT + be_instance.identifier
        )
        assert mailoutbox[0].body == settings.EMAIL_PREFIX_BODY + "Test body"


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
                "recipient-types": [
                    "municipality",
                    "leitbehoerde",
                    "service",
                    "unnotified_service",
                    "activation_service_parent",
                    "caluma_municipality",
                ],
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
):
    """Test notification permissions for KOOR roles.

    KOOR is special in that they have more complicated rules than other
    roles in Kanton Uri: Full access is granted for the following cases
    * They've created an instance themselves
    * The instance is not in a "private" state (which mostly
      excludes instances being edited before submission)
    """
    if use_forbidden_state:
        use_forbidden_state = [ur_instance.instance_state.name]
    else:
        use_forbidden_state = [instance_state_factory().name]

    mocker.patch("camac.constants.kt_uri.INSTANCE_STATES_PRIVATE", use_forbidden_state)

    url = reverse("notificationtemplate-sendmail")
    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "template-slug": notification_template.slug,
                "body": "Test body",
                "recipient-types": ["service"],
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
    settings.APPLICATION["WORKFLOW_ITEMS"]["DECISION"] = workflow_entry_factory(
        instance=sz_instance,
        workflow_date=timezone.make_aware(datetime(2019, 10, 24, 10)),
    ).workflow_item.pk

    kommunal_amount = billing_v2_entry_factory(
        instance=sz_instance, organization="municipal"
    ).final_rate
    kanton_amount = billing_v2_entry_factory(
        instance=sz_instance, organization="cantonal"
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
        f"BILLING_TOTAL_KOMMUNAL: {kommunal_amount:.2f}",
        f"BILLING_TOTAL_KANTON: {kanton_amount}",
        f"BILLING_TOTAL: {round(kommunal_amount + kanton_amount, 2)}",
        f"CURRENT_SERVICE_DESCRIPTION: {admin_svc.description}",
        f"OBJECTIONS: <QuerySet [<Objection: Objection object ({objection.id})>]>",
    ]


@pytest.mark.parametrize(
    "user__email,role__name,notification_template__body",
    [
        (
            "user@example.com",
            "Municipality",
            """
                BASE_URL: {{BASE_URL}}
                EBAU_NUMBER: {{EBAU_NUMBER}}
                FORM_NAME: {{FORM_NAME}}
                INSTANCE_ID: {{INSTANCE_ID}}
                LEITBEHOERDE_NAME: {{LEITBEHOERDE_NAME}}
                INTERNAL_DOSSIER_LINK: {{INTERNAL_DOSSIER_LINK}}
                PUBLIC_DOSSIER_LINK: {{PUBLIC_DOSSIER_LINK}}
                COMPLETED_ACTIVATIONS: {{COMPLETED_ACTIVATIONS}}
                TOTAL_ACTIVATIONS: {{TOTAL_ACTIVATIONS}}
                PENDING_ACTIVATIONS: {{PENDING_ACTIVATIONS}}
                ACTIVATION_STATEMENT_DE: {{ACTIVATION_STATEMENT_DE}}
                ACTIVATION_STATEMENT_FR: {{ACTIVATION_STATEMENT_FR}}
                ACTIVATION_ANSWER_DE: {{ACTIVATION_ANSWER_DE}}
                ACTIVATION_ANSWER_FR: {{ACTIVATION_ANSWER_FR}}
                CURRENT_SERVICE: {{CURRENT_SERVICE}}
            """,
        )
    ],
)
@pytest.mark.parametrize("total_activations,done_activations", [(2, 2), (2, 1)])
@pytest.mark.parametrize("with_activation", [True, False])
@pytest.mark.parametrize(
    "circulation_answer_name",
    [
        {
            "de": "Nicht betroffen / nicht zuständig",
            "fr": "Non concerné/e / non compétent/e",
        }
    ],
)
def test_notification_caluma_placeholders(
    admin_client,
    admin_user,
    be_instance,
    notification_template,
    mailoutbox,
    activation_factory,
    settings,
    requests_mock,
    use_caluma_form,
    total_activations,
    with_activation,
    circulation_factory,
    done_activations,
    circulation_state_factory,
    circulation_answer_factory,
    mocker,
    caluma_workflow_config_be,
    caluma_admin_user,
    circulation_answer_name,
    multilang,
):
    url = reverse("notificationtemplate-sendmail")

    STATE_DONE, STATE_WORKING = circulation_state_factory.create_batch(2)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_DONE", STATE_DONE.pk)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_WORKING", STATE_WORKING.pk)

    circulation_answer = circulation_answer_factory()

    for language, name in circulation_answer_name.items():
        circulation_answer.trans.create(language=language, name=name)

    assert not len(mailoutbox)

    circulation = circulation_factory(
        instance=be_instance, name=int(mktime(date(2020, 1, 2).timetuple()))
    )

    activations = [
        activation_factory(
            circulation=circulation,
            circulation_state=STATE_WORKING,
            circulation_answer=circulation_answer,
            service_parent=circulation.service,
        )
        for _ in range(total_activations)
    ]
    for i in range(done_activations):
        activations[i].circulation_state = STATE_DONE
        activations[i].save()

    # create "sub activation", which should not be counted
    activation_factory(
        circulation=circulation,
        circulation_state=STATE_WORKING,
        service_parent=activations[0].service,
    )

    be_instance.case.meta["ebau-number"] = "2019-01"
    be_instance.case.save()

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": ["applicant"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": be_instance.pk}}
            },
        }
    }

    if with_activation:
        data["data"]["relationships"]["activation"] = {
            "data": {"type": "activations", "id": activations[0].pk}
        }
        activation_answer_de = circulation_answer_name["de"]
        activation_answer_fr = circulation_answer_name["fr"]

        if done_activations == total_activations:
            activation_statement_de = f"Alle {total_activations} Stellungnahmen der Zirkulation vom 02.01.2020 sind nun eingegangen."
            activation_statement_fr = f"Tous les {total_activations} prises de position de la circulation du 02.01.2020 ont été reçues."
        else:
            pending_activations = total_activations - done_activations
            activation_statement_de = f"{pending_activations} von {total_activations} Stellungnahmen der Zirkulation vom 02.01.2020 stehen noch aus."
            activation_statement_fr = f"{pending_activations} de {total_activations} prises de position de la circulation du 02.01.2020 sont toujours en attente."

    else:
        activation_statement_de = ""
        activation_statement_fr = ""
        activation_answer_de = ""
        activation_answer_fr = ""
        total_activations += 1

    response = admin_client.post(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(mailoutbox) == 1

    service_name = admin_user.groups.first().service.get_name()

    mail = mailoutbox[0]
    assert [
        line.strip()
        for line in mail.body.replace(settings.EMAIL_PREFIX_BODY, "")
        .strip()
        .split("\n")
    ] == [
        line.strip()
        for line in [
            "BASE_URL: http://camac-ng.local",
            "EBAU_NUMBER: 2019-01",
            "FORM_NAME: Baugesuch",
            f"INSTANCE_ID: {be_instance.pk}",
            f"LEITBEHOERDE_NAME: {be_instance.responsible_service().get_name()}",
            f"INTERNAL_DOSSIER_LINK: http://camac-ng.local/index/redirect-to-instance-resource/instance-id/{be_instance.pk}",
            f"PUBLIC_DOSSIER_LINK: http://caluma-portal.local/instances/{be_instance.pk}",
            f"COMPLETED_ACTIVATIONS: {done_activations}",
            f"TOTAL_ACTIVATIONS: {total_activations}",
            f"PENDING_ACTIVATIONS: {total_activations-done_activations}",
            f"ACTIVATION_STATEMENT_DE: {activation_statement_de}",
            f"ACTIVATION_STATEMENT_FR: {activation_statement_fr}",
            f"ACTIVATION_ANSWER_DE: {activation_answer_de}",
            f"ACTIVATION_ANSWER_FR: {activation_answer_fr}",
            f"CURRENT_SERVICE: {service_name}",
        ]
    ]


def test_notification_template_merge_without_context(
    db, be_instance, notification_template, mocker, system_operation_user
):
    """Test sendmail without request context.

    When sending a notification through a batch job we can't provide a
    request context to the serializer. The request context is required to
    determine the user of the related history entry which gets automatically
    created.

    In this case the history entry should be sent in the name of the system
    operation user.
    """

    data = {
        "recipient_types": ["activation_deadline_yesterday"],
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
                "type": "textcomponent",
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
                "type": "textcomponent",
                "subject": "Test",
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data[0]["detail"]
        == "notification template mit diesem slug existiert bereits."
    )


@pytest.mark.parametrize("misdirect_type", [0, 99999])
@pytest.mark.parametrize("misdirect_email", [0, 99999])
@pytest.mark.parametrize("is_portal_form", [True, False])
@pytest.mark.parametrize("submitter_email", ["foo@example.org", ""])
@pytest.mark.parametrize(
    "submitter_type",
    [
        serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_APPLICANT,
        serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_PROJECT_AUTHOR,
    ],
)
def test_recipient_type_submitter_list(
    db,
    mocker,
    instance,
    camac_answer_factory,
    misdirect_type,
    misdirect_email,
    submitter_email,
    submitter_type,
    is_portal_form,
):
    mocker.patch(
        "camac.constants.kt_uri.PORTAL_FORMS",
        [instance.form.pk if is_portal_form else 9999999999],
    )

    ans_email = camac_answer_factory(answer=submitter_email, instance=instance)
    ans_submitter_type = camac_answer_factory(answer=submitter_type, instance=instance)
    mocker.patch(
        "camac.notification.serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_CQI",
        (
            ans_submitter_type.chapter_id,
            # misdirect points us to an invalid answer to test missing data
            ans_submitter_type.question_id + misdirect_type,
            ans_submitter_type.item,
        ),
    )
    mocker.patch(
        "camac.notification.serializers.NotificationTemplateSendmailSerializer.SUBMITTER_LIST_CQI_BY_TYPE",
        {
            # We only mock the type being tested
            typ: (
                ans_email.chapter_id,
                ans_email.question_id + misdirect_email,
                ans_email.item,
            )
            for typ in [
                serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_APPLICANT,
                serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_PROJECT_AUTHOR,
            ]
        },
    )

    serializer = serializers.NotificationTemplateSendmailSerializer()
    has_raised = False
    res = []

    try:
        res = serializer._get_recipients_submitter_list(instance)
    except Exception as exc:
        has_raised = exc

    if not is_portal_form:
        assert res == []
        assert not has_raised
    elif misdirect_email or not submitter_email:
        # note: misdirect_type just causes the fallback to trigger, which
        # won't cause an error per se
        assert bool(has_raised)
        assert res == []
    else:
        assert res == [{"to": "foo@example.org"}]
        assert not has_raised


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


@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize("with_activation", [True, False])
@pytest.mark.parametrize("service__email", [None, "user@camac.ch"])
def test_recipient_type_activation_service(
    db,
    be_instance,
    activation,
    group,
    user,
    with_activation,
    notification_template,
    service,
):
    """Ensure that the recipient type returns all mail addresses of users which
    have their default group set to the same group as the service which was
    invited to a circulation through an actvation.

    If the activation was not specified in the request, ensure an exception is
    raised.
    """

    data = {
        "recipient_types": ["activation_deadline_yesterday"],
        "notification_template": {
            "type": "notification-templates",
            "id": notification_template.pk,
        },
        "instance": {"id": be_instance.pk, "type": "instances"},
        **(
            {"activation": {"id": activation.pk, "type": "activations"}}
            if with_activation
            else {}
        ),
    }
    context = {"request": FakeRequest(group=group, user=user)}

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data=data, context=context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if with_activation:
        res = serializer._get_recipients_activation_service(be_instance)

        if service.email is None:
            assert res == []
        else:
            assert res == [{"to": service.email}]
    else:
        with pytest.raises(exceptions.ValidationError):
            serializer._get_recipients_activation_service(be_instance)


@pytest.mark.parametrize("with_activation", [True, False])
@pytest.mark.parametrize("service__email", [None, "user@camac.ch"])
def test_recipient_type_circulation_service(
    db,
    be_instance,
    activation,
    group,
    user,
    with_activation,
    notification_template,
    service,
):
    """Ensure that the recipient type returns the mail addresses of the service
    which created the circulation.
    """

    data = {
        "recipient_types": ["activation_deadline_yesterday"],
        "notification_template": {
            "type": "notification-templates",
            "id": notification_template.pk,
        },
        "instance": {"id": be_instance.pk, "type": "instances"},
        **(
            {"activation": {"id": activation.pk, "type": "activations"}}
            if with_activation
            else {}
        ),
    }
    context = {"request": FakeRequest(group=group, user=user)}

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data=data, context=context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if with_activation:
        res = serializer._get_recipients_circulation_service(be_instance)
        if service.email is None:
            assert res == []
        else:
            assert res == [{"to": service.email}]
    else:
        with pytest.raises(exceptions.ValidationError):
            serializer._get_recipients_circulation_service(be_instance)


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
    "submitter_type",
    [
        serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_APPLICANT,
        serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_PROJECT_AUTHOR,
        None,
    ],
)
def test_portal_submission_placeholder(
    db, instance, camac_answer_factory, mocker, submitter_type
):
    serializer = InstanceMergeSerializer(instance)
    if submitter_type is not None:
        ans_submitter_type = camac_answer_factory(
            answer=submitter_type, instance=instance
        )
        mocker.patch(
            "camac.notification.serializers.NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_CQI",
            (
                ans_submitter_type.chapter_id,
                # misdirect points us to an invalid answer to test missing data
                ans_submitter_type.question_id,
                ans_submitter_type.item,
            ),
        )
    portal_submission = serializer.get_portal_submission(instance)
    assert portal_submission == (submitter_type is not None)


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
    [
        caluma_form_models.FormQuestion.objects.create(
            form=personal_data_form, question=question
        )
        for question in personal_questions
    ]

    caluma_form_models.Question.objects.create(
        slug="applicant",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=personal_data_form,
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
        == f"{settings.EMAIL_PREFIX_BODY}parz={expected_parcel}, gs=juristic-person-name, first-name last-name, street street-number, zip , vorhaben=my description"
    )


@pytest.mark.parametrize("service__email", ["test@example.com"])
@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize(
    "notification_template__body",
    ["nfd_completion_date={{ACTIVATION.nfd_completion_date}}"],
)
def test_notification_template_sendmail_activation(
    db,
    admin_client,
    be_instance,
    activation,
    nfd_completion_date,
    notification_template,
    settings,
    mailoutbox,
):
    """Ensure that if the template has access to the activation when specified in the request."""

    nfd_completion_date.activation = activation
    nfd_completion_date.activation.save()

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
            "activation": {"id": activation.pk, "type": "activations"},
        }
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    assert len(mailoutbox) == 1

    formatted_date = nfd_completion_date.answer.strftime(settings.MERGE_DATE_FORMAT)
    assert mailoutbox[0].body == f"nfd_completion_date={formatted_date}"


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


@pytest.mark.parametrize("service__email", ["test@example.com"])
@pytest.mark.parametrize("role__name", ["support"])
@pytest.mark.parametrize(
    "notification_template__body",
    ["nfd_completion_date={{ACTIVATION.nfd_completion_date}}"],
)
def test_notification_template_service_no_notification(
    db,
    be_instance,
    activation,
    nfd_completion_date,
    notification_template,
    settings,
    mailoutbox,
):
    """Ensure that if the template has access to the activation when specified in the request."""

    activation.service.notification = 0
    activation.service.save()
    nfd_completion_date.activation = activation
    nfd_completion_date.activation.save()

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
            "activation": {"id": activation.pk, "type": "activations"},
        }
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    assert len(mailoutbox) == 0


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_unanswered_activation(
    db,
    be_instance,
    activation_factory,
    circulation_factory,
    notification_template,
    user_group,
):
    circulation = circulation_factory(instance=be_instance)
    other_circulation = circulation_factory(instance=be_instance)

    activation_factory(circulation=circulation, circulation_state__name="DONE")
    activation_factory(
        circulation=circulation,
        circulation_state__name="RUN",
        service__email="test@example.com",
    )
    # Notifications must be sent to pertaining circulations only, therefore we
    # setup some extra activations belonging to another circulation. These must not
    # appear in the recipients' list
    activation_factory(
        circulation=other_circulation,
        circulation__state="RUN",
        service__email="tist@example",
    )
    activation_factory(
        circulation=other_circulation,
        circulation__state="RUN",
        service__email="tust@example",
    )
    # to get access to validated data the serializer needs to be setup in full
    serializer = serializers.NotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["unanswered_activation"],
            "instance": {"type": "instances", "id": be_instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "circulation": {"type": "circulations", "id": circulation.pk},
        },
        # request is needed in context to get access
        context={"request": FakeRequest(group=user_group.group, user=user_group.user)},
    )
    serializer.is_valid()

    assert serializer._get_recipients_unanswered_activation(be_instance) == [
        {"to": "test@example.com"}
    ]
