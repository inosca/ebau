import datetime
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
)
from camac.ech0211.schema.ech_0211_2_0 import CreateFromDocument

from ...dossier_import.config.kt_schwyz import COORDINATES_MAPPING, PARCEL_MAPPING
from ...dossier_import.dossier_classes import Coordinates, PlotData
from ...dossier_import.writers import CamacNgListAnswerWriter
from ..constants import (
    ECH_JUDGEMENT_APPROVED_WITH_RESERVATION,
    ECH_JUDGEMENT_DECLINED,
    ECH_JUDGEMENT_WRITTEN_OFF,
)
from ..event_handlers import EventHandlerException, StatusNotificationEventHandler
from ..formatters import delivery
from ..models import Message
from ..send_handlers import KindOfProceedingsSendHandler, NoticeRulingSendHandler
from .utils import xml_data


@pytest.mark.parametrize("is_vorabklaerung", [False, True])
def test_application_retrieve_full_be(
    is_vorabklaerung,
    set_application_be,
    admin_client,
    mocker,
    ech_instance_be,
    be_ech0211_settings,
    instance_with_case,
    instance_factory,
    attachment,
    attachment_section,
    multilang,
    decision_factory,
    be_decision_settings,
    reload_ech0211_urls,
    ech_snapshot,
):
    decision = be_decision_settings["ANSWERS"]["DECISION"]["DEPRECIATED"]
    if is_vorabklaerung:
        ech_instance_be.case.workflow = caluma_workflow_models.Workflow.objects.get(
            pk="preliminary-clarification"
        )
        ech_instance_be.case.save()
        decision = be_decision_settings["ANSWERS"]["DECISION"][
            "POSITIVE_WITH_RESERVATION"
        ]
    decision_factory(instance=ech_instance_be, decision=decision)

    linked_instance = instance_with_case(instance_factory())

    attachment.instance = ech_instance_be
    attachment.context = {"tags": ["some", "tags"]}
    attachment.save()
    attachment.attachment_sections.add(attachment_section)

    linked_instance.case.meta["ebau-number"] = "2019-23"
    linked_instance.case.save()
    ech_instance_be.case.meta["ebau-number"] = "2019-23"
    ech_instance_be.case.save()

    response = admin_client.get(reverse("application", args=[ech_instance_be.pk]))
    assert response.status_code == status.HTTP_200_OK

    xml = CreateFromDocument(response.content)
    assert (
        xml.eventBaseDelivery.planningPermissionApplicationInformation[0]
        .planningPermissionApplication.decisionRuling[0]
        .judgement
        == be_decision_settings["ECH_JUDGEMENT_MAP"][
            "preliminary-clarification" if is_vorabklaerung else "building-permit"
        ][decision]
    )


def test_applications_list(
    admin_client,
    admin_user,
    set_application_be,
    be_ech0211_settings,
    ech_instance_be,
    reload_ech0211_urls,
):
    url = reverse("applications")
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(ech_instance_be.pk)


@pytest.mark.parametrize("form_id", settings.ECH_EXCLUDED_FORMS)
def test_applications_list_exclude(
    admin_client,
    admin_user,
    instance_factory,
    form_id,
    caluma_admin_user,
    set_application_be,
    be_ech0211_settings,
    reload_ech0211_urls,
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
    admin_user,
    admin_client,
    message_factory,
    give_last,
    service_factory,
    set_application_be,
    be_ech0211_settings,
    reload_ech0211_urls,
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
def test_message_retrieve_204(
    db,
    invalid_last,
    service,
    admin_client,
    message_factory,
    set_application_be,
    be_ech0211_settings,
    reload_ech0211_urls,
):
    m = message_factory(body="first xml", receiver=service)

    pk = m.pk
    if invalid_last:
        pk = "ec921e43-302a-4106-99b9-b6ff0aa929b3"

    url = f"{reverse('message')}?last={pk}"
    response = admin_client.get(f"{url}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("support", [True, False])
def test_event_post(
    support,
    admin_client,
    admin_user,
    ech_instance_case,
    be_ech0211_settings,
    role_factory,
    set_application_be,
    reload_ech0211_urls,
):
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


def test_event_post_404(
    admin_client,
    admin_user,
    ech_instance_be,
    role_factory,
    set_application_be,
    be_ech0211_settings,
    reload_ech0211_urls,
):
    group = admin_user.groups.first()
    group.role = role_factory(name="support")
    group.save()
    url = reverse("event", args=[ech_instance_be.pk, "NotAnEvent"])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["support"])
def test_event_disabled(
    admin_client, set_application_sz, sz_ech0211_settings, reload_ech0211_urls
):
    url = reverse("event", args=[1, "NotAnEvent"])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name", ["support"])
def test_send_disabled(
    admin_client, set_application_sz, sz_ech0211_settings, reload_ech0211_urls
):
    url = reverse("send")
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_event_post_400(
    admin_client,
    admin_user,
    ech_instance_be,
    role_factory,
    mocker,
    set_application_be,
    be_ech0211_settings,
    reload_ech0211_urls,
):
    group = admin_user.groups.first()
    group.role = role_factory(name="support")
    group.save()
    url = reverse("event", args=[ech_instance_be.pk, "StatusNotification"])
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
    set_application_be,
    be_ech0211_settings,
    ech_instance_be,
    ech_instance_case,
    settings,
    instance_state_factory,
    role_factory,
    attachment_section_factory,
    attachment_factory,
    service_group_factory,
    service_factory,
    caluma_workflow_config_be,
    caluma_admin_user,
    be_decision_settings,
    reload_ech0211_urls,
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
        group.service = ech_instance_be.services.first()
        group.role = role_factory(name="support")
        group.save()
        attachment_section_beteiligte_behoerden = attachment_section_factory(
            pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
        )
        attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
        attachment = attachment_factory(
            uuid="00000000-0000-0000-0000-000000000000",
            name="myFile.pdf",
            instance=ech_instance_be,
        )
        attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    state = instance_state_factory(name="circulation_init")
    expected_state = instance_state_factory(name="rejected")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

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
        ech_instance_be.refresh_from_db()
        assert ech_instance_be.instance_state == expected_state
    else:
        assert response.status_code == 403


def test_send_400_no_data(admin_client, set_application_be, be_ech0211_settings):
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
    ech_instance_be,
    be_ech0211_settings,
    mocker,
    instance_state_factory,
    role_factory,
    attachment_section_factory,
    attachment_factory,
    caluma_workflow_config_be,
    caluma_admin_user,
    settings,
    reload_ech0211_urls,
):
    attachment_section_beteiligte_behoerden = attachment_section_factory(
        pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
    )
    attachment_section_factory(pk=ATTACHMENT_SECTION_ALLE_BETEILIGTEN)
    attachment = attachment_factory(
        uuid="00000000-0000-0000-0000-000000000000",
        name="myFile.pdf",
        instance=ech_instance_be,
    )
    attachment.attachment_sections.add(attachment_section_beteiligte_behoerden)

    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.role = role_factory(name="support")
    group.save()

    state = instance_state_factory(name="coordination")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(
            slug=(
                "preliminary-clarification" if is_vorabklaerung else "building-permit"
            )
        ),
        form=caluma_form_models.Form.objects.get(slug="main-form"),
        user=caluma_admin_user,
    )
    ech_instance_be.case = case
    ech_instance_be.save()

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


