"""
Common WSGI config module. Extend from this module.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import locale
import os

import django
from django.conf import settings


def setup_environment(*, is_dav):
    """Execute setup for WSGI applications."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")
    django.setup(set_prefix=False)
    locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")

    if is_dav:
        # In WebDAV mode, we explicitly do not want to eager-load the URLconf,
        # as this gives a memory penalty if we're not actually using it:
        # Manabi has it's own URLs, and Django is only used at ORM level
        return
    if settings.EAGER_LOAD_URLCONF:
        # Load URLconf before gunicorn forks off, allowing to
        # share more memory between the workers.
        from django.urls import get_resolver

        _ = get_resolver().url_patterns


def get_dav_application():
    """Return the appropriate DAV WSGI application."""
    backend = settings.APPLICATION.get("DOCUMENT_BACKEND")
    if backend == "alexandria":
        from alexandria.dav import get_dav
    else:
        from camac.dav import get_dav
    return get_dav()
