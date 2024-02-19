import copy
import inspect
import logging
import os
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import faker
import pytest
import urllib3
from alexandria.storages.backends.s3 import SsecGlobalS3Storage
from caluma.caluma_core.faker import MultilangProvider
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow import (
    api as workflow_api,
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.test import override_settings
from django.urls import path
from django.utils.timezone import make_aware
from django.views.generic import RedirectView
from factory import Faker
from factory.base import FactoryMetaClass
from jwt import encode as jwt_encode
from minio import Minio
from minio.datatypes import Object as MinioStatObject
from pytest_factoryboy import register
from pytest_factoryboy.fixture import Box, get_model_name
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from camac.applicants import factories as applicant_factories
from camac.billing import factories as billing_factories
from camac.caluma.utils import CalumaInfo
from camac.communications import factories as communications_factories
from camac.core import factories as core_factories
from camac.document import factories as document_factories
from camac.document.tests.data import django_file
from camac.dossier_import import factories as dossier_import_factories
from camac.ech0211 import factories as ech_factories
from camac.ech0211.urls import BEUrlsConf, SZUrlsConf
from camac.faker import FreezegunAwareDatetimeProvider
from camac.gis import factories as gis_factories
from camac.instance import factories as instance_factories
from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.notification import factories as notification_factories
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.objection import factories as objection_factories
from camac.permissions import factories as permissions_factories
from camac.responsible import factories as responsible_factories
from camac.settings.testing import *  # noqa F403, F401
from camac.tags import factories as tags_factories
from camac.urls import urlpatterns as app_patterns
from camac.user import factories as user_factories
from camac.user.models import Group, User
from camac.utils import build_url


def register_module(module, prefix=""):
    # We need to pass the locals of this file to the register method to make
    # sure they are injected on the conftest locals instead of the default
    # locals which would be the locals of this function
    conftest_locals = Box(sys._getframe(1).f_locals)

    for _, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            if prefix:
                # This prefixes only the model fixtures, not the factories
                model_name = get_model_name(obj)
                register(
                    obj,
                    _name=f"{prefix}_{model_name}",
                    _caller_locals=conftest_locals,
                )
            else:
                register(obj, _caller_locals=conftest_locals)


factory_logger = logging.getLogger("factory")
factory_logger.setLevel(logging.INFO)

sorl_thumbnail_logger = logging.getLogger("sorl.thumbnail")
sorl_thumbnail_logger.setLevel(logging.INFO)

register_module(user_factories)
register_module(instance_factories)
register_module(core_factories)
register_module(document_factories)
register_module(dossier_import_factories)
register_module(notification_factories)
register_module(applicant_factories)
register_module(responsible_factories)
register_module(permissions_factories)
register_module(ech_factories)
register_module(objection_factories)
register_module(tags_factories)
register_module(communications_factories)
register_module(gis_factories)
register_module(billing_factories)

# caluma factories
register_module(caluma_form_factories, prefix="caluma")
register_module(caluma_workflow_factories, prefix="caluma")

# do not register alexandria factories, as there are too many conflicts

# TODO: Somehow the ordering of those two calls is relevant.
# Need to figure out why exactly (FreezegunAwareDatetimeProvider's
# methods aren't invoked if it's added first). This is some weird
# bug that I couldn't track down yet.
Faker.add_provider(MultilangProvider)
Faker.add_provider(FreezegunAwareDatetimeProvider)


FORM_QUESTION_MAP_BE = [
    ("main-form", "gemeinde"),
    ("main-form", "is-paper"),
    ("main-form", "baubeschrieb"),
    ("main-form", "personalien-sb"),
    ("main-form", "personalien-gesuchstellerin"),
    ("sb1", "is-paper"),
    ("sb1", "personalien-sb1-sb2"),
    ("sb2", "is-paper"),
    ("nfd", "is-paper"),
    ("decision", "decision-workflow"),
]

FORM_QUESTION_MAP_UR = [
    ("main-form", "is-paper"),
    ("main-form", "municipality"),
    ("main-form", "leitbehoerde"),
    ("main-form", "leitbehoerde-internal-form"),
    ("oereb", "is-paper"),
    ("oereb", "municipality"),
    ("oereb", "leitbehoerde"),
    ("oereb", "leitbehoerde-internal-form"),
    ("oereb-verfahren-gemeinde", "is-paper"),
    ("oereb-verfahren-gemeinde", "municipality"),
    ("oereb-verfahren-gemeinde", "leitbehoerde"),
    ("oereb-verfahren-gemeinde", "leitbehoerde-internal-form"),
]

# FIXME: This should be canton-specific (currently only BE, doesn't make sense for UR/GR
CALUMA_FORM_TYPES_SLUGS = [
    "baugesuch",
    "baugesuch-v2",
    "baugesuch-v3",
    "baugesuch-generell",
    "baugesuch-generell-v2",
    "baugesuch-generell-v3",
    "baugesuch-mit-uvp",
    "baugesuch-mit-uvp-v2",
    "baugesuch-mit-uvp-v3",
    "vorabklaerung-einfach",
    "vorabklaerung-einfach-v4",
    "vorabklaerung-vollstaendig",
    "vorabklaerung-vollstaendig-v2",
    "vorabklaerung-vollstaendig-v3",
    "vorabklaerung-vollstaendig-v4",
    "hecken-feldgehoelze-baeume",
    "baupolizeiliches-verfahren",
    "klaerung-baubewilligungspflicht",
    "zutrittsermaechtigung",
    "verlaengerung-geltungsdauer",
    "building-permit",
    "solaranlagen-meldung",
    "heat-generator",
]


@dataclass
class FakeRequest:
    group: Group
    user: User
    auth: dict = field(default_factory=dict)
    query_params: dict = field(default_factory=dict)
    META: dict = field(default_factory=dict)


@pytest.fixture
def request_mock(mocker, admin_user, group):
    auth = {
        "sub": admin_user.username,
        settings.OIDC_USERNAME_CLAIM: admin_user.username,
    }

    request_mock = mocker.patch(
        "django.test.client.WSGIRequest.caluma_info",
        new_callable=mocker.PropertyMock,
        create=True,
    )
    request_mock.return_value = CalumaInfo(
        FakeRequest(
            user=admin_user,
            group=group,
            auth=auth,
            META={"HTTP_AUTHORIZATION": f"Bearer {jwt_encode(auth,'secret')}"},
        ),
    )


@pytest.fixture
def rf(db):
    return APIRequestFactory()


@pytest.fixture
def admin_user(admin_user, group, group_location, user_group_factory):
    admin_user.username = "462afaba-aeb7-494a-8596-3497b81ed701"
    admin_user.surname = "User"
    admin_user.name = "Admin"
    admin_user.save()
    user_group_factory(group=group, user=admin_user, default_group=1)
    return admin_user


@pytest.fixture
def token(admin_user):
    return jwt_encode(
        {"aud": admin_user.groups.first().name, "username": "joël-tester"}, "secret"
    )


@pytest.fixture
def caluma_admin_user(admin_user, group, token):
    user = OIDCUser(
        token=token,
        claims={
            settings.OIDC_USERNAME_CLAIM: admin_user.username,
            settings.OIDC_GROUPS_CLAIM: [group.service_id],
            "sub": admin_user.username,
        },
    )

    user.camac_role = group.role.name
    user.camac_group = group.pk
    user.group = group.service_id

    return user


@pytest.fixture
def admin_client(db, admin_user, request_mock):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    api_client = APIClient()
    api_client.force_authenticate(user=admin_user)
    api_client.user = admin_user
    return api_client


@pytest.fixture
def override_urls_be():
    BEUrlsConf.urlpatterns += app_patterns
    BEUrlsConf.urlpatterns += [
        path(f"ech/v1/{key}", RedirectView.as_view(url=url))
        for key, url in BEUrlsConf.redirects.items()
    ]
    with override_settings(ROOT_URLCONF=BEUrlsConf):
        yield


@pytest.fixture
def override_urls_sz():
    SZUrlsConf.urlpatterns += app_patterns
    with override_settings(ROOT_URLCONF=SZUrlsConf):
        yield


@pytest.fixture
def set_application_be(settings, override_urls_be):
    application_dict = copy.deepcopy(settings.APPLICATIONS["kt_bern"])
    settings.APPLICATION = application_dict
    settings.APPLICATION_NAME = "kt_bern"
    settings.INTERNAL_BASE_URL = "http://ebau.local"

    return application_dict


@pytest.fixture
def set_application_sz(settings):
    application_dict = copy.deepcopy(settings.APPLICATIONS["kt_schwyz"])
    settings.APPLICATION = application_dict
    settings.APPLICATION_NAME = "kt_schwyz"
    settings.INTERNAL_BASE_URL = "http://ebau.local"
    return application_dict


@pytest.fixture
def set_application_ur(settings):
    application_dict = copy.deepcopy(settings.APPLICATIONS["kt_uri"])
    settings.APPLICATION = application_dict
    settings.APPLICATION_NAME = "kt_uri"
    settings.INTERNAL_BASE_URL = "http://ebau.local"
    return application_dict


@pytest.fixture
def set_application_gr(settings):
    application_dict = copy.deepcopy(settings.APPLICATIONS["kt_gr"])
    settings.APPLICATION = application_dict
    settings.APPLICATION_NAME = "kt_gr"
    settings.INTERNAL_BASE_URL = "http://ember-ebau.local"
    return application_dict


@pytest.fixture
def set_application_so(settings):
    application_dict = copy.deepcopy(settings.APPLICATIONS["kt_so"])
    settings.APPLICATION = application_dict
    settings.APPLICATION_NAME = "kt_so"
    settings.INTERNAL_BASE_URL = "http://ember-ebau.local"
    return application_dict


@pytest.fixture
def application_settings(settings):
    application_dict = copy.deepcopy(settings.APPLICATION)
    # settings fixture only restores per attribute
    # so need to set copy of dict
    settings.APPLICATION = application_dict
    return application_dict


@pytest.fixture
def multilang(application_settings):
    application_settings["IS_MULTILINGUAL"] = True


@pytest.fixture
def use_caluma_form(application_settings):
    application_settings["FORM_BACKEND"] = "caluma"
    application_settings["CALUMA"] = {
        "FORM_PERMISSIONS": ["main", "sb1", "sb2", "nfd", "dossierpruefung"],
        "HAS_PROJECT_CHANGE": True,
        "CREATE_IN_PROCESS": False,
        "USE_LOCATION": False,
        "GENERATE_IDENTIFIER": False,
    }


@pytest.fixture
def support_role(role):
    role.name = "support"
    role.save()
    return role


@pytest.fixture
def system_operation_group(support_role, group):
    group.role = support_role
    group.name = "System-Betrieb"
    group.save()
    return group


@pytest.fixture
def system_operation_user(system_operation_group, user, user_group_factory):
    user_group_factory(group=system_operation_group, user=user, default_group=1)
    user.username = "System-Betrieb"
    user.save()
    return user


@pytest.fixture(autouse=True)
def media_root(tmpdir_factory, settings):
    """Set django's MEDIA_ROOT setting to a temporary directory.

    Otherwise all files that get stored through File- and ImageFields would
    get stored in the project root and pollute it.
    """
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media_root")


@pytest.fixture
def clear_cache():
    cache.clear()


@pytest.fixture
def unoconv_pdf_mock(requests_mock):
    requests_mock.register_uri(
        "POST",
        build_url(settings.UNOCONV_URL, "/unoconv/pdf"),
        content=django_file("multiple-pages.pdf").read(),
    )


@pytest.fixture
def unoconv_invalid_mock(requests_mock):
    requests_mock.register_uri(
        "POST",
        build_url(settings.UNOCONV_URL, "/unoconv/invalid"),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@pytest.fixture
def caluma_config_be(
    settings, application_settings, use_caluma_form, be_master_data_settings
):
    application_settings["CALUMA"] = deepcopy(
        settings.APPLICATIONS["kt_bern"]["CALUMA"]
    )


@pytest.fixture
def caluma_config_ur(
    settings, application_settings, use_caluma_form, ur_master_data_settings
):
    application_settings["CALUMA"] = deepcopy(settings.APPLICATIONS["kt_uri"]["CALUMA"])


@pytest.fixture
def caluma_config_sz(
    settings, application_settings, use_caluma_form, sz_master_data_settings
):
    application_settings["CALUMA"] = deepcopy(
        settings.APPLICATIONS["kt_schwyz"]["CALUMA"]
    )
    application_settings["FORM_BACKEND"] = "camac-ng"


@pytest.fixture
def caluma_config_gr(
    settings, application_settings, use_caluma_form, gr_master_data_settings
):
    application_settings["CALUMA"] = deepcopy(settings.APPLICATIONS["kt_gr"]["CALUMA"])


@pytest.fixture
def caluma_config_so(
    settings, application_settings, use_caluma_form, so_master_data_settings
):
    application_settings["CALUMA"] = deepcopy(settings.APPLICATIONS["kt_so"]["CALUMA"])


@pytest.fixture
def use_instance_service(application_settings):
    application_settings["USE_INSTANCE_SERVICE"] = True
    application_settings["ACTIVE_SERVICES"] = deepcopy(
        settings.APPLICATIONS["kt_bern"]["ACTIVE_SERVICES"]
    )
    application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {}
    application_settings["ACTIVE_SERVICES"]["CONSTRUCTION_CONTROL"]["FILTERS"] = {}

    yield application_settings

    application_settings["USE_INSTANCE_SERVICE"] = False


@pytest.fixture
def caluma_workflow_config_be(
    settings, caluma_forms_be, caluma_config_be, use_instance_service
):
    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_bern/config/caluma_distribution.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_legal_submission_form.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_appeal_form.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_workflow.json"),
    )

    workflows = caluma_workflow_models.Workflow.objects.all()
    main_form = caluma_form_models.Form.objects.get(pk="main-form")

    workflows.update(allow_all_forms=True)

    for workflow in workflows.filter(
        pk__in=["building-permit", "preliminary-clarification"]
    ):
        workflow.allow_forms.clear()
        workflow.allow_forms.add(main_form)
        workflow.save()

    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()

    yield workflows

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


@pytest.fixture
def caluma_workflow_config_ur(
    settings,
    caluma_forms_ur,
    caluma_config_ur,
    application_settings,
    notification_template,
):
    def transform_notifications(notifications):
        if isinstance(notifications, dict):
            return notifications
        return [
            {
                "template_slug": notification_template.slug,
                "recipient_types": n["recipient_types"],
            }
            for n in notifications
        ]

    application_settings["NOTIFICATIONS"] = {
        task: transform_notifications(notifications)
        for task, notifications in settings.APPLICATIONS["kt_uri"][
            "NOTIFICATIONS"
        ].items()
    }

    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command("loaddata", settings.ROOT_DIR("kt_uri/config/caluma_workflow.json"))

    workflow = caluma_workflow_models.Workflow.objects.first()
    main_form = caluma_form_models.Form.objects.get(pk="main-form")

    workflow.allow_forms.clear()
    workflow.allow_forms.add(main_form)
    workflow.save()

    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()

    yield workflow

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


@pytest.fixture
def caluma_workflow_config_gr(
    settings,
    caluma_forms_gr,
    caluma_config_gr,
):
    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_gr/config/caluma_workflow.json"),
        settings.ROOT_DIR("kt_bern/config/caluma_distribution.json"),
    )

    workflow = caluma_workflow_models.Workflow.objects.first()
    main_form = caluma_form_models.Form.objects.get(pk="main-form")

    workflow.allow_forms.clear()
    workflow.allow_forms.add(main_form)
    workflow.save()

    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()

    yield workflow

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


