import pytest

from camac.conftest import reload_urlconf


@pytest.fixture(autouse=True, scope="function")
def enable_public_caluma_with_captcha(application_settings):
    """Autouse fixture to set the required settings.

    This makes sure that public caluma with captcha is enabled and reloads the
    urlconfig in order to avoid issues caused by the if-clause in urls.py.

    Sadly, this needs the "function" scope as `application_settings` is also
    function scope and can't be used in "module" scoped fixtures.
    """

    application_settings["ENABLE_PUBLIC_CALUMA"] = True
    application_settings["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = True

    yield reload_urlconf("camac.captcha.urls")
