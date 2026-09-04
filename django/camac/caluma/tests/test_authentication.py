from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
import pytest
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_user.views import HttpResponseUnauthorized
from django.core.signing import Signer
from django.utils.timezone import make_aware
from graphene_django.views import HttpError

from camac.caluma.views import CamacAuthenticatedGraphQLView, HttpResponseForbidden
from camac.user.models import User


def build_bearer_token() -> str:
    return jwt.encode({}, "secret", algorithm="HS256")


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

    request = rf.request(
        HTTP_AUTHORIZATION=f"Bearer {build_bearer_token()}", X_CAMAC_GROUP=group.pk
    )

    caluma_user = CamacAuthenticatedGraphQLView().get_user(request)

    assert caluma_user.username == admin_user.username
    assert caluma_user.group == group.service_id
    assert request.camac_user == admin_user


@pytest.mark.django_db
def test_authenticate_caluma_creates_missing_user(rf, settings, mocker):
    """A user that only exists in keycloak must be created on the graphql path.

    The CAMAC user is created lazily on the first request. As only the DRF
    authentication backend used to do that, a new user whose graphql request
    arrived before their first REST request was rejected with a 401.
    """
    claims = {
        settings.OIDC_USERNAME_CLAIM: "egov:1234",
        "email": "jane.doe@example.com",
        "given_name": "jane",
        "family_name": "doe",
    }
    settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.localhost"
    mocker.patch(
        "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo",
        return_value=claims,
    )
    mocker.patch(
        "camac.caluma.utils.jwt_decode", return_value={"azp": settings.KEYCLOAK_CLIENT}
    )

    assert not User.objects.filter(username="egov:1234").exists()

    request = rf.request(HTTP_AUTHORIZATION=f"Bearer {build_bearer_token()}")
    caluma_user = CamacAuthenticatedGraphQLView().get_user(request)

    assert caluma_user.username == "egov:1234"

    user = User.objects.get(username="egov:1234")
    assert user.email == "jane.doe@example.com"
    assert user.name == "jane"
    assert user.surname == "doe"
    assert request.camac_user == user


@pytest.mark.django_db
def test_authenticate_caluma_deactivated_user(rf, settings, user_factory, mocker):
    """A deactivated user must get a 401 instead of a server error.

    `build_user` raises an `AuthenticationFailed` which the graphql view has to
    translate, as it is not a DRF view.
    """
    settings.OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK = True
    user_factory(
        username="some-other-username", email="disabled@example.com", disabled=1
    )

    claims = {
        settings.OIDC_USERNAME_CLAIM: "egov:5678",
        "email": "disabled@example.com",
        "given_name": "dis",
        "family_name": "abled",
    }
    settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.localhost"
    mocker.patch(
        "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo",
        return_value=claims,
    )
    mocker.patch(
        "camac.caluma.utils.jwt_decode", return_value={"azp": settings.KEYCLOAK_CLIENT}
    )

    request = rf.request(HTTP_AUTHORIZATION=f"Bearer {build_bearer_token()}")

    with pytest.raises(HttpError) as e:
        CamacAuthenticatedGraphQLView().get_user(request)

    assert e.value.response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize("enable_public_caluma", [False, True])
def test_unauthorized_caluma(rf, application_settings, enable_public_caluma):
    application_settings["ENABLE_PUBLIC_CALUMA"] = enable_public_caluma

    # A request without a token will result in an AnonymousUser in caluma
    request = rf.request()

    if not enable_public_caluma:
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
