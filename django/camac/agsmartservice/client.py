import logging

import requests
from django.conf import settings

from camac.settings.utils import is_module_enabled
from camac.utils import build_url

logger = logging.getLogger(__name__)


class AGSmartServiceClient:
    @staticmethod
    def _raise_for_status_and_log(response):
        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.exception(
                "AG SmartService request failed with status code %s and response body: %s",
                response.status_code,
                response.text,
            )
            raise

    @staticmethod
    def get_token():
        config = settings.AGSMARTSERVICE
        response = requests.post(
            config.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": config.client_id,
                "client_secret": config.client_secret,
                "scope": settings.KEYCLOAK_SCOPES,
            },
            timeout=config.timeout_seconds,
        )
        AGSmartServiceClient._raise_for_status_and_log(response)
        return response.json()["access_token"]

    @staticmethod
    def _headers():
        return {
            "Authorization": f"Bearer {AGSmartServiceClient.get_token()}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _procedure_url(instance_id):
        config = settings.AGSMARTSERVICE
        return build_url(
            config.base_url,
            "api/v1/services",
            config.service_id,
            "procedures",
            instance_id,
        )

    @staticmethod
    def put_procedure(instance_id, payload):
        if not is_module_enabled("AGSMARTSERVICE"):
            return None

        response = requests.put(
            AGSmartServiceClient._procedure_url(instance_id),
            json=payload,
            headers=AGSmartServiceClient._headers(),
            timeout=settings.AGSMARTSERVICE.timeout_seconds,
        )
        AGSmartServiceClient._raise_for_status_and_log(response)
        return response

    @staticmethod
    def delete_procedure(instance_id):
        if not is_module_enabled("AGSMARTSERVICE"):
            return None

        response = requests.delete(
            AGSmartServiceClient._procedure_url(instance_id),
            headers=AGSmartServiceClient._headers(),
            timeout=settings.AGSMARTSERVICE.timeout_seconds,
        )
        AGSmartServiceClient._raise_for_status_and_log(response)
        return response
