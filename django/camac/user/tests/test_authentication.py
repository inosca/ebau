import pytest
from django.conf import settings
from jose.exceptions import ExpiredSignatureError, JOSEError
from rest_framework.exceptions import AuthenticationFailed

from camac.user.authentication import JSONWebTokenKeycloakAuthentication


def test_authenticate_no_headers(rf):
    request = rf.request()
    assert JSONWebTokenKeycloakAuthentication().authenticate(request) is None


def test_authenticate_disabled_user(admin_rf, admin_user):
    admin_user.disabled = True
    admin_user.save()

    request = admin_rf.request()
    with pytest.raises(AuthenticationFailed):
        assert JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("side_effect", [ExpiredSignatureError(), JOSEError()])
def test_authenticate_side_effect(admin_rf, mocker, side_effect):
    decode_token = mocker.patch("keycloak.KeycloakOpenID.decode_token")
    decode_token.side_effect = side_effect

    request = admin_rf.request()
    with pytest.raises(AuthenticationFailed):
        assert JSONWebTokenKeycloakAuthentication().authenticate(request)


@pytest.mark.parametrize("authorization", ["Bearer", "Bearer token token"])
def test_get_jwt_value_invalid_authorization(rf, authorization):
    rf.defaults = {"HTTP_AUTHORIZATION": authorization}
    request = rf.request()
    with pytest.raises(AuthenticationFailed):
        JSONWebTokenKeycloakAuthentication().get_jwt_value(request)


def test_authenticate_header(rf):
    request = rf.request()
    header = JSONWebTokenKeycloakAuthentication().authenticate_header(request)
    assert settings.KEYCLOAK_REALM in header
