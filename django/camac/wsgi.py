"""
WSGI config for project_app2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from django.conf import settings
from django.core.wsgi import get_wsgi_application

from camac.wsgi_common import get_dav_application, setup_environment

setup_environment()

if settings.MANABI_ENABLE:
    wsgi_django = get_wsgi_application()
    wsgi_dav = get_dav_application()

    def dispatch(environ, start_response):
        """Routes requests between Django and DAV services."""
        path = environ.get("PATH_INFO", "/")
        dav_prefix = "/dav"

        if path.startswith(dav_prefix):
            environ = environ.copy()
            environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + dav_prefix
            return wsgi_dav(environ, start_response)
        return wsgi_django(environ, start_response)

    application = dispatch
else:
    application = get_wsgi_application()