@pytest.fixture
def caluma_workflow_config_so(
    settings,
    caluma_forms_so,
    caluma_config_so,
):
    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_so/config/caluma_workflow.json"),
        settings.ROOT_DIR("kt_so/config/caluma_distribution.json"),
        settings.ROOT_DIR("kt_so/config/caluma_additional_demand.json"),
        settings.ROOT_DIR("kt_so/config/caluma_objection_form.json"),
    )

    workflows = caluma_workflow_models.Workflow.objects.all()
    main_form = caluma_form_models.Form.objects.get(pk="main-form")

    workflows.update(allow_all_forms=True)

    workflow = workflows.get(pk="building-permit")
    workflow.allow_forms.clear()
    workflow.allow_forms.add(main_form)
    workflow.save()

    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()

    yield workflow

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


@pytest.fixture
def caluma_audit(caluma_workflow_config_be):
    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/caluma_audit_form.json"))
    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()


@pytest.fixture
def caluma_publication(caluma_workflow_config_be):
    for slug in CALUMA_FORM_TYPES_SLUGS:
        caluma_form_models.Form.objects.create(slug=slug)

    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_publication_form.json")
    )
    caluma_form_models.Form.objects.filter(pk__in=CALUMA_FORM_TYPES_SLUGS).delete()


