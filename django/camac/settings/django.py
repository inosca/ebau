import copy
import json
import logging
import os
import re
from datetime import timedelta
from importlib import import_module

import environ
from deepmerge import always_merger
from django.utils.translation import gettext_lazy as _

from camac.constants import kt_bern as be_constants
from camac.constants.kt_bern import (
    INSTANCE_STATE_DONE,
    INSTANCE_STATE_EVALUATED,
    INSTANCE_STATE_NEW,
    INSTANCE_STATE_SB1,
)
from camac.constants.kt_uri import KOOR_SERVICE_IDS as URI_KOOR_SERVICE_IDS
from camac.settings.env import ROOT_DIR, env
from camac.utils import build_url

# We need to import the caluma settings after we merge os.environ with our
# local .env file otherwise caluma tries to get it's settings from it's own env
# file (which doesn't exist)

from caluma.settings.caluma import *  # noqa isort:skip
from alexandria.settings.alexandria import *  # noqa isort:skip

ENV = env.str("APPLICATION_ENV", default="production")
APPLICATION_NAME = env.str("APPLICATION")
APPLICATION_DIR = ROOT_DIR.path(APPLICATION_NAME)
FORM_CONFIG = json.loads(APPLICATION_DIR.file("form.json").read())


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


def require_if(condition, default_value=None):
    return env.NOTSET if condition else default_value


SECRET_KEY = env.str("DJANGO_SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DJANGO_DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=default(["*"]))
API_HOST = env.str("DJANGO_API_HOST", default="http://localhost:80")
ENABLE_SILK = env.bool("DJANGO_ENABLE_SILK", default=False)

DEMO_MODE = env.bool("DEMO_MODE", default=False)

# Token exchange (currently only for SO)
ENABLE_TOKEN_EXCHANGE = env.bool("ENABLE_TOKEN_EXCHANGE", default=False)

# Apache swallows info about HTTPS request, leading to issues with FileFields
# See https://docs.djangoproject.com/en/2.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# UR uses urec.ur.ch and urec.kt.ur.ch to refer to the same system. This makes sure
# that django infers the correct base uri in FileFields (build_absolute_uri).
USE_X_FORWARDED_HOST = env.bool("DJANGO_USE_X_FORWARDED_HOST", default=False)

# Application definition

INSTALLED_APPS = [
    "camac.apps.DjangoAdminConfig",
    "django.contrib.messages",
    "django.contrib.auth",
    "django.contrib.sessions",
    "mozilla_django_oidc",
    "django.contrib.postgres",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_json_api",
    # Caluma and it's dependencies:
    "caluma.caluma_core.apps.DefaultConfig",
    "caluma.caluma_user.apps.DefaultConfig",
    "caluma.caluma_form.apps.DefaultConfig",
    "caluma.caluma_workflow.apps.DefaultConfig",
    "caluma.caluma_data_source.apps.DefaultConfig",
    "caluma.caluma_analytics.apps.DefaultConfig",
    # GWR module
    "generic_permissions.apps.GenericPermissionsConfig",
    "ebau_gwr.linker.apps.LinkerConfig",
    "ebau_gwr.token_proxy.apps.TokenProxyConfig",
    "graphene_django",
    "localized_fields",
    "psqlextra",
    "simple_history",
    # Camac and it's dependencies
    "drf_yasg",
    "camac.core.apps.DefaultConfig",
    "camac.user.apps.DefaultConfig",
    "camac.instance.apps.DefaultConfig",
    "camac.document.apps.DefaultConfig",
    "camac.circulation.apps.DefaultConfig",
    "camac.notification.apps.DefaultConfig",
    "camac.responsible.apps.DefaultConfig",
    "camac.applicants.apps.DefaultConfig",
    "camac.auditlog.apps.DefaultConfig",
    "camac.tags.apps.DefaultConfig",
    "camac.objection.apps.DefaultConfig",
    "camac.ech0211.apps.Ech0211Config",
    "camac.migrate_to_caluma.apps.MigrateConfig",
    "camac.stats.apps.StatsConfig",
    "camac.parashift.apps.ParashiftConfig",
    "camac.dossier_import.apps.DossierImportConfig",
    "camac.communications.apps.CommunicationsConfig",
    "camac.permissions.apps.PermissionsConfig",
    "camac.gis.apps.GisConfig",
    "camac.billing.apps.BillingConfig",
    "sorl.thumbnail",
    "django_clamd",
    "django_q",
    "reversion",
    "rest_framework_xml",
    "camac.django_admin.apps.DjangoAdminConfig",
    "camac.token_exchange.apps.TokenExchangeConfig",
    # alexandria
    "alexandria.core.apps.DefaultConfig",
    "camac.alexandria.apps.AlexandriaConfig",
    # TODO: remove this when all production environments ran the migration to
    # delete the tables of this app
    "camac.file.apps.DefaultConfig",
    "manabi_migrations",
    "adminsortable2",
    "django_json_widget",
]

if DEBUG:  # pragma: no cover
    try:
        __import__("django_extensions")
        INSTALLED_APPS.append("django_extensions")
    except ImportError:
        # Nothing bad, just won't have django-extensions niceties installed
        # (Most likely the container was built without dev dependencies)
        pass

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "django.middleware.locale.LocaleMiddleware",
    "camac.middleware.SystemLocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "camac.user.middleware.GroupMiddleware",
    "camac.caluma.middleware.CalumaInfoMiddleware",
    "camac.middleware.LoggingMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "camac.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(ROOT_DIR, "camac/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            # for rendering plain-text emails
            "autoescape": False,
        },
    }
]

WSGI_APPLICATION = "camac.wsgi.application"


