import pytest

from camac.conftest import Utils
from camac.constants import kt_uri as uri_constants
from camac.instance.serializers import (
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)


def test_rejection_feedback(db, instance_factory):
    instance = instance_factory(rejection_feedback="Test")
    serializer = CalumaInstanceSerializer()

    assert (
        serializer.Meta.model.rejection_feedback.field.value_from_object(instance)
        == instance.rejection_feedback
    )


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
    utils: Utils,
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
        utils.add_answer(
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