@pytest.fixture
def caluma_workflow_config_sz(db, caluma_config_sz):
    caluma_form_models.Form.objects.create(slug="baugesuch")
    caluma_form_models.Form.objects.create(slug="bauverwaltung")
    caluma_form_models.Form.objects.create(slug="main-form")

    call_command(
        "loaddata",
        settings.ROOT_DIR("kt_schwyz/config/caluma_workflow.json"),
        settings.ROOT_DIR("kt_schwyz/config/caluma_distribution.json"),
    )

    yield caluma_workflow_models.Workflow.objects.all()

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


def yes(lang):
    return "ja" if lang == "de" else "yes"


def no(lang):
    return "nein" if lang == "de" else "no"


@pytest.fixture
def caluma_forms_be(settings):
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form",
        meta={"is-main-form": True},
        name={"de": "Baugesuch", "fr": "Demande de permis de construire"},
    )
    caluma_form_models.Form.objects.create(slug="sb1")
    caluma_form_models.Form.objects.create(slug="sb2")
    caluma_form_models.Form.objects.create(slug="nfd")
    caluma_form_models.Form.objects.create(slug="migriertes-dossier")
    caluma_form_models.Form.objects.create(slug="dossierpruefung")
    caluma_form_models.Form.objects.create(slug="publikation")
    caluma_form_models.Form.objects.create(slug="information-of-neighbors")
    caluma_form_models.Form.objects.create(slug="ebau-number")
    caluma_form_models.Form.objects.create(slug="decision")
    caluma_form_models.Form.objects.create(slug="geometer")

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    caluma_form_models.Question.objects.create(
        slug="gemeinde",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    settings.DATA_SOURCE_CLASSES = [
        "camac.caluma.extensions.data_sources.Municipalities"
    ]

    caluma_form_models.Question.objects.create(
        slug="decision-workflow", type=caluma_form_models.Question.TYPE_TEXT
    )

    for slug, lang in [("is-paper", "en"), ("projektaenderung", "de")]:
        question = caluma_form_models.Question.objects.create(
            slug=slug, type=caluma_form_models.Question.TYPE_CHOICE
        )
        options = [
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{yes(lang)}", label="Ja"
            ),
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{no(lang)}", label="Nein"
            ),
        ]
        for option in options:
            caluma_form_models.QuestionOption.objects.create(
                question=question, option=option
            )

    # some question for suggestions
    question = caluma_form_models.Question.objects.create(
        slug="baubeschrieb", type=caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
    )
    caluma_form_models.QuestionOption.objects.create(
        question=question,
        option=caluma_form_models.Option.objects.create(
            slug="baubeschrieb-erweiterung-anbau", label="Erweiterung Anbau"
        ),
    )
    caluma_form_models.QuestionOption.objects.create(
        question=question,
        option=caluma_form_models.Option.objects.create(
            slug="baubeschrieb-um-ausbau", label="Um- oder Ausbau"
        ),
    )
    question = caluma_form_models.Question.objects.create(
        slug="art-versickerung-dach", type=caluma_form_models.Question.TYPE_TEXT
    )
    caluma_form_models.Question.objects.create(
        slug="beschreibung-bauvorhaben", type=caluma_form_models.Question.TYPE_TEXT
    )

    # sb1 and sb2
    applicant_table = caluma_form_models.Form.objects.create(slug="personalien-tabelle")
    caluma_form_models.Form.objects.create(slug="rechnungsempfaengerin-tabelle")

    caluma_form_models.Question.objects.create(
        slug="personalien-sb",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="personalien-gesuchstellerin",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="personalien-sb1-sb2",
        type=caluma_form_models.Question.TYPE_TABLE,
        row_form=applicant_table,
    )
    caluma_form_models.Question.objects.create(
        slug="name-sb", type=caluma_form_models.Question.TYPE_TEXT
    )
    caluma_form_models.Question.objects.create(
        slug="name-applicant", type=caluma_form_models.Question.TYPE_TEXT
    )

    # main form
    question = caluma_form_models.Question.objects.create(
        slug="vorname-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )
    question = caluma_form_models.Question.objects.create(
        slug="name-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )

    # migrated
    geschaeftstyp = caluma_form_models.Question.objects.create(
        slug="geschaeftstyp", type=caluma_form_models.Question.TYPE_CHOICE
    )
    caluma_form_models.QuestionOption.objects.create(
        question=geschaeftstyp,
        option=caluma_form_models.Option.objects.create(
            slug="geschaeftstyp-baupolizeiliches-verfahren",
            label="Baupolizeiliches Verfahren",
        ),
    )

    # link questions with forms
    for form_id, question_id in FORM_QUESTION_MAP_BE:
        caluma_form_models.FormQuestion.objects.create(
            form_id=form_id, question_id=question_id
        )


@pytest.fixture
def caluma_forms_ur(settings):
    # forms
    for counter, form in enumerate(["main-form", "oereb", "oereb-verfahren-gemeinde"]):
        caluma_form_models.Form.objects.create(
            slug=form, meta={"is-main-form": True, "camac-form-id": counter}, name=form
        )

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    simple_questions = [
        ("municipality", caluma_form_models.Question.TYPE_TEXT),
        ("leitbehoerde", caluma_form_models.Question.TYPE_TEXT),
        ("leitbehoerde-internal-form", caluma_form_models.Question.TYPE_DYNAMIC_CHOICE),
    ]
    for slug, type in simple_questions:
        caluma_form_models.Question.objects.create(slug=slug, type=type)

    form_type_question = caluma_form_models.Question.objects.create(
        slug="form-type",
        type=caluma_form_models.Question.TYPE_CHOICE,
    )
    form_type_option = caluma_form_models.Option.objects.create(
        slug="form-type-camac-form", label="Camac Form"
    )
    caluma_form_models.QuestionOption.objects.create(
        question=form_type_question, option=form_type_option
    )

    settings.DATA_SOURCE_CLASSES = ["camac.caluma.extensions.data_sources.Locations"]

    for slug, lang in [("is-paper", "en"), ("projektaenderung", "de")]:
        question = caluma_form_models.Question.objects.create(
            slug=slug, type=caluma_form_models.Question.TYPE_CHOICE
        )
        options = [
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{yes(lang)}", label="Ja"
            ),
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{no(lang)}", label="Nein"
            ),
        ]
        for option in options:
            caluma_form_models.QuestionOption.objects.create(
                question=question, option=option
            )

    # link questions with forms
    for form_id, question_id in FORM_QUESTION_MAP_UR:
        caluma_form_models.FormQuestion.objects.create(
            form_id=form_id, question_id=question_id
        )


