import json

import pytest
from django.conf import settings
from jose.exceptions import ExpiredSignatureError, JOSEError
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed

from camac.user.authentication import JSONWebTokenKeycloakAuthentication


def test_authenticate_no_headers(rf):
    request = rf.request()
    assert JSONWebTokenKeycloakAuthentication().authenticate(request) is None


def test_authenticate_disabled_user(rf, admin_user, mocker, clear_cache):
    token_dict = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.name,
        "given_name": admin_user.surname,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_dict
    mocker.patch("keycloak.KeycloakOpenID.certs")

    mocker.patch("keycloak.KeycloakOpenID.userinfo", return_value=token_dict)

    admin_user.disabled = True
    admin_user.save()

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("demo_mode", [True, False])
@pytest.mark.parametrize(
    "token_value,username",
    [
        (
            {
                "sub": "new-here",
                "email": "new-guy@example.com",
                "family_name": "New",
                "given_name": "Guy",
                settings.OIDC_USERNAME_CLAIM: "new-here",
            },
            "new-here",
        ),
        (
            {
                "sub": "service-account-gemeinde",
                "email": "new-guy@example.com",
                "clientId": "testClient",
                settings.OIDC_USERNAME_CLAIM: "service-account-gemeinde",
            },
            "service-account-gemeinde",
        ),
    ],
)
def test_authenticate_new_user(
    rf,
    admin_user,
    mocker,
    demo_mode,
    settings,
    application_settings,
    token_value,
    username,
    applicant_factory,
    clear_cache,
):
    applicant_factory(email=token_value["email"], invitee=None)

    if demo_mode:
        admin_group = admin_user.groups.first()
        inexistent_group = 2138242342
        settings.DEMO_MODE = True
        application_settings["DEMO_MODE_GROUPS"] = [admin_group.pk, inexistent_group]

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    if demo_mode:
        assert user.groups.count() == 1
        assert user.groups.first() == admin_group
    else:
        assert user.groups.count() == 0
    assert decode_token.return_value == token


def test_authenticate_ok(rf, admin_user, mocker, clear_cache):
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.name,
        "given_name": admin_user.surname,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    assert user == admin_user
    assert decode_token.return_value == token


@pytest.mark.parametrize("is_id_token", [True, False])
@pytest.mark.parametrize(
    "authentication_header,authenticated,error",
    [
        ("", False, False),
        ("Bearer", False, True),
        ("Bearer Too many params", False, True),
        ("Basic Auth", False, True),
        ("Bearer Token", True, False),
    ],
)
@pytest.mark.parametrize("user__username", ["1"])
def test_django_admin_oidc_authentication(
    db,
    user,
    rf,
    authentication_header,
    authenticated,
    error,
    is_id_token,
    requests_mock,
    settings,
):
    userinfo = {"sub": "1", "preferred_username": "1"}
    requests_mock.get(settings.OIDC_OP_USER_ENDPOINT, text=json.dumps(userinfo))

    if not is_id_token:
        userinfo = {"client_id": "test_client", "sub": "1"}
        requests_mock.get(
            settings.OIDC_OP_USER_ENDPOINT, status_code=status.HTTP_401_UNAUTHORIZED
        )
        requests_mock.post(
            settings.OIDC_OP_INTROSPECT_ENDPOINT, text=json.dumps(userinfo)
        )

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)
    try:
        result = OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if result:
            user, auth = result
            assert user.is_authenticated


@pytest.mark.parametrize("side_effect", [ExpiredSignatureError(), JOSEError()])
def test_authenticate_side_effect(rf, mocker, side_effect, clear_cache):
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.side_effect = side_effect
    mocker.patch("keycloak.KeycloakOpenID.certs")

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("authorization", ["Bearer", "Bearer token token"])
def test_get_jwt_value_invalid_authorization(db, rf, authorization):
    request = rf.request(HTTP_AUTHORIZATION=authorization)
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().get_jwt_value(request)


def test_authenticate_header(db, rf, settings):
    request = rf.request()
    header = JSONWebTokenKeycloakAuthentication().authenticate_header(request)
    assert settings.KEYCLOAK_REALM in header
