import pytest
from django.core.cache import cache
from jose.exceptions import ExpiredSignatureError, JOSEError
from rest_framework.exceptions import AuthenticationFailed

from camac.user.authentication import JSONWebTokenKeycloakAuthentication


@pytest.fixture(scope="function", autouse=True)
def clear_cache():
    cache.clear()


def test_authenticate_no_headers(rf):
    request = rf.request()
    assert JSONWebTokenKeycloakAuthentication().authenticate(request) is None


def test_authenticate_disabled_user(rf, admin_user, mocker):
    token_dict = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.name,
        "given_name": admin_user.surname,
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
            },
            "new-here",
        ),
        (
            {
                "sub": "service-account-gemeinde",
                "email": "new-guy@example.com",
                "clientId": "testClient",
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

    assert user.username == request.caluma_info.context.user.username == username
    if demo_mode:
        assert user.groups.count() == 1
        assert user.groups.first() == admin_group
    else:
        assert user.groups.count() == 0
    assert decode_token.return_value == token


def test_authenticate_ok(rf, admin_user, mocker):
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.name,
        "given_name": admin_user.surname,
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


@pytest.mark.parametrize("side_effect", [ExpiredSignatureError(), JOSEError()])
def test_authenticate_side_effect(rf, mocker, side_effect):
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.side_effect = side_effect
    mocker.patch("keycloak.KeycloakOpenID.certs")

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("authorization", ["Bearer", "Bearer token token"])
def test_get_jwt_value_invalid_authorization(rf, authorization):
    request = rf.request(HTTP_AUTHORIZATION=authorization)
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().get_jwt_value(request)


def test_authenticate_header(rf, settings):
    request = rf.request()
    header = JSONWebTokenKeycloakAuthentication().authenticate_header(request)
    assert settings.KEYCLOAK_REALM in header


def test_authenticate_bootstrap_by_mail(
    rf,
    mocker,
    application_settings,
    user_factory,
):
    token_value = {
        "sub": "existing-already",
        "email": "existing-guy@example.com",
        "family_name": "Existing",
        "given_name": "Guy",
    },

    # The user with the same email should be updated with keycloak information
    user_factory(email=token_value['email'])

    application_settings['OIDC_BOOTSTRAP_BY_EMAIL'] = True

    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.return_value = token_value
    mocker.patch("keycloak.KeycloakOpenID.certs")

    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token")
    user, token = JSONWebTokenKeycloakAuthentication().authenticate(request)

    assert user.username == token['sub']
    assert user.name == token['family_name']
    assert user.surname == token['given_name']
    assert user.groups.count() == 0
    assert decode_token.return_value == token
