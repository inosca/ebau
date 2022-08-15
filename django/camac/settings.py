import json
import logging
import os
import re
from datetime import timedelta
from importlib import import_module

import environ
from deepmerge import always_merger
from django.db.models.expressions import Q
from django.utils.translation import gettext_lazy

from camac.constants import kt_bern as be_constants
from camac.constants.kt_bern import (
    INSTANCE_STATE_DONE,
    INSTANCE_STATE_NEW,
    INSTANCE_STATE_SB1,
)
from camac.utils import build_url

env = environ.Env()
ROOT_DIR = environ.Path(__file__) - 2

ENV_FILE = env.str("DJANGO_ENV_FILE", default=ROOT_DIR(".env"))
if os.path.exists(ENV_FILE):  # pragma: no cover
    environ.Env.read_env(ENV_FILE)

# We need to import the caluma settings after we merge os.environ with our
# local .env file otherwise caluma tries to get it's settings from it's own env
# file (which doesn't exist)

from caluma.settings.caluma import *  # noqa isort:skip

ENV = env.str("APPLICATION_ENV", default="production")
APPLICATION_NAME = env.str("APPLICATION")
APPLICATION_DIR = ROOT_DIR.path(APPLICATION_NAME)
FORM_CONFIG = json.loads(APPLICATION_DIR.file("form.json").read())


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("DJANGO_SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DJANGO_DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=default(["*"]))
API_HOST = env.str("DJANGO_API_HOST", default="http://localhost:80")
ENABLE_SILK = env.bool("DJANGO_ENABLE_SILK", default=False)

DEMO_MODE = env.bool("DEMO_MODE", default=False)

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
    "camac.gisbern.apps.GisbernConfig",
    "sorl.thumbnail",
    "django_clamd",
    "django_q",
    "reversion",
    "rest_framework_xml",
    # TODO: remove this when all production environments ran the migration to
    # delete the tables of this app
    "camac.file.apps.DefaultConfig",
    "adminsortable2",
    "manabi_migrations",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "django.middleware.common.CommonMiddleware",
    "camac.user.middleware.GroupMiddleware",
    "camac.caluma.middleware.CalumaInfoMiddleware",
    "camac.middleware.LoggingMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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

COMMON_FORM_SLUGS_BE = [
    "personalien",
    "allgemeine-angaben-kurz",
    "parzelle-tabelle",
    "personalien-tabelle",
    "projektverfasserin",
    "grundeigentumerin",
    "gebaudeeigentumerin",
    "vertreterin-mit-vollmacht",
]

DISTRIBUTION_REGEX = r"(inquir(y|ies)|distribution)"

DISTRIBUTION_DUMP_CONFIG = {
    "caluma_distribution": {
        "caluma_form.Form": Q(pk__iregex=DISTRIBUTION_REGEX),
        "caluma_form.FormQuestion": Q(form__pk__iregex=DISTRIBUTION_REGEX),
        "caluma_form.Question": Q(forms__pk__iregex=DISTRIBUTION_REGEX),
        "caluma_form.QuestionOption": Q(question__forms__pk__iregex=DISTRIBUTION_REGEX),
        "caluma_form.Option": Q(questions__forms__pk__iregex=DISTRIBUTION_REGEX),
        "caluma_workflow.Workflow": Q(pk__iregex=DISTRIBUTION_REGEX),
        "caluma_workflow.Task": Q(pk__iregex=DISTRIBUTION_REGEX),
        "caluma_workflow.TaskFlow": Q(workflow__pk__iregex=DISTRIBUTION_REGEX),
        "caluma_workflow.Flow": Q(task_flows__workflow__pk__iregex=DISTRIBUTION_REGEX),
    },
}

# Application specific settings
# an application is defined by the customer e.g. uri, schwyz, etc.
APPLICATIONS = {
    "demo": {
        "ECH0211": {
            "API_ACTIVE": False,
        },
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
        },
        "ROLE_INHERITANCE": {"trusted_service": "service"},
        "IS_MULTILINGUAL": False,
        "NOTIFICATIONS": {"SUBMIT": None, "APPLICANT": {"NEW": None, "EXISTING": None}},
        "PUBLICATION_BACKEND": "camac-ng",
        "FORM_BACKEND": "camac-ng",
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
            "FORM_PERMISSIONS": ["main", "inquiry", "inquiry-answer"],
            "HAS_PROJECT_CHANGE": False,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
        },
        "STORE_PDF": {"SECTION": 1},
        "INSTANCE_STATE_REJECTION_COMPLETE": "finished",
        "SET_SUBMIT_DATE_CAMAC_ANSWER": True,
        "REJECTION_FEEDBACK_QUESTION": {
            "CHAPTER": 20001,
            "QUESTION": 20037,
            "ITEM": 1,
        },
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {
            "REQUIRED_KEYS": [
                "external-id",
                "parzelle-nr",
                "erfassungsjahr",
                "vorhaben",
                "ort",
                "baurecht-nr",
                "gemeinde",
                "gesuchsteller",
                "documents",
            ],
            "USER": "import@koor-bg.ur.ch",
        },
        "CUSTOM_NOTIFICATION_TYPES": [
            # BE
            "inactive_municipality",
            # UR
            "submitter_list",
            "municipality_users",
            "unnotified_service_users",
            "lisag",
            "koor_np_users",
            "koor_bg_users",
            "koor_bd_users",
            "koor_sd_users",
            "responsible_koor",
        ],
    },
    "kt_schwyz": {
        "INCLUDE_STATIC_FILES": [("xml", "kt_schwyz/static/ech0211/xml/")],
        "LOG_NOTIFICATIONS": True,
        "ROLE_PERMISSIONS": {
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
        "ECH0211": {
            "API_ACTIVE": True,
            "API_LEVEL": "basic",
            "URLS_CLASS": "camac.ech0211.urls.SZUrlsConf",
        },
        "PUBLIC_ROLES": ["Publikation", "Portal"],
        "PORTAL_GROUP": 4,
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
        "PUBLICATION_DURATION": timedelta(days=20),
        "PUBLICATION_BACKEND": "camac-ng",
        "PUBLICATION_ATTACHMENT_SECTION": [4],
        "ATTACHMENT_INTERNAL_STATES": ["internal"],
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
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": [],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "CALUMA": {
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
                    "cancel": [
                        "reopen-circulation",
                    ],
                },
                "check-inquiry": {"cancel": ["revise-inquiry"]},
                "revise-inquiry": {"cancel": ["check-inquiry"]},
                "distribution": {"cancel": ["additional-demand"]},
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
                    ],
                    "complete": [
                        "building-authority",
                    ],
                },
                "finish-document": {"cancel": ["create-manual-workitems"]},
            },
            "FILL_PUBLICATION_TASK": None,
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
                    "history_text": "Zirkulationsentscheid gestartet",
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
        "DUMP_CONFIG_EXCLUDED_MODELS": [
            "document.Template",
            "user.Group",
            "user.GroupT",
            "user.GroupLocation",
            "user.Service",
            "user.ServiceT",
            "notification.NotificationTemplate",
            "notification.NotificationTemplateT",
        ],
        "INTERCHANGEABLE_FORMS": [
            "vorentscheid-gemass-ss84-pbg-v2",
            "vorentscheid-gemass-ss84-pbg-v3",
            "vorentscheid-gemass-ss84-pbg-v4",
            "vorentscheid-gemass-ss84-pbg-v5",
            "vorentscheid-gemass-ss84-pbg-v6",
            "vorentscheid-gemass-ss84-pbg-v7",
            "baugesuch-reklamegesuch-v2",
            "baugesuch-reklamegesuch-v3",
            "baugesuch-reklamegesuch-v4",
            "baugesuch-reklamegesuch-v5",
            "baugesuch-reklamegesuch-v6",
            "baugesuch-reklamegesuch-v7",
            "projektanderung-v2",
            "projektanderung-v3",
            "projektanderung-v4",
            "projektanderung-v5",
            "projektanderung-v6",
            "projektanderung-v7",
            "projektanderung-v8",
            "technische-bewilligung",
            "technische-bewilligung-v2",
            "technische-bewilligung-v3",
            "baumeldung-fur-geringfugiges-vorhaben-v2",
            "baumeldung-fur-geringfugiges-vorhaben-v3",
            "baumeldung-fur-geringfugiges-vorhaben-v4",
            "baumeldung-fur-geringfugiges-vorhaben-v5",
            "anlassbewilligungen-verkehrsbewilligungen-v2",
            "anlassbewilligungen-verkehrsbewilligungen-v3",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v2",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v3",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v4",
        ],
        "STORE_PDF": {"SECTION": 1},
        "DUMP_CONFIG_GROUPS": {
            "email_notifications": {
                "notification.NotificationTemplate": Q(type="email"),
                "notification.NotificationTemplateT": Q(template__type="email"),
            },
            "buildingauthority": {
                "caluma_form.Form": Q(pk="realisierung-tabelle"),
                "caluma_form.FormQuestion": Q(form__pk="realisierung-tabelle"),
                "caluma_form.Question": Q(pk__startswith="baukontrolle-realisierung")
                | Q(pk="bewilligungsverfahren-gr-sitzung-bewilligungsdatum"),
                "caluma_form.QuestionOption": Q(
                    question__pk__startswith="baukontrolle-realisierung"
                ),
                "caluma_form.Option": Q(
                    questions__pk__startswith="baukontrolle-realisierung"
                ),
            },
            # Distribution
            **DISTRIBUTION_DUMP_CONFIG,
        },
        "REJECTION_FEEDBACK_QUESTION": {},
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
            "TRANSFORM_COORDINATE_SYSTEM": "epsg:4326",  # use world wide coordinates instead of swiss ones
            "PROD_URL": env.str(  # this is also used in the xml delivery of the ech0211 endpoint
                "DJANGO_DOSSIER_IMPORT_PROD_URL", "https://behoerden.ebau-sz.ch/"
            ),
            "PROD_AUTH_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
                "https://ebau-sz.ch/auth/realms/ebau/protocol/openid-connect/token",
            ),
            "PROD_SUPPORT_GROUP_ID": 486,
        },
        "MASTER_DATA": {
            "canton": ("static", "SZ"),
            "organization_category": (
                "static",
                "ebausz",
            ),  # TODO: change this value 'decisionRulingType'
            "applicants": (
                "ng_table",
                [
                    "bauherrschaft",
                    "bauherrschaft-v2",
                    "bauherrschaft-v3",
                    "bauherrschaft-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "building_owners": (
                "ng_table",
                [
                    "bauherrschaft",
                    "bauherrschaft-v2",
                    "bauherrschaft-v3",
                    "bauherrschaft-override",
                ],  # TODO: hauseigentümerschaft in SZ?
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "legal_representatives": (
                "ng_table",
                "vertreter-mit-vollmacht",
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "landowners": (
                "ng_table",
                [
                    "grundeigentumerschaft",
                    "grundeigentumerschaft-v2",
                    "grundeigentumerschaft-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "project_authors": (
                "ng_table",
                [
                    "projektverfasser-planer",
                    "projektverfasser-planer-v2",
                    "projektverfasser-planer-v3",
                    "projektverfasser-planer-override",
                ],
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                        "country": ("static", "Schweiz"),
                        "is_juristic_person": (
                            "anrede",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Herr": False,
                                            "Frau": False,
                                            "Firma": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "firma",
                        "company": "firma",
                        "email": "email",
                        "phone": "tel",
                    }
                },
            ),
            "street": ("ng_answer", "ortsbezeichnung-des-vorhabens"),
            "city": ("ng_answer", "standort-ort"),
            "submit_date": ("first_workflow_entry", [10]),
            "publication_date": ("first_workflow_entry", [15]),
            "decision_date": (
                "answer",
                "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",
                {
                    "document_from_work_item": "building-authority",
                    "value_key": "date",
                },
            ),
            "construction_start_date": (
                "table",
                "baukontrolle-realisierung-table",
                {
                    "document_from_work_item": "building-authority",
                    "column_mapping": {
                        "value": (
                            "baukontrolle-realisierung-baubeginn",
                            {"value_key": "date"},
                        )
                    },
                },
            ),
            "profile_approval_date": (
                "table",
                "baukontrolle-realisierung-table",
                {
                    "document_from_work_item": "building-authority",
                    "column_mapping": {
                        "value": (
                            "baukontrolle-realisierung-schnurgeruestabnahme",
                            {"value_key": "date"},
                        )
                    },
                },
            ),
            "final_approval_date": (
                "table",
                "baukontrolle-realisierung-table",
                {
                    "document_from_work_item": "building-authority",
                    "column_mapping": {
                        "value": (
                            "baukontrolle-realisierung-schlussabnahme",
                            {"value_key": "date"},
                        )
                    },
                },
            ),
            "completion_date": (
                "table",
                "baukontrolle-realisierung-table",
                {
                    "document_from_work_item": "building-authority",
                    "column_mapping": {
                        "value": (
                            "baukontrolle-realisierung-bauende",
                            {"value_key": "date"},
                        )
                    },
                },
            ),
            "dossier_number": (
                "instance_property",
                "identifier",
            ),  # eCH0211: 3.1.1.1.1, 3.1.1.1.2
            "municipality": ("instance_property", "location"),
            "proposal": (
                "ng_answer",
                ["bezeichnung", "bezeichnung-override"],
            ),  # eCH0211: 3.1.1.2
            "remark": (
                "ng_answer",
                "vollstaendigkeitspruefung-bemerkung",
            ),  # eCH0211: 3.1.1.4
            "construction_costs": ("ng_answer", "baukosten"),  # eCH0211: 3.1.1.11
            "usage_zone": (
                "ng_answer",
                "betroffene-nutzungszonen",
            ),  # eCH0211: 3.8.1.3 TODO: verify!
            "usage_type": ("ng_answer", "art-der-nutzung"),  # TODO: verify!
            "application_type": (
                "instance_property",
                "form.description",
            ),  # `proceeding_type` in context of eCH standard
            #  SZ stores this as `instance.form.name`  # TODO: verify!
            "application_type_migrated": (  # not the same as regular application_type that requires predefined choices
                "ng_answer",
                "verfahrensart-migriertes-dossier",
            ),
            "proceeding_type": (  # TODO: verify!
                ("ng_answer", "verfahrensart")
            ),  # this is called "Verfahrensart" in context of eCH
            "coordinates": (
                "ng_table",
                "punkte",
                {"column_mapping": {"lat": "lat", "lng": "lng"}},
            ),
            "plot_data": (
                "ng_table",
                "parzellen",
                {
                    "column_mapping": {
                        "plot_number": "number",
                        "egrid_number": "egrid",
                    }
                },
            ),
            "buildings": (
                "ng_table",
                ["gwr", "gwr-v2"],
                {
                    "column_mapping": {
                        "name": "gebaeudebezeichnung",
                        "building_category": (
                            "kategorie",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Andere Wohngebäude (Wohngebäude mit Nebennutzung)": 1030,
                                            "Gebäude mit ausschliesslicher Wohnnutzung": 1020,
                                            "Gebäude ohne Wohnnutzung": 1060,
                                            "Provisorische Unterkunft": 1010,
                                            "Sonderbau": 1080,
                                            "Gebäude mit teilweiser Wohnnutzung": 1040,
                                        }
                                    },
                                )
                            },
                        ),
                        "civil_defense_shelter": (
                            "zivilschutzraum",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Ja": True,
                                            "Nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "heating_heat_generator": (
                            "heizungsart",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Einzelofenheizung": 7436,
                                            "Etagenheizung": 7499,
                                            "Zentralheizung für das Gebäude": 7450,
                                            "Zentralheizung für mehrere Gebäude": 7451,
                                            "Öffentliche Fernwärmeversorgung": 7461,
                                            "Keine Heizung": 7400,
                                            "Kein Wärmeerzeuger": 7400,
                                            "Wärmepumpe für ein Gebäude": 7410,
                                            "Wärmepumpe für mehrere Gebäude": 7411,
                                            "Thermische Solaranlage für ein Gebäude": 7420,
                                            "Thermische Solaranlage für mehrere Gebäude": 7421,
                                            "Heizkessel (generisch) für ein Gebäude": 7430,
                                            "Heizkessel (generisch) für mehrere Gebäude": 7431,
                                            "Heizkessel nicht kondensierend für ein Gebäude": 7431,
                                            "Heizkessel nicht kondensierend für mehrere Gebäude": 7432,
                                            "Heizkessel kondensierend für ein Gebäude": 7434,
                                            "Heizkessel kondensierend für mehrere Gebäude": 7435,
                                            "Ofen": 7436,
                                            "Wärmekraftkopplungsanlage für ein Gebäude": 7440,
                                            "Wärmekraftkopplungsanlage für mehrere Gebäude": 7441,
                                            "Elektrospeicher-Zentralheizung für ein Gebäude": 7450,
                                            "Elektrospeicher-Zentralheizung für mehrere Gebäude": 7451,
                                            "Elektro direkt": 7452,
                                            "Wärmetauscher (einschliesslich für Fernwärme) für ein Gebäude": 7460,
                                            "Wärmetauscher (einschliesslich für Fernwärme) für mehrere Gebäude": 7461,
                                            "Andere": 7499,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "heating_energy_source": (
                            "energietrager-heizung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Heizöl": 7530,
                                            "Holz": 7540,
                                            "Altholz": 7541,
                                            "Wärmepumpe": 7599,
                                            "Elektrizität": 7560,
                                            "Gas": 7520,
                                            "Fernwärme (Heisswasser oder Dampf)": 7581,
                                            "Kohle": 7599,
                                            "Sonnenkollektor": 7570,
                                            "Keine": 7500,
                                            "Luft": 7501,
                                            "Erdwärme (generisch)": 7510,
                                            "Erdwärmesonde": 7511,
                                            "Erdregister": 7512,
                                            "Wasser (Grundwasser, Oberflächenwasser, Abwasser)": 7513,
                                            "Holz (generisch)": 7540,
                                            "Holz (Stückholz)": 7541,
                                            "Holz (Pellets)": 7542,
                                            "Abwärme (innerhalb des Gebäudes)": 7550,
                                            "Sonne (thermisch)": 7570,
                                            "Fernwärme (generisch)": 7580,
                                            "Fernwärme (Hochtemperatur)": 7581,
                                            "Fernwärme (Niedertemperatur)": 7582,
                                            "Unbestimmt": 7598,
                                            "Andere": 7599,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_heat_generator": (
                            "waermeerzeuger-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Kein Wärmeerzeuger": 7600,
                                            "Wärmepumpe": 7610,
                                            "Thermische Solaranlage": 7620,
                                            "Heizkessel (generisch)": 7630,
                                            "Heizkessel nicht kondensierend": 7632,
                                            "Heizkessel kondensierend": 7634,
                                            "Wärmekraftkopplungsanlage": 7640,
                                            "Zentraler Elektroboiler": 7650,
                                            "Kleinboiler": 7651,
                                            "Wärmetauscher (einschliesslich für Fernwärme)": 7660,
                                            "Andere": 7699,
                                        }
                                    },
                                )
                            },
                        ),
                        "warmwater_energy_source": (
                            "energietrager-warmwasser",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "Heizöl": 7530,
                                            "Holz": 7540,
                                            "Altholz": 7541,
                                            "Wärmepumpe": 7599,
                                            "Elektrizität": 7560,
                                            "Gas": 7520,
                                            "Fernwärme (Heisswasser oder Dampf)": 7581,
                                            "Kohle": 7599,
                                            "Sonnenkollektor": 7570,
                                            "Keine": 7500,
                                            "Luft": 7501,
                                            "Erdwärme (generisch)": 7510,
                                            "Erdwärmesonde": 7511,
                                            "Erdregister": 7512,
                                            "Wasser (Grundwasser, Oberflächenwasser, Abwasser)": 7513,
                                            "Holz (generisch)": 7540,
                                            "Holz (Stückholz)": 7541,
                                            "Holz (Pellets)": 7542,
                                            "Abwärme (innerhalb des Gebäudes)": 7550,
                                            "Sonne (thermisch)": 7570,
                                            "Fernwärme (generisch)": 7580,
                                            "Fernwärme (Hochtemperatur)": 7581,
                                            "Fernwärme (Niedertemperatur)": 7582,
                                            "Unbestimmt": 7598,
                                            "Andere": 7599,
                                            "Noch nicht festgelegt": None,
                                        }
                                    },
                                )
                            },
                        ),
                        "number_of_floors": "geschosse",
                        "number_of_rooms": "wohnraeume",
                        "dwellings": (
                            "wohnungen",
                            {
                                "value_parser": (
                                    "list_mapping",
                                    {
                                        "mapping": {
                                            "location_on_floor": "lage",
                                            "number_of_rooms": "zimmer",
                                            "kitchen_facilities": "kuchenart",
                                            "has_kitchen_facilities": (
                                                ["kuchenart", "kocheinrichtung"],
                                                {
                                                    "value_parser": (
                                                        "value_mapping",
                                                        {
                                                            "mapping": {
                                                                "Ja": True,
                                                                "Nein": False,
                                                                "Küche (min. 4m²)": True,
                                                                "Kochnische (unter 4m²)": True,
                                                                "Weder Küche noch Kochnische": False,
                                                            }
                                                        },
                                                    )
                                                },
                                            ),
                                            "area": "flache",
                                            "multiple_floors": (
                                                "maisonette",
                                                {
                                                    "value_parser": (
                                                        "value_mapping",
                                                        {
                                                            "mapping": {
                                                                "Ja": True,
                                                                "Nein": False,
                                                            }
                                                        },
                                                    )
                                                },
                                            ),
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
        },
    },
    "kt_bern": {
        "ECH0211": {
            "API_ACTIVE": True,
            "API_LEVEL": "full",
            "SWAGGER_PATH": "camac.swagger.views.kt_bern",
            "URLS_CLASS": "camac.ech0211.urls.BEUrlsConf",
        },
        "INCLUDE_STATIC_FILES": [("xml", "kt_bern/static/ech0211/xml")],
        "LOG_NOTIFICATIONS": True,
        "SYSTEM_USER": "service-account-camac-admin",
        "ROLE_PERMISSIONS": {
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
        },
        "INSTANCE_PERMISSIONS": {"MUNICIPALITY_WRITE": ["correction"]},
        "CUSTOM_NOTIFICATION_TYPES": [
            "inactive_municipality",
        ],
        "CIRCULATION_STATE_END": "DONE",
        "CIRCULATION_ANSWER_UNINVOLVED": "not_concerned",
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
            ],
            "FINALIZE": [
                {
                    "template_slug": "13-meldung-termine-pflichtkontrollen-baukontrolle",
                    "recipient_types": [
                        "construction_control",
                        "involved_in_distribution",
                    ],
                }
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
                    "recipient_types": ["leitbehoerde", "involved_in_distribution"],
                },
            ],
            "DECISION_PRELIMINARY_CLARIFICATION": [
                {
                    "template_slug": "08-stellungnahme-zu-voranfrage-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "08-stellungnahme-zu-voranfrage-behoerden",
                    "recipient_types": ["leitbehoerde", "involved_in_distribution"],
                },
            ],
            "COMPLETE_MANUAL_WORK_ITEM": [
                {
                    "template_slug": "complete-manual-work-item",
                    "recipient_types": ["work_item_controlling"],
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
            ],
            "SUBMIT_TASKS": ["submit"],
            "REPORT_TASK": "sb1",
            "FINALIZE_TASK": "sb2",
            "AUDIT_TASK": "audit",
            "DECISION_TASK": "decision",
            "EBAU_NUMBER_TASK": "ebau-number",
            "SIMPLE_WORKFLOW": {
                "init-distribution": {
                    "next_instance_state": "circulation",
                    "ech_event": "camac.ech0211.signals.circulation_started",
                    "history_text": gettext_lazy("Circulation started"),
                    "notification": {
                        "template_slug": "03-verfahrensablauf-gesuchsteller",
                        "recipient_types": ["applicant"],
                    },
                },
                "complete-distribution": {
                    "next_instance_state": "coordination",
                    "ech_event": "camac.ech0211.signals.circulation_ended",
                    "history_text": gettext_lazy("Circulation completed"),
                    "notification": {
                        "template_slug": "03-verfahren-vorzeitig-beendet",
                        "recipient_types": ["unanswered_inquiries"],
                    },
                },
                # "reopen-circulation": {
                #     "next_instance_state": "circulation",
                #     "ech_event": "camac.ech0211.signals.circulation_started",
                #     "history_text": gettext_lazy("Circulation reopened"),
                # },
                "complete": {
                    "next_instance_state": "finished",
                    "ech_event": "camac.ech0211.signals.finished",
                    "history_text": gettext_lazy("Procedure completed"),
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
                "baugesuch-generell",
                "baugesuch-generell-v2",
                "baugesuch-mit-uvp",
                "baugesuch-mit-uvp-v2",
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
                    "skip": ["audit", "publication", "fill-publication"],
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
                    ],
                },
            },
            "FILL_PUBLICATION_TASK": "fill-publication",
            "INFORMATION_OF_NEIGHBORS_TASK": "information-of-neighbors",
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "AUDIT_FORMS": [
                "dossierpruefung",
                "fp-form",
                "bab-form",
                "bab-beilagen",
                "mp-form",
                "mp-abschluss",
                "mp-ausnahmen",
                "mp-bauabstaende",
                "mp-eigene-pruefgegenstaende",
                "mp-erschliessung",
                "mp-form",
                "mp-gesundheit",
                "mp-nutzungsvorschriften",
                "mp-ortsbild-und-landschaftsschutz",
                "mp-schutzinventare",
                "mp-sicherheit",
                "mp-umweltschutz",
                "mp-weitere-gegenstaende",
                "mp-weitere-vorschriften",
            ],
            "EXTEND_VALIDITY_FORM": "verlaengerung-geltungsdauer",
            "EXTEND_VALIDITY_COPY_QUESTIONS": [
                "weitere-personen",
                "strasse-flurname",
                "nr",
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
            "PUBLICATION_FORM": "publikation",
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
        "ATTACHMENT_RUNNING_ACTIVATION_STATES": ["RUN"],
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
        "DOCUMENT_MERGE_SERVICE": {
            "FORM": {
                "_base": {
                    "people_sources": [
                        # bulding permit
                        "personalien-gesuchstellerin",
                        "personalien-vertreterin-mit-vollmacht",
                        "personalien-grundeigentumerin",
                        "personalien-gebaudeeigentumerin",
                        "personalien-projektverfasserin",
                        "personalien-sb",
                        # sb1 & sb2
                        "personalien-sb1-sb2",
                    ],
                    "people_names": {
                        "name-gesuchstellerin": "familyName",
                        "vorname-gesuchstellerin": "givenName",
                        "name-juristische-person-gesuchstellerin": "juristicName",
                        "name-vertreterin": "familyName",
                        "vorname-vertreterin": "givenName",
                        "name-juristische-person-vertreterin": "juristicName",
                        "name-grundeigentuemerin": "familyName",
                        "vorname-grundeigentuemerin": "givenName",
                        "name-juristische-person-grundeigentuemerin": "juristicName",
                        "name-gebaeudeeigentuemerin": "familyName",
                        "vorname-gebaeudeeigentuemerin": "givenName",
                        "name-juristische-person-gebaeudeeigentuemerin": "juristicName",
                        "name-projektverfasserin": "familyName",
                        "vorname-projektverfasserin": "givenName",
                        "name-juristische-person-projektverfasserin": "juristicName",
                    },
                },
                "baugesuch": {
                    "forms": [
                        "baugesuch",
                        "baugesuch-v2",
                        "baugesuch-mit-uvp",
                        "baugesuch-mit-uvp-v2",
                        "baugesuch-generell",
                        "baugesuch-generell-v2",
                        "hecken-feldgehoelze-baeume",
                        "baupolizeiliches-verfahren",
                        "zutrittsermaechtigung",
                        "klaerung-baubewilligungspflicht",
                        "verlaengerung-geltungsdauer",
                    ],
                    "template": "form",
                    "personalien": "personalien",
                    "exclude_slugs": [
                        "is-paper",
                        "projektaenderung",
                        "einreichen-button",
                        "karte",
                        "dokumente-platzhalter",
                    ],
                },
                "vorabklaerung": {
                    "forms": [
                        "vorabklaerung-einfach",
                        "vorabklaerung-vollstaendig",
                        "vorabklaerung-vollstaendig-v2",
                        "solaranlagen-meldung",
                    ],
                    "template": "form",
                    "personalien": "personalien",
                    "exclude_slugs": [
                        "is-paper",
                        "projektaenderung",
                        "einreichen-button",
                        "karte",
                        "dokumente-platzhalter",
                    ],
                },
                "selbstdeklaration": {
                    "forms": ["sb1", "sb2"],
                    "template": "form",
                    "personalien": "selbstdeklaration-sb1",
                    "exclude_slugs": [
                        "is-paper",
                        "einreichen-button-sb1",
                        "einreichen-button-sb2",
                        "dokumente-sb1",
                        "dokumente-sb2",
                        "dokumente-platzhalter",
                    ],
                },
                "regular-exams": {
                    "forms": ["fp-form", "bab-form"],
                    "template": "audit-form",
                    "exclude_slugs": [
                        "bab-01-07-1972-um-und-ausgebaut-meldung",
                        "bab-naehe-von-schutzenswerten-gebaeuden-meldung",
                    ],
                },
                "material-exam": {
                    "forms": ["mp-form"],
                    "template": "form",
                },
            },
            "ADD_HEADER_DATA": True,
        },
        "GROUP_RENAME_ON_SERVICE_RENAME": True,
        "SERVICE_UPDATE_ALLOWED_ROLES": [
            "municipality-admin",
            "service-admin",
            "construction-control-admin",
        ],
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": ["core", "responsible", "document"],
        "HAS_EBAU_NUMBER": True,
        "HAS_GESUCHSNUMMER": False,
        "INSTANCE_STATE_REJECTION_COMPLETE": "finished",
        "SET_SUBMIT_DATE_CAMAC_ANSWER": True,
        "REJECTION_FEEDBACK_QUESTION": {
            "CHAPTER": 20001,
            "QUESTION": 20037,
            "ITEM": 1,
        },
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "DUMP_CONFIG_GROUPS": {
            "email_notifications": {
                "notification.NotificationTemplate": Q(type="email"),
                "notification.NotificationTemplateT": Q(template__type="email"),
            },
            # required by several form-questions
            "caluma_form_common": {
                "caluma_form.Form": Q(pk__in=COMMON_FORM_SLUGS_BE),
                "caluma_form.FormQuestion": Q(form__pk__in=COMMON_FORM_SLUGS_BE),
                "caluma_form.Question": Q(forms__pk__in=COMMON_FORM_SLUGS_BE),
                "caluma_form.QuestionOption": Q(
                    question__forms__pk__in=COMMON_FORM_SLUGS_BE
                ),
                "caluma_form.Option": Q(questions__forms__pk__in=COMMON_FORM_SLUGS_BE),
            },
            "caluma_dossier_import_form": {
                "caluma_form.Form": Q(pk="migriertes-dossier")
                | Q(pk="migriertes-dossier-daten"),
                "caluma_form.FormQuestion": Q(form__pk="migriertes-dossier")
                | Q(form__pk="migriertes-dossier-daten"),
                "caluma_form.Question": Q(forms__pk="migriertes-dossier")
                | Q(forms__pk="migriertes-dossier-daten"),
                "caluma_form.QuestionOption": Q(
                    question__forms__pk="migriertes-dossier"
                )
                | Q(question__forms__pk="migriertes-dossier-daten"),
                "caluma_form.Option": Q(questions__forms__pk="migriertes-dossier")
                | Q(questions__forms__pk="migriertes-dossier-daten"),
            },
            "caluma_form_v2": {
                "caluma_form.Form": Q(pk__endswith="-v2"),
                "caluma_form.FormQuestion": Q(form__pk__endswith="-v2"),
                "caluma_form.Question": Q(pk__endswith="-v2"),
                "caluma_form.QuestionOption": Q(question__pk__endswith="-v2"),
                "caluma_form.Option": Q(questions__pk__endswith="-v2"),
                "caluma_form.Answer": Q(
                    question__forms__pk__endswith="-v2",
                    document__isnull=True,
                ),
            },
            "caluma_form_sb2": {
                "caluma_form.Form": Q(pk="sb2"),
                "caluma_form.FormQuestion": Q(form__pk="sb2"),
                "caluma_form.Question": Q(forms__pk="sb2"),
                "caluma_form.QuestionOption": Q(question__forms__pk="sb2"),
                "caluma_form.Option": Q(questions__forms__pk="sb2"),
            },
            "caluma_information_of_neighbors_form": {
                "caluma_form.Form": Q(pk="information-of-neighbors"),
                "caluma_form.FormQuestion": Q(form__pk="information-of-neighbors"),
                "caluma_form.Question": Q(forms__pk="information-of-neighbors"),
                "caluma_form.QuestionOption": Q(
                    question__forms__pk="information-of-neighbors"
                ),
                "caluma_form.Option": Q(
                    questions__forms__pk="information-of-neighbors"
                ),
            },
            "caluma_ebau_number_form": {
                "caluma_form.Form": Q(pk="ebau-number"),
                "caluma_form.FormQuestion": Q(form__pk="ebau-number"),
                "caluma_form.Question": Q(forms__pk="ebau-number"),
                "caluma_form.QuestionOption": Q(question__forms__pk="ebau-number"),
                "caluma_form.Option": Q(questions__forms__pk="ebau-number"),
            },
            "caluma_solar_plants_form": {
                "caluma_form.Form": Q(pk__startswith="solaranlagen"),
                "caluma_form.FormQuestion": Q(form__pk__startswith="solaranlagen"),
                "caluma_form.Question": Q(forms__pk__startswith="solaranlagen")
                & ~Q(pk__in=["8-freigabequittung", "dokumente-platzhalter"]),
                "caluma_form.QuestionOption": Q(
                    question__forms__pk__startswith="solaranlagen"
                ),
                "caluma_form.Option": Q(
                    questions__forms__pk__startswith="solaranlagen"
                ),
            },
            "caluma_decision_form": {
                "caluma_form.Form": Q(pk="decision"),
                "caluma_form.FormQuestion": Q(form__pk="decision"),
                "caluma_form.Question": Q(forms__pk="decision"),
                "caluma_form.QuestionOption": Q(question__forms__pk="decision"),
                "caluma_form.Option": Q(questions__forms__pk="decision"),
            },
            # Distribution
            **DISTRIBUTION_DUMP_CONFIG,
        },
        "DUMP_CONFIG_EXCLUDED_MODELS": [
            "user.Group",
            "user.GroupT",
            "user.GroupLocation",
            "user.Service",
            "user.ServiceT",
            "notification.NotificationTemplate",
            "notification.NotificationTemplateT",
        ],
        "DOSSIER_IMPORT": {
            "WRITER_CLASS": "camac.dossier_import.config.kt_bern.KtBernDossierWriter",
            "INSTANCE_STATE_MAPPING": {
                "SUBMITTED": INSTANCE_STATE_NEW,
                "APPROVED": INSTANCE_STATE_SB1,
                "DONE": INSTANCE_STATE_DONE,
            },
            "USER": "service-account-camac-admin",
            "WORKFLOW_MAPPING": {
                "BUILDINGPERMIT": "building-permit",
                "PRELIMINARY": "preliminary-clarification",
            },
            "CALUMA_FORM": "migriertes-dossier",
            "FORM_ID": 1,
            "ATTACHMENT_SECTION_ID": 4,  # Internal
            "PROD_URL": env.str(  # this is also used in the xml delivery of the ech0211 endpoint
                "DJANGO_DOSSIER_IMPORT_PROD_URL",
                "https://ebau.apps.be.ch/",
            ),
            "PROD_AUTH_URL": env.str(
                "DJANGO_DOSSIER_IMPORT_PROD_AUTH_URL",
                "https://sso.be.ch/auth/realms/ebau/protocol/openid-connect/token",
            ),
            "PROD_SUPPORT_GROUP_ID": 10000,
        },
        "MASTER_DATA": {
            "canton": ("static", "BE"),
            "organisation_category": ("static", "ebaube"),
            "remark": ("answer", "bemerkungen"),
            "nature_risk_type": (
                "table",
                "beschreibung-der-prozessart-tabelle",
                {"column_mapping": {"risk_type": "prozessart"}},
            ),
            "applicants": (
                "table",
                "personalien-gesuchstellerin",
                {
                    "column_mapping": {
                        "last_name": "name-gesuchstellerin",
                        "first_name": "vorname-gesuchstellerin",
                        "street": "strasse-gesuchstellerin",
                        "street_number": "nummer-gesuchstellerin",
                        "zip": "plz-gesuchstellerin",
                        "town": "ort-gesuchstellerin",
                        "is_juristic_person": (
                            "juristische-person-gesuchstellerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gesuchstellerin-ja": True,
                                            "juristische-person-gesuchstellerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gesuchstellerin",
                    }
                },
            ),
            "building_owners": (
                "table",
                "personalien-gebaudeeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-gebaeudeeigentuemerin",
                        "first_name": "vorname-gebaeudeeigentuemerin",
                        "street": "strasse-gebaeudeeigentuemerin",
                        "street_number": "nummer-gebaeudeeigentuemerin",
                        "zip": "plz-gebaeudeeigentuemerin",
                        "town": "ort-gebaeudeeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-gebaeudeeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-gebaeudeeigentuemer-ja": True,
                                            "juristische-person-gebaeudeeigentuemer-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-gebaeudeeigentuemerin",
                    }
                },
            ),
            "landowners": (
                "table",
                "personalien-grundeigentumerin",
                {
                    "column_mapping": {
                        "last_name": "name-grundeigentuemerin",
                        "first_name": "vorname-grundeigentuemerin",
                        "street": "strasse-grundeigentuemerin",
                        "street_number": "nummer-grundeigentuemerin",
                        "zip": "plz-grundeigentuemerin",
                        "town": "ort-grundeigentuemerin",
                        "is_juristic_person": (
                            "juristische-person-grundeigentuemerin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-grundeigentuemerin-ja": True,
                                            "juristische-person-grundeigentuemerin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-grundeigentuemerin",
                    }
                },
            ),
            "project_authors": (
                "table",
                "personalien-projektverfasserin",
                {
                    "column_mapping": {
                        "last_name": "name-projektverfasserin",
                        "first_name": "vorname-projektverfasserin",
                        "street": "strasse-projektverfasserin",
                        "street_number": "nummer-projektverfasserin",
                        "zip": "plz-projektverfasserin",
                        "town": "ort-projektverfasserin",
                        "is_juristic_person": (
                            "juristische-person-projektverfasserin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-projektverfasserin-ja": True,
                                            "juristische-person-projektverfasserin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-projektverfasserin",
                    }
                },
            ),
            "legal_representatives": (
                "table",
                "personalien-vertreterin-mit-vollmacht",
                {
                    "column_mapping": {
                        "last_name": "name-vertreterin",
                        "first_name": "vorname-vertreterin",
                        "street": "strasse-vertreterin",
                        "street_number": "nummer-vertreterin",
                        "zip": "plz-vertreterin",
                        "town": "ort-vertreterin",
                        "is_juristic_person": (
                            "juristische-person-vertreterin",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "juristische-person-vertreterin-ja": True,
                                            "juristische-person-vertreterin-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "name-juristische-person-vertreterin",
                    }
                },
            ),
            "dossier_number": ("case_meta", "ebau-number"),
            "project": ("answer", "baubeschrieb", {"value_parser": "option"}),
            "water_protection_area": (
                "answer",
                ["gewaesserschutzbereich", "gewaesserschutzbereich-v2"],
                {"value_parser": "option"},
            ),
            "protection_area": (
                "answer",
                ["grundwasserschutzzonen", "grundwasserschutzzonen-v2"],
                {"value_parser": "option"},
            ),
            "public": ("answer", "oeffentlichkeit", {"value_parser": "option"}),
            "alcohol_serving": (
                "answer",
                "alkoholausschank",
                {
                    "value_parser": (
                        "value_mapping",
                        {
                            "mapping": {
                                "alkoholausschank-ja": "mit",
                                "alkoholausschank-nein": "ohne",
                            }
                        },
                    )
                },
            ),
            "interior_seating": (
                "table",
                "ausschankraeume",
                {"column_mapping": {"total_seats": "sitzplaetze"}},
            ),
            "outside_seating": (
                "answer",
                "sitzplaetze-garten",
            ),
            "usage_type": ("answer", "nutzungsart", {"value_parser": "option"}),
            "usage_zone": ("answer", "nutzungszone"),
            "application_type": ("answer", "geschaeftstyp"),
            "development_regulations": ("answer", "ueberbauungsordnung"),
            "situation": ("answer", "sachverhalt"),
            "proposal": ("answer", "beschreibung-bauvorhaben"),
            "description_modification": ("answer", "beschreibung-projektaenderung"),
            "street": ("answer", "strasse-flurname"),
            "street_number": ("answer", "nr"),
            "city": ("answer", "ort-grundstueck"),
            "construction_costs": ("answer", "baukosten-in-chf"),
            "municipality": ("answer", "gemeinde", {"value_parser": "dynamic_option"}),
            "plot_data": (
                "table",
                "parzelle",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid-nr",
                        "coord_east": "lagekoordinaten-ost",
                        "coord_north": "lagekoordinaten-nord",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "paper_submit_date": (
                "case_meta",
                "paper-submit-date",
                {"value_parser": "datetime"},
            ),
            "decision_date": (
                "answer",
                "decision-date",
                {
                    "document_from_work_item": "decision",
                    "value_key": "date",
                },
            ),
            "publication_date": ("answer", "datum-publikation", {"value_key": "date"}),
            "construction_start_date": (
                "answer",
                "datum-baubeginn",
                {"value_key": "date"},
            ),
            "profile_approval_date": (
                "answer",
                "datum-schnurgeruestabnahme",
                {"value_key": "date"},
            ),
            "final_approval_date": (
                "answer",
                "datum-schlussabnahme",
                {"value_key": "date"},
            ),
            "completion_date": ("answer", "bauende", {"value_key": "date"}),
            "is_paper": (
                "answer",
                "is-paper",
                {
                    "value_parser": (
                        "value_mapping",
                        {"mapping": {"is-paper-yes": True, "is-paper-no": False}},
                    )
                },
            ),
        },
        "MUNICIPALITY_DATA_SHEET": APPLICATION_DIR(
            "Verwaltungskreise und -regionen der Gemeinden.csv"
        ),
        "ENABLE_PUBLIC_ENDPOINTS": True,
        "PUBLICATION_BACKEND": "caluma",
    },
    "kt_uri": {
        "ECH0211": {
            "API_ACTIVE": False,
        },
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
        "CUSTOM_NOTIFICATION_TYPES": [
            "submitter_list",
            "municipality_users",
            "unnotified_service_users",
            "lisag",
            "koor_np_users",
            "koor_bg_users",
            "koor_bd_users",
            "koor_sd_users",
            "responsible_koor",
        ],
        "DOCUMENTS_SKIP_CONTEXT_VALIDATION": True,
        "CALUMA": {
            "FORM_PERMISSIONS": ["main"],
            "FILL_PUBLICATION_TASK": None,
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": True,
            "GENERATE_IDENTIFIER": True,
            "USE_LOCATION": True,
            "KOOR_SD_SLUGS": [
                "veranstaltung-art-sportanlass",
                "veranstaltung-art-foto-und-filmaufnahmen",
                "veranstaltung-art-andere",
            ],
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
            "SYNC_FORM_TYPE": True,
            "SUBMIT_TASKS": [],
            "MODIFICATION_ALLOW_FORMS": [
                "building-permit",
            ],
            "MODIFICATION_DISALLOW_STATES": [
                "new",
                "done",
                "old",
            ],
        },
        "STORE_PDF": {
            "SECTION": {
                "MAIN": {"DEFAULT": 12000000, "PAPER": 12000000},
            },
        },
        "DOCUMENT_MERGE_SERVICE": {
            "FORM": {
                "building-permit": {
                    "forms": [
                        "building-permit",
                        "preliminary-clarification",
                        "commercial-permit",
                        "proposal-declaration",
                        "solar-declaration",
                        "cantonal-territory-usage",
                        "technische-bewilligung",
                    ],
                    "people_sources": [
                        "applicant",
                        "landowner",
                        "project-author",
                    ],
                    "people_names": {
                        "last-name": "familyName",
                        "first-name": "givenName",
                    },
                    "template": "2-level-extended",
                    "personalien": "personalien",
                    "exclude_slugs": [
                        "is-paper",
                        "einreichen",
                        "gis-karte",
                        "form-type",
                        "allgemeine-informationen-baugesuch",
                        "allgemeine-informationen-reklamegesuch",
                        "allgemeine-informationen-baugesuch-vorabklaerung",
                        "allgemeine-informationen-meldung-solaranlage",
                        "allgemeine-informationen-proposal-declaration",
                        "parzellen-oder-baurechtsnummer",
                    ],
                },
            },
            "ADD_HEADER_DATA": False,
        },
        "ARCHIVE_FORMS": [293, 294],
        "PAPER": {
            "ALLOWED_ROLES": {
                "DEFAULT": [
                    3,  # KOOR BG
                    6,  # Sekretariat Gemeindebaubehörde
                    1061,  # KOOR NP
                ]
            },
            "ALLOWED_SERVICE_GROUPS": {
                "DEFAULT": [
                    1,  # Koordinationsstellen
                    68,  # Sekretariate Gemeindebaubehörden
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
            "Koordinationsstelle Umweltschutz AfU": "coordination",
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
            "coordination": ["new", "new_portal", "del", "rejected"],
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
            "SUBMIT_CANTONAL_TERRITORY_USAGE_SD": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-sd",
                    "recipient_types": ["koor_sd_users"],
                },
            ],
            "SUBMIT_CANTONAL_TERRITORY_USAGE_BD": [
                {
                    "template_slug": "dossier-eingereicht-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "dossier-eingereicht-koor-bd",
                    "recipient_types": ["koor_bd_users"],
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
        "PORTAL_GROUP": 685,
        "OEREB_FORM": 296,
        "INSTANCE_IDENTIFIER_FORM_ABBR": {},
        "DUMP_CONFIG_GROUPS": {
            "dashboard_document": {
                "caluma_form.Document": Q(form="dashboard"),
            },
        },
        "DUMP_CONFIG_EXCLUDED_MODELS": [
            "user.Group",
            "user.GroupT",
            "user.GroupLocation",
            "user.Service",
            "user.ServiceT",
            "notification.NotificationTemplate",
            "notification.NotificationTemplateT",
        ],
        "ENABLE_PUBLIC_ENDPOINTS": True,
        "PUBLICATION_BACKEND": "camac-ng",
        "INSTANCE_STATE_REJECTION_COMPLETE": "arch",
        "SET_SUBMIT_DATE_CAMAC_WORKFLOW": True,
        "REJECTION_FEEDBACK_QUESTION": {
            "CHAPTER": 12000000,
            "QUESTION": 12000000,
            "ITEM": 1,
        },
        "MASTER_DATA": {
            "canton": ("static", "UR"),
            "applicants": (
                "table",
                "applicant",
                {
                    "column_mapping": {
                        "last_name": "last-name",
                        "first_name": "first-name",
                        "street": "street",
                        "street_number": "street-number",
                        "zip": "zip",
                        "town": "city",
                        "country": "country",
                        "is_juristic_person": (
                            "is-juristic-person",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "is-juristic-person-no": False,
                                            "is-juristic-person-yes": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "juristic_name": "juristic-person-name",
                    }
                },
            ),
            "proposal": (
                "answer",
                [
                    "proposal-description",
                    "beschreibung-zu-mbv",
                    "bezeichnung",
                    "vorhaben-proposal-description",
                    "veranstaltung-beschrieb",
                ],
            ),
            "veranstaltung_art": (
                "answer",
                "veranstaltung-art",
            ),
            "oereb_topic": (
                "answer",
                "oereb-thema",
            ),
            "legal_state": (
                "answer",
                "typ-des-verfahrens",
            ),
            "form_type": (
                "answer",
                "form-type",
            ),
            "authority": (
                "answer",
                "leitbehoerde",
                {"value_parser": "dynamic_option"},
            ),
            "plot_data": (
                "table",
                "parcels",
                {
                    "column_mapping": {
                        "plot_number": "parcel-number",
                        "egrid_number": "e-grid",
                        "coordinates_east": "coordinates-east",
                        "coordinates_north": "coordinates-north",
                        "origin_of_coordinates": ("default", {"default": 901}),
                    }
                },
            ),
            "street": ("answer", "parcel-street"),
            "street_number": ("answer", "parcel-street-number"),
            "city": ("answer", "parcel-city"),
            "dossier_number": ("case_meta", "dossier-number"),
            "municipality": (
                "answer",
                "municipality",
                {"value_parser": "dynamic_option"},
            ),
            "category": (
                "answer",
                "category",
                {
                    "value_parser": (
                        "value_mapping",
                        {
                            "mapping": {
                                "category-hochbaute": 6011,
                                "category-tiefbaute": 6010,
                            }
                        },
                    ),
                    "default": [],
                },
            ),
            "type_of_construction": (
                "table",
                "gebaeude",
                {
                    "column_mapping": {
                        "art_der_hochbaute": (
                            "art-der-hochbaute",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "art-der-hochbaute-einfamilienhaus": 6271,
                                            "art-der-hochbaute-doppeleinfamilienhaus": 6272,
                                            "art-der-hochbaute-mehrfamilienhaus": 6273,
                                            "art-der-hochbaute-wohn-und-geschaftshaus": 6274,
                                            "art-der-hochbaute-geschaftshaus": 6294,
                                            "art-der-hochbaute-garage-oder-carport": 6278,
                                            "art-der-hochbaute-parkhaus": 6235,
                                            "art-der-hochbaute-bauten-und-anlagen-gastgewerbe": 6295,
                                            "art-der-hochbaute-heim-mit-unterkunft": 6254,
                                            "art-der-hochbaute-wohnheim-ohne-pflege": 6276,
                                            "art-der-hochbaute-spital": 6253,
                                            "art-der-hochbaute-schulen": 6251,
                                            "art-der-hochbaute-sporthallen": 6259,
                                            "art-der-hochbaute-tourismusanlagen": 6256,
                                            "art-der-hochbaute-kirchen": 6257,
                                            "art-der-hochbaute-kulturbauten": 6258,
                                            "art-der-hochbaute-oekonomie-mit-tieren-mit-tieren": 6281,
                                            "art-der-hochbaute-oekonomiegebaude": 6281,
                                            "art-der-hochbaute-forstwirtschaft": 6282,
                                            "art-der-hochbaute-materiallager": 6292,
                                            "art-der-hochbaute-silo": 6292,
                                            "art-der-hochbaute-kommunikationsanlagen": 6245,
                                            "art-der-hochbaute-kehrichtentsorgungsanlagen": 6222,
                                            "art-der-hochbaute-andere": 6299,
                                            "art-der-hochbaute-energieholzlager": 6292,
                                            "art-der-hochbaute-industrie": 6299,
                                            "art-der-hochbaute-landwirtschaft-betrieb-wohnteil": 6281,
                                            "art-der-hochbaute-reklamebauten": 6299,
                                            "art-der-hochbaute-brennstofflager": 6292,
                                        }
                                    },
                                )
                            },
                        )
                    }
                },
            ),
            "construction_costs": ("answer", "construction-cost"),
            "submit_date": ("first_workflow_entry", [10, 12]),
            "decision_date": ("last_workflow_entry", [47]),
            "construction_start_date": (
                "first_workflow_entry",
                [55],
            ),
            "construction_end_date": (
                "last_workflow_entry",
                [67],
            ),
            "approval_reason": ("php_answer", 264, {"default": 5000}),
            "type_of_applicant": ("php_answer", 267),
            "energy_devices": (
                "table",
                "haustechnik-tabelle",
                {
                    "column_mapping": {
                        "name_of_building": "gehoert-zu-gebaeudenummer",
                        "type": "anlagetyp",
                        "information_source": (
                            "default",
                            {"default": 869},
                        ),  # Gemäss Baubewilligung
                        "is_heating": (
                            "anlagetyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "anlagetyp-analgetyp-klima": False,
                                            "anlagetyp-aufzuege": False,
                                            "anlagetyp-betankungsanlage": False,
                                            "anlagetyp-lueftungsanlage": False,
                                            "anlagetyp-notstrom-aggregat": False,
                                            "anlagetyp-photovoltaische-solaranlage": False,
                                            "anlagetyp-tankanlagen": False,
                                            "anlagetyp-thermische-solaranlage": False,
                                            "anlagetyp-warmwasser": False,
                                            "anlagetyp-hauptheizung": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "is_warm_water": (
                            "anlagetyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "anlagetyp-analgetyp-klima": False,
                                            "anlagetyp-aufzuege": False,
                                            "anlagetyp-betankungsanlage": False,
                                            "anlagetyp-lueftungsanlage": False,
                                            "anlagetyp-notstrom-aggregat": False,
                                            "anlagetyp-photovoltaische-solaranlage": False,
                                            "anlagetyp-tankanlagen": False,
                                            "anlagetyp-thermische-solaranlage": False,
                                            "anlagetyp-warmwasser": True,
                                            "anlagetyp-hauptheizung": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "is_main_heating": (
                            "heizsystem-art",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "-hauptheizung": True,
                                            "-zusatzheizung": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "energy_source": (
                            "hauptheizungsanlage",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "hauptheizungsanlage-abwaerme": 7550,
                                            "hauptheizungsanlage-andere": 7599,
                                            "hauptheizungsanlage-elektrizitaet": 7560,
                                            "hauptheizungsanlage-erdsonde": 7511,
                                            "hauptheizungsanlage-erdwaerme": 7510,
                                            "hauptheizungsanlage-erdwaermesonde": 7511,
                                            "hauptheizungsanlage-fernwaerme": 7580,
                                            "hauptheizungsanlage-gas": 7520,
                                            "hauptheizungsanlage-grundwasserwaermepumpe": 7513,
                                            "hauptheizungsanlage-heizoel": 7530,
                                            "hauptheizungsanlage-holz": 7540,
                                            "hauptheizungsanlage-holzschnitzel-pellets": 7542,
                                            "hauptheizungsanlage-kachelofen-schwedenofen": 7550,
                                            "hauptheizungsanlage-luftwaermepumpe": 7501,
                                            "hauptheizungsanlage-sonne-thermisch": 7570,
                                            "hauptheizungsanlage-stueckholz": 7541,
                                            "hauptheizungsanlage-unbestimmt": 7598,
                                        }
                                    },
                                )
                            },
                        ),
                    },
                },
            ),
            "buildings": (
                "table",
                "gebaeude",
                {
                    "column_mapping": {
                        "name": "gebaeudenummer-bezeichnung",
                        "proposal": (
                            "proposal",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "proposal-neubau": 6001,
                                            "proposal-umbau-erneuerung-sanierung": 6002,
                                            "proposal-abbruch-rueckbau": 6007,
                                        }
                                    },
                                ),
                                "default": [],
                            },
                        ),
                        "building_category": (
                            "gebaeudekategorie",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "gebaeudekategorie-andere": 1030,
                                            "gebaeudekategorie-ausschliessliche-wohnnutzung": 1020,
                                            "gebaeudekategorie-ohne-wohnnutzung": 1060,
                                            "gebaeudekategorie-provisorische-unterkunft": 1010,
                                            "gebaeudekategorie-sonderbau": 1080,
                                            "gebaeudekategorie-teilweise-wohnnutzung": 1040,
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
            "dwellings": (
                "table",
                "wohnungen",
                {
                    "column_mapping": {
                        "name_of_building": "zugehoerigkeit",
                        "floor_type": (
                            "stockwerktyp",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "stockwerktyp-obergeschoss": 3101,
                                            "stockwerktyp-untergeschoss": 3401,
                                            "stockwerktyp-parterre": 3100,
                                        }
                                    },
                                )
                            },
                        ),
                        "floor_number": "stockwerknummer",
                        "location_on_floor": "lage",
                        "number_of_rooms": "wohnungsgroesse",
                        "kitchen_facilities": "kocheinrichtung",
                        "has_kitchen_facilities": (
                            "kocheinrichtung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "kocheinrichtung-keine-kocheinrichtung": False,
                                            "kocheinrichtung-kochnische-greater-4-m2": True,
                                            "kocheinrichtung-kueche-less-4-m2": True,
                                        }
                                    },
                                )
                            },
                        ),
                        "area": "flaeche-in-m2",
                        "multiple_floors": (
                            "mehrgeschossige-wohnung",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "mehrgeschossige-wohnung-ja": True,
                                            "mehrgeschossige-wohnung-nein": False,
                                        }
                                    },
                                )
                            },
                        ),
                        "usage_limitation": (
                            "zwg",
                            {
                                "value_parser": (
                                    "value_mapping",
                                    {
                                        "mapping": {
                                            "zwg-keine": 3401,
                                            "zwg-erstwohnung": 3402,
                                            "zwg-touristisch-a": 3403,
                                            "zwg-touristisch-b": 3404,
                                        }
                                    },
                                )
                            },
                        ),
                    }
                },
            ),
        },
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {
            "REQUIRED_KEYS": [
                "external-id",
                "parzelle-nr",
                "erfassungsjahr",
                "vorhaben",
                "ort",
                "baurecht-nr",
                "gemeinde",
                "gesuchsteller",
                "documents",
            ],
            "USER": "import@koor-bg.ur.ch",
        },
    },
}

