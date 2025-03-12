import pytest
import requests


def test_unknown_action(client):
    with pytest.raises(ValueError, match="Unknown action"):
        client.make_request("invalid_action")


def test_missing_uuid(client):
    with pytest.raises(ValueError, match="UUID is required"):
        client.make_request("get_resource")


def test_get_request(client, mock_session, make_mock_response, dummy_get_response_data):
    expected_url = "http://example.com/integrations/eBau/345"
    expected_headers = client.default_headers.copy()
    custom_response_headers = {"Content-Type": "application/json"}
    mock_resp = make_mock_response(
        dummy_get_response_data, headers=custom_response_headers, status=201
    )
    mock_session.get.return_value = mock_resp
    client.session = mock_session

    response = client.make_request("get_resource", uuid="345")
    assert response.json() == dummy_get_response_data
    mock_session.get.assert_called_once_with(expected_url, headers=expected_headers)
    assert response.headers.get("Content-Type") == "application/json"


def test_post_request(client, mock_session, make_mock_response):
    test_data = {
        "timeout": 60,  #
        "relation": {"type": ".eBau", "eBauId": 123},
    }
    expected_url = "http://example.com/integrations/eBau/"
    expected_headers = client.default_headers.copy()
    location_header = (
        "http://eba-example.com/integrations/35374476-0694-42ed-84d4-8da544d0a60e"
    )

    mock_resp = make_mock_response(
        {}, headers={"Location": location_header}, status=200
    )
    mock_session.post.return_value = mock_resp
    client.session = mock_session
    response = client.make_request("create_resource", data=test_data)
    assert response.json() == {}
    mock_session.post.assert_called_once_with(
        expected_url, headers=expected_headers, data=test_data
    )

    assert response.headers.get("Location") == location_header


def test_patch_request(client, mock_session, make_mock_response):
    test_data = {
        "timeout": 60,
        "id": "35374476-0694-42ed-84d4-8da544d0a60e",
        "relation": {"type": ".eBau", "eBauId": 456},
    }
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    expected_url = f"http://example.com/integrations/eBau/{uuid_value}"
    expected_headers = client.default_headers.copy()

    mock_resp = make_mock_response({}, status=200)
    mock_session.patch.return_value = mock_resp
    client.session = mock_session

    response = client.make_request("update_resource", uuid=uuid_value, data=test_data)
    assert response.json() == {}
    mock_session.patch.assert_called_once_with(
        expected_url, headers=expected_headers, data=test_data
    )


def test_extra_headers(client, mock_session, make_mock_response):
    extra_headers = {"Custom": "Header"}
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    expected_url = f"http://example.com/integrations/eBau/{uuid_value}/retry"
    combined_headers = client.default_headers.copy()
    combined_headers.update(extra_headers)

    mock_resp = make_mock_response({}, status=200)
    mock_session.post.return_value = mock_resp
    client.session = mock_session

    response = client.make_request(
        "retry", uuid=uuid_value, extra_headers=extra_headers
    )
    assert response.json() == {}
    assert response.status_code == 200
    mock_session.post.assert_called_once_with(
        expected_url, headers=combined_headers, data=None
    )


def test_http_error(client, mock_session, make_mock_response):
    uuid_value = "35374476-0694-42ed-84d4-8da544d0a60e"
    mock_response_data = {
        "errors": [{"field": "action", "errorCode": "", "message": "Failed."}],
        "empty": False,
        "rejectCount": 1,
    }
    mock_resp = make_mock_response(
        mock_response_data, status=400, error_side_effect=requests.HTTPError("HTTP 400")
    )
    mock_session.get.return_value = mock_resp
    client.session = mock_session

    with pytest.raises(requests.HTTPError):
        client.make_request("get_resource", uuid=uuid_value)


def test_unsupported_http_method(client):
    client.endpoints["invalid_method"] = {"method": "PUT", "path": "/invalid/path"}
    with pytest.raises(ValueError, match="Unsupported HTTP method"):
        client.make_request("invalid_method")
