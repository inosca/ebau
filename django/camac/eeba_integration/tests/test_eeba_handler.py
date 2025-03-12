import pytest
import requests

from camac.eeba_integration.client import EebaHandler
from camac.eeba_integration.exceptions import (
    EebaHandlerBadRequestException,
    EebaHandlerServerException,
)


def test_extract_integration_id_valid(make_mock_response):
    headers = {"Location": "http://example.com/api/integrations/123"}
    dummy_response = make_mock_response({}, headers=headers)
    integration_id = EebaHandler.extract_integration_id(dummy_response)
    assert integration_id == "123"


def test_extract_integration_id_empty(make_mock_response):
    headers = {"Location": ""}
    dummy_response = make_mock_response({}, headers=headers)
    integration_id = EebaHandler.extract_integration_id(dummy_response)
    assert integration_id is None


def test_create_eeba_integration_success(
    eeba_handler_instance, mocker, make_mock_response
):
    headers = {"Location": "http://example.com/api/integrations/456"}
    dummy_response = make_mock_response({}, headers=headers)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    result = eeba_handler_instance.create_eeba_integration(123, 30)
    assert result == {"integration_id": "456"}
    eeba_handler_instance.eeba_client.make_request.assert_called_once_with(
        action="create_resource",
        data={
            "timeout": 30,
            "relation": {"type": ".eBau", "eBauId": 123},
        },
    )


def test_create_eeba_integration_failure(
    eeba_handler_instance, mocker, make_mock_response
):
    headers = {"Location": ""}
    dummy_response = make_mock_response({}, headers=headers)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    with pytest.raises(EebaHandlerServerException) as excinfo:
        eeba_handler_instance.create_eeba_integration(123, 30)
    assert "Failed to create resource" in str(excinfo.value)
    eeba_handler_instance.eeba_client.make_request.assert_called_once()


def test_create_eeba_integration_value_error(eeba_handler_instance, mocker):
    # patch the eeba_client.make_request to raise a ValueError immediately.
    mocker.patch.object(
        eeba_handler_instance.eeba_client,
        "make_request",
        side_effect=ValueError("dummy value error"),
    )

    with pytest.raises(EebaHandlerBadRequestException) as excinfo:
        eeba_handler_instance.create_eeba_integration(
            instance_id="test-instance", timeout=10
        )
    assert "Bad request in create_eeba_integration:" in str(excinfo.value)
    assert "dummy value error" in str(excinfo.value)


