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
    handle_eeba_client_exceptions,
)
from camac.eeba_integration.state_manager import EebaIntegrationState

logger = logging.getLogger(__name__)


class EebaClient:
    def __init__(
        self,
        auth_header,
        shared_secret=settings.EEBA_INTEGRATION.get("EEBA_SHARED_SECRET"),
        base_url=settings.EEBA_INTEGRATION.get("EEBA_BASE_URL"),
    ):
        self.base_url = base_url
        self.session = requests.Session()

        # Extract token
        _, raw_token = auth_header.split()

        # Exchange it once for our scoped token
        exchanged = utils.exchange_token(self.session, raw_token)

        # Use the exchanged token for eEBA calls
        self.default_headers = {
            "Authorization": f"Bearer {exchanged}",
            # "X-EBAU-EEBA-SECRET": shared_secret, # commented out for now
            "Content-Type": "application/json",
        }

        self.endpoints = {
            "create_resource": {"method": "POST", "path": "/integrations/"},
            "update_resource": {"method": "PATCH", "path": "/integrations/{uuid}"},
            "get_resource": {"method": "GET", "path": "/integrations/{uuid}"},
            "rerun": {"method": "POST", "path": "/integrations/{uuid}/rerun"},
            "retry": {"method": "POST", "path": "/integrations/{uuid}/retry"},
        }

    @handle_eeba_client_exceptions
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
    def __init__(self, request, instance):
        self.request = request
        self.instance = instance
        self.auth_header = get_authorization_header(request)
        self.state_manager = EebaIntegrationState(instance.case.document)
        self.eeba_client = EebaClient(self.auth_header)

    def create_eeba_integration(self, timeout):
        data = {
            "timeout": timeout,
            "relation": {
                "type": ".eBau",
                "eBauId": self.instance.pk,
            },
        }

        create_response = self.eeba_client.make_request(
            action="create_resource",
            data=data,
        )
        integration_id = utils.extract_integration_id(create_response)
        if not integration_id:
            logger.error(
                "No integration_id found in create_resource response body or headers"
            )
            raise EebaHandlerServerException(
                _("Failed to create resource: No integration_id returned.")
            )

        self.state_manager.set_integration_id(integration_id)
        return integration_id

    #  Helper methods for check_eeba_needed

    def _handle_missing_integration(self, timeout):
        """
        Create a new integration, set state as 'requested', and poll for updated data.

        Return updated answer values.
        """
        integration_id = self.create_eeba_integration(timeout)
        self.state_manager.set_state("requested")
        try:
            return self.get_eeba_needed(integration_id, timeout)
        except (
            EebaHandlerBadRequestException,
            EebaHandlerServerException,
            TimeoutError,
        ):
            return self._process_failed_response(action="retry")

    def _handle_existing_integration(self, integration_id, timeout):
        """
        Based on the current state, trigger a 'rerun' or 'retry', then poll for updates.

        Return updated state, required, and web_url answer values.
        """
        current_state_value = self.state_manager.get_state()

        action = "rerun" if current_state_value in ("completed", "rerun") else "retry"

        try:
            self.eeba_client.make_request(
                action,
                uuid=integration_id,
            )
            return self.get_eeba_needed(integration_id, timeout)

        except (
            EebaHandlerBadRequestException,
            EebaHandlerServerException,
            TimeoutError,
        ):
            return self._process_failed_response(action="retry")

    def check_eeba_needed(
        self, timeout=settings.EEBA_INTEGRATION.get("EEBA_TIMEOUT_SECONDS")
    ) -> dict:
        """
        Check and handle the state of the eEBA integration.

        Return a dictionary with the latest integration_id, state, required, and web_url values.
        """
        integration_id = self.state_manager.get_integration_id()

        if not integration_id:
            state_value, required, web_url = self._handle_missing_integration(timeout)
        else:
            state_value, required, web_url = self._handle_existing_integration(
                integration_id, timeout
            )

        return {
            "integration_id": self.state_manager.get_integration_id(),
            "state": state_value,
            "required": required,
            "web_url": web_url,
        }

    # Helper methods for get_eeba_needed

    def _process_completed_response(self, response_data):
        """
        Update answers when the response status is 'completed'.

        Return the updated state, required, and web_url answer values.
        """
        self.state_manager.set_state("completed")

        eeba_required = response_data.get("relation", {}).get(
            "declarationOfWasteDisposalRequired"
        )

        required_value = (
            "eeba-required-ja"
            if eeba_required is True
            else ("eeba-required-nein" if eeba_required is False else None)
        )
        self.state_manager.set_required(required_value)

        eeba_web_url = response_data.get("relation", {}).get("webUrl")
        self.state_manager.set_web_url(eeba_web_url)

        return (
            self.state_manager.get_state(),
            self.state_manager.get_required(),
            self.state_manager.get_web_url(),
        )

    def _process_failed_response(self, action="rerun"):
        """
        Update the state when the response status is not 'completed' or request resulted in error.

        Action defaults to rerun but can also take the value retry.
        Assume that the required and web_url values are unreliable.
        """
        self.state_manager.set_state(action)
        self.state_manager.set_required(None)
        # Should we keep the web_url link even if status is not determined?
        self.state_manager.set_web_url(None)

        return (
            self.state_manager.get_state(),
            self.state_manager.get_required(),
            self.state_manager.get_web_url(),
        )

    @handle_eeba_client_exceptions
    def get_eeba_needed(self, integration_id, timeout):
        """
        Poll the 'get_resource' endpoint until a terminal state is reached, update answers.

        Update answers and return the corresponding answer values.
        Return a tuple (state_answer, required_answer, web_url_answer)
        """
        language = self.request.headers.get("Accept-Language", "de")
        extra_headers = {
            "Accept-Language": language,
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
            return self._process_completed_response(response_data)
        else:
            logger.error("Error hint for integration %s: %s", integration_id, hint)
            return self._process_failed_response(action="rerun")

    def patch_eeba_integration(self, new_instance_id):
        """
        Reassign instance_id to an existing integration.

        Retrieve the current integration ID from the document's hidden answers.
        Raise EebaHandlerBadRequestException if the integration ID is not found.
        """
        timeout = settings.EEBA_INTEGRATION.get("EEBA_TIMEOUT_SECONDS")

        integration_id = self.state_manager.get_integration_id()
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

        response = self.eeba_client.make_request(
            action="update_resource",
            data=data,
            uuid=integration_id,
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
