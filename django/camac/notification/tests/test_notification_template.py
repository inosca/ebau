import functools
import json
from datetime import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import status


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
    instance,
    notification_template,
    status_code,
    activation,
    billing_entry,
    application_settings,
    form_field_factory,
):
    application_settings["COORDINATE_QUESTION"] = "punkte"
    add_field = functools.partial(form_field_factory, instance=instance)
    add_field(
        name="punkte", value=[{"lat": 47.02433179952733, "lng": 8.634144559228435}]
    )

    url = reverse("notificationtemplate-merge", args=[notification_template.pk])

    response = admin_client.get(url, data={"instance": instance.pk})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["subject"] == instance.identifier
        assert json["data"]["attributes"]["body"] == "identifier 21.01.2017"
        assert json["data"]["id"] == "{0}-{1}".format(
            notification_template.pk, instance.pk
        )
        assert json["data"]["type"] == "notification-template-merges"


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
    ],
)
def test_notification_template_sendmail(
    admin_client,
    instance_service,
    responsible_service_factory,
    instance_responsibility_factory,
    notification_template,
    status_code,
    mailoutbox,
    activation,
    new_responsible_model,
    settings,
):
    url = reverse("notificationtemplate-sendmail", args=[notification_template.pk])
    if new_responsible_model:
        responsible = instance_responsibility_factory(
            instance=instance_service.instance, service=instance_service.service
        )
        responsible_email = responsible.user.email
    else:
        responsible = responsible_service_factory(
            instance=instance_service.instance, service=instance_service.service
        )
        responsible_email = responsible.responsible_user.email

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "id": None,
            "attributes": {
                "body": "Test body",
                "recipient-types": [
                    "applicant",
                    "municipality",
                    "leitbehoerde",
                    "service",
                    "unnotified_service",
                ],
            },
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": instance_service.instance.pk}
                }
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_204_NO_CONTENT:
        assert len(mailoutbox) == 4

        # recipient types are sorted alphabetically
        assert [(m.to, m.cc) for m in mailoutbox] == [
            (["user@example.com"], []),  # applicant
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
            == settings.EMAIL_PREFIX_SUBJECT + instance_service.instance.identifier
        )
        assert mailoutbox[0].body == settings.EMAIL_PREFIX_BODY + "Test body"


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
                BILLING_TOTAL_KOMMUNAL: {{billing_total_kommunal}}
                BILLING_TOTAL_KANTON: {{billing_total_kanton}}
                BILLING_TOTAL: {{billing_total}}
            """,
        )
    ],
)
def test_notification_placeholders(
    admin_client,
    instance,
    instance_service,
    notification_template,
    mailoutbox,
    activation,
    settings,
    workflow_entry_factory,
    billing_v2_entry_factory,
):
    settings.APPLICATION["WORKFLOW_ITEMS"]["SUBMIT"] = workflow_entry_factory(
        instance=instance, workflow_date=timezone.make_aware(datetime(2019, 7, 22, 10))
    ).workflow_item.pk
    settings.APPLICATION["WORKFLOW_ITEMS"][
        "INSTANCE_COMPLETE"
    ] = workflow_entry_factory(
        instance=instance, workflow_date=timezone.make_aware(datetime(2019, 8, 23, 10))
    ).workflow_item.pk
    settings.APPLICATION["WORKFLOW_ITEMS"]["START_CIRC"] = workflow_entry_factory(
        instance=instance, workflow_date=timezone.make_aware(datetime(2019, 9, 24, 10))
    ).workflow_item.pk

    kommunal_amount = billing_v2_entry_factory(
        instance=instance, organization="municipal"
    ).final_rate
    kanton_amount = billing_v2_entry_factory(
        instance=instance, organization="cantonal"
    ).final_rate

    url = reverse("notificationtemplate-sendmail", args=[notification_template.pk])

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {"recipient-types": ["applicant"]},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(mailoutbox) == 1

    mail = mailoutbox[0]

    assert [
        placeholder.strip()
        for placeholder in mail.body.replace(settings.EMAIL_PREFIX_BODY, "")
        .strip()
        .split("\n")
    ] == [
        f"REGISTRATION_LINK: {settings.KEYCLOAK_URL}realms/ebau/login-actions/registration?client_id=camac",
        "DATE_DOSSIERVOLLSTANDIG: 23.08.2019",
        "DATE_DOSSIEREINGANG: 22.07.2019",
        "DATE_START_ZIRKULATION: 24.09.2019",
        f"BILLING_TOTAL_KOMMUNAL: {kommunal_amount}",
        f"BILLING_TOTAL_KANTON: {kanton_amount}",
        f"BILLING_TOTAL: {round(kommunal_amount + kanton_amount, 2)}",
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
                CURRENT_SERVICE: {{CURRENT_SERVICE}}
            """,
        )
    ],
)
@pytest.mark.parametrize("total_activations,done_activations", [(2, 2), (2, 1), (0, 0)])
def test_notification_caluma_placeholders(
    admin_client,
    admin_user,
    instance,
    instance_service,
    notification_template,
    mailoutbox,
    activation_factory,
    settings,
    requests_mock,
    use_caluma_form,
    total_activations,
    circulation,
    done_activations,
    circulation_state_factory,
    mocker,
):
    url = reverse("notificationtemplate-sendmail", args=[notification_template.pk])

    STATE_DONE, STATE_WORKING = circulation_state_factory.create_batch(2)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_DONE", STATE_DONE.pk)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_WORKING", STATE_WORKING.pk)

    assert not len(mailoutbox)

    activations = [
        activation_factory(circulation=circulation, circulation_state=STATE_WORKING)
        for _ in range(total_activations)
    ]
    for i in range(done_activations):
        activations[i].circulation_state = STATE_DONE
        activations[i].save()

    requests_mock.post(
        "http://caluma:8000/graphql/",
        text=json.dumps(
            {
                "data": {
                    "allDocuments": {
                        "edges": [
                            {
                                "node": {
                                    "id": "RG9jdW1lbnQ6NjYxOGU5YmQtYjViZi00MTU2LWI0NWMtZTg0M2Y2MTFiZDI2",
                                    "meta": {
                                        "camac-instance-id": instance.pk,
                                        "ebau-number": "2019-01",
                                    },
                                    "form": {
                                        "slug": "baugesuch",
                                        "name": "Baugesuch",
                                        "meta": {"is-main-form": True},
                                    },
                                }
                            }
                        ]
                    }
                }
            }
        ),
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {"recipient-types": ["applicant"]},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(mailoutbox) == 1

    if total_activations == 0:
        activation_statement_de = (
            "Keine offenen Stellungnahmen oder keine aktive Zirkulation"
        )
        activation_statement_fr = (
            "Aucun rapports officiels ouvert ou pas de circulation active"
        )
    elif done_activations == 1:
        pending_activations = total_activations - done_activations
        activation_statement_de = f"{pending_activations} von {total_activations} Stellungnahmen stehen noch aus"
        activation_statement_fr = f"{pending_activations} des {total_activations} rapports officiels sont toujours en attente"
    else:
        activation_statement_de = (
            f"Alle {total_activations} Stellungnahmen sind nun eingegangen"
        )
        activation_statement_fr = (
            f"Tout les {total_activations} rapports officiels ont maintenant été reçus"
        )

    service_name = admin_user.groups.first().service.get_name()

    mail = mailoutbox[0]
    assert [
        line.strip()
        for line in mail.body.replace(settings.EMAIL_PREFIX_BODY, "")
        .strip()
        .split("\n")
    ] == [
        "BASE_URL: http://camac-ng.local",
        "EBAU_NUMBER: 2019-01",
        "FORM_NAME: Baugesuch",
        f"INSTANCE_ID: {instance.pk}",
        f"LEITBEHOERDE_NAME: {instance_service.service.get_name()}",
        f"INTERNAL_DOSSIER_LINK: http://camac-ng.local/index/redirect-to-instance-resource/instance-id/{instance.pk}",
        f"PUBLIC_DOSSIER_LINK: http://caluma-portal.local/instances/{instance.pk}",
        f"COMPLETED_ACTIVATIONS: {done_activations}",
        f"TOTAL_ACTIVATIONS: {total_activations}",
        f"PENDING_ACTIVATIONS: {total_activations-done_activations}",
        f"ACTIVATION_STATEMENT_DE: {activation_statement_de}",
        f"ACTIVATION_STATEMENT_FR: {activation_statement_fr}",
        f"CURRENT_SERVICE: {service_name}",
    ]
