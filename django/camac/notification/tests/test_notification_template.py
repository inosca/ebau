import functools
from datetime import date, datetime
from time import mktime

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance.models import HistoryEntry
from camac.notification.serializers import (
    NotificationTemplateSendmailSerializer,
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
    instance,
    notification_template,
    status_code,
    activation,
    billing_entry,
    application_settings,
    form_field_factory,
    notice_factory,
):
    notice_factory.create_batch(size=3, activation=activation)
    application_settings["COORDINATE_QUESTION"] = "punkte"
    application_settings["QUESTIONS_WITH_OVERRIDE"] = ["bezeichnung"]

    add_field = functools.partial(form_field_factory, instance=instance)
    add_field(
        name="punkte", value=[{"lat": 47.02433179952733, "lng": 8.634144559228435}]
    )
    add_field(name="bezeichnung", value="abc")
    add_field(name="bezeichnung-override", value="abc")

    url = reverse("notificationtemplate-merge", args=[notification_template.pk])

    response = admin_client.get(url, data={"instance": instance.pk})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["subject"] == instance.identifier
        assert json["data"]["attributes"]["body"] == "identifier 21.01.2017"
        assert json["data"]["id"] == "{0}-{1}".format(
            notification_template.slug, instance.pk
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
    caluma_workflow,
):
    url = reverse("notificationtemplate-sendmail")
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

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(slug="building-permit"),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        meta={"camac-instance-id": instance_service.instance.pk},
        user=BaseUser(),
    )

    case.document.answers.create(
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
                "instance": {
                    "data": {"type": "instances", "id": instance_service.instance.pk}
                },
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

    url = reverse("notificationtemplate-sendmail")

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": ["applicant"],
            },
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
        f"REGISTRATION_LINK: {settings.REGISTRATION_URL}",
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
@pytest.mark.parametrize("total_activations,done_activations", [(2, 2), (2, 1)])
@pytest.mark.parametrize("with_activation", [True, False])
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
    with_activation,
    circulation_factory,
    done_activations,
    circulation_state_factory,
    mocker,
    caluma_workflow,
):
    url = reverse("notificationtemplate-sendmail")

    STATE_DONE, STATE_WORKING = circulation_state_factory.create_batch(2)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_DONE", STATE_DONE.pk)
    mocker.patch("camac.constants.kt_bern.CIRCULATION_STATE_WORKING", STATE_WORKING.pk)

    assert not len(mailoutbox)

    circulation = circulation_factory(
        instance=instance, name=int(mktime(date(2020, 1, 2).timetuple()))
    )

    activations = [
        activation_factory(
            circulation=circulation,
            circulation_state=STATE_WORKING,
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

    workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(slug="building-permit"),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        meta={"camac-instance-id": instance.pk, "ebau-number": "2019-01"},
        user=BaseUser(),
    )

    data = {
        "data": {
            "type": "notification-template-sendmails",
            "attributes": {
                "template-slug": notification_template.slug,
                "recipient-types": ["applicant"],
            },
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    if with_activation:
        data["data"]["relationships"]["activation"] = {
            "data": {"type": "activations", "id": activations[0].pk}
        }

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
        l.strip()
        for l in [
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
    ]


def test_notification_template_merge_without_context(
    db, instance, notification_template, mocker, system_operation_user
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
        "recipient_types": ["activation_deadline_today"],
        "notification_template": {
            "type": "notification-templates",
            "id": notification_template.pk,
        },
        "instance": {"id": instance.pk, "type": "instances"},
    }

    sendmail_serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data=data
    )
    sendmail_serializer.is_valid(raise_exception=True)
    sendmail_serializer.save()

    entry = HistoryEntry.objects.latest("created_at")
    assert entry.instance == instance
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
@pytest.mark.parametrize("submitter_email", ["foo@example.org", ""])
@pytest.mark.parametrize(
    "submitter_type",
    [
        NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_APPLICANT,
        NotificationTemplateSendmailSerializer.SUBMITTER_TYPE_PROJECT_AUTHOR,
    ],
)
def test_recipient_type_submitter_list(
    db,
    mocker,
    instance,
    submitter_type,
    camac_answer_factory,
    misdirect_type,
    misdirect_email,
    submitter_email,
):
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
            submitter_type: (
                ans_email.chapter_id,
                ans_email.question_id + misdirect_email,
                ans_email.item,
            )
        },
    )

    serializer = NotificationTemplateSendmailSerializer()
    has_raised = False
    res = []

    try:
        res = serializer._get_recipients_submitter_list(instance)
    except Exception as exc:
        has_raised = exc

    if misdirect_type or misdirect_email or not submitter_email:
        assert bool(has_raised)
        assert res == []
    else:
        assert res == [{"to": "foo@example.org"}]
        assert not has_raised


