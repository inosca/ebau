"""
WSGI config for camac-ng WebDAV container.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from threading import Lock

from camac.wsgi_common import get_dav_application, setup_environment

setup_environment(is_dav=True)

wsgi_dav = None
wsgi_dav_lock = Lock()


def get_wsgi_dav():
    """Return the DAV application initialized in the current worker."""
    global wsgi_dav

    if wsgi_dav is None:
        with wsgi_dav_lock:
            if wsgi_dav is None:
                wsgi_dav = get_dav_application()
    return wsgi_dav


def application(environ, start_response):
    """Handle DAV requests."""
    dav_prefix = "/dav"
    environ = environ.copy()
    environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + dav_prefix
    return get_wsgi_dav()(environ, start_response)
