import json
import logging
import time

import requests
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.authentication import get_authorization_header

from camac.eeba_integration import utils
from camac.eeba_integration.exceptions import (
    EebaHandlerBadRequestException,
    EebaHandlerServerException,
    handle_exceptions,
)

logger = logging.getLogger(__name__)


class EebaClient:
    def __init__(
        self,
        auth_token,
        shared_secret=settings.EEBA_SHARED_SECRET,
        base_url=settings.EEBA_BASE_URL,
    ):
        self.base_url = base_url
        self.session = requests.Session()
        self.default_headers = {
            "X-EBAU-EEBA-SECRET": shared_secret,
            "Authorization": auth_token,
            "Content-Type": "application/json",
        }
        self.endpoints = {
            "create_resource": {"method": "POST", "path": "/integrations/"},
            "update_resource": {"method": "PATCH", "path": "/integrations/{uuid}"},
            "get_resource": {"method": "GET", "path": "/integrations/{uuid}"},
            "rerun": {"method": "POST", "path": "/integrations/{uuid}/rerun"},
            "retry": {"method": "POST", "path": "/integrations/{uuid}/retry"},
        }

    @handle_exceptions
    def make_request(self, action, data=None, uuid=None, extra_headers=None):
        if action not in self.endpoints:
            raise ValueError(_("Unknown action: %s") % action)

        endpoint = self.endpoints[action]
        method = endpoint["method"]
        path = endpoint["path"]

        if "{uuid}" in path:
            if uuid:
                path = path.replace("{uuid}", str(uuid))
            else:
                raise ValueError(_("UUID is required for action: %s") % action)

        url = self.base_url + path

        logger.info("EebaClient endpoint info: %s: %s", method, url)

        headers = self.default_headers.copy()
        if extra_headers:
            extra_headers = extra_headers.copy()
            # TODO: Cleanup
            if test_authorization := extra_headers.pop("Test-Authorization", None):
                headers["Authorization"] = test_authorization  # pragma: no cover
            headers.update(extra_headers)

        method_handlers = {
            "GET": lambda: self.session.get(url, headers=headers),
            "POST": lambda: self.session.post(
                url, headers=headers, data=json.dumps(data)
            ),
            "PATCH": lambda: self.session.patch(
                url, headers=headers, data=json.dumps(data)
            ),
        }

        try:
            response = method_handlers[method]()
        except KeyError:
            raise ValueError(_("Unsupported HTTP method: %s") % method)

        response.raise_for_status()
        return response


