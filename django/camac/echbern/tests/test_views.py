import json

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_ALLE_BETEILIGTEN,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    DECISION_JUDGEMENT_MAP,
    DECISIONS_ABGESCHRIEBEN,
    ECH_JUDGEMENT_APPROVED_WITH_RESERVATION,
    ECH_JUDGEMENT_DECLINED,
    ECH_JUDGEMENT_WRITTEN_OFF,
    VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT,
)
from camac.core.models import (
    Answer,
    Chapter,
    DocxDecision,
    Question,
    QuestionT,
    QuestionType,
)
from camac.echbern.schema.ech_0211_2_0 import CreateFromDocument

from .. import views
from ..event_handlers import EventHandlerException, StatusNotificationEventHandler
from ..models import Message
from ..send_handlers import KindOfProceedingsSendHandler, NoticeRulingSendHandler
from .caluma_document_data import baugesuch_data, vorabklaerung_data
from .utils import xml_data


@pytest.mark.parametrize("is_vorabklaerung", [False, True])
def test_application_retrieve_full(
    is_vorabklaerung,
    admin_client,
    mocker,
    ech_instance,
    instance_factory,
    docx_decision_factory,
    attachment,
    attachment_section,
    multilang,
):
    decision = DECISIONS_ABGESCHRIEBEN
    if is_vorabklaerung:
        decision = VORABKLAERUNG_DECISIONS_BEWILLIGT_MIT_VORBEHALT
    docx_decision_factory(instance=ech_instance, decision=decision)

    i = instance_factory()

    attachment.instance = ech_instance
    attachment.context = {"tags": ["some", "tags"]}
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

    if is_vorabklaerung:
        mocker.patch.object(views, "get_document", return_value=vorabklaerung_data)
    else:
        mocker.patch.object(views, "get_document", return_value=baugesuch_data)

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    xml = CreateFromDocument(response.content)
    assert (
        xml.eventBaseDelivery.planningPermissionApplicationInformation[0]
        .planningPermissionApplication.decisionRuling[0]
        .judgement
        == DECISION_JUDGEMENT_MAP[
            "preliminary-clarification" if is_vorabklaerung else "building-permit"
        ][decision]
    )


def test_applications_list(admin_client, admin_user, ech_instance):
    url = reverse("applications")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(ech_instance.pk)


@pytest.mark.parametrize("form_id", settings.ECH_EXCLUDED_FORMS)
def test_applications_list_exclude(
    admin_client,
    admin_user,
    instance_factory,
    form_id,
    caluma_admin_user,
):
    # generate an instance that should not be accessible for eCH
    form = caluma_form_models.Form.objects.create(slug=form_id)
    workflow = caluma_workflow_models.Workflow.objects.create(slug=form_id)
    workflow.allow_forms.add(form)

    instance = instance_factory(user=admin_user)
    case = workflow_api.start_case(
        workflow=workflow,
        form=form,
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    url = reverse("applications")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 0


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
def test_message_retrieve_204(db, invalid_last, service, admin_client, message_factory):
    m = message_factory(body="first xml", receiver=service)

    pk = m.pk
    if invalid_last:
        pk = "ec921e43-302a-4106-99b9-b6ff0aa929b3"

    url = f"{reverse('message')}?last={pk}"
    response = admin_client.get(f"{url}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("support", [True, False])
def test_event_post(support, admin_client, admin_user, ech_instance_case, role_factory):
    ech_instance = ech_instance_case().instance

    ech_instance.instance_state.name = "circulation_init"
    ech_instance.instance_state.save()

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
        assert Message.objects.get(receiver=ech_instance.responsible_service())


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
    ech_instance_case,
    mocker,
    instance_state_factory,
    role_factory,
    attachment_section_factory,
    attachment_factory,
    service_group_factory,
    service_factory,
    caluma_workflow_config_be,
    caluma_admin_user,
):
    if has_permission:
        service_group_baukontrolle = service_group_factory(name="construction-control")

        service_factory(
            service_group=service_group_baukontrolle,
            name=None,
            trans__name="Baukontrolle Burgdorf",
            trans__city="Burgdorf",
            trans__language="de",
        )
        group = admin_user.groups.first()
        group.service = ech_instance.services.first()
        group.role = role_factory(name="support")
        group.save()
        attachment_section_beteiligte_behoerden = attachment_section_factory(
            pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
        )
        attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
        attachment = attachment_factory(
            uuid="00000000-0000-0000-0000-000000000000",
            name="myFile.pdf",
            instance=ech_instance,
        )
        attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    state = instance_state_factory(name="circulation_init")
    expected_state = instance_state_factory(name="rejected")
    ech_instance.instance_state = state
    ech_instance.save()

    case = ech_instance_case()

    for task in ["submit", "ebau-number"]:
        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task), user=caluma_admin_user
        )

    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    if has_permission:
        assert response.status_code == 201
        ech_instance.refresh_from_db()
        assert ech_instance.instance_state == expected_state
        assert DocxDecision.objects.get(instance=ech_instance)
    else:
        assert response.status_code == 403


