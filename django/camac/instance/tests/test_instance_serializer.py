import pytest

from camac.constants import kt_uri as uri_constants
from camac.core.factories import CamacAnswerFactory
from camac.instance.serializers import CalumaInstanceSerializer


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
