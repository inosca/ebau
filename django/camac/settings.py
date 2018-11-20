import json
import os
import re

import environ

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 2

ENV_FILE = env.str("DJANGO_ENV_FILE", default=ROOT_DIR(".env"))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

ENV = env.str("APPLICATION_ENV")
APPLICATION_NAME = env.str("APPLICATION")
APPLICATION_DIR = ROOT_DIR.path(APPLICATION_NAME)
FORM_CONFIG = json.loads(APPLICATION_DIR.file("form.json").read())


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("DJANGO_SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DJANGO_DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=default(["*"]))

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.postgres",
    "django.contrib.contenttypes",
    "camac.core.apps.DefaultConfig",
    "camac.user.apps.DefaultConfig",
    "camac.instance.apps.DefaultConfig",
    "camac.document.apps.DefaultConfig",
    "camac.circulation.apps.DefaultConfig",
    "camac.notification.apps.DefaultConfig",
    "camac.responsible.apps.DefaultConfig",
    "camac.file.apps.DefaultConfig",
    "camac.applicants.apps.DefaultConfig",
    "camac.officeexporter.apps.DefaultConfig",
    "camac.auditlog.apps.DefaultConfig",
    "camac.tags.apps.DefaultConfig",
    "sorl.thumbnail",
    "django_clamd",
    "reversion",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "camac.user.middleware.GroupMiddleware",
    "camac.middleware.LoggingMiddleware",
    "reversion.middleware.RevisionMiddleware",
]

ROOT_URLCONF = "camac.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ]
        },
    }
]

WSGI_APPLICATION = "camac.wsgi.application"

# Application specific settings
# an application is defined by the customer e.g. uri, schwyz, etc.

APPLICATIONS = {
    # settings for demp app, can also used as example
    "demo": {
        # mapping between Camac role and instance permission
        "ROLE_PERMISSIONS": {
            "Municipality": "municipality",
            "Service": "service",
            "Canton": "canton",
        },
        "SUBMIT": {"NOTIFICATION_TEMPLATE": None, "WORKFLOW_ITEM": None},
    },
    "kt_schwyz": {
        # mapping between Camac role and instance permission
        "ROLE_PERMISSIONS": {
            "Gemeinde": "municipality",
            "Fachstelle": "service",
            "Fachstelle Sachbearbeiter": "service",
            "Kanton": "canton",
        },
        "SUBMIT": {"NOTIFICATION_TEMPLATE": 16, "WORKFLOW_ITEM": 10},
    }
    # add other application configuration here...
}

APPLICATION = APPLICATIONS.get(APPLICATION_NAME, {})

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {"django": {"handlers": ["console", "mail_admins"], "level": "INFO"}},
}

REQUEST_LOGGING_METHODS = env.list(
    "DJANGO_REQUEST_LOGGING_METHODS",
    default=default(["POST", "PUT", "PATCH", "DELETE"], []),
)
REQUEST_LOGGING_CONTENT_TYPES = env.list(
    "DJANGO_REQUEST_LOGGING_CONTENT_TYPES", default=["application/vnd.api+json"]
)

# Managing files

MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=default(ROOT_DIR("media")))

DEFAULT_FILE_STORAGE = env.str(
    "DJANGO_DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

THUMBNAIL_ENGINE = "sorl.thumbnail.engines.convert_engine.Engine"

ALLOWED_DOCUMENT_MIMETYPES = env.list(
    "DJANGO_ALLOWED_DOCUMENT_MIMETYPES",
    default=["image/png", "image/jpeg", "application/pdf"],
)

# Unoconv webservice
# https://github.com/zrrrzzt/tfk-api-unoconv

UNOCONV_URL = env.str("DJANGO_UNOCONV_URL", default="http://localhost:3000")


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DJANGO_DATABASE_ENGINE", default="postgresql_dbdefaults"),
        "NAME": env.str("DJANGO_DATABASE_NAME", default=APPLICATION_NAME),
        "USER": env.str("DJANGO_DATABASE_USER", default="camac"),
        "PASSWORD": env.str("DJANGO_DATABASE_PASSWORD", default=default("camac")),
        "HOST": env.str("DJANGO_DATABASE_HOST", default="localhost"),
        "PORT": env.str("DJANGO_DATABASE_PORT", default=""),
    }
}

# Cache
# https://docs.djangoproject.com/en/1.11/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": env.str(
            "DJANGO_CACHE_BACKEND",
            default="django.core.cache.backends.memcached.MemcachedCache",
        ),
        "LOCATION": env.str("DJANGO_CACHE_LOCATION", default="127.0.0.1:11211"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "de-ch"
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True


AUTH_PASSWORT_SALT = "ds5fsdFd763znsPO"
AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "camac.user.permissions.IsGroupMember",
        "camac.user.permissions.ViewPermissions",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "camac.user.authentication.JSONWebTokenKeycloakAuthentication",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "ORDERING_PARAM": "sort",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.MultiPartRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# Clamav service

CLAMD_USE_TCP = True
CLAMD_TCP_ADDR = env.str("DJANGO_CLAMD_TCP_ADDR", default="localhost")
CLAMD_ENABLED = env.bool("DJANGO_CLAMD_ENABLED", default=True)


# Keycloak service

KEYCLOAK_URL = env.str("KEYCLOAK_URL", default="http://camac-ng-keycloak.local/auth/")
KEYCLOAK_REALM = env.str("KEYCLOAK_REALM", default="ebau")
KEYCLOAK_CLIENT = env.str("KEYCLOAK_CLIENT", default="camac")

# Email definition

DEFAULT_FROM_EMAIL = env.str(
    "DJANGO_DEFAULT_FROM_EMAIL", default("webmaster@localhost")
)

SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default("root@localhost"))

EMAIL_HOST = env.str("DJANGO_EMAIL_HOST", default("localhost"))
EMAIL_PORT = env.str("DJANGO_EMAIL_PORT", 25)

EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER", "")
EMAIL_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.str("DJANGO_EMAIL_USE_TLS", False)

# Merge definition
MERGE_DATE_FORMAT = env.str("DJANGO_MERGE_DATE_FORMAT", "%d.%m.%Y")
MERGE_ANSWER_PERIOD = env.int("DJANGO_MERGE_ANSWER_PERIOD", 20)


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of DJANGO_ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search("(.+) \<(.+@.+)\>", admin)
        if not match:
            raise environ.ImproperlyConfigured(
                'In DJANGO_ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("DJANGO_ADMINS", default=[]))