@pytest.fixture
def caluma_forms_gr(settings):
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form", meta={"is-main-form": True}, name="Baugesuch"
    )
    caluma_form_models.Form.objects.create(slug="dossierpruefung")
    caluma_form_models.Form.objects.create(slug="decision")
    caluma_form_models.Form.objects.create(slug="formal-exam")
    caluma_form_models.Form.objects.create(slug="material-exam")
    caluma_form_models.Form.objects.create(slug="publikation")
    caluma_form_models.Form.objects.create(slug="construction-monitoring")

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    caluma_form_models.Question.objects.create(
        slug="gemeinde",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    settings.DATA_SOURCE_CLASSES = [
        "camac.caluma.extensions.data_sources.Municipalities"
    ]

    for slug, lang in [("is-paper", "en"), ("projektaenderung", "de")]:
        question = caluma_form_models.Question.objects.create(
            slug=slug, type=caluma_form_models.Question.TYPE_CHOICE
        )
        options = [
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{yes(lang)}", label="Ja"
            ),
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{no(lang)}", label="Nein"
            ),
        ]
        for option in options:
            caluma_form_models.QuestionOption.objects.create(
                question=question, option=option
            )

    caluma_form_models.Question.objects.create(
        slug="beschreibung-bauvorhaben", type=caluma_form_models.Question.TYPE_TEXT
    )

    # main form
    question = caluma_form_models.Question.objects.create(
        slug="vorname-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )
    question = caluma_form_models.Question.objects.create(
        slug="name-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )


@pytest.fixture
def caluma_forms_so(settings):
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form", meta={"is-main-form": True}, name="Baugesuch"
    )
    caluma_form_models.Form.objects.create(slug="formelle-pruefung")
    caluma_form_models.Form.objects.create(slug="materielle-pruefung")
    caluma_form_models.Form.objects.create(slug="entscheid")
    caluma_form_models.Form.objects.create(slug="publikation")
    caluma_form_models.Form.objects.create(slug="erdwaermesonden")
    caluma_form_models.Form.objects.create(slug="personalien-tabelle")

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    caluma_form_models.Question.objects.create(
        slug="gemeinde",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    settings.DATA_SOURCE_CLASSES = [
        "camac.caluma.extensions.data_sources.Municipalities"
    ]

    for slug, lang in [("is-paper", "en"), ("projektaenderung", "de")]:
        question = caluma_form_models.Question.objects.create(
            slug=slug, type=caluma_form_models.Question.TYPE_CHOICE
        )
        options = [
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{yes(lang)}", label="Ja"
            ),
            caluma_form_models.Option.objects.create(
                slug=f"{slug}-{no(lang)}", label="Nein"
            ),
        ]
        for option in options:
            caluma_form_models.QuestionOption.objects.create(
                question=question, option=option
            )

    caluma_form_models.Question.objects.create(
        slug="beschreibung-bauvorhaben", type=caluma_form_models.Question.TYPE_TEXT
    )


@pytest.fixture
def portal_group(application_settings, group_factory):
    group = group_factory()
    application_settings["PORTAL_GROUP"] = group.pk
    return group


@pytest.fixture
def portal_user(portal_group, user_factory, user_group_factory):
    user = user_factory()
    user_group_factory(group=portal_group, user=user, default_group=1)
    return user


@pytest.fixture
def instance_with_case(db, caluma_admin_user):
    def wrapper(instance, workflow="building-permit", form="main-form", context={}):
        instance.case = workflow_api.start_case(
            workflow=caluma_workflow_models.Workflow.objects.get(pk=workflow),
            form=caluma_form_models.Form.objects.get(pk=form),
            user=caluma_admin_user,
            context={**context, "instance": instance.pk},
        )
        instance.save()

        return instance

    return wrapper


@pytest.fixture
def be_instance(
    instance_service,
    caluma_workflow_config_be,
    instance_with_case,
    distribution_settings,
):
    instance = instance_with_case(
        instance_service.instance, context={"instance": instance_service.instance}
    )
    instance.case.meta.update(
        {
            "submit-date": instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
            "paper-submit-date": instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
        }
    )
    instance.case.save()
    return instance


@pytest.fixture
def sz_instance(instance, caluma_workflow_config_sz, instance_with_case):
    return instance_with_case(instance, form="baugesuch")


@pytest.fixture
def ur_instance(instance, caluma_workflow_config_ur, instance_with_case):
    return instance_with_case(instance)


@pytest.fixture
def gr_instance(instance, caluma_workflow_config_gr, instance_with_case):
    return instance_with_case(instance)


@pytest.fixture
def so_instance(instance, caluma_workflow_config_so, instance_with_case):
    return instance_with_case(instance)


@pytest.fixture
def construction_control_for(service_factory):
    """Return a function that turns a service into a "Leitbehörde" and create a "Baukontrolle" along with it."""

    def wrapper(service):
        service.trans.update(name="Leitbehörde XY")
        service.service_group.name = "municipality"
        service.service_group.save()

        return service_factory(
            trans__name="Baukontrolle XY", service_group__name="construction-control"
        )

    return wrapper


@pytest.fixture
def sz_person_factory(db, form_field_factory, faker):
    def wrapper(sz_instance, role, title=None):
        new_person = {
            "anrede": title or faker.prefix_nonbinary(),
            "vorname": faker.first_name(),
            "name": faker.last_name(),
            "firma": faker.company(),
            "strasse": faker.street_name(),
            "plz": faker.pyint(min_value=1000, max_value=9999),
            "ort": faker.city(),
        }
        role_persons, created = sz_instance.fields.get_or_create(
            name=role, defaults={"value": [new_person]}
        )
        if not created:  # pragma: no cover
            role_persons.value += new_person
            role_persons.save()
        return role_persons

    return wrapper


@pytest.fixture
def sz_master_data_case(db, sz_instance, form_field_factory, workflow_entry_factory):
    # Simple data
    form_field_factory(instance=sz_instance, name="bezeichnung", value="Grosses Haus")
    form_field_factory(instance=sz_instance, name="baukosten", value=129000)

    # Applicant
    form_field_factory(
        instance=sz_instance,
        name="bauherrschaft",
        value=[
            {
                "anrede": "Herr",
                "vorname": "Max",
                "name": "Mustermann",
                "firma": "ACME AG",
                "strasse": "Teststrasse 2",
                "plz": 1233,
                "ort": "Musterdorf",
            }
        ],
    )

    # Applicant V2
    form_field_factory(
        instance=sz_instance,
        name="bauherrschaft-v2",
        value=[
            {
                "anrede": "Herr",
                "vorname": "Max",
                "name": "Mustermann",
                "firma": "ACME AG",
                "strasse": "Teststrasse 2",
                "plz": 1233,
                "ort": "Musterdorf",
            }
        ],
    )

    # Applicant override (Vollständigkeitsprüfung)
    form_field_factory(
        instance=sz_instance,
        name="bauherrschaft-override",
        value=[
            {
                "anrede": "Herr",
                "vorname": "Max",
                "name": "Mustermann",
                "firma": "ACME AG",
                "strasse": "Teststrasse 3",
                "plz": 5678,
                "ort": "Musterdorf",
            }
        ],
    )

    # Plot data
    form_field_factory(
        instance=sz_instance,
        name="parzellen",
        value=[
            {
                "number": 1234,
                "egrid": "CH1234567890",
            }
        ],
    )

    return sz_instance.case


@pytest.fixture
def decision_factory(be_instance, document_factory, work_item_factory):
    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_decision_form.json")
    )

    def factory(
        instance=be_instance,
        decision="decision-decision-assessment-accepted",
        decision_type="decision-approval-type-building-permit",
        decision_date=date.today(),
        decision_geometer="decision-geometer-no",
    ):
        work_item = instance.case.work_items.filter(task_id="decision").first()

        if not work_item:
            work_item = work_item_factory(
                case=instance.case,
                task_id="decision",
                status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
                document=document_factory(form_id="decision"),
            )

        if decision:
            work_item.document.answers.create(
                question_id="decision-decision-assessment", value=decision
            )
        if decision_type:
            work_item.document.answers.create(
                question_id="decision-approval-type", value=decision_type
            )
        if decision_date:
            work_item.document.answers.create(
                question_id="decision-date", date=decision_date
            )

        if decision_geometer:
            work_item.document.answers.create(
                question_id="decision-geometer",
                value=decision_geometer,
            )

        return work_item

    return factory