# Application specific settings
# an application is defined by the customer e.g. uri, schwyz, etc.
APPLICATIONS = {
    "test": {
        "SHORT_NAME": "test",
        "INTERNAL_FRONTEND": "ebau",
        "USE_CAMAC_ADMIN": True,
        "LOG_NOTIFICATIONS": True,
        # Mapping between camac role and instance permission.
        "ROLE_PERMISSIONS": {
            # Commonly used roles
            "Applicant": "applicant",
            "Municipality": "municipality",
            "Administration Leitbehörde": "municipality",
            "Coordination": "coordination",
            "Service": "service",
            "TrustedService": "trusted_service",
            "Reader": "reader",
            "Canton": "canton",
            "PublicReader": "public_reader",
            "Support": "support",
            "Commission": "commission",
            "OrganizationReadonly": "organization_readonly",
            "Oereb Api": "oereb_api",
            "municipality-lead": "municipality",
            "municipality-clerk": "municipality",
            "service-lead": "service",
            "service-clerk": "service",
            "subservice": "service",
            "Geometer": "geometer",
            "uso": "uso",
        },
        "ADMIN_GROUP": 1,
        "ROLE_INHERITANCE": {"trusted_service": "service"},
        "IS_MULTILINGUAL": False,
        "NOTIFICATIONS": {"SUBMIT": None, "APPLICANT": {"NEW": None, "EXISTING": None}},
        "FORM_BACKEND": "camac-ng",
        "THUMBNAIL_SIZE": "x300",
        "WORKFLOW_ITEMS": {
            "SUBMIT": None,
            "INSTANCE_COMPLETE": None,
            "PUBLICATION": None,
            "START_CIRC": None,
            "DECISION": None,
        },
        "PAPER": {
            "ALLOWED_ROLES": {"DEFAULT": []},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": []},
        },
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SERVICE_UPDATE_ALLOWED_ROLES": [
            "Administration Leitbehörde"
        ],  # if unset, all are allowed
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": ["core", "responsible", "document"],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "PORTAL_GROUP": None,
        "CALUMA": {
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "HAS_PROJECT_CHANGE": False,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
        },
        "STORE_PDF": {"SECTION": 1},
        "SET_SUBMIT_DATE_CAMAC_ANSWER": True,
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {
            "WRITER_CLASS": "camac.dossier_import.writers.DossierWriter",
        },
        "CUSTOM_NOTIFICATION_TYPES": [
            # BE
            "inactive_municipality",
            "geometer_acl_services",
            # UR
            "municipality_users",
            "unnotified_service_users",
            "lisag",
            "koor_np_users",
            "koor_bg_users",
            "koor_bd_users",
            "koor_sd_users",
            "koor_afe_users",
            "responsible_koor",
            # GR
            "aib",
            "gvg",
            # SZ
            "involved_in_construction_step",
            "localized_geometer",
            "tax_administration",
        ],
        "ATTACHMENT_SECTION_INTERNAL": 4,
        "DOCUMENT_BACKEND": "camac-ng",
    },
    "kt_schwyz": {
        "SHORT_NAME": "sz",
        "INTERNAL_FRONTEND": "camac",
        "INCLUDE_STATIC_FILES": [("xml", "kt_schwyz/static/ech0211/xml/")],
        "USE_CAMAC_ADMIN": True,
        "LOG_NOTIFICATIONS": True,
        "ROLE_PERMISSIONS": {
            "Portal": "applicant",
            "Gemeinde": "municipality",
            "Gemeinde Sachbearbeiter": "municipality",
            "Fachstelle": "service",
            "Fachstelle Sachbearbeiter": "service",
            "Kanton": "canton",
            "Lesezugriff": "reader",
            "Publikation": "public_reader",
            "Fachstelle Leitbehörde": "municipality",
            "Support": "support",
        },
        "GENERALIZED_ROLE_MAPPING": {
            "Gemeinde": "municipality-lead",
            "Gemeinde Sachbearbeiter": "municipality-clerk",
            "Fachstelle": "service-lead",
            "Fachstelle Sachbearbeiter": "service-clerk",
            "Lesezugriff": "readonly",
            "Fachstelle Leitbehörde": "municipality-lead",
            "Support": "support",
        },
        "PUBLIC_ROLES": ["Publikation", "Portal"],
        "INSTANCE_HIDDEN_STATES": {
            "municipality": ["new"],
            "service": ["new"],
            "reader": ["subm"],
        },
        "PORTAL_GROUP": 4,
        "ADMIN_GROUP": 1,
        "SERVICE_GROUPS_FOR_DISTRIBUTION": {
            "roles": {
                "Gemeinde": [
                    {"id": "4", "localized": False},
                    {"id": "5", "localized": True},
                ],
                "Gemeinde Sachbearbeiter": [
                    {"id": "4", "localized": False},
                    {"id": "5", "localized": True},
                ],
                "Fachstelle Leitbehörde": [
                    {"id": "3", "localized": False},
                    {"id": "4", "localized": False},
                ],
            },
            "groups": {
                7: [  # Baugesuchszentrale
                    {"id": "1", "localized": False},
                    {"id": "2", "localized": False},
                ],
            },
        },
        "INTER_SERVICE_GROUP_VISIBILITIES": {
            # Externe Fachstellen
            1: [1, 2, 3, 4],
            # Fachstellen
            2: [1, 2, 3, 4],
            # Gemeinde
            3: [4, 5],
            # Baugesuchszentrale
            4: [1, 2, 4],
            # Fachstellen Gemeinden
            5: [5],
        },
        "GEOMETER_FORM_FIELDS": {
            "geometer",
            "geometer-v2",
            "geometer-v3",
            "geometer-v4",
        },
        # Important: All versions of the geometer form-field option need to be included!
        # geometer form-field option: service ids
        "LOCALIZED_GEOMETER_SERVICE_MAPPING": {
            # geometer
            "Trigonet AG (Stans)": [
                152,  # Trigonet AG (Geometer) - (deactivated)
            ],
            "Geoterra AG (Siebnen, Pfäffikon, Einsiedeln)": [
                129,  # Geoterra AG (Geometer) - (deactivated)
                147,  # Geoterra AG (Gde_Bez Ingenieur) - (deactivated)
            ],
            "GEO Netz AG (Schwyz, Lachen)": [
                313,  # GEO Netz AG (Geometer)
            ],
            "HSK Ingenieur AG (Goldau, Küssnacht, Brunnen)": [
                # No service found
            ],
            "geometrie plus ag (Freienbach, Einsiedeln)": [
                144,  # geometrie plus ag (Gde_Bez Ingenieur)
                154,  # geometrie plus ag (Geometer)
            ],
            "Wild Ingenieure AG (Küssnacht)": [
                150,  # Wild Ingenieure AG (Geometer)
                151,  # Wild Ingenieure AG (Gde_Bez Ingenieur)
            ],
            # geometer-v2 (only removal)
            # geometer-v3
            "Geoinfra Ingenieure AG (Pfäffikon, Siebnen, Einsiedeln, Goldau, Küssnacht, Brunnen)": [
                148,  # Geoinfra Goldau (Geometer)
                149,  # Geoinfra Goldau (Gde_Bez Ingenieur)
                299,  # Geoinfra Küssnacht (Geometer)
                300,  # Geoinfra Küssnacht (Gde_Bez Ingenieur)
                301,  # Geoinfra Brunnen (Geometer)
                302,  # Geoinfra Brunnen (Gde_Bez Ingenieur)
                303,  # Geoinfra Siebnen (Geometer)
                304,  # Geoinfra Einsiedeln (Geometer)
                305,  # Geoinfra Pfäffikon (Geometer)
                306,  # Geoinfra Pfäffikon (Gde_Bez Ingenieur)
                333,  # Geoinfra Siebnen (Gde_Bez Ingenieur)
                334,  # Geoinfra Siebnen (Gde Umwelt)
            ],
            "geometrie plus ag (Freienbach)": [
                144,  # geometrie plus ag (Gde_Bez Ingenieur)
                154,  # geometrie plus ag (Geometer)
            ],
            "GEO Netz AG (Lachen, Schwyz)": [
                313,  # GEO Netz AG (Geometer)
            ],
            # geometer-v4
            "geometrie plus ag (Einsiedeln, Freienbach)": [
                144,  # geometrie plus ag (Gde_Bez Ingenieur),
                154,  # geometrie plus ag (Geometer)
            ],
        },
        "TAX_ADMINISTRATION": 196,  # Kantonale Steuerverwaltung
        "NOTIFICATIONS": {
            "SUBMIT": "gesuchseingang",
            "APPLICANT": {
                "NEW": "gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "gesuchsbearbeitungs-einladung-bestehend",
            },
            "COMPLETE_MANUAL_WORK_ITEM": [
                {
                    "template_slug": "complete-manual-work-item",
                    "recipient_types": ["work_item_controlling"],
                }
            ],
        },
        "CUSTOM_NOTIFICATION_TYPES": [
            "involved_in_construction_step",
            "localized_geometer",
            "tax_administration",
        ],
        "PUBLICATION_DURATION": timedelta(days=20),
        "PUBLICATION_ATTACHMENT_SECTION": [4],
        "ATTACHMENT_INTERNAL_STATES": ["internal"],
        "ATTACHMENT_SECTION_INTERNAL": None,
        "ATTACHMENT_DELETEABLE_STATES": [
            "new",
            "rejected",
        ],
        "IS_MULTILINGUAL": False,
        "CIRCULATION_STATE_END": "DONE",
        "FORM_BACKEND": "camac-ng",
        "COORDINATE_QUESTION": "punkte",
        "LOCATION_NAME_QUESTION": "ortsbezeichnung-des-vorhabens",
        "WORKFLOW_ITEMS": {
            "SUBMIT": 10,
            "INSTANCE_COMPLETE": 14,
            "PUBLICATION": 15,
            "START_CIRC": 44,
            "DECISION": 47,
        },
        "QUESTIONS_WITH_OVERRIDE": [
            "bezeichnung",
            "bauherrschaft",
            "bauherrschaft-v2",
            "bauherrschaft-v3",
            "projektverfasser-planer",
            "projektverfasser-planer-v2",
            "projektverfasser-planer-v3",
            "grundeigentumerschaft",
            "grundeigentumerschaft-v2",
        ],
        "INSTANCE_IDENTIFIER_FORM_ABBR": {
            "geschaeftskontrolle": "IG",
            "municipality": "GS",
            "district": "BS",
            "canton": "KS",
            "astra": "PA",
            "esti": "PE",
            "bavb": "PB",
            "bavs": "PS",
            "bazl": "PL",
            "vbs": "PV",
            "uebrige": "PU",
        },
        "INSTANCE_MERGE_CONFIG": {
            "BAUVERWALTUNG": {
                "TASK_SLUG": "building-authority",
            }
        },
        "CALUMA_INSTANCE_FORMS": [
            "geschaeftskontrolle",
        ],
        "INTERNAL_INSTANCE_FORMS": [
            "geschaeftskontrolle",
        ],
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": [],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "CALUMA": {
            "FORM_PERMISSIONS": [
                "bauverwaltung",
                "inquiry",
                "inquiry-answer",
            ],
            "INTERNAL_FORMS": [
                "voranfrage",
                "voranfrage-personalien",
                "are-geschaeft",
                "koordinaten",
            ],
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "ACTIVATION_EXCLUDE_ROLES": ["Lesezugriff"],
            "SUBMIT_TASKS": ["submit", "submit-additional-demand", "formal-addition"],
            "REJECTION_TASK": "reject-form",
            "PRE_COMPLETE": {
                "complete-check": {"cancel": ["reject-form"]},
                "reject-form": {"cancel": ["complete-check", "depreciate-case"]},
                "formal-addition": {"cancel": ["archive-instance"]},
                "make-decision": {
                    "skip": [
                        "depreciate-case",
                    ],
                },
                "check-inquiry": {"cancel": ["revise-inquiry"]},
                "revise-inquiry": {"cancel": ["check-inquiry"]},
                "distribution": {
                    "cancel": ["additional-demand", "submit-additional-demand"]
                },
                "depreciate-case": {
                    # CAUTION: When importing dossiers this section is modified in runtime to avoid unwanted
                    # outcomes when fast-forwarding workflow states of imported cases.
                    "cancel": [
                        "formal-addition",
                        "complete-check",
                        "reject-form",
                        "publication",
                        "distribution",
                        "additional-demand",
                        "submit-additional-demand",
                        "make-decision",
                    ]
                },
                "archive-instance": {
                    "cancel": [
                        "create-manual-workitems",
                        "publication",
                    ],
                    "complete": [
                        "building-authority",
                    ],
                },
                "finish-document": {"cancel": ["create-manual-workitems"]},
            },
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": False,
            "PUBLICATION_TASK_SLUG": "publication",
            "CREATE_IN_PROCESS": True,
            "SIMPLE_WORKFLOW": {
                "formal-addition": {
                    "next_instance_state": "subm",
                },
                "complete-check": {
                    "next_instance_state": "comm",
                    "history_text": "Dossier angenommen",
                    "notification": {
                        "template_slug": "bewilligungsprozess-gestartet",
                        "recipient_types": ["applicant"],
                    },
                },
                "reject-form": {
                    "next_instance_state": "rejected",
                    "history_text": "Dossier zurückgewiesen",
                    "notification": {
                        "template_slug": "ruckweisung",
                        "recipient_types": ["applicant"],
                    },
                },
                "make-decision": {
                    "next_instance_state": "done",
                    "history_text": "Bewilligung erteilt",
                },
                "archive-instance": {
                    "next_instance_state": "arch",
                    "history_text": "Dossier archiviert",
                },
                "depreciate-case": {
                    "next_instance_state": "stopped",
                    "history_text": "Dossier abgeschrieben",
                },
                "additional-demand": {
                    "next_instance_state": "nfd",
                    "history_text": "Nachforderung gestartet",
                    "notification": {
                        "template_slug": "nachforderung",
                        "recipient_types": ["applicant"],
                    },
                },
                "init-distribution": {
                    "next_instance_state": "circ",
                    "history_text": "Zirkulation gestartet",
                },
                "complete-distribution": {
                    "next_instance_state": "redac",
                },
                "complete-instance": {
                    "next_instance_state": "instance-completed",
                    "history_text": "Verfahren abgeschlossen",
                },
            },
        },
        "HAS_EBAU_NUMBER": False,
        "HAS_GESUCHSNUMMER": True,
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "SHORT_DOSSIER_NUMBER": True,
        "INTERCHANGEABLE_FORMS": [
            "vorentscheid-gemass-ss84-pbg-v2",
            "vorentscheid-gemass-ss84-pbg-v3",
            "vorentscheid-gemass-ss84-pbg-v4",
            "vorentscheid-gemass-ss84-pbg-v5",
            "vorentscheid-gemass-ss84-pbg-v6",
            "vorentscheid-gemass-ss84-pbg-v7",
            "vorentscheid-gemass-ss84-pbg-v8",
            "vorentscheid-gemass-ss84-pbg-v9",
            "baugesuch-reklamegesuch-v2",
            "baugesuch-reklamegesuch-v3",
            "baugesuch-reklamegesuch-v4",
            "baugesuch-reklamegesuch-v5",
            "baugesuch-reklamegesuch-v6",
            "baugesuch-reklamegesuch-v7",
            "baugesuch-reklamegesuch-v8",
            "baugesuch-reklamegesuch-v9",
            "projektanderung-v2",
            "projektanderung-v3",
            "projektanderung-v4",
            "projektanderung-v5",
            "projektanderung-v6",
            "projektanderung-v7",
            "projektanderung-v8",
            "projektanderung-v9",
            "projektanderung-v10",
            "technische-bewilligung",
            "technische-bewilligung-v2",
            "technische-bewilligung-v3",
            "technische-bewilligung-v4",
            "baumeldung-fur-geringfugiges-vorhaben-v2",
            "baumeldung-fur-geringfugiges-vorhaben-v3",
            "baumeldung-fur-geringfugiges-vorhaben-v4",
            "baumeldung-fur-geringfugiges-vorhaben-v5",
            "baumeldung-fur-geringfugiges-vorhaben-v6",
            "anlassbewilligungen-verkehrsbewilligungen-v2",
            "anlassbewilligungen-verkehrsbewilligungen-v3",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v2",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v4",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v5",
        ],
        "STORE_PDF": {"SECTION": 1},
        "FORM_FIELD_HISTORY_ENTRY": [
            {
                "name": "materieller-pruefbericht-bemerkung",
                "title": "Materieller Prüfbericht (Bemerkung)",
            },
            {
                "name": "materieller-pruefbericht",
                "title": "Materieller Prüfbericht",
            },
        ],
        "ADDRESS_FORM_FIELDS": [
            "ortsbezeichnung-des-vorhabens",
            "standort-spezialbezeichnung",
            "standort-ort",
        ],
        "CONSTRUCTION_ZONE_LOCATION_FORM_FIELD": "lage",
        "INTENT_FORM_FIELDS": [
            "bezeichnung",
            "bezeichnung-override",
        ],
        "DOSSIER_IMPORT": {
            "WRITER_CLASS": "camac.dossier_import.config.kt_schwyz.KtSchwyzDossierWriter",
            "INSTANCE_STATE_MAPPING": {"SUBMITTED": 2, "APPROVED": 8, "DONE": 10},
            "USER": "service-account-camac-admin",
            "FORM_ID": 29,  # "migriertes-dossier"
            "CALUMA_FORM": "baugesuch",  # "dummy"-Form
            "ATTACHMENT_SECTION_ID": 7,  # attachmentsection for imported documents
            "LOCATION_REQUIRED": True,  # this is a workaround to account for differing validation requirements per config
            "RESOURCE_ID_PATH": "/index/template/resource-id/25#/dossier-import/",  # That's required for `reversing` the URL to the dossier-import resource tab in the UI
            "TRANSFORM_COORDINATE_SYSTEM": "epsg:4326",  # use world wide coordinates instead of swiss ones
            "PROD_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_URL", "https://behoerden.ebau-sz.ch/"
            ),
            "PROD_AUTH_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
                "https://ebau-sz.ch/auth/realms/ebau/protocol/openid-connect/token",
            ),
            "PROD_SUPPORT_GROUP_ID": 486,
        },
        "THUMBNAIL_SIZE": "x300",
        "DOCUMENT_BACKEND": "camac-ng",
    },
    "kt_bern": {
        "SHORT_NAME": "be",
        "INTERNAL_FRONTEND": "camac",
        "TAGGED_RELEASES": True,
        "USE_CAMAC_ADMIN": True,
        "INCLUDE_STATIC_FILES": [("xml", "kt_bern/static/ech0211/xml")],
        "LOG_NOTIFICATIONS": True,
        "SYSTEM_USER": "service-account-camac-admin",
        "ATTACHMENT_SECTION_INTERNAL": 4,
        "ROLE_PERMISSIONS": {
            "applicant": "applicant",
            "service-lead": "service",
            "service-clerk": "service",
            "service-readonly": "service",
            "service-admin": "service",
            "subservice": "service",
            "municipality-lead": "municipality",
            "municipality-clerk": "municipality",
            "municipality-readonly": "municipality",
            "municipality-admin": "municipality",
            "construction-control-lead": "municipality",
            "construction-control-clerk": "municipality",
            "construction-control-readonly": "municipality",
            "construction-control-admin": "municipality",
            "support": "support",
            "geometer-lead": "geometer",
            "geometer-clerk": "geometer",
            "geometer-readonly": "geometer",
            "geometer-admin": "geometer",
        },
        "INSTANCE_PERMISSIONS": {"MUNICIPALITY_WRITE": ["correction"]},
        "CUSTOM_NOTIFICATION_TYPES": [
            "inactive_municipality",
            "geometer_acl_services",
        ],
        "CIRCULATION_STATE_END": "DONE",
        "CIRCULATION_ANSWER_UNINVOLVED": "not_concerned",
        "COPY_RESPONSIBLE_PERSON_ON_SUBMIT": True,
        "THUMBNAIL_SIZE": "x300",
        "NOTIFICATIONS": {
            "SUBMIT": [
                {
                    "template_slug": "00-empfang-anfragebaugesuch-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "00-empfang-anfragebaugesuch-behorden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "SUBMIT_PRELIMINARY_CLARIFICATION": [
                {
                    "template_slug": "00-empfang-vorabklaerung-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "00-empfang-anfragebaugesuch-behorden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "SUBMIT_HEAT_GENERATOR": [
                {
                    "template_slug": "00-empfang-meldung-waermeerzeugerersatz-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "00-empfang-meldung-waermeerzeugerersatz-behoerden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "REPORT": [
                {
                    "template_slug": "11-meldung-selbstdeklaration-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "11-meldung-selbstdeklaration-baukontrolle",
                    "recipient_types": [
                        "construction_control",
                        "involved_in_distribution",
                    ],
                },
                {
                    "template_slug": "11-meldung-selbstdeklaration-geometer",
                    "recipient_types": ["geometer_acl_services"],
                },
            ],
            "FINALIZE": [
                {
                    "template_slug": "13-meldung-termine-pflichtkontrollen-baukontrolle",
                    "recipient_types": [
                        "construction_control",
                        "involved_in_distribution",
                    ],
                },
                {
                    "template_slug": "notify-geometer-sb2-complete",
                    "recipient_types": [
                        "geometer_acl_services",
                    ],
                },
            ],
            "APPLICANT": {
                "NEW": "gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "gesuchsbearbeitungs-einladung-bestehend",
            },
            "CHANGE_RESPONSIBLE_SERVICE": {
                "template_slug": "02-benachrichtigung-baubewilligungsbehorde",
                "recipient_types": ["leitbehoerde"],
            },
            "DECISION": [
                {
                    "template_slug": "08-entscheid-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "08-entscheid-behoerden",
                    "recipient_types": [
                        "leitbehoerde",
                        "involved_in_distribution",
                        "inactive_municipality",
                    ],
                },
            ],
            "DECISION_PRELIMINARY_CLARIFICATION": [
                {
                    "template_slug": "08-beurteilung-zu-voranfrage-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "08-beurteilung-zu-voranfrage-behoerden",
                    "recipient_types": [
                        "leitbehoerde",
                        "involved_in_distribution",
                        "inactive_municipality",
                    ],
                },
            ],
            "COMPLETE_MANUAL_WORK_ITEM": [
                {
                    "template_slug": "complete-manual-work-item",
                    "recipient_types": ["work_item_controlling"],
                }
            ],
            "CREATE_MANUAL_WORK_ITEM": [
                {
                    "template_slug": "create-manual-work-item",
                    "recipient_types": ["work_item_addressed"],
                }
            ],
            "PERMISSION_ACL_GRANTED": [
                {
                    "template_slug": "invited-via-permission-acl",
                    "recipient_types": ["acl_authorized"],
                }
            ],
        },
        "IS_MULTILINGUAL": True,
        "FORM_BACKEND": "caluma",
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
            "phone",
        ],
        "CALUMA": {
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "FORM_PERMISSIONS": [
                "main",
                "sb1",
                "sb2",
                "nfd",
                "dossierpruefung",
                "publikation",
                "information-of-neighbors",
                "ebau-number",
                "decision",
                "inquiry",
                "inquiry-answer",
                "geometer",
            ],
            "SUBMIT_TASKS": ["submit"],
            "REPORT_TASK": "sb1",
            "FINALIZE_TASK": "sb2",
            "AUDIT_TASK": "audit",
            "EBAU_NUMBER_TASK": "ebau-number",
            "SIMPLE_WORKFLOW": {
                "init-distribution": {
                    "next_instance_state": "circulation",
                    "ech_event": "camac.ech0211.signals.circulation_started",
                    "history_text": _("Circulation started"),
                    "notification": {
                        "template_slug": "03-verfahrensablauf-gesuchsteller",
                        "recipient_types": ["applicant"],
                    },
                },
                "complete-distribution": {
                    "next_instance_state": "coordination",
                    "ech_event": "camac.ech0211.signals.circulation_ended",
                    "notification": {
                        "template_slug": "03-verfahren-vorzeitig-beendet",
                        "recipient_types": ["unanswered_inquiries"],
                    },
                },
                "complete": {
                    "next_instance_state": "finished",
                    "ech_event": "camac.ech0211.signals.finished",
                    "history_text": _("Procedure completed"),
                },
            },
            "INTERNAL_FORMS": [
                "baupolizeiliches-verfahren",
                "zutrittsermaechtigung",
                "klaerung-baubewilligungspflicht",
            ],
            "MODIFICATION_ALLOW_FORMS": [
                "baugesuch",
                "baugesuch-v2",
                "baugesuch-v3",
                "baugesuch-generell",
                "baugesuch-generell-v2",
                "baugesuch-generell-v3",
                "baugesuch-mit-uvp",
                "baugesuch-mit-uvp-v2",
                "baugesuch-mit-uvp-v3",
            ],
            "MODIFICATION_DISALLOW_STATES": [
                "new",
                "finished",
                "archived",
            ],
            "COPY_PAPER_ANSWER_TO": ["nfd", "sb1", "sb2"],
            "COPY_PERSONAL": [
                {
                    "TASK": "sb1",
                    "DOCUMENT": lambda work_item: work_item.case.document,
                    "SOURCE": "personalien-sb",
                    "TARGET": "personalien-sb1-sb2",
                    "FALLBACK": "personalien-gesuchstellerin",
                },
                {
                    "TASK": "sb2",
                    "DOCUMENT": lambda work_item: work_item.case.work_items.get(
                        task_id="sb1"
                    ).document,
                    "SOURCE": "personalien-sb1-sb2",
                    "TARGET": "personalien-sb1-sb2",
                    "FALLBACK": None,
                },
            ],
            "COPY_TANK_INSTALLATION": [
                {
                    "TASK": "sb2",
                    "DOCUMENT": lambda work_item: work_item.case.document,
                    "SOURCE": "lagerung-von-stoffen-v2",
                    "TARGET": "lagerung-von-stoffen-v2",
                    "FALLBACK": None,
                },
            ],
            "PRE_COMPLETE": {
                "decision": {
                    "skip": [
                        "audit",
                        "publication",
                        "fill-publication",
                        "legal-submission",
                        "appeal",
                    ],
                    "cancel": [
                        "create-manual-workitems",
                        "create-publication",
                        "information-of-neighbors",
                        "create-information-of-neighbors",
                    ],
                    "complete": ["nfd"],
                },
                "complete": {
                    "skip": ["check-sb1", "check-sb2"],
                    "cancel": [
                        "create-manual-workitems",
                        "create-publication",
                        "fill-publication",
                        "geometer",
                    ],
                },
            },
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "EXTEND_VALIDITY_FORM": "verlaengerung-geltungsdauer",
            "EXTEND_VALIDITY_COPY_QUESTIONS": [
                "weitere-personen",
                "verantwortliche-person-sb-identisch",
                "strasse-flurname",
                "nr",
                "plz-grundstueck-v3",
                "ort-grundstueck",
                "gemeinde",
                "beschreibung-bauvorhaben",
            ],
            "EXTEND_VALIDITY_COPY_TABLE_QUESTIONS": [
                "personalien-gesuchstellerin",
                "personalien-vertreterin-mit-vollmacht",
                "personalien-grundeigentumerin",
                "personalien-gebaudeeigentumerin",
                "personalien-projektverfasserin",
                "personalien-sb",
                "parzelle",
            ],
            "PUBLIC_STATUS": {
                "MAP": {
                    be_constants.INSTANCE_STATE_NEW: be_constants.PUBLIC_INSTANCE_STATE_CREATING,
                    be_constants.INSTANCE_STATE_EBAU_NUMMER_VERGEBEN: be_constants.PUBLIC_INSTANCE_STATE_RECEIVING,
                    be_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS: be_constants.PUBLIC_INSTANCE_STATE_COMMUNAL,
                    be_constants.INSTANCE_STATE_IN_PROGRESS: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
                    be_constants.INSTANCE_STATE_IN_PROGRESS_INTERNAL: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
                    be_constants.INSTANCE_STATE_KOORDINATION: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
                    be_constants.INSTANCE_STATE_VERFAHRENSPROGRAMM_INIT: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
                    be_constants.INSTANCE_STATE_ZIRKULATION: be_constants.PUBLIC_INSTANCE_STATE_IN_PROGRESS,
                    be_constants.INSTANCE_STATE_REJECTED: be_constants.PUBLIC_INSTANCE_STATE_REJECTED,
                    be_constants.INSTANCE_STATE_CORRECTED: be_constants.PUBLIC_INSTANCE_STATE_CORRECTED,
                    be_constants.INSTANCE_STATE_SB1: be_constants.PUBLIC_INSTANCE_STATE_SB1,
                    be_constants.INSTANCE_STATE_SB2: be_constants.PUBLIC_INSTANCE_STATE_SB2,
                    be_constants.INSTANCE_STATE_TO_BE_FINISHED: be_constants.PUBLIC_INSTANCE_STATE_FINISHED,
                    be_constants.INSTANCE_STATE_FINISHED: be_constants.PUBLIC_INSTANCE_STATE_FINISHED,
                    be_constants.INSTANCE_STATE_ARCHIVED: be_constants.PUBLIC_INSTANCE_STATE_ARCHIVED,
                    be_constants.INSTANCE_STATE_DONE: be_constants.PUBLIC_INSTANCE_STATE_DONE,
                    be_constants.INSTANCE_STATE_DONE_INTERNAL: be_constants.PUBLIC_INSTANCE_STATE_DONE,
                },
                "DEFAULT": be_constants.PUBLIC_INSTANCE_STATE_CREATING,
            },
        },
        "ATTACHMENT_AFTER_DECISION_STATES": [
            "rejected",
            "correction",
            "sb1",
            "sb2",
            "conclusion",
            "finished",
            "finished_internal",
            "evaluated",
        ],
        "PORTAL_GROUP": 6,
        "ADMIN_GROUP": 1,
        "DEMO_MODE_GROUPS": [
            23395,
            23396,
            23399,
            23400,
            23403,
            23404,
            23407,
            23408,
            23412,
            23415,
        ],
        "USE_INSTANCE_SERVICE": True,
        "ACTIVE_SERVICES": {
            "MUNICIPALITY": {
                "FILTERS": {
                    "service__service_group__name__in": [
                        "municipality",
                        "district",
                        "lead-service",
                    ]
                },
                "DEFAULT": True,
            },
            "CONSTRUCTION_CONTROL": {
                "FILTERS": {"service__service_group__name": "construction-control"},
                "INSTANCE_STATES": [
                    ("sb1", "coordination"),
                    ("sb2", "sb1"),
                    ("conclusion", "sb2"),
                    ("finished", "conclusion"),
                ],
            },
        },
        "STORE_PDF": {
            "SECTION": {
                "MAIN": {"DEFAULT": 1, "PAPER": 13},
                "SB1": {"DEFAULT": 6, "PAPER": 10},
                "SB2": {"DEFAULT": 5, "PAPER": 11},
            }
        },
        "PAPER": {
            "ALLOWED_ROLES": {
                "SB1": [5, 20005],
                "SB2": [5, 20005],
                "DEFAULT": [3, 20004],
            },
            "ALLOWED_SERVICE_GROUPS": {"SB1": [3], "SB2": [3], "DEFAULT": [2, 20000]},
        },
        "DOCUMENT_BACKEND": "camac-ng",
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SUBSERVICE_ROLES": ["subservice"],
        "SERVICE_UPDATE_ALLOWED_ROLES": [
            "municipality-admin",
            "service-admin",
            "construction-control-admin",
            "geometer-admin",
        ],
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": ["core", "responsible", "document"],
        "HAS_EBAU_NUMBER": True,
        "HAS_GESUCHSNUMMER": False,
        "SET_SUBMIT_DATE_CAMAC_ANSWER": True,
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "DOSSIER_IMPORT": {
            "WRITER_CLASS": "camac.dossier_import.config.kt_bern.KtBernDossierWriter",
            "INSTANCE_STATE_MAPPING": {
                "BUILDINGPERMIT": {
                    "SUBMITTED": INSTANCE_STATE_NEW,
                    "APPROVED": INSTANCE_STATE_SB1,
                    "REJECTED": INSTANCE_STATE_DONE,
                    "WRITTEN OFF": INSTANCE_STATE_DONE,
                    "DONE": INSTANCE_STATE_DONE,
                },
                "PRELIMINARY": {
                    "SUBMITTED": INSTANCE_STATE_NEW,
                    "APPROVED": INSTANCE_STATE_EVALUATED,
                    "REJECTED": INSTANCE_STATE_EVALUATED,
                    "WRITTEN OFF": INSTANCE_STATE_EVALUATED,
                    "DONE": INSTANCE_STATE_EVALUATED,
                },
            },
            "USER": "service-account-camac-admin",
            "WORKFLOW_MAPPING": {
                "BUILDINGPERMIT": "building-permit",
                "PRELIMINARY": "preliminary-clarification",
            },
            "CALUMA_FORM": "migriertes-dossier",
            "FORM_ID": 1,
            "ATTACHMENT_SECTION_ID": 4,  # Internal
            "PROD_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_URL",
                "https://ebau.apps.be.ch/",
            ),
            "PROD_AUTH_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
                "https://sso.be.ch/auth/realms/ebau/protocol/openid-connect/token",
            ),
            "PROD_SUPPORT_GROUP_ID": 10000,
            "RESOURCE_ID_PATH": "/index/template/resource-id/2000000#/dossier-import/",  # That's required for `reversing` the URL to the dossier-import resource tab in the UI
        },
        "MUNICIPALITY_DATA_SHEET": APPLICATION_DIR(
            "Verwaltungskreise und -regionen der Gemeinden.csv"
        ),
        "ATTACHMENT_MAX_SIZE": 100 * 1024 * 1024,
    },
    "kt_uri": {
        "SHORT_NAME": "ur",
        "INTERNAL_FRONTEND": "camac",
        "USE_CAMAC_ADMIN": True,
        "ENABLE_PUBLIC_CALUMA": True,
        "LOG_NOTIFICATIONS": False,
        "FORM_BACKEND": "caluma",
        "PUBLICATION_DURATION": timedelta(days=20),
        "PORTAL_USER_ID": 1209,
        "USE_OEREB_FIELDS_FOR_PUBLIC_ENDPOINT": True,
        "LINK_INSTANCES_ON_COPY": True,
        "CIRCULATION_STATE_END": "OK",
        "APPLICANT_GROUP_ID": 685,  # We reuse the Portal User group
        "SEQUENCE_NAMESPACE_APPS": ["core", "document", "responsible"],
        "THUMBNAIL_SIZE": "x600",
        "ATTACHMENT_SECTION_INTERNAL": None,
        "CUSTOM_NOTIFICATION_TYPES": [
            "municipality_users",
            "unnotified_service_users",
            "lisag",
            "koor_np_users",
            "koor_bg_users",
            "koor_bd_users",
            "koor_sd_users",
            "koor_afe_users",
            "responsible_koor",
        ],
        "DOCUMENTS_SKIP_CONTEXT_VALIDATION": True,
        "CALUMA": {
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "FILL_PUBLICATION_TASK": None,
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": True,
            "USE_LOCATION": True,
            "KOOR_SD_SLUGS": [
                "veranstaltung-art-sportanlass",
                "veranstaltung-art-foto-und-filmaufnahmen",
                "veranstaltung-art-andere",
            ],
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
            "SYNC_FORM_TYPE": True,
            "SUBMIT_TASKS": ["submit"],
            "MODIFICATION_ALLOW_FORMS": [
                "building-permit",
            ],
            "MODIFICATION_DISALLOW_STATES": [
                "new",
                "done",
                "old",
            ],
            "SIMPLE_WORKFLOW": {
                "accept": {
                    "next_instance_state": "comm",
                },
                "complete-distribution": {
                    "next_instance_state": "done",
                },
                "construction-supervision": {
                    "next_instance_state": "control",
                },
                "archive": {
                    "next_instance_state": "arch",
                },
            },
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
        },
        "STORE_PDF": {
            "SECTION": {
                "MAIN": {"DEFAULT": 12000000, "PAPER": 12000000},
            },
        },
        "DOCUMENT_BACKEND": "camac-ng",
        "ARCHIVE_FORMS": [293, 294],
        "PAPER": {
            "ALLOWED_ROLES": {
                "DEFAULT": [
                    3,  # KOOR BG
                    6,  # Sekretariat Gemeindebaubehörde
                    1061,  # KOOR NP
                    1101,  # KOOR BD
                    1106,  # KOOR AfU
                    1107,  # KOOR ALA
                    1127,  # KOOR AfE
                    1128,  # KOOR AFJ
                    1129,  # KOOR SD
                    1133,  # KOOR AfG
                    1130,  # Bundesstelle
                ]
            },
            "ALLOWED_SERVICE_GROUPS": {
                "DEFAULT": [
                    1,  # Koordinationsstellen
                    68,  # Sekretariate Gemeindebaubehörden
                    70,  # Bundesstellen
                ]
            },
        },
        "ROLE_PERMISSIONS": {
            "Bundesstelle": "coordination",
            "Gemeinde als Vernehmlassungsstelle": "service",
            "Koordinationsstelle Baudirektion BD": "coordination",
            "Koordinationsstelle Baugesuche BG": "coordination",
            "Koordinationsstelle Nutzungsplanung NP": "coordination",
            "Koordinationsstelle Energie AfE": "coordination",
            "Koordinationsstelle Forst und Jagd AFJ": "coordination",
            "Koordinationsstelle Landwirtschaft ALA": "coordination",
            "Koordinationsstelle Sicherheitsdirektion SD": "coordination",
            "Koordinationsstelle Umwelt AfU": "coordination",
            "Koordinationsstelle Amt für das Grundbuch AfG": "coordination",
            "Mitglied der Gemeindebaubehörde": "municipality",  # TODO Maybe we should introduce a municipality_readonly role?
            "Mitglied einer Kommission oder Fachgruppe": "commission",
            "Organisation mit Leseberechtigung": "organization_readonly",
            "Sekretariat der Gemeindebaubehörde": "municipality",
            "Vernehmlassungsstelle Gemeindezirkulation": "service",
            "Vernehmlassungsstelle mit Koordinationsaufgaben": "trusted_service",
            "Vernehmlassungsstelle ohne Koordinationsaufgaben": "trusted_service",
            "System-Betrieb": "support",
            "Oereb Api": "oereb_api",
            # "Portal User": None,  # Uses the fallback permissions
            # "Admin": None,
            # "Architect": None,
            # "Guest": None,  # TODO AFAIK we don't grant unauthenticated users access to endpoints
        },
        "ROLE_INHERITANCE": {"trusted_service": "service"},
        "INSTANCE_HIDDEN_STATES": {
            "municipality": ["del"],
            "coordination": ["new_portal", "del", "rejected"],
            "trusted_service": ["new", "new_portal", "del", "rejected"],
            "oereb_api": ["new", "new_portal", "del", "rejected"],
        },
        "INSTANCE_PERMISSIONS": {
            "MUNICIPALITY_WRITE": ["comm", "ext_gem", "done", "old", "control"]
        },
        "NOTIFICATIONS": {
            "SUBMIT": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-gemeinde",
                    "recipient_types": ["municipality_users"],
                },
            ],
            "SUBMIT_KOOR_SD": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-sd",
                    "recipient_types": ["koor_sd_users"],
                },
            ],
            "SUBMIT_KOOR_BD": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-bd",
                    "recipient_types": ["koor_bd_users"],
                },
            ],
            "SUBMIT_KOOR_AFE": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-afe",
                    "recipient_types": ["koor_afe_users"],
                },
            ],
            "SUBMIT_KOOR_NP": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-np",
                    "recipient_types": ["koor_np_users"],
                },
            ],
            "APPLICANT": {
                "NEW": "01-gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "02-gesuchsbearbeitungs-einladung-bestehend",
            },
        },
        "HAS_EBAU_NUMBER": False,
        "HAS_GESUCHSNUMMER": False,
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
            "city",
            "zip",
            "address",
            "phone",
        ],
        "COORDINATION_SERVICE_IDS": URI_KOOR_SERVICE_IDS,
        "PORTAL_GROUP": 685,
        "ADMIN_GROUP": 1,
        "OEREB_FORMS": [296, 305],
        "INSTANCE_IDENTIFIER_FORM_ABBR": {},
        "SET_SUBMIT_DATE_CAMAC_WORKFLOW": True,
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {},
        "GENERALIZED_ROLE_MAPPING": {
            "Vernehmlassungsstelle mit Koordinationsaufgaben": "service-lead",
            "Sekretariat der Gemeindebaubehörde": "municipality-lead",
            "Mitglied der Gemeindebaubehörde": "municipality-clerk",
            "Vernehmlassungsstelle ohne Koordinationsaufgaben": "service-lead",
            "Mitglied einer Kommission oder Fachgruppe": "service-clerk",
            "Gemeinde als Vernehmlassungsstelle": "service-lead",
            "Vernehmlassungsstelle Gemeindezirkulation": "service-lead",
            "Organisation mit Leseberechtigung": "readonly",
            "Bundesstelle": "service-lead",
            "System-Betrieb": "support",
            "Oereb Api": "readonly",
            "Koordinationsstelle Baugesuche BG": "coordination-lead",
            "Koordinationsstelle Nutzungsplanung NP": "coordination-lead",
            "Koordinationsstelle Baudirektion BD": "coordination-lead",
            "Koordinationsstelle Umwelt AfU": "coordination-lead",
            "Koordinationsstelle Landwirtschaft ALA": "coordination-lead",
            "Koordinationsstelle Energie AfE": "coordination-lead",
            "Koordinationsstelle Forst und Jagd AFJ": "coordination-lead",
            "Koordinationsstelle Sicherheitsdirektion SD": "coordination-lead",
            "Portal User": "portal-user",
        },
        "USE_INSTANCE_SERVICE": True,
        "ACTIVE_SERVICES": {
            "MUNICIPALITY": {
                "FILTERS": {
                    "service__service_group__name__in": [
                        "Sekretariate Gemeindebaubehörden",
                        "Koordinationsstellen",
                    ]
                },
                "DEFAULT": True,
            },
        },
        "SERVICE_GROUPS_FOR_DISTRIBUTION": {
            "roles": {
                "Sekretariat der Gemeindebaubehörde": [
                    {"id": "1", "localized": False},  # Koordinationsstellen
                    {"id": "41", "localized": True},  # Gemeinderäte
                    {"id": "67", "localized": True},  # Mitglieder Baukommission
                    {"id": "69", "localized": True},  # Gemeinde Servicestellen
                    {
                        "id": "72",
                        "localized": False,
                    },  # Infrastrukturanlagen Pendenzen von Gemeinden
                ],
                "Koordinationsstelle Baugesuche BG": [
                    {"id": "1", "localized": False},  # Koordinationsstellen
                    {"id": "2", "localized": False},  # Fachstellen Baudirektion
                    {"id": "41", "localized": False},  # Gemeinderäte
                    {"id": "61", "localized": False},  # Fachstellen Justizdirektion
                    {"id": "70", "localized": False},  # Bundesstellen
                    {
                        "id": "72",
                        "localized": False,
                    },  # Infrastrukturanlagen Pendenzen von Gemeinden
                ],
                "Koordinationsstelle Umwelt AfU": [
                    {
                        "id": "62",
                        "localized": False,
                    },  # Fachstellen Gesundheits- Sozial- und Umweltdirektion
                ],
                "Koordinationsstelle Forst und Jagd AFJ": [
                    {"id": "2", "localized": False},  # Fachstellen Baudirektion
                ],
            },
        },
        "INTER_SERVICE_GROUP_VISIBILITIES": {},
    },
    "demo": {
        "SHORT_NAME": "demo",
        "INTERNAL_FRONTEND": "ebau",
        "USE_CAMAC_ADMIN": True,
        "LOG_NOTIFICATIONS": True,
        # Mapping between camac role and instance permission.
        "ROLE_PERMISSIONS": {
            "service": "service",
            "municipality": "municipality",
            "support": "support",
        },
        "ADMIN_GROUP": 1,
        "IS_MULTILINGUAL": True,
        "FORM_BACKEND": "caluma",
        "THUMBNAIL_SIZE": "x300",
        "WORKFLOW_ITEMS": {
            "SUBMIT": None,
            "INSTANCE_COMPLETE": None,
            "PUBLICATION": None,
            "START_CIRC": None,
            "DECISION": None,
        },
        "PAPER": {
            "ALLOWED_ROLES": {"DEFAULT": []},
            "ALLOWED_SERVICE_GROUPS": {"DEFAULT": []},
        },
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SERVICE_UPDATE_ALLOWED_ROLES": [
            "Administration Leitbehörde"
        ],  # if unset, all are allowed
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": ["core", "responsible", "document"],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "PORTAL_GROUP": 20097,
        "CALUMA": {
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "SUBMIT_TASKS": ["submit"],
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "HAS_PROJECT_CHANGE": False,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
        },
        "USE_INSTANCE_SERVICE": True,
        "ACTIVE_SERVICES": {
            "MUNICIPALITY": {
                "FILTERS": {
                    "service__service_group__name__in": [
                        "municipality",
                    ]
                },
                "DEFAULT": True,
            },
        },
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {},
        "CUSTOM_NOTIFICATION_TYPES": [],
        "NOTIFICATIONS": {
            "SUBMIT": [
                {
                    "template_slug": "00-empfang-anfragebaugesuch-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "00-empfang-anfragebaugesuch-behorden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
        },
        "ATTACHMENT_SECTION_INTERNAL": 4,
        "DOCUMENT_BACKEND": "camac-ng",
        "GENERALIZED_ROLE_MAPPING": {
            "municipality": "municipality-lead",
            "service": "service-lead",
            "support": "support",
        },
    },
    "kt_gr": {
        "SHORT_NAME": "gr",
        "INTERNAL_FRONTEND": "ebau",
        "USE_CAMAC_ADMIN": False,
        "INCLUDE_STATIC_FILES": [("xml", "kt_bern/static/ech0211/xml")],
        "LOG_NOTIFICATIONS": True,
        "STORE_PDF": {
            "SECTION": {
                "MAIN": {
                    "DEFAULT": "beilagen-zum-gesuch-weitere-gesuchsunterlagen",
                    "PAPER": "beilagen-zum-gesuch-weitere-gesuchsunterlagen",
                }
            },
        },
        # Mapping between camac role and instance permission.
        "ROLE_PERMISSIONS": {
            "municipality-lead": "municipality",
            "municipality-admin": "municipality",
            "service-lead": "service",
            "service-admin": "service",
            "subservice": "service",
            "support": "support",
            "uso": "uso",
        },
        "ADMIN_GROUP": 1,
        "IS_MULTILINGUAL": True,
        "FORM_BACKEND": "caluma",
        "THUMBNAIL_SIZE": "x300",
        "WORKFLOW_ITEMS": {
            "SUBMIT": None,
            "INSTANCE_COMPLETE": None,
            "PUBLICATION": None,
            "START_CIRC": None,
            "DECISION": None,
        },
        "PAPER": {
            "ALLOWED_ROLES": {
                "DEFAULT": [
                    3,  # municipality-lead
                ]
            },
            "ALLOWED_SERVICE_GROUPS": {
                "DEFAULT": [
                    2,  # municipality
                ]
            },
        },
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SERVICE_UPDATE_ALLOWED_ROLES": [
            "municipality-admin",
            "service-admin",
        ],  # if unset, all are allowed
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": ["core", "responsible", "document"],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "PORTAL_GROUP": 3,
        "CALUMA": {
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "SUBMIT_TASKS": ["submit"],
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": True,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
            "MODIFICATION_ALLOW_FORMS": [
                "baugesuch",
            ],
            "PRE_COMPLETE": {
                "decision": {
                    "skip": [
                        "publication",
                        "fill-publication",
                    ],
                    "cancel": [
                        "create-publication",
                    ],
                    "complete": ["additional-demand"],
                },
                "fill-publication": {"complete": ["publication"]},
                "construction-acceptance": {"cancel": ["create-manual-workitems"]},
            },
            "SIMPLE_WORKFLOW": {
                "formal-exam": {
                    "next_instance_state": "init-distribution",
                    "history_text": _("Preliminary exam performed"),
                    "ech_event": "camac.ech0211.signals.exam_completed",
                },
                "init-distribution": {
                    "next_instance_state": "circulation",
                    "history_text": _("Circulation started"),
                },
                "complete-distribution": {
                    "next_instance_state": "decision",
                },
                "send-additional-demand": {
                    "history_text": _("Additional demand sent"),
                    "notification": {
                        "template_slug": "send-additional-demand",
                        "recipient_types": ["applicant", "additional_demand_inviter"],
                    },
                },
                "fill-additional-demand": {
                    "history_text": _("Additional demand was answered"),
                    "notification": {
                        "template_slug": "fill-additional-demand",
                        "recipient_types": ["work_item_controlling"],
                    },
                },
                "construction-acceptance": {
                    "next_instance_state": "finished",
                    "history_text": _("Construction monitoring performed"),
                    # for notification see events/construction-acceptance.py
                },
            },
            "PUBLIC_STATUS": {
                "USE_SLUGS": True,
                "MAP": {
                    "new": "creation",
                    "subm": "submitted",
                    "init-distribution": "inProcedure",
                    "correction": "inProcedure",
                    "circulation": "inProcedure",
                    "construction-acceptance": "constructionAcceptance",
                    "decision": "inProcedure",
                    "finished": "done",
                    "rejected": "rejected",
                },
                "DEFAULT": "inProcedure",
            },
        },
        "INSTANCE_PERMISSIONS": {"MUNICIPALITY_WRITE": ["correction"]},
        "USE_INSTANCE_SERVICE": True,
        "ACTIVE_SERVICES": {
            "MUNICIPALITY": {
                "FILTERS": {
                    "service__service_group__name__in": [
                        "municipality",
                    ]
                },
                "DEFAULT": True,
            },
        },
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {},
        "CUSTOM_NOTIFICATION_TYPES": ["gvg", "aib"],
        "NOTIFICATIONS": {
            "SUBMIT": [
                {
                    "template_slug": "empfang-anfragebaugesuch-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "empfang-anfragebaugesuch-behorden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "APPLICANT": {
                "NEW": "gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "gesuchsbearbeitungs-einladung-bestehend",
            },
            "DECISION": [
                {
                    "template_slug": "entscheid-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "entscheid-behoerden",
                    "recipient_types": ["leitbehoerde"],
                },
                {
                    "template_slug": "entscheid-behoerden",
                    "recipient_types": ["gvg"],
                },
            ],
            "NON_BUILDING_PERMIT_DECISION": [
                {
                    "template_slug": "beurteilung-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "beurteilung-behoerden",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "CONSTRUCTION_ACCEPTANCE": [
                {
                    "template_slug": "bauabnahme",
                    "recipient_types": ["aib"],
                },
                {
                    "template_slug": "bauabnahme-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
            ],
        },
        "SUBSERVICE_ROLES": ["subservice"],
        "DOCUMENT_BACKEND": "alexandria",
    },
    "kt_so": {
        "SHORT_NAME": "so",
        "INTERNAL_FRONTEND": "ebau",
        "TAGGED_RELEASES": True,
        "USE_CAMAC_ADMIN": False,
        "LOG_NOTIFICATIONS": True,
        "ENABLE_PUBLIC_CALUMA": True,
        # Mapping between camac role and instance permission.
        "ROLE_PERMISSIONS": {
            "applicant": "applicant",
            "municipality-admin": "municipality",
            "municipality-lead": "municipality",
            "municipality-clerk": "municipality",
            "municipality-construction-monitoring": "municipality",
            "municipality-read": "municipality",
            "service-admin": "service",
            "service-lead": "service",
            "service-clerk": "service",
            "subservice": "service",
            "support": "support",
        },
        "DEMO_MODE_GROUPS": [
            5,  # Leitung Gemeinde Solothurn
            8,  # Einsichtsberechtigte Gemeinde Solothurn
            539,  # Leitung Amt für Umwelt (AfU)
        ],
        "ADMIN_GROUP": 1,
        "IS_MULTILINGUAL": True,
        "FORM_BACKEND": "caluma",
        "THUMBNAIL_SIZE": "x300",
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SERVICE_UPDATE_ALLOWED_ROLES": [],  # if unset, all are allowed
        "SEQUENCE_NAMESPACE_APPS": [],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "PAPER": {
            "ALLOWED_ROLES": {
                "DEFAULT": [
                    5,  # municipality-lead
                ]
            },
            "ALLOWED_SERVICE_GROUPS": {
                "DEFAULT": [
                    1,  # municipality
                ]
            },
        },
        "PORTAL_GROUP": 2,
        "CALUMA": {
            "MANUAL_WORK_ITEM_TASK": "create-manual-workitems",
            "SUBMIT_TASKS": ["submit"],
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": True,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
            "MODIFICATION_ALLOW_FORMS": [],
            "SIMPLE_WORKFLOW": {
                "formal-exam": {
                    "next_instance_state": "material-exam",
                    "history_text": _("Formal exam performed"),
                },
                "material-exam": {
                    "next_instance_state": "init-distribution",
                    "history_text": _("Material exam performed"),
                },
                "init-distribution": {
                    "next_instance_state": "distribution",
                    "history_text": _("Circulation started"),
                },
                "complete-distribution": {
                    "next_instance_state": "decision",
                },
                "send-additional-demand": {
                    "notification": {
                        "template_slug": "nachforderung-neu",
                        "recipient_types": ["applicant"],
                    },
                },
                "fill-additional-demand": {
                    "notification": {
                        "template_slug": "nachforderung-beantwortet",
                        "recipient_types": ["work_item_controlling"],
                    },
                },
            },
            "PRE_COMPLETE": {
                # Cancel init-additional-demand after material-exam as it will
                # again be created in the distribution child case
                "material-exam": {"cancel": ["init-additional-demand"]},
                # Complete publication work item after the first filled and
                # completed publication
                "fill-publication": {"complete": ["publication"]},
                # Cancel additional demands outside of the distribution when the
                # distribution is completed in order to have the same behaviour
                # as additional demands inside the distribution
                "distribution": {"cancel": ["additional-demand"]},
                # Complete, skip and cancel various work items after decision
                "decision": {
                    "skip": ["publication", "fill-publication", "objections"],
                    "cancel": ["create-publication"],
                },
            },
            "PUBLIC_STATUS": {
                "USE_SLUGS": True,
                "MAP": {
                    "new": "creation",
                    "subm": "submitted",
                    "material-exam": "submitted",
                    "init-distribution": "inProcedure",
                    "distribution": "inProcedure",
                    "correction": "inProcedure",
                    "decision": "inProcedure",
                    "construction-monitoring": "constructionMonitoring",
                    "finished": "done",
                    "reject": "inProcedure",
                    "rejected": "rejected",
                    "withdrawal": "withdrawn",
                    "withdrawn": "withdrawn",
                },
                "DEFAULT": "inProcedure",
            },
        },
        "INSTANCE_PERMISSIONS": {"MUNICIPALITY_WRITE": ["correction"]},
        "USE_INSTANCE_SERVICE": True,
        "DOSSIER_IMPORT": {},
        "CUSTOM_NOTIFICATION_TYPES": [],
        "NOTIFICATIONS": {
            "SUBMIT": [
                {
                    "template_slug": "empfang-baugesuch-bauherrschaft",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "empfang-baugesuch-gemeinde",
                    "recipient_types": ["leitbehoerde"],
                },
            ],
            "APPLICANT": {
                "NEW": "gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "gesuchsbearbeitungs-einladung-bestehend",
            },
            "DECISION": [
                {
                    "template_slug": "entscheid-bauherrschaft",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "entscheid-behoerden",
                    "recipient_types": ["involved_in_distribution"],
                },
            ],
            "DOSSIERKORREKTUR": [
                {
                    "template_slug": "dossierkorrektur",
                    "recipient_types": ["applicant"],
                },
            ],
        },
        "SUBSERVICE_ROLES": ["subservice"],
        "ACTIVE_SERVICES": {
            "MUNICIPALITY": {
                "FILTERS": {
                    "service__service_group__name__in": [
                        "municipality",
                    ]
                },
                "DEFAULT": True,
            },
        },
        "DOCUMENT_BACKEND": "alexandria",
        "STORE_PDF": {
            "SECTION": {
                "MAIN": {
                    "DEFAULT": "beilagen-zum-gesuch-weitere-gesuchsunterlagen",
                    "PAPER": "beilagen-zum-gesuch-weitere-gesuchsunterlagen",
                }
            },
        },
    },
}

APPLICATION = APPLICATIONS.get(APPLICATION_NAME, {})

PUBLIC_BASE_URL = build_url(
    env.str("DJANGO_PUBLIC_BASE_URL", default=default("http://ebau-portal.local"))
)

INTERNAL_BASE_URL = build_url(
    env.str("DJANGO_INTERNAL_BASE_URL", default=default("http://ebau.local"))
)

PUBLIC_INSTANCE_URL_TEMPLATE = env.str(
    "DJANGO_PUBLIC_INSTANCE_URL_TEMPLATE",
    default=build_url(PUBLIC_BASE_URL, "/instances/{instance_id}"),
)

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
            "format": "[%(asctime)s] %(message)s",
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
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "camac": {"handlers": ["console", "mail_admins"], "level": "INFO"},
    },
}

REQUEST_LOGGING_METHODS = env.list(
    "DJANGO_REQUEST_LOGGING_METHODS",
    default=default(["POST", "PUT", "PATCH", "DELETE"], []),
)
REQUEST_LOGGING_CONTENT_TYPES = env.list(
    "DJANGO_REQUEST_LOGGING_CONTENT_TYPES", default=["application/vnd.api+json"]
)
REQUEST_LOGGING_HTTP_4XX_LOG_LEVEL = env.str(
    "DJANGO_REQUEST_LOGGING_HTTP_4XX_LOG_LEVELS",
    default=default(logging.ERROR, logging.INFO),
)

# Managing files

MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=default(ROOT_DIR("media")))
MEDIA_URL = "/api/v1/"
TEMPFILE_DOWNLOAD_PATH = env.str(
    "DJANGO_TEMPFILE_DOWNLOAD_PATH", default="/tmp/camac/tmpfiles"
)
TEMPFILE_DOWNLOAD_URL = env.str("DJANGO_TEMPFILE_DOWNLOAD_URL", default="/zips")
# in seconds
TEMPFILE_RETENTION_TIME = env.int(
    "DJANGO_TEMPFILE_RETENTION_TIME", default=(60 * 60 * 24)
)

