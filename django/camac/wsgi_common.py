"""
Common WSGI config module. Extend from this module.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import locale
import os

import django
from django.conf import settings


def setup_environment():
    """Execute setup for WSGI applications."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")
    django.setup(set_prefix=False)
    locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")


def get_dav_application():
    """Return the appropriate DAV WSGI application."""
    backend = settings.APPLICATION.get("DOCUMENT_BACKEND")
    if backend == "alexandria":
        from alexandria.dav import get_dav
    else:
        from camac.dav import get_dav
    return get_dav()