@pytest.fixture
def active_inquiry_factory(
    instance, service, distribution_settings, work_item_factory, answer_factory
):
    def factory(
        for_instance=instance,
        addressed_service=service,
        controlling_service=service,
        **kwargs,
    ):
        distribution_work_item = for_instance.case.work_items.filter(
            task_id=distribution_settings["DISTRIBUTION_TASK"]
        ).first()

        if not distribution_work_item:
            distribution_work_item = work_item_factory(
                task_id=distribution_settings["DISTRIBUTION_TASK"],
                status=caluma_workflow_models.WorkItem.STATUS_READY,
                case=for_instance.case,
                addressed_groups=[str(service.pk)],
                child_case__family=for_instance.case,
                child_case__workflow_id=distribution_settings["DISTRIBUTION_WORKFLOW"],
            )

        assert distribution_work_item.child_case.family == for_instance.case

        inquiry = work_item_factory(
            case=distribution_work_item.child_case,
            task_id=distribution_settings["INQUIRY_TASK"],
            addressed_groups=[str(addressed_service.pk)],
            controlling_groups=[str(controlling_service.pk)],
            child_case__family=for_instance.case,
            child_case__workflow_id=distribution_settings["INQUIRY_WORKFLOW"],
            child_case__document__form_id=distribution_settings["INQUIRY_ANSWER_FORM"],
            document__form_id=distribution_settings["INQUIRY_FORM"],
            status=kwargs.pop("status", caluma_workflow_models.WorkItem.STATUS_READY),
            deadline=kwargs.pop("deadline", make_aware(faker.Faker().date_time())),
            **kwargs,
        )

        if kwargs.get("created_at"):
            inquiry.created_at = kwargs.get("created_at")
            inquiry.save()
            inquiry.child_case.created_at = kwargs.get("created_at")
            inquiry.child_case.save()

        answer_factory(
            document=inquiry.document,
            question_id=distribution_settings["QUESTIONS"]["DEADLINE"],
            value=None,
            date=inquiry.deadline.date(),
        )

        return inquiry

    return factory