STATIC_ROOT = ROOT_DIR("staticfiles")
STATICFILES_DIRS = []  # declare empyt list in order to append config specific dirs

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DEFAULT_FILE_STORAGE = env.str(
    "DJANGO_DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
FILE_UPLOAD_PERMISSIONS = env.int("FILE_UPLOAD_PERMISSIONS", default=0o644)

THUMBNAIL_ENGINE = "sorl.thumbnail.engines.convert_engine.Engine"
THUMBNAIL_FLATTEN = True

DEFAULT_DOCUMENT_MIMETYPES = env.list(
    "DJANGO_DEFAULT_DOCUMENT_MIMETYPES",
    default=["image/png", "image/jpeg", "application/pdf"],
)
ALLOWED_DOCUMENT_MIMETYPES = env.list(
    "DJANGO_ALLOWED_DOCUMENT_MIMETYPES",
    default=[
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        "application/xml",
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/tiff",
        "text/plain",
    ],
)

# Unoconv webservice
# https://github.com/zrrrzzt/tfk-api-unoconv

UNOCONV_URL = env.str("DJANGO_UNOCONV_URL", default="http://unoconv:3000")


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
database_options = {}
if env.bool("DATABASE_ENABLE_SSL", default=False):  # pragma: no cover
    database_options["sslmode"] = "require"

DATABASES = {
    "default": {
        "ENGINE": "camac.core.postgresql_dbdefaults.psqlextra",
        "NAME": env.str("DATABASE_NAME", default=APPLICATION_NAME),
        "USER": env.str("DATABASE_USER", default="camac"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("camac")),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default=database_options),
    }
}

