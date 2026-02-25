import logging
import os
import time
from enum import StrEnum
from typing import Dict, List, Optional

import httpx
from django.conf import settings
from dotenv import load_dotenv

log = logging.getLogger(__name__)


class ReplicationStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"
    EXCEPTION = "exception"


def raise_for_status_and_log(response: httpx.Response):  # pragma: no cover
    if response.is_error:
        request = response.request
        log.warning(
            f"Request Details:\n"
            f"URL: {request.url}\n"
            f"Method: {request.method}\n"
            f"Headers: {request.headers}\n"
            f"Body: {request.content.decode('utf-8', 'ignore')}"
        )

        log.warning(
            f"Response Details:\n"
            f"Status Code: {response.status_code}\n"
            f"Headers: {response.headers}\n"
            f"Body: {response.text}"
        )
        response.raise_for_status()


class EbauDocumentClient:  # pragma: no cover
    def __new__(cls, base_url, *args, **kwargs):
        if cls.is_service_available(base_url):
            return super().__new__(cls)
        else:
            log.warning(
                f"EBAU document REST endpoint "
                f"{base_url} "
                f"is not available, using local mock implementation."
            )
            from camac.dossier_import.config.kt_ag_sap_migration.documents.dev_ebau_document_client import (
                DevEbauDocumentClient,
            )

            return DevEbauDocumentClient()

    @staticmethod
    def is_service_available(base_url):
        try:
            response = httpx.head(base_url + "openapi.json", timeout=5, verify=False)
            # allow any code - not allowed methods, authorization required, ...
            return response.status_code >= 200
        except Exception:
            return False

    def __init__(self, base_url, username, password):
        base_url = base_url.rstrip("/")
        username = username
        password = password
        auth = (username, password) if username and password else None
        timeout_values = httpx.Timeout(
            connect=60.0,
            read=60.0,
            write=60.0,
            pool=60.0,
        )

        self._client = httpx.Client(
            base_url=base_url, auth=auth, verify=False, timeout=timeout_values
        )

    def initialize_infrastructure(self, clear_db: bool = False):
        """
        Perform infrastructure setup checks and create missing infrastructure.

        :return: Response data from the API as a dictionary.
        """
        response = self._client.post(
            "/infrastructure/initialize", params={"appdb": clear_db}
        )

        self._handle_response_exceptions(response, "Initialization failed")
        log.info("initialize_infrastructure complete.")

    def replicate_data(
        self,
        purge: Optional[bool] = False,
        commune_id: Optional[List[int]] = None,
        request_id: Optional[List[str]] = None,
        status_commune: Optional[List[dict]] = None,
        status_canton: Optional[List[dict]] = None,
        submission_date_from: Optional[str] = None,
        submission_date_to: Optional[str] = None,
    ) -> str:
        """
        Replicate ERP/DVS documents based on the provided filters.

        :param purge: Whether to purge existing documents before copying.
        :param commune_id: List of commune IDs to filter.
        :param request_id: List of request identifiers to filter.
        :param status_commune: List of status options for communes.
        :param status_canton: List of status options for cantons.
        :param submission_date_from: Start date for submission filtering (format: YYYY-MM-DD).
        :param submission_date_to: End date for submission filtering (format: YYYY-MM-DD).

        :return: The replication ID string from the API response.
        """
        params = {
            "purge": purge,
            "communeId": commune_id or [],
            "status_commune": status_commune or [],
            "status_canton": status_canton or [],
            "submissionDateFrom": submission_date_from,
            "submissionDateTo": submission_date_to,
        }

        # Clean up None values
        params = {k: v for k, v in params.items() if v}

        body = {"requestId": request_id or []}

        response = self._client.post("/data/erp/replicate", params=params, json=body)

        self._handle_response_exceptions(response, "Replication failed")
        replication_id = response.json().get("replication_id")
        log.info(f"Replication startet with replication_id: {replication_id}")
        return replication_id

    def is_any_replication_running(self) -> bool:
        """Check if there are any replications in status "running".

        :return: True if there is a running replication.
        """

        result = self._fetch_replication_status()
        if not result:
            return False

        for r in result:
            status = r.get("status")
            if status == ReplicationStatus.RUNNING:
                log.info("There is a running replication.")
                return True

        log.info("There is no running replication.")
        return False

    def get_replication_status(
        self, replication_id: str
    ) -> Optional[ReplicationStatus]:
        """Check the status of a specific ERP/DVS replication.

        :param replication_id: The unique replication ID to check the status for.
        :return: the ReplicationStatus
        """
        result = self._find_replication_status(replication_id)

        status = result.get("status")

        log.info(f"Replication status is {status} for replication_id: {replication_id}")
        return ReplicationStatus(status) if status else None

    def _find_replication_status(self, replication_id: str):
        result_list = self._fetch_replication_status(replication_id)

        status = next((r for r in result_list if r.get("id") == replication_id), None)

        if status:
            return status

        log.warning(
            f"Replication not directly found for replication_id: {replication_id}. Trying to find it in all results ..."
        )
        result_list = self._fetch_replication_status()
        status = next((r for r in result_list if r.get("id") == replication_id), None)
        if status:
            return status

        raise ValueError(f"Replication not found for replication_id: {replication_id}")

    def _fetch_replication_status(
        self, replication_id: Optional[str] = None
    ) -> List[Dict]:
        params = {"replication_id": replication_id} if replication_id else None
        response = self._client.get(
            url="/data/erp/checkReplication",
            params=params,
        )
        raise_for_status_and_log(response)
        result = response.json()
        log.info(
            f"Status request for replication id: '{replication_id}' returned: '{result}'"
        )
        return result

    def download_replication_csv_log(self, replication_id: str) -> str:
        """Download the ERP/DVS replication CSV file transfer log using replication ID."""
        response = self._client.get(
            url="/data/erp/downloadReplicationCsv",
            params={"id": replication_id},
        )
        raise_for_status_and_log(response)
        log.info(
            f"Download of replication CSV log successful for replication_id: {replication_id}"
        )
        return response.text

    def _handle_response_exceptions(self, response: httpx.Response, error_prefix: str):
        """
        Handle common response validation and generate consistent exceptions.

        :param response: The HTTP response object to validate.
        :param error_prefix: The error message prefix for exceptions.
        :raises Exception: If the response status or content indicates an error.
        """
        raise_for_status_and_log(response)

        result = response.json()
        if result.get("status") and result.get("status") != "success":
            message = result.get("message", "An error occurred.")
            details = result.get("details", "No details available.")
            raise Exception(f"{error_prefix}: {message} - {details}")


