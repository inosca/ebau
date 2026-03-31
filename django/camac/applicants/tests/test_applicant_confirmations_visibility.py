import pytest

from camac.applicants.models import ApplicantConfirmation, ApplicantConfirmationRound
from camac.permissions.api import GRANT_CHOICES, grant
from camac.permissions.conditions import Static
from camac.permissions.switcher import PERMISSION_MODE


@pytest.fixture
def permissions_setup(
    db, access_level_factory, admin_user, instance_factory, permissions_settings
):
    instance1 = instance_factory()
    instance2 = instance_factory()

    access_level1 = access_level_factory()
    access_level2 = access_level_factory()

    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level1.pk: [("applicant-confirmation-read", Static())],
        access_level2.pk: {},
    }

    grant(
        instance1,
        grant_type=GRANT_CHOICES.USER.value,
        access_level=access_level1,
        user=admin_user,
    )

    grant(
        instance2,
        grant_type=GRANT_CHOICES.USER.value,
        access_level=access_level2,
        user=admin_user,
    )

    return instance1, instance2


def test_applicant_confirmation_visibility(
    applicant_confirmation_factory, fake_request, permissions_setup
):
    instance1, instance2 = permissions_setup

    visible = applicant_confirmation_factory(round__instance=instance1)
    applicant_confirmation_factory(round__instance=instance2)

    qs = ApplicantConfirmation.objects.for_request(fake_request)

    assert qs.count() == 1
    assert qs.first() == visible


def test_applicant_confirmation_round_visibility(
    applicant_confirmation_round_factory, fake_request, permissions_setup
):
    instance1, instance2 = permissions_setup

    visible = applicant_confirmation_round_factory(instance=instance1)
    applicant_confirmation_round_factory(instance=instance2)

    qs = ApplicantConfirmationRound.objects.for_request(fake_request)

    assert qs.count() == 1
    assert qs.first() == visible
