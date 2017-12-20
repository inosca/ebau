"""This is an example settings file for production use."""

from .settings import *  # noqa: F401,F403

DEBUG = False

# add some random string
# see http://oonlab.com/edx/django/python/2016/08/09/generate-secret-key-django
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'camac',
        'USER':     'camac',
        'PASSWORD': 'camac',
        'HOST':     'localhost'
    }
}

# list of hosts which are allowed to connect to this service
ALLOWED_HOSTS = []
