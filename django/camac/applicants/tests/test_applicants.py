import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.permissions.conditions import Always
from camac.permissions.events import Trigger
from camac.permissions.models import AccessLevel
from camac.permissions.switcher import PERMISSION_MODE


@pytest.fixture
def app_settings_with_notif_templates(application_settings, notification_template):
    application_settings["NOTIFICATIONS"]["APPLICANT"][
        "NEW"
    ] = notification_template.slug
    application_settings["NOTIFICATIONS"]["APPLICANT"][
        "EXISTING"
    ] = notification_template.slug


@pytest.mark.parametrize(
    "role__name,instance__user,expected_applicants",
    [
        ("Applicant", LazyFixture("admin_user"), 1),
        ("Public", LazyFixture("user"), 0),
    ],
)
def test_applicant_list(
    admin_client, role, be_instance, django_assert_num_queries, expected_applicants
):
    url = reverse("applicant-list")

    with django_assert_num_queries(2):
        response = admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == expected_applicants


def test_applicant_update(admin_client, be_instance):
    url = reverse("applicant-detail", args=[be_instance.involved_applicants.first().pk])

    response = admin_client.patch(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.fixture
def applicant_permissions_module(permissions_settings, access_level_factory):
    lvl = access_level_factory(slug="applicant", applicable_area="APPLICANT")
    muni = access_level_factory(slug="municipality", applicable_area="INTERNAL")

    # Bern already does the "right" thing
    mod = "camac.permissions.config.kt_bern.PermissionEventHandlerBE"

    permissions_settings["EVENT_HANDLER"] = mod
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.AUTO_ON

    permissions_settings.setdefault("ACCESS_LEVELS", {})

    permissions_settings["ACCESS_LEVELS"][lvl.slug] = [
        ("applicant-add", Always()),
        ("applicant-remove", Always()),
        ("applicant-read", Always()),
    ]
    permissions_settings["ACCESS_LEVELS"][muni.slug] = [
        ("applicant-read", Always()),
    ]

    # return value is just for parametrization id
    return "permissions_module_active"


def _sync_applicants(instance):
    # Factories / fixtures don't trigger permission events, so we have to
    for appl in instance.involved_applicants.all():
        Trigger.applicant_added(None, appl.instance, appl)


@pytest.mark.parametrize("use_permission_mod", [True, False])
@pytest.mark.parametrize(
    "role__name,instance__user,extra_applicants,expected_status",
    [
        ("Applicant", LazyFixture("admin_user"), 0, status.HTTP_403_FORBIDDEN),
        ("Applicant", LazyFixture("admin_user"), 1, status.HTTP_204_NO_CONTENT),
        ("Municipality", LazyFixture("admin_user"), 1, status.HTTP_403_FORBIDDEN),
        ("Service", LazyFixture("admin_user"), 1, status.HTTP_403_FORBIDDEN),
        ("Canton", LazyFixture("admin_user"), 1, status.HTTP_403_FORBIDDEN),
        ("Support", LazyFixture("admin_user"), 1, status.HTTP_204_NO_CONTENT),
    ],
)
def test_applicant_delete(
    admin_client,
    be_instance,
    applicant_factory,
    extra_applicants,
    expected_status,
    active_inquiry_factory,
    use_permission_mod,
    request,
    role,
    instance_acl_factory,
):
    active_inquiry_factory(be_instance)
    if extra_applicants:
        applicant_factory.create_batch(extra_applicants, instance=be_instance)

    if use_permission_mod:
        # TODO can we lazyfixture this?
        request.getfixturevalue("applicant_permissions_module")
        _sync_applicants(be_instance)
        if role.name == "Municipality":
            instance_acl_factory(
                user=admin_client.user,
                grant_type="USER",
                access_level_id="municipality",
                instance=be_instance,
            )

    url = reverse("applicant-detail", args=[be_instance.involved_applicants.first().pk])

    response = admin_client.delete(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize("use_permission_mod", [True, False])
@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,passed_email,existing_user,expected_status",
    [
        ("Applicant", "test@example.com", False, status.HTTP_201_CREATED),
        ("Applicant", "user@example.com", True, status.HTTP_201_CREATED),
        ("Applicant", "Test@example.com", False, status.HTTP_201_CREATED),
        ("Applicant", "User@example.com", True, status.HTTP_201_CREATED),
        ("Applicant", "exists@example.com", None, status.HTTP_400_BAD_REQUEST),
        ("Applicant", "Exists@example.com", None, status.HTTP_400_BAD_REQUEST),
        ("Applicant", "old@example.com", None, status.HTTP_201_CREATED),
        ("Applicant", "new@example.com", None, status.HTTP_400_BAD_REQUEST),
        ("Municipality", "test@example.com", None, status.HTTP_403_FORBIDDEN),
        ("Service", "test@example.com", None, status.HTTP_403_FORBIDDEN),
        ("Canton", "test@example.com", None, status.HTTP_403_FORBIDDEN),
        ("Support", "user@example.com", True, status.HTTP_201_CREATED),
    ],
)
def test_applicant_create(
    admin_client,
    user_factory,
    role,
    be_instance,
    applicant_factory,
    passed_email,
    existing_user,
    expected_status,
    app_settings_with_notif_templates,
    use_permission_mod,
    request,
):
    url = reverse("applicant-list")

    applicant_factory(
        instance=be_instance,
        invitee=user_factory(email="exists@example.com"),
        email="exists@example.com",
    )
    if use_permission_mod:
        # TODO can we lazyfixture this?
        request.getfixturevalue("applicant_permissions_module")
        _sync_applicants(be_instance)

    # This simulates a case where a user was invited with an email, then changed
    # it's email (which is totally possible) and then another user registered
    # with that old email address. That user should be allowed to be invited
    # since it's a different user.
    user_factory(email="old@example.com")
    applicant_factory(
        instance=be_instance,
        invitee=user_factory(email="new@example.com"),
        email="old@example.com",
    )

    user_factory(email="user@example.com")

    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "applicants",
                "attributes": {"email": passed_email},
                "relationships": {
                    "instance": {"data": {"id": be_instance.pk, "type": "instances"}}
                },
            }
        },
    )

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        assert response.json()["data"]["relationships"]["user"]["data"]["id"] == str(
            admin_client.user.id
        )
        assert response.json()["data"]["attributes"]["email"] == passed_email.lower()

    if existing_user:
        assert response.json()["data"]["relationships"]["invitee"]["data"]


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
def test_applicant_create_multiple_users(
    admin_client, be_instance, user_factory, app_settings_with_notif_templates
):
    url = reverse("applicant-list")

    user_factory(email="test@example.com")
    user_factory(email="test@example.com")

    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "applicants",
                "attributes": {"email": "test@example.com"},
                "relationships": {
                    "instance": {"data": {"id": be_instance.pk, "type": "instances"}}
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
def test_missing_applicant_access_level(
    admin_client,
    be_instance,
    user_factory,
    app_settings_with_notif_templates,
    applicant_permissions_module,
    caplog,
    permissions_settings,
):
    url = reverse("applicant-list")

    # In this test specifically, we want to test what happens if the
    # applicant access level is missing
    AccessLevel.objects.filter(slug="applicant").delete()

    # We need to be in "old" mode, as otherwise the "new" permissions code will
    # reject adding applicants (since there are no permissions)
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    the_user = user_factory(email="test@example.com")

    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "applicants",
                "attributes": {"email": "test@example.com"},
                "relationships": {
                    "instance": {"data": {"id": be_instance.pk, "type": "instances"}}
                },
            }
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    invitee_id = response.json()["data"]["relationships"]["invitee"]["data"]["id"]
    assert str(invitee_id) == str(the_user.pk)

    # This is the warning we're looking for
    assert "Access level 'applicant' is not configured" in caplog.messages
