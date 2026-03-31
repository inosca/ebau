from datetime import datetime, timezone

import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants import kt_uri as uri_constants
from camac.instance.serializers import (
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)
from camac.tests.form_utils import FormUtils


def test_rejection_feedback(db, instance_factory):
    instance = instance_factory(rejection_feedback="Test")
    serializer = CalumaInstanceSerializer()

    assert (
        serializer.Meta.model.rejection_feedback.field.value_from_object(instance)
        == instance.rejection_feedback
    )


@pytest.mark.parametrize(
    "publication_entry__publication_date", [datetime(2026, 1, 30, tzinfo=timezone.utc)]
)
@pytest.mark.parametrize("role__name", ["Canton"])
@pytest.mark.parametrize(
    "publication_entry__publication_journal_number, expected_output",
    [
        (3, 3),
        (None, 5),
    ],
)
def test_amtsblattnummer_placeholder_sz(
    db,
    notification_template,
    publication_entry,
    admin_client,
    sz_instance,
    expected_output,
):
    notification_template.body = (
        "{% for p in publications %}W{{p.calendar_week}}{% endfor %}"
    )
    notification_template.save()
    publication_entry.is_published = 1
    publication_entry.save()
    url = reverse("notificationtemplate-merge", args=[notification_template.pk])

    response = admin_client.get(url, data={"instance": sz_instance.pk})
    assert response.status_code == status.HTTP_200_OK
    assert f"W{expected_output}" == response.json()["data"]["attributes"]["body"]


@pytest.mark.parametrize(
    "form_slug,expected_authority_pk",
    [
        ("pgv-gemeindestrasse", str(uri_constants.BAUDIREKTION_AUTHORITY_ID)),
        ("konzession-waermeentnahme", str(uri_constants.AMT_FUER_ENERGIE_AUTHORITY_ID)),
        (
            "bohrbewilligung-waermeentnahme",
            str(uri_constants.AMT_FUER_ENERGIE_AUTHORITY_ID),
        ),
        ("bgbb", str(uri_constants.KOOR_AFG_AUTHORITY_ID)),
    ],
)
def test_get_authority(
    db,
    ur_instance,
    form_slug,
    caluma_answer_factory,
    expected_authority_pk,
    caluma_workflow_config_ur,
    mocker,
):
    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()
    mocker.patch.object(uri_constants, "KOOR_AFG_GROUP_ID", ur_instance.group.pk)

    caluma_answer_factory(
        document=ur_instance.case.document,
        question=ur_instance.case.document.form.questions.get(slug="municipality"),
        value=uri_constants.BFS_NR_DIVERSE_GEMEINDEN,
    )

    serializer = CalumaInstanceSubmitSerializer()

    assert serializer._get_authority_pk(ur_instance) == expected_authority_pk, (
        "it sets the correct authority for the dossier type"
    )


@pytest.mark.parametrize(
    "form_slug,service_name,veranstaltungs_art",
    [
        (
            "cantonal-territory-usage",
            "KOOR_SD_SERVICE_ID",
            "veranstaltung-art-sportanlass",
        ),
        ("cantonal-territory-usage", "KOOR_BD_SERVICE_ID", None),
        ("konzession-waermeentnahme", "KOOR_AFE_SERVICE_ID", None),
        ("bohrbewilligung-waermeentnahme", "KOOR_AFE_SERVICE_ID", None),
        ("pgv-gemeindestrasse", "KOOR_BD_SERVICE_ID", None),
        ("bgbb", "KOOR_AFG_SERVICE_ID", None),
        ("einfache-anfrage", "KOOR_NP_SERVICE_ID", None),
    ],
)
def test_ur_get_responsible_service(
    db,
    ur_instance,
    form_slug,
    service_name,
    service_factory,
    mocker,
    form_utils: FormUtils,
    set_application_ur,
    veranstaltungs_art,
    caluma_form_question_factory,
    rf,
):
    serializer = CalumaInstanceSubmitSerializer(context={"request": rf.request()})
    mock_service = service_factory()

    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()

    mocker.patch.object(uri_constants, service_name, mock_service.pk)

    if veranstaltungs_art:
        caluma_form_question_factory(
            form=ur_instance.case.document.form,
            question__slug="veranstaltung-art",
        )
        form_utils.add_answer(
            ur_instance.case.document,
            "veranstaltung-art",
            "veranstaltung-art-sportanlass",
        )

    if service_name == "KOOR_AFG_SERVICE_ID":
        assert (
            serializer._ur_get_responsible_service(ur_instance)
            == ur_instance.group.service
        )
    else:
        assert serializer._ur_get_responsible_service(ur_instance) == mock_service


@pytest.mark.parametrize(
    "form_slug,expected_notifications",
    [
        (
            "baugesuch",
            (
                "empfang-anfragebaugesuch-behorden",
                "empfang-anfragebaugesuch-gesuchsteller",
            ),
        ),
        (
            "vorlaeufige-beurteilung",
            (
                "empfang-anfragevorabklarung-behorden",
                "empfang-anfragevorabklarung-gesuchsteller",
            ),
        ),
        (
            "vorlaeufige-beurteilung-v3",
            (
                "empfang-anfragevorabklarung-behorden",
                "empfang-anfragevorabklarung-gesuchsteller",
            ),
        ),
        (
            "other",
            (
                "empfang-anfragebaugesuch-behorden",
                "empfang-anfragebaugesuch-gesuchsteller",
            ),
        ),
    ],
)
def test_send_notifications_gr(
    db,
    instance_factory,
    caluma_case_factory,
    form_slug,
    expected_notifications,
    set_application_gr,
    mocker,
):
    case = caluma_case_factory(document__form__slug=form_slug)
    instance_factory(case=case)

    serializer = CalumaInstanceSubmitSerializer()

    mocked_send = mocker.patch.object(serializer, "_send_notification")
    serializer._send_notifications(case)

    assert mocked_send.call_count == 2
    assert set(
        [call.kwargs["template_slug"] for call in mocked_send.call_args_list]
    ) == set(expected_notifications)


def test_close_form_timelines(
    db,
    instance_factory,
    caluma_case_factory,
    form_timeline_factory,
    set_application_gr,
    timelines_settings,
):
    timelines_settings.enabled = True
    case = caluma_case_factory(document__form__slug="baugesuch")
    instance_factory(case=case)

    timeline = form_timeline_factory(instance=case.instance, end_date=None)
    assert timeline.end_date is None
    serializer = CalumaInstanceSubmitSerializer()
    serializer._close_formtimeline(case.instance)

    timeline.refresh_from_db()
    assert timeline.end_date is not None
