import json
import logging
import os
import re
from datetime import timedelta

import environ
from django.db.models.expressions import Q
from django.utils.translation import gettext_lazy

from camac.constants import kt_bern as be_constants
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

# UR uses camac.ur.ch and camac.kt.ur.ch to refer to the same system. This makes sure
# that django infers the correct base uri in FileFields (build_absolute_uri).
USE_X_FORWARDED_HOST = env.bool("DJANGO_USE_X_FORWARDED_HOST", default=False)

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
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
    "camac.echbern.apps.EchbernConfig",
    "camac.migrate_to_caluma",
    "camac.stats.apps.StatsConfig",
    "camac.parashift",
    "sorl.thumbnail",
    "django_clamd",
    "reversion",
    "rest_framework_xml",
    "gisbern",
    # TODO: remove this when all production environments ran the migration to
    # delete the tables of this app
    "camac.file.apps.DefaultConfig",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "camac.user.middleware.GroupMiddleware",
    "camac.caluma.middleware.CalumaInfoMiddleware",
    "camac.middleware.LoggingMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
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
    "demo": {
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
        },
        "ROLE_INHERITANCE": {"trusted_service": "service"},
        "IS_MULTILINGUAL": False,
        "NOTIFICATIONS": {"SUBMIT": None, "APPLICANT": {"NEW": None, "EXISTING": None}},
        "PUBLICATION_DURATION": timedelta(days=30),
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
            "FORM_PERMISSIONS": ["main"],
            "HAS_PROJECT_CHANGE": False,
            "CREATE_IN_PROCESS": False,
            "GENERATE_IDENTIFIER": False,
            "USE_LOCATION": False,
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": True,
        },
        "STORE_PDF": {"SECTION": 1},
        "ECH_API": True,
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
                "parashift-id",
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
    "kt_schwyz": {
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
        "PORTAL_GROUP": 4,
        "NOTIFICATIONS": {
            "SUBMIT": "gesuchseingang",
            "APPLICANT": {
                "NEW": "gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "gesuchsbearbeitungs-einladung-bestehend",
            },
            "PUBLICATION_PERMISSION": "publikation-einsehen",
        },
        "PUBLICATION_DURATION": timedelta(days=30),
        "PUBLICATION_BACKEND": "camac-ng",
        "IS_MULTILINGUAL": False,
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
            "projektverfasser-planer",
            "grundeigentumerschaft",
        ],
        "INSTANCE_IDENTIFIER_FORM_ABBR": {
            "geschaeftskontrolle": "GK",
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
        # please also update django/Makefile command when changing apps here
        "SEQUENCE_NAMESPACE_APPS": [],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "CALUMA": {
            "CIRCULATION_WORKFLOW": "circulation",
            "CIRCULATION_TASK": "circulation",
            "CIRCULATION_FORM": "circulation",
            "ACTIVATION_INIT_TASK": "write-statement",
            "ACTIVATION_TASKS": [
                "write-statement",
                "check-statement",
                "revise-statement",
                "alter-statement",
            ],
            "ACTIVATION_RELEVANT_TASKS": [
                "write-statement",
                "check-statement",
            ],
            "ACTIVATION_EXCLUDE_ROLES": ["Lesezugriff"],
            "SUBMIT_TASKS": ["submit", "submit-additional-demand", "formal-addition"],
            "REJECTION_TASK": "reject-form",
            "PRE_COMPLETE": {
                "complete-check": {"cancel": ["reject-form"]},
                "reject-form": {"cancel": ["complete-check", "depreciate-case"]},
                "start-circulation": {"cancel": ["skip-circulation"]},
                "skip-circulation": {"cancel": ["start-circulation"]},
                "formal-adittion": {"cancel": ["archive-instance"]},
                "start-additional-circulation": {
                    "cancel": ["check-statements", "start-decision"]
                },
                "start-decision": {
                    "skip": ["check-statements"],
                    "cancel": ["start-additional-circulation", "additional-demand"],
                },
                "reopen-circulation": {"cancel": ["make-decision"]},
                "make-decision": {
                    "cancel": [
                        "reopen-circulation",
                        "depreciate-case",
                    ]
                },
                "check-statement": {"cancel": ["revise-statement"]},
                "revise-statement": {"cancel": ["check-statement"]},
                "depreciate-case": {
                    "cancel": [
                        "formal-addition",
                        "complete-check",
                        "reject-form",
                        "start-circulation",
                        "publication",
                        "skip-circulation",
                        "circulation",
                        "additional-demand",
                        "submit-additional-demand",
                        "start-additional-circulation",
                        "check-statements",
                        "start-decision",
                        "make-decision",
                        "reopen-circulation",
                    ]
                },
                "archive-instance": {
                    "cancel": [
                        "create-manual-workitems",
                    ]
                },
            },
            "SAVE_DOSSIER_NUMBER_IN_CALUMA": False,
            "PUBLICATION_TASK_SLUG": "publication",
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
                "archive-form": {
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
                "skip-circulation": {
                    "next_instance_state": "redac",
                    "history_text": "Zirkulationsentscheid gestartet",
                },
                "start-decision": {
                    "next_instance_state": "redac",
                    "history_text": "Zirkulationsentscheid gestartet",
                },
                "reopen-circulation": {
                    "next_instance_state": "circ",
                    "history_text": "Zurück zur Zirkulation",
                },
            },
        },
        "HAS_EBAU_NUMBER": False,
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
            "baugesuch-reklamegesuch-v2",
            "baugesuch-reklamegesuch-v3",
            "baugesuch-reklamegesuch-v4",
            "projektanderung-v2",
            "projektanderung-v3",
            "projektanderung-v4",
            "technische-bewilligung",
            "baumeldung-fur-geringfugiges-vorhaben-v2",
            "baumeldung-fur-geringfugiges-vorhaben-v3",
            "anlassbewilligungen-verkehrsbewilligungen-v2",
            "projektgenehmigungsgesuch-gemass-ss15-strag-v2",
        ],
        "STORE_PDF": {"SECTION": 1},
        "DUMP_CONFIG_GROUPS": {
            "email_notifications": {
                "notification.NotificationTemplate": Q(type="email"),
                "notification.NotificationTemplateT": Q(template__type="email"),
            },
        },
        "REJECTION_FEEDBACK_QUESTION": {},
        "FORM_FIELD_HISTORY_ENTRY": [
            {
                "name": "materieller-pruefbericht-bemerkung",
                "title": "Materieller Prüfbericht",
            }
        ],
        "MASTER_DATA": {
            "applicants": (
                "ng_table",
                "bauherrschaft",
                {
                    "column_mapping": {
                        "last_name": "name",
                        "first_name": "vorname",
                        "street": "strasse",
                        "zip": "plz",
                        "town": "ort",
                    }
                },
            ),
            "proposal": ("ng_answer", "bezeichnung"),
            "construction_costs": ("ng_answer", "baukosten"),
            "submit_date": ("workflow_entry", 10),
        },
    },
    "kt_bern": {
        "LOG_NOTIFICATIONS": True,
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
                    "recipient_types": ["construction_control", "service"],
                },
            ],
            "FINALIZE": [
                {
                    "template_slug": "13-meldung-termine-pflichtkontrollen-baukontrolle",
                    "recipient_types": ["construction_control", "service"],
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
                    "template_slug": "08-entscheid-gemeindeleitbehorde",
                    "recipient_types": ["leitbehoerde"],
                },
                {
                    "template_slug": "08-entscheid-amts-und-fachstellen",
                    "recipient_types": ["service"],
                },
            ],
            "DECISION_PRELIMINARY_CLARIFICATION": [
                {
                    "template_slug": "08-stellungnahme-zu-voranfrage-gesuchsteller",
                    "recipient_types": ["applicant"],
                },
                {
                    "template_slug": "08-entscheid-gemeindeleitbehorde",
                    "recipient_types": ["leitbehoerde"],
                },
                {
                    "template_slug": "08-entscheid-amts-und-fachstellen",
                    "recipient_types": ["service"],
                },
            ],
            "END_CIRCULATION": [
                {
                    "template_slug": "03-verfahren-vorzeitig-beendet",
                    "recipient_types": ["unanswered_activation"],
                },
            ],
            "ECH_KIND_OF_PROCEEDINGS": [
                {
                    "template_slug": "03-verfahrensablauf-gesuchsteller",
                    "recipient_types": ["applicant"],
                }
            ],
            "ECH_TASK": [
                {
                    "template_slug": "03-verfahrensablauf-fachstelle",
                    "recipient_types": ["unnotified_service"],
                }
            ],
            "ECH_ACCOMPANYING_REPORT": [
                {
                    "template_slug": "05-bericht-erstellt",
                    "recipient_types": ["activation_service_parent"],
                }
            ],
        },
        "PUBLICATION_DURATION": timedelta(),
        "IS_MULTILINGUAL": True,
        "FORM_BACKEND": "caluma",
        "OIDC_SYNC_USER_ATTRIBUTES": [
            "language",
            "email",
            "username",
            "name",
            "surname",
        ],
        "CALUMA": {
            "FORM_PERMISSIONS": [
                "main",
                "sb1",
                "sb2",
                "nfd",
                "dossierpruefung",
                "publikation",
            ],
            "CIRCULATION_WORKFLOW": "circulation",
            "CIRCULATION_TASK": "circulation",
            "CIRCULATION_FORM": "circulation",
            "ACTIVATION_INIT_TASK": "activation",
            "ACTIVATION_TASKS": ["activation"],
            "ACTIVATION_RELEVANT_TASKS": ["activation"],
            "SUBMIT_TASKS": ["submit"],
            "REPORT_TASK": "sb1",
            "FINALIZE_TASK": "sb2",
            "AUDIT_TASK": "audit",
            "DECISION_TASK": "decision",
            "EBAU_NUMBER_TASK": "ebau-number",
            "SIMPLE_WORKFLOW": {
                "reopen-circulation": {
                    "next_instance_state": "circulation",
                    "ech_event": "camac.echbern.signals.circulation_started",
                    "history_text": gettext_lazy("Circulation reopened"),
                },
                "skip-circulation": {
                    "next_instance_state": "coordination",
                    "ech_event": "camac.echbern.signals.circulation_ended",
                    "history_text": gettext_lazy("Circulation skipped"),
                },
                "start-decision": {
                    "next_instance_state": "coordination",
                    "ech_event": "camac.echbern.signals.circulation_ended",
                    "history_text": gettext_lazy("Circulation completed"),
                },
                "complete": {
                    "next_instance_state": "finished",
                    "ech_event": "camac.echbern.signals.finished",
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
                "start-decision": {
                    "complete": ["check-activation"],
                    "cancel": ["start-circulation"],
                },
                "skip-circulation": {"cancel": ["init-circulation"]},
                "init-circulation": {"cancel": ["skip-circulation"]},
                "start-circulation": {"cancel": ["check-activation", "start-decision"]},
                "decision": {
                    "skip": ["audit", "publication", "fill-publication"],
                    "cancel": [
                        "reopen-circulation",
                        "create-manual-workitems",
                        "create-publication",
                    ],
                    "complete": ["nfd"],
                },
                "reopen-circulation": {"cancel": ["decision"]},
                "complete": {
                    "skip": ["check-sb1", "check-sb2", "fill-publication"],
                    "cancel": [
                        "create-manual-workitems",
                        "create-publication",
                    ],
                },
            },
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
            20003,
            20006,
            20096,
            20144,
            20069,
            22648,
            20165,
            22642,
            20291,
        ],  # DE
        # "DEMO_MODE_GROUPS": [22274, 22271, 20099, 20078, 23248],  # FR
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
                    "sb1",
                    "sb2",
                    "conclusion",
                    "finished",
                    "finished_internal",
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
        "ECH_API": True,
        "DOCUMENT_MERGE_SERVICE": {
            "FORM": {
                "_base": {
                    "people_sources": {
                        # bulding permit
                        "personalien-gesuchstellerin",
                        "personalien-vertreterin-mit-vollmacht",
                        "personalien-grundeigentumerin",
                        "personalien-gebaudeeigentumerin",
                        "personalien-projektverfasserin",
                        "personalien-sb",
                        # sb1 & sb2
                        "personalien-sb1-sb2",
                    },
                    "people_names": {
                        "name-gesuchstellerin": "familyName",
                        "vorname-gesuchstellerin": "givenName",
                        "name-vertreterin": "familyName",
                        "vorname-vertreterin": "givenName",
                        "name-grundeigentuemerin": "familyName",
                        "vorname-grundeigentuemerin": "givenName",
                        "name-gebaeudeeigentuemerin": "familyName",
                        "vorname-gebaeudeeigentuemerin": "givenName",
                        "name-projektverfasserin": "familyName",
                        "vorname-projektverfasserin": "givenName",
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
                        "vorabklaerung-einfach",
                        "vorabklaerung-vollstaendig",
                        "vorabklaerung-vollstaendig-v2",
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
            "MUNICIPALITY_SLUG": "gemeinde",
            "MUNICIPALITY_MODEL": "camac.user.models.Service",
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
        "INSTANCE_STATE_REJECTION_COMPLETE": "finished",
        "SET_SUBMIT_DATE_CAMAC_ANSWER": True,
        "REJECTION_FEEDBACK_QUESTION": {
            "CHAPTER": 20001,
            "QUESTION": 20037,
            "ITEM": 1,
        },
        "SUGGESTIONS": [
            (
                "art-versickerung-dach",
                "art-versickerung-dach-oberflaechengewaesser",
                [20063],
            ),
            (
                "art-versickerung-platz",
                "art-versickerung-platz-oberflachengewasser",
                [20063],
            ),
            (
                "art-versickerung-dach-v2",
                "art-versickerung-dach-v2-oberflaechengewaesser",
                [20063],
            ),
            (
                "art-versickerung-platz-v2",
                "art-versickerung-platz-v2-oberflaechengewaesser",
                [20063],
            ),
            (
                "ausnahme-im-sinne-von-artikel-64-kenv",
                "ausnahme-im-sinne-von-artikel-64-kenv-ja",
                [20046],
            ),
            ("aussenlaerm", "aussenlaerm-ja", [20054]),
            (
                "bau-im-wald-oder-innerhalb-von-30-m-abstand",
                "bau-im-wald-oder-innerhalb-von-30-m-abstand-ja",
                [20048],
            ),
            ("baubeschrieb", "baubeschrieb-erweiterung-anbau", [20068, 20055]),
            ("baubeschrieb", "baubeschrieb-neubau", [20055]),
            ("baubeschrieb", "baubeschrieb-technische-anlage", [20055]),
            ("baubeschrieb", "baubeschrieb-tiefbauanlage", [20068]),
            ("baubeschrieb", "baubeschrieb-um-ausbau", [20055, 20068]),
            ("baubeschrieb", "baubeschrieb-umnutzung", [20055]),
            ("baugruppe-bauinventar", "baugruppe-bauinventar-ja", [20043]),
            (
                "bauten-oder-pfaehlen-im-grundwasser",
                "bauten-oder-pfaehlen-im-grundwasser-ja",
                [20050],
            ),
            ("belasteter-standort", "belasteter-standort-ja", [20050]),
            ("besondere-brandrisiken", "besondere-brandrisiken-ja", [20057]),
            ("brandbelastung", "brandbelastung-ja", [20057]),
            (
                "eigenstaendiger-grossverbraucher",
                "eigenstaendiger-grossverbraucher-ja",
                [20046],
            ),
            ("erhaltenswert", "erhaltenswert-ja", [20043]),
            ("feuerungsanlagen", "feuerungsanlagen-holzfeuerungen", [20057]),
            (
                "feuerungsanlagen",
                "feuerungsanlagen-ol-oder-gasfeuerungen-350-kw",
                [20057],
            ),
            (
                "feuerungsanlagen",
                "feuerungsanlagen-pellet-schnitzelfeuerungsanlage",
                [20055],
            ),
            (
                "feuerungsanlagen",
                "feuerungsanlagen-pellet-schnitzelfeuerungsanlage",
                [20054],
            ),
            (
                "feuerungsanlagen",
                "feuerungsanlagen-pellet-schnitzelfeuerungsanlage",
                [20057],
            ),
            (
                "gebiet-mit-archaeologischen-objekten",
                "gebiet-mit-archaeologischen-objekten-ja",
                [20043],
            ),
            ("gebiet-mit-naturgefahren", "gebiet-mit-naturgefahren-ja", [20049]),
            ("gefahrenstufe", "gefahrenstufe-blau", [20049]),
            ("gefahrenstufe", "gefahrenstufe-rot", [20049]),
            ("gefahrenstufe", "gefahrenstufe-unbestimmt", [20049]),
            ("gefaehrliche-stoffe", "gefaehrliche-stoffe-ja", [20055]),
            (
                "gentechnisch-veraenderte-organismen",
                "gentechnisch-veraenderte-organismen-ja",
                [20060],
            ),
            (
                "geplante-anlagen",
                "geplante-anlagen-solar-oder-photovoltaik-anlage",
                [20054],
            ),
            ("grundwasserschutzzonen", "grundwasserschutzzonen-s1", [20050]),
            ("grundwasserschutzzonen", "grundwasserschutzzonen-s2sh", [20050]),
            ("grundwasserschutzzonen", "grundwasserschutzzonen-s3sm", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-s1", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-s2", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-s3-s3zu", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-sa", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-sbw", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-sh", [20050]),
            ("grundwasserschutzzonen-v2", "grundwasserschutzzonen-v2-sm", [20050]),
            (
                "ist-das-vorhaben-energierelevant",
                "ist-das-vorhaben-energierelevant-ja",
                [20046],
            ),
            (
                "ist-durch-das-bauvorhaben-boden-betroffen",
                "ist-durch-das-bauvorhaben-boden-betroffen-ja",
                [20050],
            ),
            (
                "ist-durch-das-bauvorhaben-boden-ober-unterboden-betroffen-v2",
                "ist-durch-das-bauvorhaben-boden-ober-unterboden-betroffen-v2-ja",
                [20050],
            ),
            (
                "ist-mit-bauabfaellen-zu-rechnen",
                "ist-mit-bauabfaellen-zu-rechnen-ja",
                [20050],
            ),
            ("k-objekt", "k-objekt-ja", [20043]),
            (
                "klassierung-der-taetigkeit",
                "klassierung-der-taetigkeit-klasse-3",
                [20055],
            ),
            (
                "klassierung-der-taetigkeit",
                "klassierung-der-taetigkeit-klasse-4",
                [20055],
            ),
            ("maschinelle-arbeitsmittel", "maschinelle-arbeitsmittel-ja", [20055]),
            (
                "maschinen-aus-den-folgenden-kategorien",
                "maschinen-aus-den-folgenden-kategorien-erzeugung",
                [20055],
            ),
            (
                "maschinen-aus-den-folgenden-kategorien",
                "maschinen-aus-den-folgenden-kategorien-reinigung",
                [20055],
            ),
            (
                "maschinen-aus-den-folgenden-kategorien",
                "maschinen-aus-den-folgenden-kategorien-strom",
                [20055],
            ),
            (
                "maschinen-aus-den-folgenden-kategorien",
                "maschinen-aus-den-folgenden-kategorien-transport",
                [20055],
            ),
            (
                "maschinen-aus-den-folgenden-kategorien",
                "maschinen-aus-den-folgenden-kategorien-werkhoefe",
                [20055],
            ),
            ("naturschutz", "naturschutz-ja", [20065]),
            ("nutzungsart", "nutzungsart-andere", [20054, 20055]),
            ("nutzungsart", "nutzungsart-dienstleistung", [20054, 20055]),
            ("nutzungsart", "nutzungsart-gastgewerbe", [20054, 20055]),
            ("nutzungsart", "nutzungsart-gewerbe", [20054, 20055, 20074]),
            ("nutzungsart", "nutzungsart-industrie", [20054, 20055, 20074]),
            ("nutzungsart", "nutzungsart-lager", [20054, 20055]),
            ("nutzungsart", "nutzungsart-landwirtschaft", [20054, 20055, 20074]),
            ("nutzungsart", "nutzungsart-verkauf", [20054, 20055]),
            ("organismen-in-anlage", "organismen-in-anlage-andere", [20055]),
            ("organismen-in-anlage", "organismen-in-anlage-bakterien", [20055]),
            ("organismen-in-anlage", "organismen-in-anlage-viren", [20055]),
            ("rrb", "rrb-ja", [20043]),
            ("schuetzenswert", "schuetzenswert-ja", [20043]),
            (
                "sind-belange-des-gewasserschutzes-betroffen",
                "sind-belange-des-gewasserschutzes-betroffen-ja",
                [20050],
            ),
            (
                "sind-belange-des-gewaesserschutzes-betroffen-v2",
                "sind-belange-des-gewaesserschutzes-betroffen-v2-ja",
                [20050],
            ),
            ("versickerung", "versickerung-nein", [20063]),
            ("versickerung-v2", "versickerung-v2-nein", [20063]),
            ("verunreinigte-abluft", "verunreinigte-abluft-ja", [20054]),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-andere",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-diagnostik",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-forschung",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-gewaechshaus",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-produktion",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-tieranlage",
                [20055],
            ),
            (
                "verwendungszweck-der-anlage",
                "verwendungszweck-der-anlage-unterricht",
                [20055],
            ),
            ("was-fuer-ein-vorhaben", "was-fuer-ein-vorhaben-andere", [20055]),
            ("was-fuer-ein-vorhaben", "was-fuer-ein-vorhaben-grossraumbueros", [20055]),
            ("was-fuer-ein-vorhaben", "was-fuer-ein-vorhaben-spitaeler", [20055]),
            (
                "was-fuer-ein-vorhaben",
                "was-fuer-ein-vorhaben-verkaufsgeschaefte",
                [20055],
            ),
            (
                "wassergefaehrdende-explosive-stoffe",
                "wassergefaehrdende-explosive-stoffe-ja",
                [20050, 20060],
            ),
            (
                "welche-art-vorhaben",
                "welche-art-vorhaben-erstellung-aussenraum",
                [20068],
            ),
            (
                "welche-art-vorhaben",
                "welche-art-vorhaben-fischhaltung-aquakulturanlage",
                [20050, 20051, 20052, 20053, 20063],
            ),
            ("welche-waermepumpen", "welche-waermepumpen-boden-untergrund", [20053]),
            ("welche-waermepumpen", "welche-waermepumpen-luft", [20054]),
            ("welche-waermepumpen", "welche-waermepumpen-wasser", [20053, 20063]),
            (
                "werden-brandschutzabstaende-unterschritten",
                "werden-brandschutzabstande-unterschritten-ja",
                [20057],
            ),
            ("werden-siloanlagen-erstellt", "werden-siloanlagen-erstellt-ja", [20055]),
            ("wildtierschutz", "wildtierschutz-ja", [20064]),
            ("gesuchstyp", "gesuchstyp-baum", [20065]),
            ("gesuchstyp", "gesuchstyp-hecke-feldgehoelz", [20065]),
            (
                "handelt-es-sich-um-ein-sensibles-objekt",
                "handelt-es-sich-um-ein-sensibles-objekt-ja",
                [20075, 20076, 20077, 20078],
            ),
        ],
        "NOTIFICATIONS_EXCLUDED_TASKS": [],
        "DUMP_CONFIG_GROUPS": {
            "email_notifications": {
                "notification.NotificationTemplate": Q(type="email"),
                "notification.NotificationTemplateT": Q(template__type="email"),
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
        "MASTER_DATA": {
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
            "dossier_number": ("case_meta", "ebau-number"),
            "proposal": ("answer", "beschreibung-bauvorhaben"),
            "modification": ("answer", "beschreibung-projektaenderung"),
            "street": ("answer", "strasse-flurname"),
            "street_number": ("answer", "nr"),
            "city": ("answer", "ort-grundstueck"),
            "construction_costs": ("answer", "baukosten-in-chf"),
            "municipality": ("dynamic_option", "gemeinde"),
            "plot_data": (
                "table",
                "parzelle",
                {
                    "column_mapping": {
                        "plot_number": "parzellennummer",
                        "egrid_number": "e-grid-nr",
                    }
                },
            ),
            "submit_date": ("case_meta", "submit-date", {"value_parser": "datetime"}),
            "paper_submit_date": (
                "case_meta",
                "paper-submit-date",
                {"value_parser": "datetime"},
            ),
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
        "ENABLE_PUBLIC_CALUMA": True,
        "PUBLICATION_BACKEND": "caluma",
    },
    "kt_uri": {
        "LOG_NOTIFICATIONS": False,
        "FORM_BACKEND": "caluma",
        "PUBLICATION_DURATION": timedelta(days=20),
        "PORTAL_USER_ID": 1209,
        "APPLICANT_GROUP_ID": 685,  # We reuse the Portal User group
        "SEQUENCE_NAMESPACE_APPS": ["core", "document", "responsible"],
        "CUSTOM_NOTIFICATION_TYPES": [
            "submitter_list",
            "municipality_users",
            "unnotified_service_users",
            "lisag",
            "koor_np_users",
            "koor_bg_users",
            "responsible_koor",
        ],
        "CALUMA": {
            "FORM_PERMISSIONS": ["main"],
            "HAS_PROJECT_CHANGE": True,
            "CREATE_IN_PROCESS": True,
            "GENERATE_IDENTIFIER": True,
            "USE_LOCATION": True,
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
                    ],
                    "people_sources": {
                        "applicant",
                        "landowner",
                        "project-author",
                    },
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
            "MUNICIPALITY_SLUG": "municipality",
            "MUNICIPALITY_MODEL": "camac.user.models.Location",
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
            "Support": "support",
            # "Portal User": None,  # Uses the fallback permissions
            # "Admin": None,
            # "Architect": None,
            # "Guest": None,  # TODO AFAIK we don't grant unauthenticated users access to endpoints
        },
        "ROLE_INHERITANCE": {"trusted_service": "service"},
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
            "APPLICANT": {
                "NEW": "01-gesuchsbearbeitungs-einladung-neu",
                "EXISTING": "02-gesuchsbearbeitungs-einladung-bestehend",
            },
        },
        # The following services don't receive notifications if they have
        # overdue circulation activations.
        "NOTIFY_OVERDUE_EXCLUDED_SERVICES": [
            88,  # ARE BaB Kreis 1
            261,  # ARE BaB Kreis 2
            262,  # ARE BaB Kreis 3
            90,  # ARE NP
        ],
        "HAS_EBAU_NUMBER": False,
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
        "ENABLE_PUBLIC_CALUMA": False,
        "PUBLICATION_BACKEND": "camac-ng",
        "INSTANCE_STATE_REJECTION_COMPLETE": "arch",
        "SET_SUBMIT_DATE_CAMAC_WORKFLOW": True,
        "REJECTION_FEEDBACK_QUESTION": {
            "CHAPTER": 12000000,
            "QUESTION": 12000000,
            "ITEM": 1,
        },
        "MASTER_DATA": {
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
            "plot_data": (
                "table",
                "parcels",
                {
                    "column_mapping": {
                        "plot_number": "parcel-number",
                        "egrid_number": "e-grid",
                    }
                },
            ),
            "street": ("answer", "parcel-street"),
            "street_number": ("answer", "parcel-street-number"),
            "city": ("answer", "parcel-city"),
            "dossier_number": ("case_meta", "dossier-number"),
            "municipality": ("dynamic_option", "municipality"),
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
                                "value_mapping": {
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
                                    "art-der-hochbaute-landwirtschaft": 6281,
                                    "art-der-hochbaute-forstwirtschaft": 6282,
                                    "art-der-hochbaute-materiallager": 6292,
                                    "art-der-hochbaute-silo": 6292,
                                    "art-der-hochbaute-kommunikationsanlagen": 6245,
                                    "art-der-hochbaute-kehrichtentsorgungsanlagen": 6222,
                                    "art-der-hochbaute-andere": 6299,
                                }
                            },
                        )
                    }
                },
            ),
            "construction_costs": ("answer", "construction-cost"),
            "submit_date": ("workflow_entry", [10, 12]),
        },
        "SIDE_EFFECTS": {
            "document_downloaded": "camac.document.side_effects.create_workflow_entry",
        },
        "DOSSIER_IMPORT": {
            "REQUIRED_KEYS": [
                "parashift-id",
                "parzelle-nr",
                "erfassungsjahr",
                "vorhaben",
                "ort",
                "baurecht-nr",
                "gemeinde",
                "gesuchsteller",
                "documents",
            ],
            "USER": "admin",
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
    env.str("DJANGO_PUBLIC_BASE_URL", default=default("http://caluma-portal.local"))
)

