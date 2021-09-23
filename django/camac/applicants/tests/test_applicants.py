import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


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
    activation,
):
    if extra_applicants:
        applicant_factory.create_batch(extra_applicants, instance=be_instance)

    url = reverse("applicant-detail", args=[be_instance.involved_applicants.first().pk])

    response = admin_client.delete(url)

    assert response.status_code == expected_status


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
):
    url = reverse("applicant-list")

    applicant_factory(
        instance=be_instance,
        invitee=user_factory(email="exists@example.com"),
        email="exists@example.com",
    )

    # This simulates a case where a user was invited with an email, then changed
    # it's email (which is totally possible) and then another user registered
    # with that old email address. That user should be allowed to be invited
    # since it's a different user.
    user_factory(email="old@example.com"),
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
