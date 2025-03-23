import pytest
import requests
from caluma.caluma_form.models import Answer
from django.conf import settings

from camac.eeba_integration import utils
from camac.eeba_integration.client import EebaHandler
from camac.eeba_integration.exceptions import (
    EebaHandlerBadRequestException,
    EebaHandlerServerException,
)

# Tests for create_eeba_integration


def test_create_eeba_integration_success(
    db, eeba_handler_instance, gr_instance, make_mock_response, mocker
):
    headers = {"Location": "http://example.com/api/integrations/456"}
    dummy_response = make_mock_response({}, headers=headers)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    integration_id = eeba_handler_instance.create_eeba_integration(gr_instance, 30)
    assert integration_id == "456"
    eeba_handler_instance.eeba_client.make_request.assert_called_once_with(
        action="create_resource",
        data={
            "timeout": 30,
            "relation": {"type": ".eBau", "eBauId": gr_instance.pk},
        },
        # TODO: Cleanup
        extra_headers={"Test-Authorization": None},
    )


def test_create_eeba_integration_failure(
    db, eeba_handler_instance, gr_instance, make_mock_response, mocker
):
    headers = {"Location": ""}
    dummy_response = make_mock_response({}, headers=headers)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    with pytest.raises(EebaHandlerServerException) as excinfo:
        eeba_handler_instance.create_eeba_integration(gr_instance, 30)
    assert "Failed to create resource" in str(excinfo.value)


def test_create_eeba_integration_value_error(
    db, eeba_handler_instance, gr_instance, mocker
):
    mocker.patch.object(
        eeba_handler_instance.eeba_client,
        "make_request",
        side_effect=EebaHandlerServerException("dummy server error"),
    )
    with pytest.raises(EebaHandlerServerException) as excinfo:
        eeba_handler_instance.create_eeba_integration(gr_instance, 10)
    assert "dummy server error" in str(excinfo.value)


# Tests for _handle_missing_integration