@pytest.mark.parametrize("correct_municipality", [True, False])
@pytest.mark.parametrize("user_group__default_group", [True, False])
@pytest.mark.parametrize("user__email", [None, "", "foo@example.org"])
@pytest.mark.parametrize("instance__location", [LazyFixture("location")])
def test_recipient_type_municipality_users(
    db,
    instance,
    location,
    location_factory,
    user_group,
    correct_municipality,
    role,
    mocker,
):
    mocker.patch("camac.constants.kt_uri.ROLE_MUNICIPALITY", role.pk)
    user_group.group.locations.add(
        location if correct_municipality else location_factory()
    )

    serializer = NotificationTemplateSendmailSerializer()
    res = serializer._get_recipients_municipality_users(instance)

    if correct_municipality and user_group.default_group and user_group.user.email:
        assert res == [{"to": "foo@example.org"}]
    else:
        assert res == []


@pytest.mark.parametrize("user_group__default_group", [True, False])
@pytest.mark.parametrize("user__email", [None, "", "foo@example.org"])
def test_recipient_type_unnotified_service_users(
    db, instance, activation, user_group, mocker, notification_template
):
    mocker.patch(
        "camac.constants.kt_uri.CIRCULATION_STATE_IDLE", activation.circulation_state_id
    )

    class FakeRequest:
        group = user_group.group
        user = user_group.user

    # Setup the serializer fully, as the recipient type depends on
    # some of the request data
    serializer = NotificationTemplateSendmailSerializer(
        data={
            "template_slug": notification_template.slug,
            "body": "Test body",
            "recipient_types": [],
            "circulation": {"type": "circulations", "id": activation.circulation.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
            "instance": {"type": "instances", "id": instance.pk},
        },
        context={"request": FakeRequest},
    )
    serializer.is_valid()
    assert not serializer.errors
    res = serializer._get_recipients_unnotified_service_users(instance)

    if user_group.default_group and user_group.user.email:
        assert res == [{"to": "foo@example.org"}]
    else:
        assert res == []


@pytest.mark.parametrize(
    "recipient_method",
    ["_get_recipients_koor_np_users", "_get_recipients_koor_bg_users"],
)
@pytest.mark.parametrize("user_group__default_group", [True, False])
@pytest.mark.parametrize("user__email", [None, "", "foo@example.org"])
def test_recipient_type_koor_users(
    db, instance, role, recipient_method, mocker, user_group
):

    mocker.patch("camac.constants.kt_uri.KOOR_BG_ROLE_ID", role.pk)
    mocker.patch("camac.constants.kt_uri.KOOR_NP_ROLE_ID", role.pk)

    serializer = NotificationTemplateSendmailSerializer()
    method = getattr(serializer, recipient_method)
    res = method(instance)

    if user_group.default_group and user_group.user.email:
        assert res == [{"to": "foo@example.org"}]
    else:
        assert res == []


@pytest.mark.parametrize("group__name", ["Lisag"])
def test_recipient_type_lisag(db, instance, group):

    serializer = NotificationTemplateSendmailSerializer()
    res = serializer._get_recipients_lisag(instance)
    assert res == [{"to": group.email}]