INTERNAL_BASE_URL = build_url(
    env.str("DJANGO_INTERNAL_BASE_URL", default=default("http://camac-ng.local"))
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
TEMPFILE_DOWNLOAD_PATH = env.str(
    "DJANGO_TEMPFILE_DOWNLOAD_PATH", default="/tmp/camac/tmpfiles"
)
TEMPFILE_DOWNLOAD_URL = env.str("DJANGO_TEMPFILE_DOWNLOAD_URL", default="/zips")
# in seconds
TEMPFILE_RETENTION_TIME = env.int(
    "DJANGO_TEMPFILE_RETENTION_TIME", default=(60 * 60 * 24)
)

STATIC_ROOT = ROOT_DIR("staticfiles")

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
    env.str("KEYCLOAK_URL", default="http://camac-ng-keycloak.local/auth/"),
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
        "Attention: Cette demande ne peut être traitée dans eBau.\n\n"
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
GIS_BASE_URL = build_url(env.str("GIS_BASE_URL", "https://www.geoservice.apps.be.ch"))
GIS_API_USER = env.str("GIS_API_USER", "")
GIS_API_PASSWORD = env.str("GIS_API_PASSWORD", "")

GIS_SKIP_BOOLEAN_LAYERS = env.list("GIS_SKIP_BOOLEAN_LAYERS", default=[])

GIS_SKIP_SPECIAL_LAYERS = env.list("GIS_SKIP_SPECIAL_LAYERS", default=[])

DOCUMENT_MERGE_SERVICE_URL = build_url(
    env.str("DOCUMENT_MERGE_SERVICE_URL", "http://document-merge-service:8000/api/v1/")
)

ECH_EXCLUDED_FORMS = [
    "verlaengerung-geltungsdauer",
    "migriertes-dossier",
    "baupolizeiliches-verfahren",
    "hecken-feldgehoelze-baeume",
    "klaerung-baubewilligungspflicht",
    "zutrittsermaechtigung",
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
