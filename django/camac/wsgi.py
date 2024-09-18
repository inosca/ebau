"""
WSGI config for camac-ng project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import locale
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")

application = get_wsgi_application()
