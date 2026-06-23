import pytest
from django.db.models import QuerySet

from camac.applicants.models import ApplicantConfirmation, ApplicantConfirmationRound


def pk_set(qs_or_list):
    if isinstance(qs_or_list, QuerySet):
        pks = qs_or_list.values_list("pk", flat=True)
    else:
        pks = [obj.pk for obj in qs_or_list]

    return set(pks)


@pytest.mark.django_db
def test_applicant_confirmation_queryset(applicant_confirmation_factory):
    pending = applicant_confirmation_factory(
        status=ApplicantConfirmation.Status.PENDING
    )
    confirmed = applicant_confirmation_factory(
        status=ApplicantConfirmation.Status.CONFIRMED
    )

    qs = ApplicantConfirmation.objects.all()

    assert pk_set(qs.only_pending()) == pk_set([pending])
    assert pk_set(qs.only_confirmed()) == pk_set([confirmed])
    assert qs.has_pending()
    assert not qs.only_confirmed().has_pending()

    qs.cancel_pending()
    pending.refresh_from_db()
    assert pending.closed_at is not None
    assert pending.status == ApplicantConfirmation.Status.CANCELED

    qs.invalidate_confirmed()
    confirmed.refresh_from_db()
    assert confirmed.closed_at is not None
    assert confirmed.status == ApplicantConfirmation.Status.INVALIDATED


@pytest.mark.django_db
def test_applicant_confirmation_round_queryset(
    applicant_confirmation_round_factory, caluma_document_factory
):
    document = caluma_document_factory()

    for_document = applicant_confirmation_round_factory(
        document=document, status=ApplicantConfirmationRound.Status.CANCELED
    )
    active1 = applicant_confirmation_round_factory(
        document=caluma_document_factory(),
        status=ApplicantConfirmationRound.Status.RUNNING,
    )
    active2 = applicant_confirmation_round_factory(
        document=caluma_document_factory(),
        status=ApplicantConfirmationRound.Status.COMPLETED,
    )

    qs = ApplicantConfirmationRound.objects.all()

    assert pk_set(qs.for_document(document)) == pk_set([for_document])
    assert pk_set(qs.only_active()) == pk_set([active1, active2])
    assert qs.has_active()
    assert not qs.for_document(document).has_active()