# Sequence ranges to be used for each developer. Note: NEVER EVER
# EVER change this without talking to the affected developers. New
# developers should just be appended instead (which is safe).
SEQUENCE_NAMESPACES_SIZE = 1000000
SEQUENCE_NAMESPACES = {}


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

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

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

# https://docs.djangoproject.com/en/4.0/releases/3.2/#customizing-type-of-auto-created-primary-keys
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


DEFAULT_LOCALE_CODE = "de_CH"
LANGUAGE_CODE = "de"
LANGUAGES = [
    ("de", _("German")),
    ("fr", _("French")),
    ("it", _("Italian")),
]
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(ROOT_DIR, "camac", "instance", "placeholders", "locale"),
    os.path.join(ROOT_DIR, "locale"),
)


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
        "camac.filters.MultilingualSearchFilter",
        "rest_framework.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
    ),
    "ORDERING_PARAM": "sort",
    "SEARCH_PARAM": "search",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.MultiPartRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True

# Clamav service

CLAMD_USE_TCP = True
CLAMD_TCP_ADDR = env.str("DJANGO_CLAMD_TCP_ADDR", default="localhost")
CLAMD_ENABLED = env.bool("DJANGO_CLAMD_ENABLED", default=True)


# Keycloak service

KEYCLOAK_URL = build_url(
    env.str("KEYCLOAK_URL", default="http://ebau-keycloak.local/auth/"),
    trailing=True,
)
KEYCLOAK_REALM = env.str("KEYCLOAK_REALM", default="ebau")
KEYCLOAK_CLIENT = env.str("KEYCLOAK_CLIENT", default="camac")
KEYCLOAK_PORTAL_CLIENT = env.str("KEYCLOAK_PORTAL_CLIENT", default="portal")

