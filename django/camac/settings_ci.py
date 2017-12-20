"""This is a settings file for GitLab CI to use."""
from .settings import *  # noqa: F401,F403

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'camac',
        'USER':     'camac',
        'PASSWORD': 'camac',
        'HOST':     'postgres'
    }
}
