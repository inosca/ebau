from functools import lru_cache
from logging import getLogger

import requests
from django.conf import settings
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from urllib3.util import Retry

log = getLogger(__name__)


class GeofenceMiddleware:
    """
    Middleware for IP Geofencing, only allowed regions can make requests.

    Can only be used through @decorator_from_middleware.
    """

    def __init__(self, view, *args, **kwargs):
        pass

    def process_view(self, view, view_func, view_args, view_kwargs):
        request = (
            view.request
        )  # first arg should be request not view, unsure why this happens
        geofence_settings = settings.ECH0211.get("GEOFENCE", {})
        if not geofence_settings.get("ENABLE"):
            return None

        client_ip, is_routable = get_client_ip(request)

        if client_ip is None:
            return HttpResponseForbidden("Unable to get the client's IP address")

        # The client's IP address is publicly routable on the Internet
        if is_routable:
            try:
                country = GeofenceMiddleware.get_ip_region(client_ip)
            except requests.exceptions.RequestException as e:
                log.warning(e)
                return None

            if country not in geofence_settings["REGIONS"]:
                return HttpResponseForbidden(
                    f"Outside of allowed region, client's IP address: {client_ip}"
                )

        return None

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