APPLICATIONS["kt_bern"]["DUMP_CONFIG_GROUPS"] = {
    **APPLICATIONS["kt_bern"]["DUMP_CONFIG_GROUPS"],
    "caluma_audit_form": {
        "caluma_form.Option": Q(
            questions__forms__pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"]
        ),
        "caluma_form.Question": Q(
            forms__pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"]
        ),
        "caluma_form.Form": Q(pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"]),
        "caluma_form.QuestionOption": Q(
            question__forms__pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"]
        ),
        "caluma_form.FormQuestion": Q(
            form__pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"]
        ),
        "caluma_form.Answer": Q(
            question__forms__pk__in=APPLICATIONS["kt_bern"]["CALUMA"]["AUDIT_FORMS"],
            document__isnull=True,
        ),
    },
    "caluma_publication_form": {
        "caluma_form.Option": Q(
            questions__forms__pk=APPLICATIONS["kt_bern"]["CALUMA"]["PUBLICATION_FORM"]
        ),
        "caluma_form.Question": Q(
            forms__pk=APPLICATIONS["kt_bern"]["CALUMA"]["PUBLICATION_FORM"]
        ),
        "caluma_form.Form": Q(pk=APPLICATIONS["kt_bern"]["CALUMA"]["PUBLICATION_FORM"]),
        "caluma_form.QuestionOption": Q(
            question__forms__pk=APPLICATIONS["kt_bern"]["CALUMA"]["PUBLICATION_FORM"]
        ),
        "caluma_form.FormQuestion": Q(
            form__pk=APPLICATIONS["kt_bern"]["CALUMA"]["PUBLICATION_FORM"]
        ),
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
INTERNAL_INSTANCE_URL_TEMPLATE = env.str(
    "DJANGO_INTERNAL_INSTANCE_URL_TEMPLATE",
    default=build_url(
        INTERNAL_BASE_URL,
        "/index/redirect-to-instance-resource/instance-id/{instance_id}",
    ),
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

DATABASES = {
    "default": {
        "ENGINE": "camac.core.postgresql_dbdefaults.psqlextra",
        "NAME": env.str("DATABASE_NAME", default=APPLICATION_NAME),
        "USER": env.str("DATABASE_USER", default="camac"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("camac")),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default=""),
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

LOCALE_NAME = "de_CH"
LANGUAGE_CODE = "de"
LANGUAGES = [("de", "German"), ("fr", "French")]
TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (os.path.join(ROOT_DIR, "locale"),)


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
            "Es dient nur zu Testzwecken und kann ignoriert werden\n\n"
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
GIS_API_USER = env.str("GIS_API_USER", "")
GIS_API_PASSWORD = env.str("GIS_API_PASSWORD", "")

GIS_SKIP_BOOLEAN_LAYERS = env.list("GIS_SKIP_BOOLEAN_LAYERS", default=[])

GIS_SKIP_SPECIAL_LAYERS = env.list("GIS_SKIP_SPECIAL_LAYERS", default=[])

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
    "MANABI_SHARED_KEY", default=default("bNEZsIjvxDAiLhDA1chvF9zL9OJYPNlCqNPlm7KbhmU")
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

# Parashift
PARASHIFT_BASE_URI = env.str(
    "PARASHIFT_BASE_URI", default="https://api.parashift.io/v2"
)

PARASHIFT_SOURCE_FILES_URI = env.str(
    "PARASHIFT_SOURCE_FILES_URI",
    default="https://individual-extraction.api.parashift.io/v1",
)

PARASHIFT_TENANT_ID = env.int("PARASHIFT_TENANT_ID", default=1665)
PARASHIFT_API_KEY = env.str("PARASHIFT_API_KEY", default="ey...")

Q_CLUSTER = {
    "name": "DjangORM",
    "workers": 2,
    "timeout": 2 * 3600,  # 2 hours
    "retry": 24 * 3600,  # retry tomorrow
    "queue_limit": 50,
    "bulk": 10,
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

OIDC_RP_CLIENT_ID = env.str("DJANGO_OIDC_RP_CLIENT_ID", default="camac")
OIDC_RP_CLIENT_SECRET = env.str("DJANGO_OIDC_RP_CLIENT_SECRET", default=None)

OIDC_DEFAULT_BASE_URL = env.str(
    "DJANGO_OIDC_DEFAULT_BASE_URL",
    default=f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect",
)

OIDC_OP_AUTHORIZATION_ENDPOINT = env.str(
    "DJANGO_OIDC_OP_AUTHORIZATION_ENDPOINT", default=f"{OIDC_DEFAULT_BASE_URL}/auth"
)

OIDC_OP_TOKEN_ENDPOINT = env.str(
    "DJANGO_OIDC_OP_TOKEN_ENDPOINT", default=f"{OIDC_DEFAULT_BASE_URL}/token"
)
OIDC_OP_USER_ENDPOINT = env.str(
    "DJANGO_OIDC_USERINFO_ENDPOINT", default=f"{OIDC_DEFAULT_BASE_URL}/userinfo"
)

# admin page after completing server-side authentication flow
LOGIN_REDIRECT_URL = env.str(
    "DJANGO_OIDC_ADMIN_LOGIN_REDIRECT_URL",
    default=f"{INTERNAL_BASE_URL}/django-admin/",
)

OIDC_RP_SIGN_ALGO = env.str("DJANGO_OIDC_RP_SIGN_ALGO", default="RS256")

OIDC_OP_JWKS_ENDPOINT = env.str(
    "DJANGO_OIDC_OP_JWKS_ENDPOINT", default=f"{OIDC_DEFAULT_BASE_URL}/certs"
)

OIDC_EMAIL_CLAIM = env.str("DJANGO_OIDC_EMAIL_CLAIM", default="email")

OIDC_FIRSTNAME_CLAIM = env.str("DJANGO_OIDC_FIRSTNAME_CLAIM", default="given_name")

OIDC_LASTNAME_CLAIM = env.str("DJANGO_OIDC_LASTNAME_CLAIM", default="family_name")

OIDC_OP_INTROSPECT_ENDPOINT = env.str(
    "DJANGO_OIDC_OP_INTROSPECT_ENDPOINT",
    default=f"{OIDC_DEFAULT_BASE_URL}/token/introspect",
)

STATICFILES_DIRS += APPLICATIONS[APPLICATION_NAME].get("INCLUDE_STATIC_FILES", [])


def load_module_settings(module_name):
    module = getattr(
        import_module(f"camac.settings_{module_name.lower()}"), module_name.upper()
    )
    app_config = module.get(APPLICATION_NAME, {})

    return (
        always_merger.merge(module["default"], app_config)
        if app_config.get("ENABLED")
        else {}
    )


DISTRIBUTION = load_module_settings("distribution")