KEYCLOAK_OIDC_TOKEN_URL = build_url(
    KEYCLOAK_URL, f"/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=10
)
REGISTRATION_URL = env.str(
    "DJANGO_REGISTRATION_URL",
    default=build_url(
        KEYCLOAK_URL,
        f"/realms/{KEYCLOAK_REALM}/login-actions/registration?client_id={KEYCLOAK_CLIENT}",
    ),
)

# Token exchange config
TOKEN_EXCHANGE_CLIENT = env.str("TOKEN_EXCHANGE_CLIENT", default="token-exchange")
TOKEN_EXCHANGE_CLIENT_SECRET = env.str(
    "TOKEN_EXCHANGE_CLIENT",
    default=default(
        "76e3ScwJqsP0EMsYHKmEyBjlE1bNeOU1", require_if(ENABLE_TOKEN_EXCHANGE)
    ),
)
TOKEN_EXCHANGE_USERNAME_TEMPLATE = "egov:{identifier}"

# External JWT token config
TOKEN_EXCHANGE_JWE_SECRET = env.str(
    "TOKEN_EXCHANGE_JWE_SECRET",
    default=default(
        "somerandomutf8secretthatisexactly64biteslongforencyption12345678",
        require_if(ENABLE_TOKEN_EXCHANGE),
    ),
)
TOKEN_EXCHANGE_JWT_SECRET = env.str(
    "TOKEN_EXCHANGE_JWT_SECRET",
    default=default("my-secret", require_if(ENABLE_TOKEN_EXCHANGE)),
)
TOKEN_EXCHANGE_JWT_ISSUER = env.str(
    "TOKEN_EXCHANGE_JWT_ISSUER",
    default=default("http://egov.local", require_if(ENABLE_TOKEN_EXCHANGE)),
)
TOKEN_EXCHANGE_JWT_IDENTIFIER_PROPERTY = "profileId"
TOKEN_EXCHANGE_JWT_SYNC_PROPERTIES = {
    # jwt_property: keycloak_property
    "firstName": "firstName",
    "name": "lastName",
    "email": "email",
}