@pytest.fixture
def master_data_is_visible_mock(mocker):
    mocker.patch(
        "camac.instance.master_data.MasterData._answer_is_visible", return_value=True
    )


@pytest.fixture
def gql():
    """Fixture to load GraphQL files as string into tests.

    By default the function will look for the file in a sibling directory "gql"
    of the test file. For example:

    `gql("foo")` called in `/a/b/tests/test.py` will resolve to
    `/a/b/tests/gql/foo.graphql`.

    If this behaviour is not preferred, you can also pass a path directly to the
    function as a second parameter.
    """

    def wrapper(name, path=None):
        if not path:
            base = os.path.dirname(
                inspect.getouterframes(inspect.currentframe())[1].filename
            )
            path = os.path.join(base, "gql")

        file = os.path.join(path, f"{name}.graphql")

        return Path(file).read_text()

    return wrapper


@pytest.fixture
def minio_mock(mocker):
    stat_response = MinioStatObject(
        # taken from a real-world minio stat() call
        bucket_name="alexandria-media",
        object_name="a3d0429d-5400-47ac-9d02-124592302631_attack.wav",
        etag="5d41402abc4b2a76b9719d911017c592",
        size=8200,
        last_modified=datetime(2021, 3, 5, 15, 24, 33, tzinfo=timezone.utc),
        content_type="application/pdf",
        metadata=urllib3._collections.HTTPHeaderDict(
            {
                "Accept-Ranges": "bytes",
                "Content-Length": "5",
                "Content-Security-Policy": "block-all-mixed-content",
                "Content-Type": "binary/octet-stream",
                "ETag": '"5d41402abc4b2a76b9719d911017c592"',
                "Last-Modified": "Fri, 05 Mar 2021 15:24:33 GMT",
                "Server": "MinIO",
                "Vary": "Origin",
                "X-Amz-Request-Id": "16697BAAD69D2214",
                "X-Xss-Protection": "1; mode=block",
                "Date": "Fri, 05 Mar 2021 15:25:15 GMT",
            }
        ),
        owner_id=None,
        owner_name=None,
        storage_class=None,
        version_id=None,
    )
    mocker.patch.object(Minio, "presigned_get_object")
    mocker.patch.object(Minio, "presigned_put_object")
    mocker.patch.object(Minio, "stat_object")
    mocker.patch.object(Minio, "bucket_exists")
    mocker.patch.object(Minio, "make_bucket")
    mocker.patch.object(Minio, "remove_object")
    mocker.patch.object(Minio, "copy_object")
    mocker.patch.object(Minio, "put_object")
    Minio.presigned_put_object.return_value = "http://minio/upload-url"
    Minio.stat_object.return_value = stat_response
    Minio.bucket_exists.return_value = True

    mocker.patch("storages.backends.s3.S3Storage.save")
    mocker.patch("storages.backends.s3.S3Storage.open")
    SsecGlobalS3Storage.save.return_value = "name-of-the-file"
    SsecGlobalS3Storage.open.return_value = django_file("multiple-pages.pdf")
    return Minio


