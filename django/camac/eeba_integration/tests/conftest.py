import pytest
from caluma.caluma_form.models import Answer

from camac.eeba_integration.client import EebaClient, EebaHandler


@pytest.fixture(autouse=True)
def override_eeba_base_url(settings):
    settings.EEBA_BASE_URL = "https://example.com"


@pytest.fixture(autouse=True)
def patch_get_authorization_header(mocker):
    mocker.patch(
        "camac.eeba_integration.client.get_authorization_header",
        return_value="dummy_auth_token",
    )


@pytest.fixture(autouse=True)
def patch_has_camac_edit_permissions(mocker):
    mocker.patch(
        "camac.eeba_integration.views.CustomPermission.has_camac_edit_permission",
        return_value=True,
    )


@pytest.fixture
def clean_eeba_answers(gr_instance):
    """
    Ensure that no Answer objects for specific questions exist before a test runs.

    Also clean up after the test.
    """
    document = gr_instance.case.document
    slugs = ["eeba-integration-id", "eeba-state", "eeba-required", "eeba-web-url"]
    # Clear answers  before the test
    Answer.objects.filter(document=document, question__slug__in=slugs).delete()
    yield
    # Clear answers after the test
    Answer.objects.filter(document=document, question__slug__in=slugs).delete()


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
        self.caluma_info = None


@pytest.fixture
def dummy_request():
    return DummyRequest(data={}, headers={"Accept-Language": "de"})


@pytest.fixture
def eeba_handler_instance(db, dummy_request, gr_instance, client):
    handler = EebaHandler(dummy_request, gr_instance)
    handler.eeba_client = client
    return handler
