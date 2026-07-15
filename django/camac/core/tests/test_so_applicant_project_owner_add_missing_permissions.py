import pytest
from django.core.management import call_command

from camac.applicants.models import ROLE_CHOICES, Applicant
from camac.permissions.models import InstanceACL

COMMAND = "so_applicant_project_owner_add_missing_permissions"


@pytest.fixture
def so_applicant_setup(
    set_application_so,
    so_permissions_settings,
    so_access_levels,
    settings,
    user_factory,
    notification_template,
):
    settings.ENABLE_TOKEN_EXCHANGE = True
    settings.TOKEN_EXCHANGE_USERNAME_PREFIX = "egov:"
    settings.APPLICATION["NOTIFICATIONS"]["APPLICANT"] = {
        "NEW": notification_template.slug,
        "EXISTING": notification_template.slug,
    }

    user_factory(username=settings.APPLICATION["SYSTEM_USER"])


@pytest.fixture
def so_instance(so_instance):
    """Drop the applicant the instance factory adds, so tests start clean."""

    so_instance.involved_applicants.all().delete()
    return so_instance


@pytest.fixture
def internal_user(user_factory):
    def factory(email):
        return user_factory(username=f"internal-{email}", email=email)

    return factory


@pytest.fixture
def portal_user(user_factory):
    def factory(email, disabled=False):
        return user_factory(username=f"egov:{email}", email=email, disabled=disabled)

    return factory


def active_applicant_acls(instance, user):
    return InstanceACL.currently_active().filter(
        instance=instance, user=user, access_level="applicant"
    )


@pytest.mark.django_db
def test_wrong_application(set_application_be):
    with pytest.raises(Exception, match="Only for Kt SO"):
        call_command(COMMAND, commit=True)


@pytest.mark.django_db
def test_token_exchange_disabled(
    so_applicant_setup, so_instance, applicant_factory, internal_user, settings
):
    """Without token exchange every project owner would look wrongly linked."""

    settings.ENABLE_TOKEN_EXCHANGE = False

    email = "someone@example.com"
    applicant = applicant_factory(
        instance=so_instance,
        invitee=internal_user(email),
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    with pytest.raises(Exception, match="token exchange"):
        call_command(COMMAND, commit=True)

    assert Applicant.objects.filter(pk=applicant.pk).exists()


@pytest.mark.django_db
def test_grants_missing_acl(
    so_applicant_setup, so_instance, applicant_factory, portal_user
):
    user = portal_user("someone@example.com")
    applicant = applicant_factory(
        instance=so_instance,
        invitee=user,
        email=user.email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    assert not active_applicant_acls(so_instance, user).exists()

    call_command(COMMAND, commit=True)

    applicant.refresh_from_db()
    assert applicant.invitee == user
    assert active_applicant_acls(so_instance, user).count() == 1


@pytest.mark.django_db
def test_moves_applicant_to_portal_user(
    so_applicant_setup,
    so_instance,
    applicant_factory,
    internal_user,
    portal_user,
    mailoutbox,
):
    email = "someone@example.com"
    internal = internal_user(email)
    portal = portal_user(email)

    old_applicant = applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND, commit=True)

    assert not Applicant.objects.filter(pk=old_applicant.pk).exists()

    new_applicant = so_instance.involved_applicants.get()
    assert new_applicant.invitee == portal
    assert new_applicant.email == email
    assert new_applicant.role == ROLE_CHOICES.PROJECT_OWNER

    assert active_applicant_acls(so_instance, portal).count() == 1
    assert not active_applicant_acls(so_instance, internal).exists()

    # The address already got the "existing account" invitation, and the portal
    # account it points at does exist - no need to mail again.
    assert mailoutbox == []


@pytest.mark.django_db
def test_moves_applicant_without_portal_user(
    so_applicant_setup,
    so_instance,
    applicant_factory,
    internal_user,
    mailoutbox,
):
    email = "someone@example.com"
    internal = internal_user(email)

    old_applicant = applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND, commit=True)

    assert not Applicant.objects.filter(pk=old_applicant.pk).exists()

    new_applicant = so_instance.involved_applicants.get()
    assert new_applicant.invitee is None
    assert new_applicant.email == email

    assert not active_applicant_acls(so_instance, internal).exists()
    assert not InstanceACL.currently_active().filter(access_level="applicant").exists()

    # They were told to log in with an account they never had, so they get the
    # registration invitation now.
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [email]


@pytest.mark.django_db
def test_disabled_portal_user_is_ignored(
    so_applicant_setup, so_instance, applicant_factory, internal_user, portal_user
):
    email = "someone@example.com"
    internal = internal_user(email)
    disabled = portal_user(email, disabled=True)

    applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND, commit=True)

    migrated = so_instance.involved_applicants.get(email=email)
    assert migrated.invitee is None
    assert not active_applicant_acls(so_instance, disabled).exists()


@pytest.mark.django_db
def test_portal_user_is_already_applicant(
    so_applicant_setup, so_instance, applicant_factory, internal_user, portal_user
):
    email = "someone@example.com"
    internal = internal_user(email)
    portal = portal_user(email)

    existing = applicant_factory(
        instance=so_instance,
        invitee=portal,
        email=email,
        role=ROLE_CHOICES.ADMIN,
    )
    old_applicant = applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND, commit=True)

    assert not Applicant.objects.filter(pk=old_applicant.pk).exists()

    existing.refresh_from_db()
    assert existing.role == ROLE_CHOICES.PROJECT_OWNER
    assert so_instance.involved_applicants.count() == 1

    # The ACL was already granted while filling in the missing ones
    assert active_applicant_acls(so_instance, portal).count() == 1


@pytest.mark.django_db
def test_leaves_other_applicants_alone(
    so_applicant_setup, so_instance, applicant_factory, internal_user
):
    """Only project owners were affected by the bug."""

    email = "someone@example.com"
    internal = internal_user(email)

    applicant = applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.ADMIN,
    )

    call_command(COMMAND, commit=True)

    applicant.refresh_from_db()
    assert applicant.invitee == internal
    assert active_applicant_acls(so_instance, internal).count() == 1


@pytest.mark.django_db
def test_is_idempotent(
    so_applicant_setup, so_instance, applicant_factory, internal_user, portal_user
):
    email = "someone@example.com"
    internal = internal_user(email)
    portal = portal_user(email)

    applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND, commit=True)
    call_command(COMMAND, commit=True)

    assert so_instance.involved_applicants.get().invitee == portal
    assert active_applicant_acls(so_instance, portal).count() == 1


@pytest.mark.django_db
def test_dry_run(
    so_applicant_setup,
    so_instance,
    applicant_factory,
    internal_user,
    portal_user,
    mailoutbox,
):
    email = "someone@example.com"
    internal = internal_user(email)
    portal_user(email)

    old_applicant = applicant_factory(
        instance=so_instance,
        invitee=internal,
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND)

    assert so_instance.involved_applicants.get() == old_applicant
    assert not InstanceACL.objects.filter(instance=so_instance).exists()
    assert mailoutbox == []


@pytest.mark.django_db
def test_dry_run_previews_mail(
    so_applicant_setup,
    so_instance,
    applicant_factory,
    internal_user,
    mailoutbox,
    capsys,
):
    email = "someone@example.com"

    applicant_factory(
        instance=so_instance,
        invitee=internal_user(email),
        email=email,
        role=ROLE_CHOICES.PROJECT_OWNER,
    )

    call_command(COMMAND)

    assert f"Would send Mail to {email}" in capsys.readouterr().out
    assert mailoutbox == []