@pytest.fixture
def enable_ech(application_settings):
    application_settings["ECH0211"]["API_ACTIVE"] = True
    application_settings["ECH0211"]["API_LEVEL"] = "full"
    application_settings["DOSSIER_IMPORT"]["PROD_URL"] = "ebau.local"


@pytest.fixture
def notification_add_recipient_type():  # pragma: todo cover
    """Add notification module recipient type.

    The notification module allows configuring custom (canton-specific) recipient
    types. As those are setup at startup, we need a way to add the canton-specific
    ones for testing. This is the tool to do that.
    """

    # Hocus Pocus...

    rt_field = PermissionlessNotificationTemplateSendmailSerializer._declared_fields[
        "recipient_types"
    ]
    original_kwargs_choices = rt_field._kwargs["choices"]
    original_choices = rt_field.choices

    def do_the_magic(name):
        # don't extend, we need to call the setter
        rt_field._set_choices({**rt_field.choices, name: name})
        # some parts of the field use the `kwargs` as it was stored during
        # construction time, not the actual "choices" field that you could
        # even "officially" set...
        rt_field._kwargs["choices"] = rt_field._kwargs["choices"] + (name,)

    yield do_the_magic

    rt_field._set_choices(original_choices)
    rt_field._kwargs["choices"] = original_kwargs_choices


@pytest.fixture
def configure_custom_notification_types(
    notification_add_recipient_type, settings
):  # pragma: todo cover
    """Configure custom notification types in the notification serializer.

    The notification module allows configuring custom (canton-specific) recipient
    types. As those are setup at startup, we need a way to add the canton-specific
    ones for testing. This is the tool to do that. You need to call this fixture
    *inside* the test function, to ensure the notification module's serializer
    is properly configured.

    Example:
    >>> test_foo(configure_custom_notification_types, settings):
    >>>    settings.APPLICATION = { ... }
    >>>    # need to configure the notification types
    >>>    configure_custom_notification_types()
    """

    callstate = {}

    def do_it():
        callstate["x"] = 1
        for notification_type in settings.APPLICATION["CUSTOM_NOTIFICATION_TYPES"]:
            notification_add_recipient_type(notification_type)

    yield do_it

    if not callstate:  # pragma: no cover
        raise RuntimeError(
            "configure_custom_notification_types fixture used but not called. "
            "You need to call configure_custom_notification_types inside your "
            "test to make it work"
        )


class Utils:
    @staticmethod
    def _question(slug, type, label=None, options=None):
        question = caluma_form_models.Question.objects.filter(pk=slug).first()
        if question is None:
            question = caluma_form_factories.QuestionFactory(
                pk=slug,
                type=type,
                **({"label": label} if label else {}),
            )
        if options:
            for option in options:
                caluma_form_factories.QuestionOptionFactory(
                    question=question,
                    option__slug=option,
                    option__label=option.capitalize(),
                )
        return question

    @staticmethod
    def _get_question_type(value, options):
        if options:
            if isinstance(value, list):  # pragma: no cover
                return caluma_form_models.Question.TYPE_MULTIPLE_CHOICE
            return caluma_form_models.Question.TYPE_CHOICE
        if isinstance(value, date):
            return caluma_form_models.Question.TYPE_DATE
        if isinstance(value, int):
            return caluma_form_models.Question.TYPE_INTEGER
        return caluma_form_models.Question.TYPE_TEXT

    @staticmethod
    def add_answer(
        document,
        question,
        value,
        label=None,
        question_label=None,
        options=None,
    ):
        question_type = Utils._get_question_type(value, options)
        value_key = (
            "date"
            if question_type == caluma_form_models.Question.TYPE_DATE
            else "value"
        )

        answer = caluma_form_factories.AnswerFactory(
            document=document,
            question=Utils._question(question, question_type, question_label, options),
            **{value_key: value},
        )

        if label:
            if not isinstance(label, list):
                label = [label]

            if not isinstance(value, list):
                value = [value]

            for val, lab in zip(value, label):
                if not isinstance(lab, dict):
                    lab = {"de": lab, "fr": lab}

                caluma_form_factories.QuestionOptionFactory(
                    question_id=question, option__slug=val, option__label=lab
                )

        return answer

    @staticmethod
    def add_table_answer(document, question, rows, table_answer=None, row_form_id=None):
        answer = (
            Utils.add_answer(document, question, None)
            if not table_answer
            else table_answer
        )

        for i, row in enumerate(reversed(rows)):
            row_args = {"form_id": row_form_id} if row_form_id else {}
            row_document = caluma_form_factories.DocumentFactory(
                family=document.family, **row_args
            )
            for column, value in row.items():
                options = None
                if isinstance(value, dict):
                    options = value["options"]
                    value = value["value"]
                Utils.add_answer(row_document, column, value, options=options)

            caluma_form_factories.AnswerDocumentFactory(
                document=row_document, answer=answer, sort=i
            )

        return answer


