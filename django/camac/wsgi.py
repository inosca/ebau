"""
WSGI config for project_app2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")

if settings.MANABI_ENABLE:
    from .dav import get_dav

    wsgi_ɗav = get_dav()
    wsgi_django = get_wsgi_application()

    def dispatch(environ, start_response):
        path = environ["PATH_INFO"] or "/"
        dav_prefix = "/dav"
        if path.startswith(dav_prefix):
            environ = environ.copy()
            environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + dav_prefix
            environ["PATH_INFO"] = path[len(dav_prefix) :]
            return wsgi_ɗav(environ, start_response)
        else:
            return wsgi_django(environ, start_response)

    application = dispatch
else:

    application = get_wsgi_application()
