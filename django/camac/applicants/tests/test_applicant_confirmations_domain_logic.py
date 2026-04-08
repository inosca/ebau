from functools import partial

import pytest
from caluma.caluma_form.models import Question
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied, ValidationError

from camac.applicants.models import ApplicantConfirmation, ApplicantConfirmationRound


@pytest.fixture
def permission_mock(mocker):
    return mocker.patch("camac.permissions.api.PermissionManager.require_all")


@pytest.fixture
def form_setup(
    applicants_settings,
    caluma_form_question_factory,
    caluma_question_option_factory,
):
    form_question = caluma_form_question_factory(
        question__pk=applicants_settings.confirmation_question,
        question__type=Question.TYPE_MULTIPLE_CHOICE,
    )

    for option in applicants_settings.confirmation_answer:
        caluma_question_option_factory(
            question=form_question.question,
            option__pk=option,
        )

    return form_question.form


@pytest.mark.parametrize(
    ("form_scenario", "error_scenario", "error_cls", "error_msg"),
    [
        ("main_form", None, None, None),
        ("additional_demand", None, None, None),
        (
            "material_exam",
            None,
            ImproperlyConfigured,
            r" can only be created for the main document or additional demands",
        ),
        (
            "main_form",
            "has_active",
            ValidationError,
            r"already an active applicant confirmation round",
        ),
        (
            "main_form",
            "no_applicants",
            ValidationError,
            r"without any individual confirmations",
        ),
    ],
)
def test_applicant_confirmation_round_start_for_document(
    db,
    additional_demand_settings,
    applicant_confirmation_round_factory,
    applicant_factory,
    caluma_case_factory,
    caluma_document_factory,
    caluma_work_item_factory,
    error_cls,
    error_msg,
    error_scenario,
    fake_request,
    form_scenario,
    instance,
    mocker,
    permission_mock,
):
    applicants_mock = mocker.patch(
        "camac.applicants.models.get_applicants_requiring_confirmation",
        return_value=[
            (a, []) for a in applicant_factory.create_batch(3, instance=instance)
        ],
    )

    document = caluma_document_factory()

    case = caluma_case_factory()
    case.instance = instance
    case.save()

    if form_scenario == "main_form":
        document.case = case
        document.save()
    elif form_scenario == "additional_demand":
        document.work_item = caluma_work_item_factory(
            case=case, task__pk=additional_demand_settings["FILL_TASK"]
        )
        document.save()
    elif form_scenario == "material_exam":
        document.work_item = caluma_work_item_factory(case=case)
        document.save()

    if error_scenario == "has_active":
        applicant_confirmation_round_factory(
            document=document,
            status=ApplicantConfirmationRound.Status.RUNNING,
        )
    elif error_scenario == "no_applicants":
        applicants_mock.return_value = []

    start_fn = partial(
        ApplicantConfirmationRound.objects.start_for_document,
        document,
        fake_request,
    )

    if error_cls:
        with pytest.raises(error_cls, match=error_msg):
            start_fn()
    else:
        round = start_fn()

        assert permission_mock.call_count == 1
        assert permission_mock.call_args[0][1] == "applicant-confirmation-start"

        if form_scenario == "main_form":
            assert round.step == ApplicantConfirmationRound.Step.SUBMIT
        else:
            assert round.step == ApplicantConfirmationRound.Step.ADDITIONAL_DEMAND


@pytest.mark.freeze_time("2026-03-30 11:22")
@pytest.mark.parametrize(
    ("is_last", "error_scenario", "error_cls", "error_msg"),
    [
        (False, None, None, None),
        (True, None, None, None),
        (False, "not_user", PermissionDenied, None),
        (
            False,
            "not_pending",
            ValidationError,
            r"Only pending applicant confirmations can be confirmed",
        ),
        (
            False,
            "round_not_running",
            ValidationError,
            r"can only be confirmed while the round is running",
        ),
    ],
)
def test_applicant_confirmation_confirm(
    db,
    admin_user,
    applicant_confirmation_factory,
    applicant_confirmation_round_factory,
    applicants_settings,
    caluma_document_factory,
    error_cls,
    error_msg,
    error_scenario,
    fake_request,
    form_setup,
    is_last,
    permission_mock,
    user_factory,
):
    round = applicant_confirmation_round_factory(
        status=(
            ApplicantConfirmationRound.Status.COMPLETED
            if error_scenario == "round_not_running"
            else ApplicantConfirmationRound.Status.RUNNING
        ),
        document=caluma_document_factory(form=form_setup),
    )
    confirmation = applicant_confirmation_factory(
        status=(
            ApplicantConfirmation.Status.CONFIRMED
            if error_scenario == "not_pending"
            else ApplicantConfirmation.Status.PENDING
        ),
        applicant__invitee=(
            user_factory() if error_scenario == "not_user" else admin_user
        ),
        round=round,
    )
    applicant_confirmation_factory(
        status=(
            ApplicantConfirmation.Status.CONFIRMED
            if is_last
            else ApplicantConfirmation.Status.PENDING
        ),
        round=round,
    )

    if error_cls:
        with pytest.raises(error_cls, match=error_msg):
            confirmation.confirm(fake_request)
    else:
        confirmation.confirm(fake_request)

        assert permission_mock.call_count == 1
        assert permission_mock.call_args[0][1] == "applicant-confirmation-confirm"

        assert confirmation.status == ApplicantConfirmation.Status.CONFIRMED
        assert confirmation.closed_at.isoformat() == "2026-03-30T11:22:00+00:00"

        if is_last:
            round.refresh_from_db()

            assert round.status == ApplicantConfirmationRound.Status.COMPLETED
            assert round.closed_at.isoformat() == "2026-03-30T11:22:00+00:00"

            # Confirmation question is set
            assert round.document.answers.filter(
                question_id=applicants_settings.confirmation_question,
                value=applicants_settings.confirmation_answer,
            ).exists()


