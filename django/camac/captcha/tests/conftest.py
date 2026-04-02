import sys
from importlib import reload

import pytest
from django.urls import clear_url_caches


@pytest.fixture(autouse=True)
def captcha_urls(application_settings):
    """Ensure captcha URLs are registered for captcha tests.

    The captcha URL conf is evaluated once at import time based on
    ENABLE_PUBLIC_CALUMA_CAPTCHA. We need to reload it after enabling the
    setting so that reverse('captcha-generate') works regardless of test order.
    """
    application_settings["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = True

    clear_url_caches()
    for urlconf in ["camac.captcha.urls", "camac.urls"]:
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])

    yield

    # Restore URLs to the state without captcha after the test
    application_settings["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = False
    clear_url_caches()
    for urlconf in ["camac.captcha.urls", "camac.urls"]:
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
