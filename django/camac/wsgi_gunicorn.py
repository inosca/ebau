"""
WSGI config for camac-ng project without integrated dav.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from wsgi_common import setup_environment

setup_environment()

application = get_wsgi_application()