@pytest.mark.freeze_time("2026-03-30 11:23")
@pytest.mark.parametrize(
    ("status", "error_cls", "error_msg"),
    [
        (ApplicantConfirmationRound.Status.COMPLETED, None, None),
        (
            ApplicantConfirmationRound.Status.CANCELED,
            ValidationError,
            r"Only completed applicant confirmation rounds can be invalidated",
        ),
    ],
)
def test_applicant_confirmation_round_invalidate(
    db,
    applicant_confirmation_factory,
    applicant_confirmation_round_factory,
    applicants_settings,
    caluma_document_factory,
    error_cls,
    error_msg,
    fake_request,
    form_setup,
    permission_mock,
    status,
):
    round = applicant_confirmation_round_factory(
        status=status, document=caluma_document_factory(form=form_setup)
    )
    applicant_confirmation_factory.create_batch(
        3, round=round, status=ApplicantConfirmation.Status.CONFIRMED
    )

    if error_cls:
        with pytest.raises(error_cls, match=error_msg):
            round.invalidate(fake_request)
    else:
        round.invalidate(fake_request)

        assert permission_mock.call_count == 1
        assert permission_mock.call_args[0][1] == "applicant-confirmation-invalidate"

        assert round.status == ApplicantConfirmationRound.Status.INVALIDATED
        assert round.closed_at.isoformat() == "2026-03-30T11:23:00+00:00"

        # All confirmations are invalidated
        assert round.confirmations.count() == 3
        assert (
            round.confirmations.filter(
                status=ApplicantConfirmation.Status.INVALIDATED
            ).count()
            == 3
        )

        # Confirmation question is reset
        assert round.document.answers.filter(
            question_id=applicants_settings.confirmation_question,
            value=[],
        ).exists()


@pytest.mark.freeze_time("2026-03-30 11:24")
@pytest.mark.parametrize(
    ("status", "error_cls", "error_msg"),
    [
        (ApplicantConfirmationRound.Status.RUNNING, None, None),
        (
            ApplicantConfirmationRound.Status.COMPLETED,
            ValidationError,
            r"Only running applicant confirmation rounds can be canceled",
        ),
    ],
)
def test_applicant_confirmation_round_cancel(
    db,
    applicant_confirmation_factory,
    applicant_confirmation_round_factory,
    caluma_document_factory,
    error_cls,
    error_msg,
    fake_request,
    form_setup,
    permission_mock,
    status,
):
    round = applicant_confirmation_round_factory(
        status=status, document=caluma_document_factory(form=form_setup)
    )
    applicant_confirmation_factory.create_batch(
        2, round=round, status=ApplicantConfirmation.Status.CONFIRMED
    )
    applicant_confirmation_factory.create_batch(
        3, round=round, status=ApplicantConfirmation.Status.PENDING
    )

    if error_cls:
        with pytest.raises(error_cls, match=error_msg):
            round.cancel(fake_request)
    else:
        round.cancel(fake_request)

        assert permission_mock.call_count == 1
        assert permission_mock.call_args[0][1] == "applicant-confirmation-cancel"

        assert round.status == ApplicantConfirmationRound.Status.CANCELED
        assert round.closed_at.isoformat() == "2026-03-30T11:24:00+00:00"

        # Confirmed confirmations are invalidated and pending confirmations are canceled
        assert round.confirmations.count() == 5
        assert (
            round.confirmations.filter(
                status=ApplicantConfirmation.Status.INVALIDATED
            ).count()
            == 2
        )
        assert (
            round.confirmations.filter(
                status=ApplicantConfirmation.Status.CANCELED
            ).count()
            == 3
        )


def test_applicant_confirmation_properties(
    db, applicant_confirmation_factory, caluma_question_factory, user_factory
):
    user = user_factory(name="John", surname="Doe")

    confirmation_with_user = applicant_confirmation_factory(applicant__invitee=user)
    confirmation_without_user = applicant_confirmation_factory(
        applicant__invitee=None,
        applicant__email="john.doe@acme.com",
    )

    assert confirmation_with_user.user == user
    assert confirmation_without_user.user is None

    assert confirmation_with_user.display_name == "John Doe"
    assert confirmation_without_user.display_name == "john.doe@acme.com"

    confirmation_with_user.source_questions.set(
        [
            caluma_question_factory(label="Applicant"),
            caluma_question_factory(label="Landowner"),
        ]
    )
    assert sorted(confirmation_with_user.roles) == ["Applicant", "Landowner"]
