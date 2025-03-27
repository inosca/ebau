"""
WSGI config for camac-ng WebDAV container.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from camac.wsgi_common import get_dav_application, setup_environment

setup_environment()
wsgi_dav = get_dav_application()


def application(environ, start_response):
    """Handle DAV requests."""
    dav_prefix = "/dav"
    environ = environ.copy()
    environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + dav_prefix
    return wsgi_dav(environ, start_response)
