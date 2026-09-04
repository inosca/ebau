import logging

from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from camac.billing.kt_ag.models import (
    RapagOrderNumberSequence,
    RapagSalesOrder,
    RapagSalesOrderGetItem,
    RapagSalesOrderResponse,
    RapagStatus,
)

logger = logging.getLogger(__name__)


class RapagClient:
    """Client for the DIBA REST interface (RAPAG)."""

    def __init__(self):
        self.base_url = settings.BILLING.rapag.base_url
        self._session: OAuth2Session | None = None

    def _get_session(self) -> OAuth2Session:
        if self._session is None:
            client = BackendApplicationClient(
                client_id=settings.BILLING.rapag.client_id
            )
            self._session = OAuth2Session(client=client)
            self._session.fetch_token(
                token_url=settings.BILLING.rapag.token_url,
                client_id=settings.BILLING.rapag.client_id,
                client_secret=settings.BILLING.rapag.client_secret,
            )
        return self._session

    def get_sales_orders(
        self,
        ktag_auftr_key: str | None = None,
        ktag_status: RapagStatus | str | None = None,
        ktag_eing_datum: str | None = None,
    ) -> list[RapagSalesOrderGetItem]:
        """Retrieve status information for DIBA requests."""
        url = f"{self.base_url}/http/rest/salesorder"
        headers = {"Accept": "application/json"}

        params = {}
        params["ktagBusCase"] = "DIBA"
        if ktag_auftr_key:
            params["ktagAuftrKey"] = ktag_auftr_key
        if ktag_status:  # pragma: no cover
            params["ktagStatus"] = (
                ktag_status.value
                if isinstance(ktag_status, RapagStatus)
                else ktag_status
            )
        if ktag_eing_datum:  # pragma: no cover
            params["ktagEingDatum"] = ktag_eing_datum

        session = self._get_session()
        response = session.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except Exception as e:  # pragma: no cover
            logger.error(f"Error {response.status_code} calling {url}: {response.text}")
            raise e

        return [RapagSalesOrderGetItem.from_dict(item) for item in response.json()]

    def create_sales_order(self, order: RapagSalesOrder) -> RapagSalesOrderResponse:
        """Transmit sales order data to the backend."""
        url = f"{self.base_url}/http/rest/salesorder"

        json_data = order.to_dict()

        json_data["auftrKey"] = f"DIBA{RapagOrderNumberSequence.get_next()}"

        # Enrich with constant values
        constants = {
            "busCase": "DIBA",
            "bukrs": "6003",
            "vtweg": "6C",
            "spart": "10",
            "vkbur": "6C01",
            "auart": "ZTA0",
        }
        json_data |= constants

        session = self._get_session()
        response = session.post(url, json=json_data)
        try:
            response.raise_for_status()
        except Exception as e:  # pragma: no cover
            logger.error(f"Error {response.status_code} calling {url}: {response.text}")
            raise e
        return RapagSalesOrderResponse.from_dict(response.json())