def create_ebau_document_client() -> EbauDocumentClient:  # pragma: no cover
    return EbauDocumentClient(
        **settings.DOSSIER_IMPORT["EBAU_DOCUMENT_CLIENT"]["connection"]
    )


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    load_dotenv(".env.test_from_stage_ebau_offen")

    client = EbauDocumentClient(
        os.getenv("EBAU_DOCUMENT_CLIENT_BASE_URL", "unknown"),
        os.getenv("EBAU_DOCUMENT_CLIENT_USERNAME", "unknown"),
        os.getenv("EBAU_DOCUMENT_CLIENT_PASSWORD", "unknown"),
    )
    client.initialize_infrastructure()
    # replication_id = client.replicate_data(commune_id=[4221])  # Abtwil
    replication_id = client.replicate_data(commune_id=[4271])  # Aarburg
    # replication_id = "ba6cabaf-0d2b-41af-b332-dbaef684e33d"
    print(replication_id)
    while client.get_replication_status(replication_id) == ReplicationStatus.RUNNING:
        print("Waiting for replication to complete...")
        time.sleep(10)
    print("Replication completed.")
    csv_content = client.download_replication_csv_log(replication_id)
    with open(f"{replication_id}.csv", "w", encoding="utf-8", newline="") as f:
        f.write(csv_content)