# JWT token claim used as the username for newly created Camac users. (This is
# also used in the caluma settings.py, we redefine it here so it is explicit)
OIDC_USERNAME_CLAIM = env.str("OIDC_USERNAME_CLAIM", default="sub")

# Map existing users to OIDC identities by their mail address
OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK = env.str(
    "OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK", default=False
)

# Email definition

DEFAULT_FROM_EMAIL = env.str(
    "DJANGO_DEFAULT_FROM_EMAIL", default("webmaster@localhost")
)

SUPPORT_EMAIL_ADDRESS = env.str(
    "SUPPORT_EMAIL_ADDRESS", default("support@example.com", "")
)

SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default("root@localhost"))

EMAIL_HOST = env.str("DJANGO_EMAIL_HOST", default("localhost"))
EMAIL_PORT = env.str("DJANGO_EMAIL_PORT", 25)

EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.str("DJANGO_EMAIL_USE_TLS", False)

EMAIL_PREFIX_SUBJECT = env.str("EMAIL_PREFIX_SUBJECT", default("[eBau Test]: ", ""))
EMAIL_PREFIX_BODY = env.str(
    "EMAIL_PREFIX_BODY",
    default(
        (
            "Hinweis: Diese Nachricht wurde von einem Testsystem versendet.\n"
            "Sie dient nur zu Testzwecken und kann ignoriert werden.\n\n"
        ),
        "",
    ),
)
EMAIL_PREFIX_BODY_SPECIAL_FORMS = env.str(
    "EMAIL_PREFIX_BODY_SPECIAL_FORMS",
    (
        "Achtung: Dieses Gesuch kann nur in eBau bearbeitet werden.\n"
        "Attention: Cette demande ne peut être traitée dans que eBau.\n\n"
    ),
)

