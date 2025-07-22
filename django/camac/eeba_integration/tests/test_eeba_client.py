import json

import pytest
import requests

from camac.eeba_integration import exceptions


def test_unknown_action(eeba_client):
    with pytest.raises(
        exceptions.EebaHandlerBadRequestException, match="Unknown action"
    ):
        eeba_client.make_request("invalid_action")


def test_missing_uuid(eeba_client):
    with pytest.raises(
        exceptions.EebaHandlerBadRequestException, match="UUID is required"
    ):
        eeba_client.make_request("get_resource")


def test_get_request(eeba_client, mock_eeba_session, make_eeba_mock_response):
    expected_url = (
        "http://example.com/integrations/35374476-0694-42ed-84d4-8da544d0a60e"
    )
    expected_headers = eeba_client.default_headers.copy()
    custom_response_headers = {"Content-Type": "application/json"}
    dummy_get_response_data = {
        "id": "35374476-0694-42ed-84d4-8da544d0a60e",
        "relationId": "18424aaa-074a-4fc4-ad5b-806b8f8e71fa",
        "creationDate": "2024-01-01T12:00:00+02:00",
        "status": "completed",
        "hint": "Integration completed!",
        "timeout": 60,
        "relation": {
            "type": ".eBau",
            "operationalResponse": "partiallyTransient",
            "eEbaId": "GR-EBA-ABCDEF",
            "eBauId": 345,
            "creationDate": "2024-01-01T12:00:00+02:00",
            "modificationDate": "2024-01-03T12:00:00+02:00",
            "declarationOfWasteDisposalRequired": True,
            "recordOfWasteDisposalRequired": True,
            "status": "inProgress",
            "statusText": "",
            "anuReviewRequired": False,
            "webUrl": "https://eba.gr.ch/web/form/GR-EBA-ABCDEF",
        },
    }
    mock_resp = make_eeba_mock_response(
        dummy_get_response_data, headers=custom_response_headers, status=201
    )
    mock_eeba_session.get.return_value = mock_resp
    eeba_client.session = mock_eeba_session

    response = eeba_client.make_request(
        "get_resource", uuid="35374476-0694-42ed-84d4-8da544d0a60e"
    )
    assert response.json() == dummy_get_response_data
    mock_eeba_session.get.assert_called_once_with(
        expected_url, headers=expected_headers
    )
    assert response.headers.get("Content-Type") == "application/json"


def test_post_request(eeba_client, mock_eeba_session, make_eeba_mock_response):
    test_data = {
        "timeout": 60,
        "relation": {"type": ".eBau", "eBauId": 123},
    }
    expected_url = "http://example.com/integrations/"
    expected_headers = eeba_client.default_headers.copy()
    location_header = (
        "http://eba-example.com/integrations/35374476-0694-42ed-84d4-8da544d0a60e"
    )

    mock_resp = make_eeba_mock_response(
        {}, headers={"Location": location_header}, status=200
    )
    mock_eeba_session.post.return_value = mock_resp
    eeba_client.session = mock_eeba_session
    response = eeba_client.make_request("create_resource", data=test_data)
    assert response.json() == {}
    mock_eeba_session.post.assert_called_once_with(
        expected_url, headers=expected_headers, data=json.dumps(test_data)
    )

    assert response.headers.get("Location") == location_header


def test_patch_request(eeba_client, mock_eeba_session, make_eeba_mock_response):
    test_data = {
        "timeout": 60,
        "id": "35374476-0694-42ed-84d4-8da544d0a60e",
        "relation": {"type": ".eBau", "eBauId": 456},
    }
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    expected_url = f"http://example.com/integrations/{uuid_value}"
    expected_headers = eeba_client.default_headers.copy()

    mock_resp = make_eeba_mock_response({}, status=200)
    mock_eeba_session.patch.return_value = mock_resp
    eeba_client.session = mock_eeba_session

    response = eeba_client.make_request(
        "update_resource", uuid=uuid_value, data=test_data
    )
    assert response.json() == {}
    mock_eeba_session.patch.assert_called_once_with(
        expected_url, headers=expected_headers, data=json.dumps(test_data)
    )


def test_extra_headers(eeba_client, mock_eeba_session, make_eeba_mock_response):
    extra_headers = {"Custom": "Header"}
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    expected_url = f"http://example.com/integrations/{uuid_value}/retry"
    combined_headers = eeba_client.default_headers.copy()
    combined_headers.update(extra_headers)

    mock_resp = make_eeba_mock_response({}, status=200)
    mock_eeba_session.post.return_value = mock_resp
    eeba_client.session = mock_eeba_session

    response = eeba_client.make_request(
        "retry", uuid=uuid_value, extra_headers=extra_headers
    )
    assert response.json() == {}
    assert response.status_code == 200
    mock_eeba_session.post.assert_called_once_with(
        expected_url, headers=combined_headers, data=json.dumps(None)
    )


def test_http_error(eeba_client, mock_eeba_session, make_eeba_mock_response):
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    mock_response_data = {
        "errors": [{"field": "action", "errorCode": "", "message": "Failed."}],
        "empty": False,
        "rejectCount": 1,
    }
    mock_resp = make_eeba_mock_response(
        mock_response_data, status=400, error_side_effect=requests.HTTPError("HTTP 400")
    )
    mock_eeba_session.get.return_value = mock_resp
    eeba_client.session = mock_eeba_session

    with pytest.raises(exceptions.EebaHandlerServerException):
        eeba_client.make_request("get_resource", uuid=uuid_value)


def test_unsupported_http_method(eeba_client):
    eeba_client.endpoints["invalid_method"] = {"method": "PUT", "path": "/invalid/path"}
    with pytest.raises(
        exceptions.EebaHandlerBadRequestException, match="Unsupported HTTP method"
    ):
        eeba_client.make_request("invalid_method")
