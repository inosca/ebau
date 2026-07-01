import logging

import pytest
import requests

from camac.agsmartservice.client import AGSmartServiceClient


def _response(mocker, json_data=None, error=None, text="", status_code=200):
    response = mocker.MagicMock()
    response.json.return_value = json_data or {}
    response.raise_for_status.side_effect = error
    response.text = text
    response.status_code = status_code
    return response


def test_get_token(mocker, settings, ag_agsmartservice_settings):
    settings.KEYCLOAK_SCOPES = "openid"
    ag_agsmartservice_settings.client_id = "client-id"
    ag_agsmartservice_settings.client_secret = "client-secret"
    post = mocker.patch(
        "camac.agsmartservice.client.requests.post",
        return_value=_response(mocker, {"access_token": "access-token"}),
    )

    assert AGSmartServiceClient.get_token() == "access-token"
    post.assert_called_once_with(
        "https://my.example.url/api/v1/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "client-id",
            "client_secret": "client-secret",
            "scope": "openid",
        },
        timeout=30,
    )


def test_put_procedure(mocker, ag_agsmartservice_settings):
    mocker.patch.object(AGSmartServiceClient, "get_token", return_value="access-token")
    put_response = _response(mocker)
    put = mocker.patch(
        "camac.agsmartservice.client.requests.put", return_value=put_response
    )
    payload = {"title": "Test"}

    response = AGSmartServiceClient.put_procedure("INSTANCEID", payload)

    assert response == put_response
    put.assert_called_once_with(
        "https://my.example.url/meine-vorgaenge-service/api/v1/services/ABCD001337/procedures/INSTANCEID",
        json=payload,
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    put_response.raise_for_status.assert_called_once_with()


def test_delete_procedure(mocker, ag_agsmartservice_settings):
    mocker.patch.object(AGSmartServiceClient, "get_token", return_value="access-token")
    delete_response = _response(mocker)
    delete = mocker.patch(
        "camac.agsmartservice.client.requests.delete", return_value=delete_response
    )

    response = AGSmartServiceClient.delete_procedure("INSTANCEID")

    assert response == delete_response
    delete.assert_called_once_with(
        "https://my.example.url/meine-vorgaenge-service/api/v1/services/ABCD001337/procedures/INSTANCEID",
        headers={
            "Authorization": "Bearer access-token",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    delete_response.raise_for_status.assert_called_once_with()


def test_http_error_is_raised_and_response_body_is_logged(
    mocker, caplog, ag_agsmartservice_settings
):
    mocker.patch.object(AGSmartServiceClient, "get_token", return_value="access-token")
    mocker.patch(
        "camac.agsmartservice.client.requests.put",
        return_value=_response(
            mocker,
            error=requests.HTTPError("HTTP 400"),
            text='{"message": "Invalid procedure"}',
            status_code=400,
        ),
    )

    with caplog.at_level(logging.ERROR), pytest.raises(requests.HTTPError):
        AGSmartServiceClient.put_procedure("INSTANCEID", {})

    assert "status code 400" in caplog.text
    assert '{"message": "Invalid procedure"}' in caplog.text


@pytest.mark.parametrize("method", ["put", "delete"])
def test_disabled_module_does_not_send_request(
    method, mocker, disable_agsmartservice_settings
):
    request = mocker.patch(f"camac.agsmartservice.client.requests.{method}")

    if method == "put":
        assert AGSmartServiceClient.put_procedure("INSTANCEID", {}) is None
    else:
        assert AGSmartServiceClient.delete_procedure("INSTANCEID") is None

    request.assert_not_called()