# Merge definition
MERGE_DATE_FORMAT = env.str("DJANGO_MERGE_DATE_FORMAT", "%d.%m.%Y")
MERGE_ANSWER_PERIOD = env.int("DJANGO_MERGE_ANSWER_PERIOD", 20)

# override locale-based setting for template handling
SHORT_DATE_FORMAT = MERGE_DATE_FORMAT


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of DJANGO_ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:
            raise environ.ImproperlyConfigured(
                'In DJANGO_ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("DJANGO_ADMINS", default=[]))
DEVELOPER_EMAIL_DOMAINS = env.list(
    "DJANGO_DEVELOPER_EMAIL_DOMAINS", default=["adfinis.com"]
)

# GIS API (Kt. BE)
GIS_BASE_URL = build_url(
    env.str(
        "GIS_BASE_URL",
        default(
            "https://www.geoservice2-test.apps.be.ch",
            "https://www.geoservice.apps.be.ch",
        ),
    )
)
BE_GIS_ENABLE_QUEUE = env.bool("BE_GIS_ENABLE_QUEUE", default=True)

BE_GIS_POLYGON_LAYER_ID = env.str(
    "BE_GIS_POLYGON_LAYER_ID", default="DIPANU_DIPANUF_VW_13541"
)
BE_GIS_POLYGON_SERVICE_CODE = env.str(
    "BE_GIS_POLYGON_SERVICE_CODE", default="of_planningcadastre01_de_ms_wfs"
)

GIS_REQUESTS_BATCH_SIZE = env.int("GIS_REQUESTS_BATCH_SIZE", default=4)

# GIS API (KT. GR)
GR_GIS_BASE_URL = env.str("GR_GIS_BASE_URL", default="https://wps.geo.gr.ch")
GIS_API_USER = env.str("GIS_API_USER", "")
GIS_API_PASSWORD = env.str("GIS_API_PASSWORD", "")
GR_ECH0206_BASE_URL = env.str(
    "GR_ECH0206_BASE_URL", default="https://madd.bfs.admin.ch/eCH-0206"
)

GIS_SKIP_BOOLEAN_LAYERS = env.list("GIS_SKIP_BOOLEAN_LAYERS", default=[])

GIS_SKIP_SPECIAL_LAYERS = env.list("GIS_SKIP_SPECIAL_LAYERS", default=[])

SO_GIS_BASE_URL = env.str(
    "SO_GIS_BASE_URL", default=default("https://geo-i.so.ch", "https://geo.so.ch")
)
SO_GIS_VERIFY_SSL = env.bool("SO_GIS_VERIFY_SSL", default=True)
ADMIN_GIS_BASE_URL = env.str("ADMIN_GIS_BASE_URL", default="https://api3.geo.admin.ch")
ADMIN_GIS_VERIFY_SSL = env.bool("ADMIN_GIS_VERIFY_SSL", default=True)

DOCUMENT_MERGE_SERVICE_URL = build_url(
    env.str("DOCUMENT_MERGE_SERVICE_URL", "http://document-merge-service:8000/api/v1/")
)

ECH_EXCLUDED_WORKFLOWS = ["internal"]
ECH_EXCLUDED_FORMS = [
    "verlaengerung-geltungsdauer",
    "migriertes-dossier",
    "baupolizeiliches-verfahren",
    "hecken-feldgehoelze-baeume",
    "klaerung-baubewilligungspflicht",
    "zutrittsermaechtigung",
    "solaranlagen-meldung",
    "heat-generator",
]

# Swagger settings
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "DEEP_LINKING": True,
    "SECURITY_DEFINITIONS": {
        "oauth2": {
            "type": "oauth2",
            "tokenUrl": KEYCLOAK_OIDC_TOKEN_URL,
            "flow": "application",
            "scopes": {},
        }
    },
    "DEFAULT_PAGINATOR_INSPECTORS": [
        "camac.swagger.schema.DjangoRestJsonApiResponsePagination",
        "drf_yasg.inspectors.CoreAPICompatInspector",
    ],
    "DEFAULT_FIELD_INSPECTORS": [
        "camac.swagger.schema.ModelSerializerInspector",
        "drf_yasg.inspectors.CamelCaseJSONFilter",
        "drf_yasg.inspectors.ReferencingSerializerInspector",
        "drf_yasg.inspectors.RelatedFieldInspector",
        "drf_yasg.inspectors.ChoiceFieldInspector",
        "drf_yasg.inspectors.FileFieldInspector",
        "drf_yasg.inspectors.DictFieldInspector",
        "drf_yasg.inspectors.HiddenFieldInspector",
        "drf_yasg.inspectors.RecursiveFieldInspector",
        "drf_yasg.inspectors.SerializerMethodFieldInspector",
        "drf_yasg.inspectors.SimpleFieldInspector",
        "drf_yasg.inspectors.StringDefaultFieldInspector",
    ],
    "DEFAULT_GENERATOR_CLASS": "camac.swagger.generators.OptInOpenAPISchemaGenerator",
}

