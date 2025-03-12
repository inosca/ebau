import logging
import time
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.authentication import get_authorization_header

from camac.eeba_integration.exceptions import (
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
        }
        self.endpoints = {
            "create_resource": {"method": "POST", "path": "/integrations/eBau/"},
            "update_resource": {"method": "PATCH", "path": "/integrations/eBau/{uuid}"},
            "get_resource": {"method": "GET", "path": "/integrations/eBau/{uuid}"},
            "rerun": {"method": "POST", "path": "/integrations/eBau/{uuid}/rerun"},
            "retry": {"method": "POST", "path": "/integrations/eBau/{uuid}/retry"},
        }

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

        headers = self.default_headers.copy()
        if extra_headers:
            headers.update(extra_headers)

        if method == "GET":
            response = self.session.get(url, headers=headers)
        elif method == "POST":
            response = self.session.post(url, headers=headers, data=data)
        elif method == "PATCH":
            response = self.session.patch(url, headers=headers, data=data)
        else:
            raise ValueError(_("Unsupported HTTP method: %s") % method)

        response.raise_for_status()
        return response


class EebaHandler:
    def __init__(self, request):
        self.request = request
        self.auth_token = get_authorization_header(request)
        self.eeba_client = EebaClient(self.auth_token)

    @staticmethod
    def extract_integration_id(response):
        location_url = response.headers.get("Location", "").strip()
        if not location_url:
            return None

        parsed_path = urlparse(location_url).path.rstrip("/")
        path_segments = [segment for segment in parsed_path.split("/") if segment]
        return path_segments[-1] if path_segments else None

    @handle_exceptions
    def create_eeba_integration(self, instance_id, timeout):
        data = {
            "timeout": timeout,
            "relation": {
                "type": ".eBau",
                "eBauId": instance_id,
            },
        }
        create_response = self.eeba_client.make_request(
            action="create_resource",
            data=data,
        )
        integration_id = self.extract_integration_id(create_response)
        if not integration_id:
            logger.error(
                _("No integration_id found in create_resource response headers")
            )
            raise EebaHandlerServerException(
                _("Failed to create resource: No integration_id returned.")
            )
        return {"integration_id": integration_id}

    @handle_exceptions
    def check_eeba_needed(self, request, integration_id, timeout):
        """Poll get integration until status is completed, unprocessable or failed."""
        language = self.request.headers.get("Accept-Language", "de")
        extra_headers = {"Accept-Language": language}
        response = self.poll_action(
            action="get_resource",
            uuid=integration_id,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return response.json()

    @handle_exceptions
    def retry_eeba_check(self, request, integration_id, retry_action, timeout):
        """Retry processing of the integration and polls get integration."""
        self.eeba_client.make_request(action=retry_action, uuid=integration_id)
        language = self.request.headers.get("Accept-Language", "de")
        extra_headers = {"Accept-Language": language}
        response = self.poll_action(
            action="get_resource",
            uuid=integration_id,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return response.json()

    @handle_exceptions
    def patch_eeba_integration(self, request, integration_id, new_instance_id, timeout):
        """Reassign instance_id to existing integration."""
        data = {
            "timeout": timeout,
            "relation": {
                "type": ".eBau",
                "eBauId": new_instance_id,
            },
        }
        response = self.eeba_client.make_request(
            action="update_resource", data=data, uuid=integration_id
        )
        return response.json()

    @staticmethod
    def process_response(response):
        """
        Process the client's response to determine whether polling should continue.

        return tuple (continue_polling, result) where continue_polling is a boolean
                   indicating whether to continue polling, and result is the response to return
                   if polling should stop.
        """
        if not response:
            logger.error(_("Empty response received from client."))
            raise EebaHandlerServerException(_("Empty response received from client."))

        status = response.get("status")
        if status is None:
            logger.error(_("Response missing 'status' field: %s"), response)
            raise EebaHandlerServerException(_("Response missing 'status' field."))

        if status == "completed":
            logger.info(_("Polling successful: Task completed."))
            return False, response
        elif status in ("failed", "unprocessable"):
            logger.error(_("Polling stopped: Task failed with status '%s'."), status)
            return False, response
        elif status in ("init", "inProgress"):
            logger.info(_("Polling: Task is still processing..."))
            return True, None
        else:  # pragma: no cover
            logger.warning(_("Unexpected status received: %s"), status)
            return True, None

    def poll_action(
        self, action, uuid=None, extra_headers=None, timeout=60, interval=5
    ):
        """
        Poll the given action until it reaches a terminal state or the timeout is exceeded.

        raise:
            TimeoutError: If the polling exceeds the specified timeout.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = self.eeba_client.make_request(
                    action=action, extra_headers=extra_headers, uuid=uuid
                )
                continue_polling, result = EebaHandler.process_response(response)
                if not continue_polling:
                    return result
            except requests.exceptions.RequestException as e:
                logger.error(_("Request error encountered during polling: %s"), e)
                raise
            except Exception as e:  # pragma: no cover
                logger.exception(
                    _("An unexpected error occurred during polling: %s"), e
                )
                raise

            time.sleep(interval)
            continue

        logger.error(_("Polling timed out after %s seconds."), timeout)
        raise TimeoutError(_("Polling timed out."))
