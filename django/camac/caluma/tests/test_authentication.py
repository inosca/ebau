import pytest

from ..views import CamacAuthenticatedGraphQLView


@pytest.mark.parametrize(
    "request_headers", [{"HTTP_AUTHORIZATION": "Bearer some_token"}, {}]
)
def test_authenticate_caluma(rf, settings, admin_user, mocker, request_headers):
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

    request = rf.request(**request_headers)

    caluma_user = CamacAuthenticatedGraphQLView().get_user(request)

    if request_headers:
        assert admin_user.username == caluma_user.username
        assert admin_user == request.camac_user
    else:
        assert str(caluma_user) == "AnonymousUser"
        assert request.camac_user is None