def test_handle_missing_integration_success(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document

    integration_id = "int-123"
    mocker.patch.object(
        eeba_handler_instance, "create_eeba_integration", return_value=integration_id
    )

    completed_response = {
        "status": "completed",
        "relation": {
            "declarationOfWasteDisposalRequired": True,
            "webUrl": "http://completed.example.com",
        },
        "hint": "",
    }
    mocker.patch.object(
        eeba_handler_instance, "poll_action", return_value=completed_response
    )

    result = eeba_handler_instance._handle_missing_integration(
        gr_instance, document, 30
    )
    integration_answer, state_answer, required_answer, web_url_answer = result

    assert integration_answer.value == integration_id
    assert state_answer.value == "completed"
    assert required_answer.value == "eeba-required-ja"
    assert web_url_answer.value == "http://completed.example.com"

    integration_answer = Answer.objects.get(
        document=document, question__slug="eeba-integration-id"
    )
    assert integration_answer.value == integration_id


def test_handle_missing_integration_failed_response_timeout(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document

    integration_id = "int-123"
    mocker.patch.object(
        eeba_handler_instance, "create_eeba_integration", return_value=integration_id
    )

    mocker.patch.object(
        eeba_handler_instance,
        "get_eeba_needed",
        side_effect=TimeoutError("Test timeout"),
    )

    result = eeba_handler_instance._handle_missing_integration(
        gr_instance, document, 30
    )
    integration_answer, state_answer, required_answer, web_url_answer = result

    assert integration_answer.value == integration_id

    assert state_answer.value == "retry"
    assert required_answer.value is None
    assert web_url_answer.value is None


def test_handle_missing_integration_failed_response_server_exception(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document

    integration_id = "int-123"
    mocker.patch.object(
        eeba_handler_instance, "create_eeba_integration", return_value=integration_id
    )

    mocker.patch.object(
        eeba_handler_instance,
        "get_eeba_needed",
        side_effect=EebaHandlerServerException("Test server exception"),
    )

    result = eeba_handler_instance._handle_missing_integration(
        gr_instance, document, 30
    )
    integration_answer, state_answer, required_answer, web_url_answer = result

    assert integration_answer.value == integration_id

    assert state_answer.value == "retry"
    assert required_answer.value is None
    assert web_url_answer.value is None


# Tests for _handle_existing_integration


@pytest.mark.parametrize(
    "initial_state",
    [
        ("rerun"),
        ("retry"),
        ("completed"),
    ],
)
def test_handle_existing_integration_success(
    db,
    clean_eeba_answers,
    eeba_handler_instance,
    gr_instance,
    mocker,
    initial_state,
):
    document = gr_instance.case.document
    integration_value = "int-789"
    integration_answer = utils.save_hidden_answer(
        document, "eeba-integration-id", integration_value
    )
    utils.save_hidden_answer(document, "eeba-state", initial_state)

    def mock_get_eeba_needed(document, integration_id, timeout):
        state_ans = utils.save_hidden_answer(document, "eeba-state", "completed")
        required_ans = utils.save_hidden_answer(
            document, "eeba-required", "eeba-required-nein"
        )
        web_url_ans = utils.save_hidden_answer(
            document, "eeba-web-url", "http://updated.example.com"
        )
        return (state_ans, required_ans, web_url_ans)

    mocker.patch.object(
        eeba_handler_instance, "get_eeba_needed", side_effect=mock_get_eeba_needed
    )

    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock()

    result = eeba_handler_instance._handle_existing_integration(
        document, integration_answer, 30
    )
    state_answer, required_answer, web_url_answer = result
    assert state_answer.value == "completed"
    assert required_answer.value == "eeba-required-nein"
    assert web_url_answer.value == "http://updated.example.com"


def test_handle_existing_integration_failed_response(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document
    integration_value = "int-000"
    integration_answer = utils.save_hidden_answer(
        document, "eeba-integration-id", integration_value
    )
    utils.save_hidden_answer(document, "eeba-state", "completed")
    utils.save_hidden_answer(document, "eeba-required", "eeba-required-nein")
    utils.save_hidden_answer(document, "eeba-web-url", "http://completed.example.com")

    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        side_effect=TimeoutError("Test timeout")
    )

    def mock_process_failed_response(document, action):
        state_ans = utils.save_hidden_answer(document, "eeba-state", action)
        required_ans = utils.save_hidden_answer(document, "eeba-required", None)
        web_url_ans = utils.save_hidden_answer(document, "eeba-web-url", None)
        return (state_ans, required_ans, web_url_ans)

    mocker.patch.object(
        eeba_handler_instance,
        "_process_failed_response",
        side_effect=mock_process_failed_response,
    )

    result = eeba_handler_instance._handle_existing_integration(
        document, integration_answer, 30
    )
    state_answer, required_answer, web_url_answer = result

    assert state_answer.value == "retry"
    assert required_answer.value is None
    assert web_url_answer.value is None


# Tests for check_eeba_needed


def test_check_eeba_needed_missing_integration(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    integration_id = "int-missing"
    mocker.patch.object(
        eeba_handler_instance, "create_eeba_integration", return_value=integration_id
    )

    completed_response = {
        "status": "completed",
        "relation": {
            "declarationOfWasteDisposalRequired": True,
            "webUrl": "http://missing.example.com",
        },
        "hint": "",
    }
    mocker.patch.object(
        eeba_handler_instance, "poll_action", return_value=completed_response
    )

    result = eeba_handler_instance.check_eeba_needed(gr_instance, 30)
    assert result["integration_id"] == integration_id
    assert result["state"] == "completed"
    assert result["required"] == "eeba-required-ja"
    assert result["web_url"] == "http://missing.example.com"


def test_check_eeba_needed_existing_integration(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document
    integration_value = "int-existing"
    utils.save_hidden_answer(document, "eeba-integration-id", integration_value)

    def mock_handle_existing(doc, integration_ans, timeout):
        state_ans = utils.save_hidden_answer(document, "eeba-state", "completed")
        required_ans = utils.save_hidden_answer(
            document, "eeba-required", "eeba-required-nein"
        )
        web_url_ans = utils.save_hidden_answer(
            document, "eeba-web-url", "http://existing.example.com"
        )
        return (state_ans, required_ans, web_url_ans)

    mocker.patch.object(
        eeba_handler_instance,
        "_handle_existing_integration",
        side_effect=mock_handle_existing,
    )

    result = eeba_handler_instance.check_eeba_needed(gr_instance, 30)
    assert result["integration_id"] == integration_value
    assert result["state"] == "completed"
    assert result["required"] == "eeba-required-nein"
    assert result["web_url"] == "http://existing.example.com"


# Tests for get_eeba_needed


def test_get_eeba_needed_completed(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document
    integration_id = "int-101"
    completed_response = {
        "status": "completed",
        "relation": {
            "declarationOfWasteDisposalRequired": True,
            "webUrl": "http://completed.com",
        },
        "hint": "",
    }
    mocker.patch.object(
        eeba_handler_instance, "poll_action", return_value=completed_response
    )

    result = eeba_handler_instance.get_eeba_needed(document, integration_id, 30)
    state_answer, required_answer, web_url_answer = result
    assert state_answer.value == "completed"
    assert required_answer.value == "eeba-required-ja"
    assert web_url_answer.value == "http://completed.com"


def test_get_eeba_needed_non_completed(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document
    integration_id = "int-202"
    inprogress_response = {"status": "failed", "hint": "failure"}
    mocker.patch.object(
        eeba_handler_instance, "poll_action", return_value=inprogress_response
    )

    def mock_process_failed(document, action):
        state_ans = utils.save_hidden_answer(document, "eeba-state", action)
        required_ans = utils.save_hidden_answer(document, "eeba-required", None)
        web_url_ans = utils.save_hidden_answer(document, "eeba-web-url", None)
        return (state_ans, required_ans, web_url_ans)

    mocker.patch.object(
        eeba_handler_instance,
        "_process_failed_response",
        side_effect=mock_process_failed,
    )

    result = eeba_handler_instance.get_eeba_needed(document, integration_id, 30)
    state_answer, required_answer, web_url_answer = result
    assert state_answer.value == "rerun"
    assert required_answer.value is None
    assert web_url_answer.value is None


# Tests for patch_eeba_integration


def test_patch_eeba_integration_success(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance, mocker
):
    document = gr_instance.case.document
    integration_value = "int-patch"
    utils.save_hidden_answer(document, "eeba-integration-id", integration_value)

    dummy_response = {}
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    result = eeba_handler_instance.patch_eeba_integration(
        gr_instance, new_instance_id="new-123"
    )
    assert result == dummy_response
    eeba_handler_instance.eeba_client.make_request.assert_called_once_with(
        action="update_resource",
        data={
            "timeout": settings.EEBA_TIMEOUT_SECONDS,
            "relation": {"type": ".eBau", "eBauId": "new-123"},
        },
        uuid=integration_value,
        # TODO: Cleanup
        extra_headers={"Test-Authorization": None},
    )


def test_patch_eeba_integration_failure(
    db, clean_eeba_answers, eeba_handler_instance, gr_instance
):
    with pytest.raises(EebaHandlerBadRequestException) as excinfo:
        eeba_handler_instance.patch_eeba_integration(
            gr_instance, new_instance_id="new-123"
        )
    assert "Integration ID not found for patching" in str(excinfo.value)


# Tests for process_response_data


def test_process_response_data_completed():
    response = {"status": "completed", "data": "foo"}
    continue_polling, result = EebaHandler.process_response_data(response)
    assert continue_polling is False
    assert result == response


def test_process_response_data_failed():
    response = {"status": "failed", "data": "bar"}
    continue_polling, result = EebaHandler.process_response_data(response)
    assert continue_polling is False
    assert result == response


def test_process_response_data_in_progress():
    response = {"status": "inProgress"}
    continue_polling, result = EebaHandler.process_response_data(response)
    assert continue_polling is True
    assert result is None


def test_process_response_data_status_unexpected():
    response = {"status": "something strange"}
    continue_polling, result = EebaHandler.process_response_data(response)
    assert continue_polling is True
    assert result is None


def test_process_response_data_empty():
    with pytest.raises(EebaHandlerServerException):
        EebaHandler.process_response_data(None)


def test_process_response_data_missing_status():
    with pytest.raises(EebaHandlerServerException):
        EebaHandler.process_response_data({"data": "something"})


# Tests for poll_action


def test_poll_action_success(eeba_handler_instance, mocker, make_mock_response):
    mocker.patch("time.sleep", return_value=None)
    response_dict = {"status": "completed", "result": "done"}
    dummy_response = make_mock_response(response_dict)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    result = eeba_handler_instance.poll_action(
        action="get_resource",
        uuid="111",
        extra_headers={"Accept-Language": "en"},
        timeout=0.5,
        interval=0.1,
    )
    assert result == response_dict
    eeba_handler_instance.eeba_client.make_request.assert_called()


def test_poll_action_timeout(eeba_handler_instance, mocker, make_mock_response):
    response_dict = {"status": "inProgress"}
    dummy_response = make_mock_response(response_dict)
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        return_value=dummy_response
    )

    with pytest.raises(TimeoutError) as excinfo:
        eeba_handler_instance.poll_action(
            action="get_resource",
            uuid="222",
            extra_headers={"Accept-Language": "en"},
            timeout=0.5,
            interval=0.1,
        )
    assert "Polling timed out" in str(excinfo.value)


def test_poll_action_request_exception(eeba_handler_instance, mocker):
    mocker.patch("time.sleep", return_value=None)
    exception = requests.exceptions.RequestException("Test Request Exception")
    eeba_handler_instance.eeba_client.make_request = mocker.MagicMock(
        side_effect=exception
    )

    with pytest.raises(requests.exceptions.RequestException) as excinfo:
        eeba_handler_instance.poll_action(
            action="get_resource",
            uuid="test-uuid",
            extra_headers={"Accept-Language": "en"},
            timeout=0.5,
            interval=0.1,
        )
    assert "Test Request Exception" in str(excinfo.value)
