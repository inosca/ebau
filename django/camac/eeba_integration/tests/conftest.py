import pytest

from camac.eeba_integration.client import EebaClient, EebaHandler


@pytest.fixture(autouse=True)
def patch_get_authorization_header(mocker):
    mocker.patch(
        "camac.eeba_integration.client.get_authorization_header",
        return_value="dummy_auth_token",
    )


@pytest.fixture
def client():
    auth_token = "test_auth_token"
    shared_secret = "test_shared_secret"
    base_url = "http://example.com"
    return EebaClient(auth_token, shared_secret, base_url)


@pytest.fixture
def mock_session(mocker):
    return mocker.MagicMock()


@pytest.fixture
def make_mock_response(mocker):
    def _make_response(json_data, status=200, error_side_effect=None, headers=None):
        response = mocker.MagicMock()
        response.json.return_value = json_data
        response.status_code = status
        response.headers = headers if headers else {}
        if error_side_effect:
            response.raise_for_status.side_effect = error_side_effect
        else:
            response.raise_for_status.return_value = None
        return response

    return _make_response


class DummyRequest:
    def __init__(self, data=None, headers=None):
        self.data = data or {}
        self.headers = headers or {}


@pytest.fixture
def dummy_request():
    return DummyRequest(data={}, headers={"Accept-Language": "de"})


@pytest.fixture
def eeba_handler_instance(dummy_request, client):
    handler = EebaHandler(dummy_request)
    handler.eeba_client = client
    return handler


@pytest.fixture
def dummy_get_response_data():
    return {
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
