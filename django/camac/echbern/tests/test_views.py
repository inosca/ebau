import json

import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_bern import (
    INSTANCE_STATE_DOSSIERPRUEFUNG,
    INSTANCE_STATE_KOORDINATION,
    INSTANCE_STATE_REJECTED,
)
from camac.core.models import (
    Answer,
    Chapter,
    DocxDecision,
    Question,
    QuestionT,
    QuestionType,
)

from .. import send_handlers, views
from ..event_handlers import EventHandlerException, StatusNotificationEventHandler
from ..models import Message
from .caluma_responses import document_form, full_document
from .utils import xml_data


def test_application_retrieve_full(
    admin_client,
    mocker,
    ech_instance,
    instance_factory,
    docx_decision_factory,
    requests_mock,
    attachment,
    attachment_section,
):
    docx_decision_factory(instance=ech_instance.pk)

    i = instance_factory()

    attachment.instance = ech_instance
    attachment.save()
    attachment.attachment_sections.add(attachment_section)

    qtype = QuestionType.objects.create(name="text")
    q = Question.objects.create(question_type=qtype)
    QuestionT.objects.create(question=q, name="eBau-Nummer", language="de")
    chapter = Chapter.objects.create()
    Answer.objects.create(
        instance=i, question=q, answer="2019-23", item=1, chapter=chapter
    )
    Answer.objects.create(
        instance=ech_instance, question=q, answer="2019-23", item=1, chapter=chapter
    )

    url = reverse("application", args=[ech_instance.pk])

    mocker.patch.object(views, "get_authorization_header", return_value="token")
    requests_mock.post("http://caluma:8000/graphql/", json=full_document)

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_applications_list(admin_client, admin_user, instance, instance_factory):
    i = instance_factory(user=admin_user)
    url = reverse("applications")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(i.instance_id)


@pytest.mark.parametrize("give_last", [False, True])
def test_message_retrieve(
    admin_user, admin_client, message_factory, give_last, service_factory
):
    receiver = admin_user.groups.first().service
    dummy_receiver = service_factory()
    message_factory(body="zeroth xml", receiver=dummy_receiver)
    message_factory(body="first xml", receiver=receiver)
    m2 = message_factory(body="second xml", receiver=receiver)
    message_factory(body="third xml", receiver=dummy_receiver)
    message_factory(body="fourth xml", receiver=receiver)

    url = reverse("message")
    if give_last:
        url = f"{url}?last={m2.pk}"
    response = admin_client.get(f"{url}")

    assert response.status_code == status.HTTP_200_OK
    expected = b"first xml"
    if give_last:
        expected = b"fourth xml"

    assert response.content == expected


@pytest.mark.parametrize("invalid_last", [False, True])
def test_message_retrieve_404(db, invalid_last, service, admin_client, message_factory):
    m = message_factory(body="first xml", receiver=service)

    pk = m.pk
    if invalid_last:
        pk = "ec921e43-302a-4106-99b9-b6ff0aa929b3"

    url = f"{reverse('message')}?last={pk}"
    response = admin_client.get(f"{url}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("support", [True, False])
def test_event_post(support, admin_client, admin_user, ech_instance, role_factory):
    if support:
        group = admin_user.groups.first()
        group.role = role_factory(name="support")
        group.save()
    url = reverse("event", args=[ech_instance.pk, "StatusNotification"])
    response = admin_client.post(
        url, data=json.dumps({"activation_id": 23}), content_type="application/json"
    )

    status_code = status.HTTP_403_FORBIDDEN
    if support:
        status_code = status.HTTP_201_CREATED

    assert response.status_code == status_code

    if support:
        assert Message.objects.get(receiver=ech_instance.active_service)


def test_event_post_404(admin_client, admin_user, ech_instance, role_factory):
    group = admin_user.groups.first()
    group.role = role_factory(name="support")
    group.save()
    url = reverse("event", args=[ech_instance.pk, "NotAnEvent"])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_event_post_400(admin_client, admin_user, ech_instance, role_factory, mocker):
    group = admin_user.groups.first()
    group.role = role_factory(name="support")
    group.save()
    url = reverse("event", args=[ech_instance.pk, "StatusNotification"])
    mocker.patch.object(
        StatusNotificationEventHandler, "run", side_effect=EventHandlerException()
    )

    response = admin_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("has_permission", [True, False])
def test_send(
    has_permission,
    admin_client,
    admin_user,
    ech_instance,
    mocker,
    requests_mock,
    instance_state_factory,
    role_factory,
):
    if has_permission:
        group = admin_user.groups.first()
        group.service = ech_instance.services.first()
        group.role = role_factory(name="support")
        group.save()

    state = instance_state_factory(pk=INSTANCE_STATE_DOSSIERPRUEFUNG)
    expected_state = instance_state_factory(pk=INSTANCE_STATE_REJECTED)
    ech_instance.instance_state = state
    ech_instance.save()

    mocker.patch.object(views, "get_authorization_header", return_value="token")
    requests_mock.post("http://caluma:8000/graphql/", json=document_form)

    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    if has_permission:
        assert response.status_code == 201
        ech_instance.refresh_from_db()
        assert ech_instance.instance_state == expected_state
        assert DocxDecision.objects.get(instance=ech_instance.pk)
    else:
        assert response.status_code == 403


def test_send_400_no_data(admin_client):
    url = reverse("send")
    response = admin_client.post(url)

    assert response.status_code == 400


@pytest.mark.parametrize("is_vorabklaerung,judgement", [(False, 2), (True, 3)])
def test_send_400_invalid_judgement(
    is_vorabklaerung,
    judgement,
    admin_client,
    admin_user,
    ech_instance,
    mocker,
    requests_mock,
    instance_state_factory,
    role_factory,
):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.role = role_factory(name="support")
    group.save()

    state = instance_state_factory(pk=INSTANCE_STATE_KOORDINATION)
    ech_instance.instance_state = state
    ech_instance.save()

    mocker.patch.object(views, "get_authorization_header", return_value="token")
    requests_mock.post("http://caluma:8000/graphql/", json=document_form)

    if is_vorabklaerung:
        mocker.patch.object(
            send_handlers, "get_form_slug", return_value="vorabklaerung"
        )

    url = reverse("send")
    response = admin_client.post(
        url,
        data=xml_data("notice_ruling").replace(
            "<ns2:judgement>4</ns2:judgement>",
            f"<ns2:judgement>{judgement}</ns2:judgement>",
        ),
        content_type="application/xml",
    )

    assert response.status_code == 400


def test_send_403(admin_client, admin_user, ech_instance):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    assert response.status_code == 403


def test_send_unparseable_message(admin_client, admin_user, ech_instance):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    url = reverse("send")
    response = admin_client.post(
        url,
        data=xml_data("notice_ruling").replace("eventNotice", "blablabla"),
        content_type="application/xml",
    )

    assert response.status_code == 400


def test_send_unknown_instance(admin_client, admin_user):
    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    assert response.status_code == 404