# Schwyz Publication
PUBLICATION_API_URL = build_url(
    env.str("PUBLICATION_API_URL", "https://amtsblatt-test.webtech.ch/api/v1/baugesuch")
)
PUBLICATION_API_USER = env.str("PUBLICATION_API_USER", "")
PUBLICATION_API_PASSWORD = env.str("PUBLICATION_API_PASSWORD", "")

if ENABLE_SILK and not env.bool("TEST_SUITE_RUNNING", False):  # pragma: no cover
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.extend(
        [
            "django.contrib.sessions.middleware.SessionMiddleware",
            "silk.middleware.SilkyMiddleware",
        ]
    )

    SILKY_AUTHENTICATION = False
    SILKY_AUTHORISATION = False
    SILKY_META = True
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True

# Whether to migrate Portal users on first login. See authentication.py for
# detailed description of what the migrations does.
URI_MIGRATE_PORTAL_USER = env.bool("URI_MIGRATE_PORTAL_USER", default=False)

MANABI_ENABLE = env.bool("MANABI_ENABLE", default=default(True, False))

# These are security relevant: provide a default that cannot be abused
MANABI_SHARED_KEY = env.str(
    "MANABI_SHARED_KEY",
    default=default(
        "bNEZsIjvxDAiLhDA1chvF9zL9OJYPNlCqNPlm7KbhmU",
        require_if(MANABI_ENABLE),
    ),
)

MANABI_TOKEN_ACTIVATE_TIMEOUT = env.int("MANABI_TOKEN_ACTIVATE_TIMEOUT", default=600)
MANABI_TOKEN_REFRESH_TIMEOUT = env.int("MANABI_TOKEN_REFRESH_TIMEOUT", default=600)
MANABI_DEBUG = env.bool("MANABI_DEBUG", default=default(True, False))

# GWR
GWR_FERNET_KEY = env.str(
    "GWR_FERNET_KEY", default=default("RvjN3KHR3rZl9knGv3w_HkfapedVQ8F_TihgrFJgbXc=")
)
GWR_HOUSING_STAT_WSK_ID = env.int("GWR_WSK_ID", default=default(0))
GWR_HOUSING_STAT_BASE_URI = env.str(
    "GWR_HOUSING_STAT_BASE_URI",
    default="https://www.housing-stat.ch/regbl/api/ech0216/2",
)


# Until running tasks can be manually canceled we want a timeout
DJANGO_Q_TASK_TIMEOUT_HOURS = env.int("DJANGO_Q_TASK_TIMEOUT_HOURS", default=6)

# We use q-cluster for importing.
# - no retry of failed imports
# - timeout required because we cannot abort running imports (except killing the worker but that seems excessive)
# - ack_failures option keeps a clean queue and allows to identify timed out imports
Q_CLUSTER = {
    "name": "DjangORM",
    "workers": 4,
    "queue_limit": 50,
    "timeout": DJANGO_Q_TASK_TIMEOUT_HOURS * 60 * 60,
    "retry": DJANGO_Q_TASK_TIMEOUT_HOURS * 60 * 60 * 2,
    "ack_failures": True,  # discards failed tasks after timeout
    "orm": "default",
}

DOSSIER_IMPORT_CLIENT_ID = env.str(
    "DJANGO_DOSSIER_IMPORT_CLIENT_ID", default="dossier-import"
)
DOSSIER_IMPORT_CLIENT_SECRET = env.str(
    "DJANGO_DOSSIER_IMPORT_CLIENT_SECRET",
    default="KlYAayhG99lMGIUGKXhm9ha7lUNqQuD4",
)

# Django-Admin OIDC
AUTHENTICATION_BACKENDS = [
    "camac.user.authentication.DjangoAdminOIDCAuthenticationBackend",
]
OIDC_RP_CLIENT_ID = KEYCLOAK_CLIENT
OIDC_RP_CLIENT_SECRET = None
OIDC_DEFAULT_BASE_URL = build_url(
    KEYCLOAK_URL, "/realms/", KEYCLOAK_REALM, "/protocol/openid-connect"
)
OIDC_OP_AUTHORIZATION_ENDPOINT = build_url(OIDC_DEFAULT_BASE_URL, "/auth")
OIDC_OP_TOKEN_ENDPOINT = build_url(OIDC_DEFAULT_BASE_URL, "/token")
OIDC_OP_USER_ENDPOINT = build_url(OIDC_DEFAULT_BASE_URL, "/userinfo")
OIDC_RP_SIGN_ALGO = env.str("DJANGO_OIDC_RP_SIGN_ALGO", default="RS256")
OIDC_OP_JWKS_ENDPOINT = build_url(OIDC_DEFAULT_BASE_URL, "/certs")
OIDC_OP_INTROSPECT_ENDPOINT = build_url(OIDC_DEFAULT_BASE_URL, "/token/introspect")
LOGIN_REDIRECT_URL = build_url(INTERNAL_BASE_URL, "/django/admin/")
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 120
OIDC_EXEMPT_URLS = [re.compile(r"^(?!/django).*")]

OIDC_EMAIL_CLAIM = env.str("DJANGO_OIDC_EMAIL_CLAIM", default="email")
OIDC_FIRSTNAME_CLAIM = env.str("DJANGO_OIDC_FIRSTNAME_CLAIM", default="given_name")
OIDC_LASTNAME_CLAIM = env.str("DJANGO_OIDC_LASTNAME_CLAIM", default="family_name")

OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)

STATICFILES_DIRS += APPLICATIONS[APPLICATION_NAME].get("INCLUDE_STATIC_FILES", [])


def load_module_settings(module_name, application_name=APPLICATION_NAME):
    module = getattr(
        import_module(f"camac.settings.modules.{module_name.lower()}"),
        module_name.upper(),
    )
    app_config = module.get(application_name, {})

    return (
        always_merger.merge(copy.deepcopy(module["default"]), app_config)
        if app_config.get("ENABLED")
        else {}
    )


APPEAL = load_module_settings("appeal")
DISTRIBUTION = load_module_settings("distribution")
PARASHIFT = load_module_settings("parashift")
PUBLICATION = load_module_settings("publication")
DECISION = load_module_settings("decision")
ADDITIONAL_DEMAND = load_module_settings("additional_demand")
DJANGO_ADMIN = load_module_settings("django_admin")
CORRECTION = load_module_settings("correction")
DMS = load_module_settings("dms")
REJECTION = load_module_settings("rejection")
WITHDRAWAL = load_module_settings("withdrawal")
PERMISSIONS = load_module_settings("permissions")
COMMUNICATIONS = load_module_settings("communications")
PLACEHOLDERS = load_module_settings("placeholders")
MASTER_DATA = load_module_settings("master_data")
DUMP = load_module_settings("dump")
CONSTRUCTION_MONITORING = load_module_settings("construction_monitoring")
ECH0211 = load_module_settings("ech0211")

# Alexandria
ALEXANDRIA = load_module_settings("alexandria")
ALEXANDRIA_CREATED_BY_USER_PROPERTY = "alexandria_user"
ALEXANDRIA_CREATED_BY_GROUP_PROPERTY = "alexandria_group"
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = [
    "camac.alexandria.extensions.visibilities.CustomVisibility"
]
GENERIC_PERMISSIONS_PERMISSION_CLASSES = [
    "camac.alexandria.extensions.permissions.CustomPermission"
]
GENERIC_PERMISSIONS_VALIDATION_CLASSES = [
    "camac.alexandria.extensions.validations.CustomValidation"
]


is_s3_storage = DEFAULT_FILE_STORAGE == "storages.backends.s3.S3Storage"

AWS_S3_ACCESS_KEY_ID = env.str(
    "AWS_S3_ACCESS_KEY_ID",
    default=default("minio", require_if(is_s3_storage)),
)
AWS_S3_SECRET_ACCESS_KEY = env.str(
    "AWS_S3_SECRET_ACCESS_KEY",
    default=default("minio123", require_if(is_s3_storage)),
)
AWS_S3_ENDPOINT_URL = env.str(
    "AWS_S3_ENDPOINT_URL",
    default=default("http://ember-ebau.local", require_if(is_s3_storage)),
)
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default="ebau-media")