def test_send_403(
    admin_client, admin_user, ech_instance_be, be_ech0211_settings, settings
):
    settings.APPLICATION = settings.APPLICATIONS["kt_bern"]
    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
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
    ech_instance_be,
    be_ech0211_settings,
    instance_factory,
    attachment_section_factory,
    attachment_factory,
    settings,
    mocker,
    be_distribution_settings,
    reload_ech0211_urls,
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
    admin_client,
    admin_user,
    ech_instance_be,
    be_ech0211_settings,
    instance_state_factory,
    role_factory,
    settings,
    reload_ech0211_urls,
):
    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.role = role_factory(name="support")
    group.save()

    state = instance_state_factory(name="circulation_init")
    ech_instance_be.instance_state = state
    ech_instance_be.save()

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
    admin_client,
    admin_user,
    ech_instance_be,
    match,
    replace,
    settings,
    be_ech0211_settings,
    reload_ech0211_urls,
):
    group = admin_user.groups.first()
    group.service = ech_instance_be.services.first()
    group.save()

    url = reverse("send")
    response = admin_client.post(
        url,
        data=xml_data("notice_ruling").replace(match, replace),
        content_type="application/xml",
    )

    assert response.status_code == 400


def test_send_unknown_instance(
    admin_client, set_application_be, be_ech0211_settings, reload_ech0211_urls
):
    url = reverse("send")
    response = admin_client.post(
        url, data=xml_data("notice_ruling"), content_type="application/xml"
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "plot_data,coordinates,decision,site_address",
    [
        (None, None, None, None),
        (
            [
                PlotData(
                    egrid="CH123-4-567", number=1234567, municipality="Hintertupfigen"
                )
            ],
            [Coordinates(n=8.5592041911, e=47.0636626694)],
            {
                "date": datetime.datetime(2021, 1, 11),
                "decicion": "accepted",
            },
            {"street": ""},
        ),
        (None, None, None, {"street": "Somewhere over the Rainbow 10b"}),
        (None, None, None, {"street": "Somewhere"}),
    ],
)
@pytest.mark.freeze_time("2020-02-01")
@pytest.mark.parametrize("application_type", ["Baugesuch", "Vorabklärung"])
def test_application_retrieve_full_sz(
    admin_client,
    set_application_sz,
    ech_instance_sz,
    sz_ech0211_settings,
    application_type,
    instance_state_factory,
    plot_data,
    coordinates,
    site_address,
    decision,
    snapshot,
    mocker,
    request,
    work_item_factory,
    master_data_is_visible_mock,
    reload_ech0211_urls,
):
    ech_instance_sz.form.description = application_type
    ech_instance_sz.form.save()
    mocker.patch.object(  # make for a deterministic message_id
        delivery, "__defaults__", (None, None, str(ech_instance_sz.pk), None)
    )
    if hasattr(site_address, "values") and site_address.values():
        addr_field, _ = ech_instance_sz.fields.get_or_create(
            name="ortsbezeichnung-des-vorhabens",
            defaults={"value": site_address["street"]},
        )
    if plot_data:
        CamacNgListAnswerWriter(
            target="parzellen", column_mapping=PARCEL_MAPPING
        ).write(ech_instance_sz, plot_data)
    if coordinates:
        CamacNgListAnswerWriter(
            target="punkte", column_mapping=COORDINATES_MAPPING
        ).write(ech_instance_sz, coordinates)

    if decision and decision.get("date"):
        # determinining decision date in SZ requires a value from
        # the work_item document of task "building-authority"
        work_item_factory(
            task_id="make-decision",
            case=ech_instance_sz.case,
            status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
        )

    resp = admin_client.get(reverse("application", args=[ech_instance_sz.pk]))
    assert resp.status_code == status.HTTP_200_OK


def test_message_invalid_last(admin_client, set_application_be, reload_ech0211_urls):
    response = admin_client.get(reverse("message"), data={"last": "invalid-uuid"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert b"'last' parameter must be a valid UUID" in response.content
