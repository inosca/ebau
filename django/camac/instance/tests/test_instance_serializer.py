import pytest

from camac.constants import kt_uri as uri_constants
from camac.core.factories import CamacAnswerFactory
from camac.instance.serializers import (
    CalumaInstanceSerializer,
    CalumaInstanceSubmitSerializer,
)


@pytest.mark.parametrize(
    "application_name,expected_answer",
    [
        ("kt_uri", "string from camac answer"),
        ("kt_be", "string from from instance"),
    ],
)
def test_rejection_feedback(
    db, instance_factory, settings, application_name, expected_answer, mocker
):
    instance = instance_factory(
        rejection_feedback=(
            "string from from instance" if application_name == "kt_be" else None
        )
    )
    settings.APPLICATION_NAME = application_name

    if application_name == "kt_uri":
        camac_answer = CamacAnswerFactory(instance=instance, answer=expected_answer)
        mocker.patch.object(
            uri_constants, "REJECTION_FEEDBACK_CHAPTER_ID", camac_answer.chapter.pk
        )
        mocker.patch.object(
            uri_constants, "REJECTION_FEEDBACK_QUESTION_ID", camac_answer.question.pk
        )

    serializer = CalumaInstanceSerializer()

    assert (
        serializer.get_rejection_feedback(instance) == expected_answer
    ), "it returns the camac answer for uri and the instance rejection feedback for the other cantons"


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
    answer_factory,
    expected_authority_pk,
    caluma_workflow_config_ur,
    mocker,
):
    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()
    mocker.patch.object(uri_constants, "KOOR_AFG_GROUP_ID", ur_instance.group.pk)

    answer_factory(
        document=ur_instance.case.document,
        question=ur_instance.case.document.form.questions.get(slug="municipality"),
        value=uri_constants.BFS_NR_DIVERSE_GEMEINDEN,
    )

    serializer = CalumaInstanceSubmitSerializer()

    assert (
        serializer._get_authority_pk(ur_instance) == expected_authority_pk
    ), "it sets the correct authority for the dossier type"


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
    ],
)
def test_ur_get_responsible_service(
    db,
    ur_instance,
    form_slug,
    service_name,
    service_factory,
    mocker,
    utils,
    set_application_ur,
    veranstaltungs_art,
    form_question_factory,
):
    serializer = CalumaInstanceSubmitSerializer()
    mock_service = service_factory()

    ur_instance.case.document.form_id = form_slug
    ur_instance.case.document.save()

    mocker.patch.object(uri_constants, service_name, mock_service.pk)
    mocker.patch.object(uri_constants, "KOOR_AFG_GROUP_ID", ur_instance.group.pk)

    if veranstaltungs_art:
        form_question_factory(
            form=ur_instance.case.document.form,
            question__slug="veranstaltung-art",
        )
        utils.add_answer(
            ur_instance.case.document,
            "veranstaltung-art",
            "veranstaltung-art-sportanlass",
        )

    assert serializer._ur_get_responsible_service(ur_instance) == mock_service
