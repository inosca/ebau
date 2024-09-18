import pytest
from django.urls import reverse
from graphene_django.views import HttpError
from rest_framework import status

from camac.caluma.conftest import *  # noqa: F403
from camac.caluma.views import CamacAuthenticatedGraphQLView
from camac.token_exchange.permissions import get_lot


@pytest.mark.parametrize(
    "has_token,has_lot,expected_value",
    [
        (True, True, 1),
        (False, True, None),
        (True, False, None),
    ],
)
def test_get_lot(rf, has_token, has_lot, expected_value, mocker):
    headers = {}
    token_data = {}

    if has_token:
        headers["HTTP_AUTHORIZATION"] = "Bearer foo"

    if has_lot:
        token_data["lot"] = 1

    mocker.patch("camac.token_exchange.permissions.decode", return_value=token_data)

    assert get_lot(rf.request(**headers)) == expected_value


@pytest.mark.parametrize(
    "role_name,lot,expected_status",
    [
        ("public", 1, status.HTTP_200_OK),
        ("public", 2, status.HTTP_200_OK),
        ("public", None, status.HTTP_403_FORBIDDEN),
        ("applicant", 1, status.HTTP_403_FORBIDDEN),
        ("applicant", 2, status.HTTP_200_OK),
        ("applicant", None, status.HTTP_403_FORBIDDEN),
        # Role without LoT requirement
        ("municipality", 1, status.HTTP_200_OK),
        ("municipality", 2, status.HTTP_200_OK),
        ("municipality", None, status.HTTP_200_OK),
    ],
)
def test_require_lot_permission(
    db, admin_client, expected_status, lot, mocker, role_name
):
    mocker.patch("camac.token_exchange.permissions.get_lot", return_value=lot)
    mocker.patch("camac.user.permissions.get_role_name", return_value=role_name)

    response = admin_client.get(reverse("me"))
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role_name,lot,expect_error",
    [
        ("public", 1, False),
        ("public", 2, False),
        ("public", None, True),
        ("applicant", 1, True),
        ("applicant", 2, False),
        ("applicant", None, True),
        # Role without LoT requirement
        ("municipality", 1, False),
        ("municipality", 2, False),
        ("municipality", None, False),
    ],
)
def test_require_lot_permission_graphql(
    db, admin_user, expect_error, group, lot, mocker, rf, role_name, settings
):
    mocker.patch(
        "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo",
        return_value={
            "sub": admin_user.username,
            "email": admin_user.email,
            "family_name": admin_user.surname,
            "given_name": admin_user.name,
            settings.OIDC_USERNAME_CLAIM: admin_user.username,
        },
    )
    mocker.patch("camac.caluma.utils.jwt_decode")
    mocker.patch("camac.token_exchange.permissions.get_lot", return_value=lot)
    mocker.patch("camac.user.permissions.get_role_name", return_value=role_name)

    settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.local"

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token", X_CAMAC_GROUP=group.pk)

    if expect_error:
        with pytest.raises(HttpError) as e:
            CamacAuthenticatedGraphQLView().get_user(request)

        assert e.value.response.status_code == status.HTTP_403_FORBIDDEN
    else:
        CamacAuthenticatedGraphQLView().get_user(request)