@pytest.fixture
def utils():
    return Utils


@pytest.fixture
def ur_master_data_case(
    db,
    ur_instance,
    workflow_entry_factory,
    camac_answer_factory,
    master_data_is_visible_mock,
    utils,
):
    ur_instance.case.meta = {"dossier-number": "1201-21-003"}
    ur_instance.case.save()

    document = ur_instance.case.document

    # Simple data
    utils.add_answer(document, "proposal-description", "Grosses Haus")
    utils.add_answer(document, "parcel-street", "Musterstrasse")
    utils.add_answer(document, "parcel-street-number", 4)
    utils.add_answer(document, "construction-cost", 129000)
    utils.add_answer(document, "parcel-city", "Musterdorf")
    utils.add_answer(document, "category", ["category-hochbaute", "category-tiefbaute"])
    utils.add_answer(document, "veranstaltung-art", ["veranstaltung-art-umbau"])
    utils.add_answer(document, "oereb-thema", ["oereb-thema-knp"])
    utils.add_answer(document, "form-type", ["form-type-oereb"])
    utils.add_answer(document, "typ-des-verfahrens", ["typ-des-verfahrens-genehmigung"])

    # Municipality
    utils.add_answer(document, "municipality", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="municipality",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Altdorf"},
    )

    # Authority
    utils.add_answer(document, "leitbehoerde", "1")
    caluma_form_factories.DynamicOptionFactory(
        question_id="leitbehoerde",
        document=ur_instance.case.document,
        slug="1",
        label={"de": "Leitbehörde Altdorf"},
    )

    # Plot
    utils.add_table_answer(
        document,
        "parcels",
        [
            {
                "parcel-number": 123456789,
                "e-grid": "CH123456789",
                "coordinates-east": 2690970.9,
                "coordinates-north": 1192891.9,
            }
        ],
    )

    # Applicant
    utils.add_table_answer(
        document,
        "applicant",
        [
            {
                "first-name": "Max",
                "last-name": "Mustermann",
                "is-juristic-person": "is-juristic-person-yes",
                "juristic-person-name": "ACME AG",
                "street": "Teststrasse",
                "street-number": 123,
                "zip": 1233,
                "city": "Musterdorf",
                "country": "Schweiz",
            }
        ],
    )

    # Submit date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-16 08:00:06+00",
        group=1,
        workflow_item__pk=12,
    )

    # Decision date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-20 08:00:06+00",
        group=1,
        workflow_item__pk=47,
    )

    # Construction start date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-25 08:00:06+00",
        group=1,
        workflow_item__pk=55,
    )

    # Construction end date
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-07-30 08:00:06+00",
        group=1,
        workflow_item__pk=67,
    )

    # Approval reason
    camac_answer_factory(answer=5031, question__question_id=264, instance=ur_instance)

    # Type of applicant
    camac_answer_factory(
        answer=6141,
        question__question_id=267,
        instance=ur_instance,
    )

    # Buildings
    utils.add_table_answer(
        document,
        "gebaeude",
        [
            {
                "art-der-hochbaute": "art-der-hochbaute-parkhaus",
                "gebaeudenummer-bezeichnung": "Villa",
                "proposal": ["proposal-neubau"],
                "gebaeudekategorie": "gebaeudekategorie-ohne-wohnnutzung",
            }
        ],
    )

    # Dwellings
    utils.add_table_answer(
        document,
        "wohnungen",
        [
            {
                "zugehoerigkeit": "Villa",
                "stockwerktyp": "stockwerktyp-obergeschoss",
                "stockwerknummer": "2",
                "lage": "Süd",
                "wohnungsgroesse": "20",
                "kocheinrichtung": "kocheinrichtung-kochnische-greater-4-m2",
                "flaeche-in-m2": "420",
                "mehrgeschossige-wohnung": "mehrgeschossige-wohnung-ja",
                "zwg": "zwg-keine",
            },
            {
                "zugehoerigkeit": "Villa",
                "stockwerktyp": "stockwerktyp-parterre",
                "lage": "Nord",
                "wohnungsgroesse": "10",
                "kocheinrichtung": "kocheinrichtung-keine-kocheinrichtung",
                "flaeche-in-m2": "72",
                "mehrgeschossige-wohnung": "mehrgeschossige-wohnung-nein",
                "zwg": "zwg-erstwohnung",
            },
        ],
    )

    # Energy devices
    utils.add_table_answer(
        document,
        "haustechnik-tabelle",
        [
            {
                "gehoert-zu-gebaeudenummer": "Villa",
                "anlagetyp": "anlagetyp-hauptheizung",
                "heizsystem-art": "-hauptheizung",
                "hauptheizungsanlage": "hauptheizungsanlage-sonne-thermisch",
            },
        ],
    )

    return ur_instance.case