def test_check_eeba_needed_success(
    eeba_handler_instance,
    dummy_request,
    mocker,
    make_mock_response,
    dummy_get_response_data,
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    dummy_request.headers["Accept-Language"] = "en"

    dummy_response = make_mock_response(dummy_get_response_data)
    eeba_handler_instance.poll_action = mocker.MagicMock(return_value=dummy_response)

    result = eeba_handler_instance.check_eeba_needed(
        dummy_request, integration_id, timeout=30
    )

    assert result == dummy_get_response_data
    eeba_handler_instance.poll_action.assert_called_once_with(
        action="get_resource",
        uuid="35374476-0694-42ed-84d4-8da544d0a60e",
        extra_headers={"Accept-Language": "en"},
        timeout=30,
    )


def test_check_eeba_needed_request_exception(eeba_handler_instance, mocker):
    eeba_handler_instance.request.headers = {"Accept-Language": "en"}
    # patch the eeba_client.make_request (called inside poll_action) to raise a RequestException.
    mocker.patch.object(
        eeba_handler_instance.eeba_client,
        "make_request",
        side_effect=requests.exceptions.RequestException("dummy request error"),
    )

    with pytest.raises(EebaHandlerServerException) as excinfo:
        eeba_handler_instance.check_eeba_needed(
            eeba_handler_instance.request, integration_id="test-uuid", timeout=10
        )
    assert "Server error in check_eeba_needed:" in str(excinfo.value)
    assert "dummy request error" in str(excinfo.value)


def test_patch_eeba_integration_success(
    eeba_handler_instance, dummy_request, make_mock_response, mocker
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    dummy_response = make_mock_response({})
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    result = eeba_handler_instance.patch_eeba_integration(
        dummy_request, integration_id, new_instance_id="567", timeout=30
    )
    assert result == {}
    eeba_handler_instance.eeba_client.make_request.assert_called_once_with(
        action="update_resource",
        data={
            "timeout": 30,
            "relation": {"type": ".eBau", "eBauId": "567"},
        },
        uuid="35374476-0694-42ed-84d4-8da544d0a60e",
    )


def test_retry_eeba_check_success(
    eeba_handler_instance,
    dummy_get_response_data,
    dummy_request,
    make_mock_response,
    mocker,
):
    integration_id = "35374476-0694-42ed-84d4-8da544d0a60e"
    dummy_request.headers["Accept-Language"] = "en"

    dummy_response = make_mock_response(dummy_get_response_data)
    eeba_handler_instance.poll_action = mocker.MagicMock(return_value=dummy_response)

    dummy_retry_response = make_mock_response({})
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_retry_response
    )

    result = eeba_handler_instance.retry_eeba_check(
        dummy_request, integration_id, "retry", timeout=30
    )

    assert result == dummy_get_response_data
    eeba_handler_instance.eeba_client.make_request.assert_called_with(
        action="retry", uuid="35374476-0694-42ed-84d4-8da544d0a60e"
    )
    eeba_handler_instance.poll_action.assert_called_with(
        action="get_resource",
        uuid="35374476-0694-42ed-84d4-8da544d0a60e",
        extra_headers={"Accept-Language": "en"},
        timeout=30,
    )


def test_process_response_completed():
    response = {"status": "completed", "data": "foo"}
    continue_polling, result = EebaHandler.process_response(response)
    assert continue_polling is False
    assert result == response


def test_process_response_failed():
    response = {"status": "failed", "data": "bar"}
    continue_polling, result = EebaHandler.process_response(response)
    assert continue_polling is False
    assert result == response


def test_process_response_in_progress():
    response = {"status": "inProgress"}
    continue_polling, result = EebaHandler.process_response(response)
    assert continue_polling is True
    assert result is None


def test_process_response_empty():
    with pytest.raises(EebaHandlerServerException):
        EebaHandler.process_response(None)


def test_process_response_missing_status():
    with pytest.raises(EebaHandlerServerException):
        EebaHandler.process_response({"data": "something"})


def test_poll_action_success(eeba_handler_instance, mocker, make_mock_response):
    # patch time.sleep to avoid real delays.
    mocker.patch("time.sleep", return_value=None)
    # simulate eeba_client.make_request returning a "completed" response on first call.
    response_dict = {"status": "completed", "result": "done"}
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=response_dict
    )

    result = eeba_handler_instance.poll_action(
        action="get_resource", uuid="111", timeout=5, interval=0.1
    )
    assert result == response_dict
    eeba_handler_instance.eeba_client.make_request.assert_called()


def test_poll_action_timeout(eeba_handler_instance, mocker, make_mock_response):
    # simulate eeba_client.make_request always returning an inProgress status.
    response_dict = {"status": "inProgress"}
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=response_dict
    )

    with pytest.raises(TimeoutError):
        eeba_handler_instance.poll_action(
            action="get_resource", uuid="222", timeout=0.5, interval=0.1
        )


def test_poll_action_request_exception(eeba_handler_instance, mocker):
    # patch time.sleep to avoid real delays.
    mocker.patch("time.sleep", return_value=None)
    # configure make_request to raise a RequestException
    exception = requests.exceptions.RequestException("Test Request Exception")
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        side_effect=exception
    )

    with pytest.raises(requests.exceptions.RequestException) as excinfo:
        eeba_handler_instance.poll_action(
            action="get_resource", uuid="test-uuid", timeout=1, interval=0.1
        )
    assert "Test Request Exception" in str(excinfo.value)
