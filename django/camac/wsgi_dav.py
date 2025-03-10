"""
WSGI config for camac-ng WebDAV container.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import locale
import os

import django
from django.conf import settings

locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")

django.setup(set_prefix=False)

backend = settings.APPLICATION["DOCUMENT_BACKEND"]
if backend == "alexandria":
    from alexandria.dav import get_dav
else:
    from camac.dav import get_dav

wsgi_dav = get_dav()


def application(environ, start_response):
    dav_prefix = "/dav"
    environ = environ.copy()
    environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + dav_prefix
    return wsgi_dav(environ, start_response)
