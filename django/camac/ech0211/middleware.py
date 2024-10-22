from functools import lru_cache
from logging import getLogger

import requests
from django.conf import settings
from django.core.exceptions import PermissionDenied
from ipware import get_client_ip
from urllib3.util import Retry

log = getLogger(__name__)


class GeofenceMiddleware:
    """Middleware for IP Geofencing, only allowed regions can make requests."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        geofence_settings = settings.ECH0211.get("GEOFENCE", {})
        if not geofence_settings.get("ENABLE"):
            response = self.get_response(request)
            return response

        client_ip, is_routable = get_client_ip(request)

        if client_ip is None:
            raise PermissionDenied("Unable to get the client's IP address")

        # The client's IP address is publicly routable on the Internet
        if is_routable:
            try:
                country = self.get_ip_region(client_ip)
            except requests.exceptions.RequestException as e:
                log.warning(e)
                response = self.get_response(request)
                return response

            if country not in geofence_settings["REGIONS"]:
                raise PermissionDenied(
                    f"Outside of allowed region, client's IP address: {client_ip}"
                )

        response = self.get_response(request)
        return response

    @staticmethod
    @lru_cache
    def get_ip_region(ip):
        """
        Get the client's geolocation based on the IP address with an external API.

        Used API: https://www.geoplugin.com/
        Rate limited to 120 requests per minute
        """
        with requests.Session() as session:
            session.mount(
                "http://",
                requests.adapters.HTTPAdapter(
                    max_retries=Retry(total=3, backoff_factor=0.1)
                ),
            )
            geo_info_response = session.get(f"http://www.geoplugin.net/json.gp?ip={ip}")
        geo_info_response.raise_for_status()
        geo_info = geo_info_response.json()
        return geo_info["geoplugin_countryCode"]