class EebaHandler:
    def __init__(self, request):
        self.request = request
        self.auth_token = get_authorization_header(request)
        self.eeba_client = EebaClient(self.auth_token)

    def create_eeba_integration(self, instance, timeout):
        data = {
            "timeout": timeout,
            "relation": {
                "type": ".eBau",
                "eBauId": instance.pk,
            },
        }
        create_response = self.eeba_client.make_request(
            action="create_resource",
            data=data,
            extra_headers={
                "Test-Authorization": self.request.headers.get("Test-Authorization")
            },
        )
        integration_id = utils.extract_integration_id(create_response)
        if not integration_id:
            logger.error(
                "No integration_id found in create_resource response body or headers"
            )
            raise EebaHandlerServerException(
                _("Failed to create resource: No integration_id returned.")
            )
        # Save the integration answer here?
        # utils.save_hidden_answer(instance.case.document, "eeba-integration-id", integration_id)
        return integration_id

    #  Helper methods for check_eeba_needed

    def _handle_missing_integration(self, instance, document, timeout):
        """
        Create a new integration, mark state as 'requested', and poll for updated data.

        Return updated answer objects.
        """
        integration_id = self.create_eeba_integration(instance, timeout)
        integration_answer = utils.save_hidden_answer(
            document, "eeba-integration-id", integration_id
        )
        state_answer = utils.save_hidden_answer(document, "eeba-state", "requested")
        try:
            state_answer, required_answer, web_url_answer = self.get_eeba_needed(
                document, integration_id, timeout
            )

        except (
            EebaHandlerBadRequestException,
            EebaHandlerServerException,
            TimeoutError,
        ):
            state_answer, required_answer, web_url_answer = (
                self._process_failed_response(document, action="retry")
            )

        return integration_answer, state_answer, required_answer, web_url_answer

    def _handle_existing_integration(self, document, integration_answer, timeout):
        """
        Based on the current state, trigger a 'rerun' or 'retry', then poll for updates.

        Return updated state, required, and web_url answers.
        """
        # TODO: Cleanup
        extra_headers = {
            "Test-Authorization": self.request.headers.get("Test-Authorization")
        }
        current_state = utils.get_answer_object("eeba-state", document)
        current_state_value = utils.get_answer_value(current_state)

        if current_state_value in ("completed", "rerun"):
            action = "rerun"
        else:
            action = "retry"

        try:
            self.eeba_client.make_request(
                action, uuid=integration_answer.value, extra_headers=extra_headers
            )
            return self.get_eeba_needed(document, integration_answer.value, timeout)
        except (
            EebaHandlerBadRequestException,
            EebaHandlerServerException,
            TimeoutError,
        ):
            return self._process_failed_response(document, action="retry")

    def check_eeba_needed(
        self, instance, timeout=settings.EEBA_TIMEOUT_SECONDS
    ) -> dict:
        """
        Check and handle the state of the eEBA integration.

        Return a dictionary with the latest integration_id, state, required, and web_url values.
        """
        document = instance.case.document

        integration_answer = utils.get_answer_object("eeba-integration-id", document)

        if not integration_answer or not integration_answer.value:
            integration_answer, state_answer, required_answer, web_url_answer = (
                self._handle_missing_integration(instance, document, timeout)
            )
        else:
            state_answer, required_answer, web_url_answer = (
                self._handle_existing_integration(document, integration_answer, timeout)
            )

        return {
            "integration_id": utils.get_answer_value(integration_answer),
            "state": utils.get_answer_value(state_answer),
            "required": utils.get_answer_value(required_answer),
            "web_url": utils.get_answer_value(web_url_answer),
        }

    # Helper methods for get_eeba_needed

    def _process_completed_response(self, document, response_data):
        """
        Update answers when the response status is 'completed'.

        Return the updated state, required, and web_url answer objects.
        """
        state_answer = utils.save_hidden_answer(document, "eeba-state", "completed")
        eeba_required = response_data.get("relation", {}).get(
            "declarationOfWasteDisposalRequired"
        )
        required_value = (
            "eeba-required-ja"
            if eeba_required is True
            else ("eeba-required-nein" if eeba_required is False else None)
        )
        required_answer = utils.save_hidden_answer(
            document, "eeba-required", required_value
        )
        eeba_web_url = response_data.get("relation", {}).get("webUrl")
        web_url_answer = utils.save_hidden_answer(
            document, "eeba-web-url", eeba_web_url
        )
        return state_answer, required_answer, web_url_answer

    def _process_failed_response(self, document, action="rerun"):
        """
        Update the state when the response status is not 'completed' or request resulted in error.

        Action defaults to rerun but can also take the value retry.
        Assume that the required and web_url values are unreliable.
        """
        state_answer = utils.save_hidden_answer(document, "eeba-state", action)
        required_answer = utils.save_hidden_answer(document, "eeba-required", None)
        # Should we keep the web_url link even if status is not determined?
        web_url_answer = utils.save_hidden_answer(document, "eeba-web-url", None)
        return state_answer, required_answer, web_url_answer

    @handle_exceptions
    def get_eeba_needed(self, document, integration_id, timeout):
        """
        Poll the 'get_resource' endpoint until a terminal state is reached, update answers.

        Update and return the corresponding answer objects.
        Return a tuple (state_answer, required_answer, web_url_answer)
        """
        language = self.request.headers.get("Accept-Language", "de")
        # TODO: Cleanup
        extra_headers = {
            "Accept-Language": language,
            "Test-Authorization": self.request.headers.get("Test-Authorization"),
        }

        response_data = self.poll_action(
            action="get_resource",
            uuid=integration_id,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        status = response_data.get("status")
        hint = response_data.get("hint")

        if status == "completed":
            return self._process_completed_response(document, response_data)
        else:
            logger.error("Error hint for integration %s: %s", integration_id, hint)
            return self._process_failed_response(document, action="rerun")

    def patch_eeba_integration(self, instance, new_instance_id):
        """
        Reassign instance_id to an existing integration.

        Retrieve the current integration ID from the document's hidden answers.
        Raise EebaHandlerBadRequestException if the integration ID is not found.
        """
        timeout = settings.EEBA_TIMEOUT_SECONDS
        document = instance.case.document
        integration_answer = utils.get_answer_object("eeba-integration-id", document)
        integration_id = utils.get_answer_value(integration_answer)

        if not integration_id:
            raise EebaHandlerBadRequestException(
                "Integration ID not found for patching."
            )

        data = {
            "timeout": timeout,
            "relation": {
                "type": ".eBau",
                "eBauId": new_instance_id,
            },
        }
        # TODO: Cleanup
        extra_headers = {
            "Test-Authorization": self.request.headers.get("Test-Authorization")
        }
        response = self.eeba_client.make_request(
            action="update_resource",
            data=data,
            uuid=integration_id,
            extra_headers=extra_headers,
        )

        logger.info(
            "Successfully patched integration %s with new instance ID %s",
            integration_id,
            new_instance_id,
        )
        return response

    @staticmethod
    def process_response_data(response_data):
        """
        Process the client's response to determine whether polling should continue.

        Return a tuple (continue_polling, result) where
        continue_polling is a boolean indicating if polling should continue,
        and result is the data to return if polling stops.
        """
        if not response_data:
            logger.error(_("Empty response received from client."))
            raise EebaHandlerServerException(_("Empty response received from client."))

        status = response_data.get("status")
        if status is None:
            logger.error("Response missing 'status' field: %s", response_data)
            raise EebaHandlerServerException(_("Response missing 'status' field."))

        if status == "completed":
            logger.info("Polling successful: Task completed.")
            return False, response_data
        elif status in ("failed", "unprocessable"):
            logger.error("Polling stopped: Task failed with status '%s'.", status)
            return False, response_data
        elif status in ("init", "inProgress"):
            logger.info("Polling: Task is still processing...")
            return True, None
        else:  # pragma: no cover
            logger.warning("Unexpected status received: %s", status)
            return True, None

    def poll_action(
        self, action, uuid=None, extra_headers=None, timeout=60, interval=5
    ):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = self.eeba_client.make_request(
                action=action, extra_headers=extra_headers, uuid=uuid
            )
            continue_polling, result = EebaHandler.process_response_data(
                response.json()
            )
            if not continue_polling:
                return result
            time.sleep(interval)
        logger.error("Polling timed out after %s seconds.", timeout)
        raise TimeoutError(_("Polling timed out."))