def test_send_400_no_data(admin_client):
    url = reverse("send")
    response = admin_client.post(url)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "is_vorabklaerung,judgement",
    [
        (False, ECH_JUDGEMENT_APPROVED_WITH_RESERVATION),
        (True, ECH_JUDGEMENT_WRITTEN_OFF),
    ],
)
def test_send_400_invalid_judgement(
    is_vorabklaerung,
    judgement,
    admin_client,
    admin_user,
    ech_instance,
    mocker,
    instance_state_factory,
    role_factory,
    attachment_section_factory,
    attachment_factory,
    caluma_workflow_config_be,
    caluma_admin_user,
):
    attachment_section_beteiligte_behoerden = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
    attachment = attachment_factory(
        uuid="00000000-0000-0000-0000-000000000000",
        name="myFile.pdf",
        instance=ech_instance,
    )
    attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.role = role_factory(name="support")
    group.save()

    state = instance_state_factory(name="coordination")
    ech_instance.instance_state = state
    ech_instance.save()

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(
            slug=(
                "preliminary-clarification" if is_vorabklaerung else "building-permit"
            )
        ),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        user=caluma_admin_user,
    )
    ech_instance.case = case
    ech_instance.save()

    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )

    url = reverse("send")
    response = admin_client.post(
        url,
        data=xml_data("notice_ruling").replace(
            f"<ns2:judgement>{ECH_JUDGEMENT_DECLINED}</ns2:judgement>",
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


@pytest.mark.parametrize("ech_message", ["notice_ruling", "kind_of_proceedings"])
def test_send_403_attachment_permissions(
    ech_message,
    admin_client,
    ech_instance,
    instance_factory,
    attachment_section_factory,
    attachment_factory,
    mocker,
):
    mocker.patch.object(
        NoticeRulingSendHandler, "has_permission", return_value=(True, None)
    )
    mocker.patch.object(
        KindOfProceedingsSendHandler, "has_permission", return_value=(True, None)
    )

    attachment_section_beteiligte_behoerden = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
    attachment = attachment_factory(
        uuid="00000000-0000-0000-0000-000000000000",
        name="myFile.pdf",
        instance=instance_factory(),
    )
    attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data(ech_message), content_type="application/xml"
    )

    assert response.status_code == 403


def test_send_404_attachment_missing(
    admin_client, admin_user, ech_instance, instance_state_factory, role_factory
):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.role = role_factory(name="support")
    group.save()

    state = instance_state_factory(name="circulation_init")
    ech_instance.instance_state = state
    ech_instance.save()

    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    assert response.status_code == 404
    assert (
        response.content
        == b"No document found for uuids: 00000000-0000-0000-0000-000000000000."
    )


@pytest.mark.parametrize(
    "match,replace", [("eventNotice", "blablabla"), ("xmlns:ns2=", "xmlns:ns4=")]
)
def test_send_unparseable_message(
    admin_client, admin_user, ech_instance, match, replace
):
    group = admin_user.groups.first()
    group.service = ech_instance.services.first()
    group.save()

    url = reverse("send")
    response = admin_client.post(
        url,
        data=xml_data("notice_ruling").replace(match, replace),
        content_type="application/xml",
    )

    assert response.status_code == 400


def test_send_unknown_instance(admin_client):
    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    assert response.status_code == 404
