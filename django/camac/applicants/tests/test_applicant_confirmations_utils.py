import pytest
from rest_framework.exceptions import ValidationError

from camac.applicants.utils import get_applicants_requiring_confirmation
from camac.tests.form_utils import FormUtils


@pytest.mark.django_db
def test_get_applicants_requiring_confirmation(
    applicant_factory,
    applicants_settings,
    caluma_case_factory,
    form_utils: FormUtils,
    instance,
):
    instance.case = caluma_case_factory()
    instance.save()

    document = instance.case.document

    applicant = applicant_factory(instance=instance)
    applicant_and_landowner = applicant_factory(instance=instance)

    question = applicants_settings.applicant_identifier_question

    form_utils.add_table_answer(
        document,
        "gesuchstellerin",
        [{question: str(applicant.pk)}, {question: str(applicant_and_landowner.pk)}],
    )
    form_utils.add_table_answer(
        document,
        "grundeigentuemerin",
        [{question: str(applicant_and_landowner.pk)}],
    )

    result = get_applicants_requiring_confirmation(instance)
    parsed = sorted(
        [(app.pk, sorted([q.pk for q in questions])) for app, questions in result],
        key=lambda i: i[0],
    )

    assert len(result) == 2
    assert parsed == [
        (applicant.pk, ["gesuchstellerin"]),
        (applicant_and_landowner.pk, ["gesuchstellerin", "grundeigentuemerin"]),
    ]

    form_utils.add_table_answer(
        document,
        "rechnungsempfaengerin",
        [{question: "9999999"}],
    )

    with pytest.raises(ValidationError, match=r"No applicant with ID 9999999 found."):
        get_applicants_requiring_confirmation(instance)
