import datetime
import os

import environ

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str('DJANGO_ENV_FILE', default=django_root('.env'))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str('ENV', 'production')


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == 'production' else default_dev


SECRET_KEY = env.str('DJANGO_SECRET_KEY', default=default('uuuuuuuuuu'))
DEBUG = env.bool('DJANGO_DEBUG', default=default(True, False))
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=default(['*']))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'camac.core.apps.DefaultConfig',
    'camac.user.apps.DefaultConfig',
    'camac.instance.apps.DefaultConfig',
    'camac.document.apps.DefaultConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'camac.user.middleware.JWTAuthenticationMiddleware',
    'django_downloadview.SmartDownloadMiddleware',
]

ROOT_URLCONF = 'camac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]

WSGI_APPLICATION = 'camac.wsgi.application'

# Managing files

DOWNLOADVIEW_BACKEND = env.str(
    'DJANGO_DOWNLOADVIEW_BACKEND',
    default=default(
        'django_downloadview.middlewares.DownloadDispatcherMiddleware'
    )
)
DOWNLOADVIEW_RULES = env.list('DJANGO_DOWNLOADVIEW_RULES', default=default([]))

MEDIA_ROOT = env.str(
    'DJANGO_MEDIA_ROOT', default=default(django_root('media'))
)

DEFAULT_FILE_STORAGE = env.str(
    'DJANGO_DEFAULT_FILE_STORAGE',
    default='django.core.files.storage.FileSystemStorage'
)


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'DJANGO_DATABASE_ENGINE',
            default='django.db.backends.postgresql_psycopg2'
        ),
        'NAME': env.str('DJANGO_DATABASE_NAME', default='camac'),
        'USER': env.str('DJANGO_DATABASE_USER', default='camac'),
        'PASSWORD': env.str(
            'DJANGO_DATABASE_PASSWORD', default=default('camac')
        ),
        'HOST': env.str('DJANGO_DATABASE_HOST', default='localhost'),
        'PORT': env.str('DJANGO_DATABASE_PORT', default='')
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },  # noqa: E501
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },  # noqa: E501
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# TODO check if PHP stores datetime timezone aware or not
USE_TZ = False


AUTH_PASSWORT_SALT = 'ds5fsdFd763znsPO'
AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
        'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_METADATA_CLASS':
        'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.MultiPartRenderer'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json',
}

JSON_API_FORMAT_KEYS = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),
    'JWT_ALLOW_REFRESH': True,
}
