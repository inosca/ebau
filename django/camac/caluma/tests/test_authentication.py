import pytest
from caluma.caluma_user.views import HttpResponseUnauthorized
from graphene_django.views import HttpError

from ..views import CamacAuthenticatedGraphQLView


def test_authenticate_caluma(rf, settings, admin_user, group, mocker):
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.name,
        "given_name": admin_user.surname,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }
    settings.OIDC_USERINFO_ENDPOINT = "http://fake-endpoint.local"
    userinfo = mocker.patch(
        "caluma.caluma_user.views.AuthenticationGraphQLView.get_userinfo"
    )
    userinfo.return_value = token_value

    mocker.patch("camac.caluma.api.jwt_decode")

    request = rf.request(HTTP_AUTHORIZATION="Bearer some_token", X_CAMAC_GROUP=group.pk)

    caluma_user = CamacAuthenticatedGraphQLView().get_user(request)

    assert caluma_user.username == admin_user.username
    assert caluma_user.group == group.service_id
    assert request.camac_user == admin_user


def test_unauthorized_caluma(rf):
    # A request without a token will result in an AnonymousUser in caluma
    request = rf.request()

    with pytest.raises(HttpError) as e:
        CamacAuthenticatedGraphQLView().get_user(request)

    assert isinstance(e.value.response, HttpResponseUnauthorized)
