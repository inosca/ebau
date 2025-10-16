from datetime import datetime, timedelta

import pytest
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_user.views import HttpResponseUnauthorized
from django.core.signing import Signer
from django.utils.timezone import make_aware
from graphene_django.views import HttpError

from camac.caluma.views import HttpResponseForbidden

from ..views import CamacAuthenticatedGraphQLView


def test_authenticate_caluma(rf, settings, admin_user, group, mocker):
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.surname,
        "given_name": admin_user.name,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.localhost"
    userinfo = mocker.patch(
        "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo"
    )
    userinfo.return_value = token_value

    mocker.patch(
        "camac.caluma.utils.jwt_decode", return_value={"azp": settings.KEYCLOAK_CLIENT}
    )

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token", X_CAMAC_GROUP=group.pk)

    caluma_user = CamacAuthenticatedGraphQLView().get_user(request)

    assert caluma_user.username == admin_user.username
    assert caluma_user.group == group.service_id
    assert request.camac_user == admin_user


@pytest.mark.parametrize(
    "has_token,enable_public_caluma,username",
    [(False, False, None), (False, True, None), (True, False, "nonexistent-username")],
)
def test_unauthorized_caluma(
    rf,
    mocker,
    settings,
    application_settings,
    has_token,
    enable_public_caluma,
    username,
):
    application_settings["ENABLE_PUBLIC_CALUMA"] = enable_public_caluma

    if has_token:
        headers = {"HTTP_AUTHORIZATION": "Bearer some_token"}
        userinfo = mocker.patch(
            "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo"
        )
        userinfo.return_value = {settings.OIDC_USERNAME_CLAIM: username}
        settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.localhost"
        mocker.patch("camac.caluma.utils.jwt_decode")
    else:
        headers = {}

    # A request without a token will result in an AnonymousUser in caluma
    request = rf.request(**headers)

    if has_token or not enable_public_caluma:
        with pytest.raises(HttpError) as e:
            CamacAuthenticatedGraphQLView().get_user(request)

        assert isinstance(e.value.response, HttpResponseUnauthorized)
    else:
        assert isinstance(
            CamacAuthenticatedGraphQLView().get_user(request), AnonymousUser
        )


@pytest.mark.parametrize("has_valid_token", [True, False])
def test_forbidden_caluma_captcha(
    rf,
    settings,
    application_settings,
    has_valid_token,
):
    application_settings["ENABLE_PUBLIC_CALUMA"] = True
    application_settings["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = True

    if has_valid_token:
        signer = Signer()
        expiry = make_aware(datetime.now() + timedelta(minutes=15)).timestamp()

        header_value = signer.sign_object({"key": "abcd", "expiry": expiry})
    else:
        header_value = None

    request = rf.request(HTTP_X_CAMAC_PUBLIC_TOKEN=header_value)

    if not has_valid_token:
        with pytest.raises(HttpError) as e:
            CamacAuthenticatedGraphQLView().get_user(request)

        assert isinstance(e.value.response, HttpResponseForbidden)
    else:
        assert isinstance(
            CamacAuthenticatedGraphQLView().get_user(request), AnonymousUser
        )
