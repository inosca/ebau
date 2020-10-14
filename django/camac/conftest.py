import inspect
import logging
from dataclasses import dataclass

import pytest
from caluma.caluma_core.faker import MultilangProvider
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_workflow import (
    factories as caluma_workflow_factories,
    models as caluma_workflow_models,
)
from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.utils import timezone
from factory import Faker
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from pytest_factoryboy.fixture import get_model_name
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from camac.applicants import factories as applicant_factories
from camac.core import factories as core_factories
from camac.document import factories as document_factories
from camac.document.tests.data import django_file
from camac.echbern import factories as ech_factories
from camac.faker import FreezegunAwareDatetimeProvider
from camac.instance import factories as instance_factories
from camac.notification import factories as notification_factories
from camac.objection import factories as objection_factories
from camac.responsible import factories as responsible_factories
from camac.user import factories as user_factories
from camac.user.authentication import CalumaInfo
from camac.user.models import Group, User
from camac.utils import build_url


def register_module(module, prefix=""):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            if prefix:
                # This prefixes only the model fixtures, not the factories
                model_name = get_model_name(obj)
                register(obj, _name=f"{prefix}_{model_name}")
            else:
                register(obj)


factory_logger = logging.getLogger("factory")
factory_logger.setLevel(logging.INFO)

sorl_thumbnail_logger = logging.getLogger("sorl.thumbnail")
sorl_thumbnail_logger.setLevel(logging.INFO)

register_module(user_factories)
register_module(instance_factories)
register_module(core_factories)
register_module(document_factories)
register_module(notification_factories)
register_module(applicant_factories)
register_module(responsible_factories)
register_module(ech_factories)
register_module(objection_factories)

# caluma factories
register_module(caluma_form_factories, prefix="caluma")
register_module(caluma_workflow_factories, prefix="caluma")

# TODO: Somehow the ordering of those two calls is relevant.
# Need to figure out why exactly (FreezegunAwareDatetimeProvider's
# methods aren't invoked if it's added first). This is some weird
# bug that I couldn't track down yet.
Faker.add_provider(MultilangProvider)
Faker.add_provider(FreezegunAwareDatetimeProvider)


FORM_QUESTION_MAP = [
    ("main-form", "gemeinde"),
    ("main-form", "municipality"),  # Kt. UR
    ("main-form", "is-paper"),
    ("main-form", "baubeschrieb"),
    ("main-form", "personalien-sb"),
    ("main-form", "personalien-gesuchstellerin"),
    ("sb1", "is-paper"),
    ("sb1", "personalien-sb1-sb2"),
    ("sb2", "is-paper"),
    ("nfd", "is-paper"),
]


@dataclass
class FakeRequest:
    group: Group
    user: User


@pytest.fixture
def request_mock(mocker):
    request_mock = mocker.patch(
        "django.test.client.WSGIRequest.caluma_info",
        new_callable=mocker.PropertyMock,
        create=True,
    )
    request_mock.return_value = CalumaInfo(
        {
            "sub": "462afaba-aeb7-494a-8596-3497b81ed701",
            settings.OIDC_USERNAME_CLAIM: "foo",
        }
    )


@pytest.fixture
def rf(db):
    return APIRequestFactory()


@pytest.fixture
def admin_user(admin_user, group, group_location, user_group_factory):
    admin_user.username = "462afaba-aeb7-494a-8596-3497b81ed701"
    admin_user.surname = "Admin"
    admin_user.name = "User"
    admin_user.save()
    user_group_factory(group=group, user=admin_user, default_group=1)
    return admin_user


@pytest.fixture
def admin_client(db, admin_user, request_mock):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    client.user = admin_user
    return client


@pytest.fixture
def application_settings(settings):
    application_dict = dict(settings.APPLICATION)
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
        "FORM_PERMISSIONS": ["main", "sb1", "sb2", "nfd"],
        "HAS_PROJECT_CHANGE": True,
        "CREATE_IN_PROCESS": False,
        "USE_LOCATION": True,
        "GENERATE_DOSSIER_NR": False,
    }


@pytest.fixture
def ech_mandatory_answers_baugesuch():
    return {
        "ech-subject": "Baugesuch",
        "gemeinde": "Testgemeinde",
        "parzelle": [{"parzellennummer": "1586"}],
        "personalien-gesuchstellerin": [
            {
                "name-gesuchstellerin": "Testname",
                "ort-gesuchstellerin": "Testort",
                "plz-gesuchstellerin": 2323,
                "strasse-gesuchstellerin": "Teststrasse",
                "vorname-gesuchstellerin": "Testvorname",
                "juristische-person-gesuchstellerin": "Nein",
            }
        ],
    }


@pytest.fixture
def ech_mandatory_answers_einfache_vorabklaerung():
    return {
        "ech-subject": "Einfache Vorabklärung",
        "gemeinde": "Testgemeinde",
        "name-gesuchstellerin-vorabklaerung": "Testname",
        "ort-gesuchstellerin": "Testort",
        "plz-gesuchstellerin": 23235,  # non standard swiss zip
        "strasse-gesuchstellerin": "Teststrasse",
        "vorname-gesuchstellerin-vorabklaerung": "Testvorname",
    }


@pytest.fixture
def ech_mandatory_answers_vollstaendige_vorabklaerung():
    return {
        "ech-subject": "Vollständige Vorabklärung",
        "gemeinde": "Testgemeinde",
        "personalien-gesuchstellerin": [
            {
                "name-gesuchstellerin": "Testname",
                "ort-gesuchstellerin": "Testort",
                "plz-gesuchstellerin": 232,  # non standard swiss zip
                "strasse-gesuchstellerin": "Teststrasse",
                "vorname-gesuchstellerin": "Testvorname",
                "juristische-person-gesuchstellerin": "Nein",
            }
        ],
    }


@pytest.fixture
def caluma_config_bern(db):
    """
    Load the caluma config for kt_bern.

    Execution of this fixture takes some time. Only use if really necessary.
    """
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config-caluma-form.json"))
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config-caluma-workflow.json"))


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
def nfd_completion_date(
    activation, camac_question_factory, camac_chapter_factory, activation_answer_factory
):
    """Return a sample nfd completion date.

    In Uri the nfd completion date gets set after a service has completed the
    "Nachforderung" process on an instance with an activation.
    """
    return activation_answer_factory(
        chapter=camac_chapter_factory(pk=41),
        question=camac_question_factory(pk=243),
        item=1,
        activation=activation,
        answer=timezone.now(),
    )


@pytest.fixture
def caluma_config_be(settings, use_caluma_form):
    settings.APPLICATION["CALUMA"] = settings.APPLICATIONS["kt_bern"]["CALUMA"]


@pytest.fixture
def caluma_config_sz(settings):
    settings.APPLICATION["CALUMA"] = settings.APPLICATIONS["kt_schwyz"]["CALUMA"]


@pytest.fixture
def use_instance_service(application_settings):
    application_settings["USE_INSTANCE_SERVICE"] = True
    application_settings["ACTIVE_SERVICES"] = settings.APPLICATIONS["kt_bern"][
        "ACTIVE_SERVICES"
    ]
    application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {}
    application_settings["ACTIVE_SERVICES"]["CONSTRUCTION_CONTROL"]["FILTERS"] = {}

    def wrap(municipality_id=None, construction_control_id=None):
        if municipality_id:
            application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {
                "service__pk": municipality_id
            }
        if construction_control_id:
            application_settings["ACTIVE_SERVICES"]["CONSTRUCTION_CONTROL"][
                "FILTERS"
            ] = {"service__pk": construction_control_id}

        return application_settings

    yield wrap

    application_settings["USE_INSTANCE_SERVICE"] = False


@pytest.fixture
def caluma_workflow_config_be(
    settings, caluma_forms, caluma_config_be, use_instance_service
):
    forms = [
        caluma_form_models.Form.objects.create(slug="baugesuch"),
        caluma_form_models.Form.objects.create(slug="baugesuch-generell"),
        caluma_form_models.Form.objects.create(slug="baugesuch-mit-uvp"),
        caluma_form_models.Form.objects.create(slug="vorabklaerung-einfach"),
        caluma_form_models.Form.objects.create(slug="vorabklaerung-vollstaendig"),
        caluma_form_models.Form.objects.create(slug="hecken-feldgehoelze-baeume"),
    ]

    call_command("loaddata", settings.ROOT_DIR("kt_bern/config-caluma-workflow.json"))

    workflows = caluma_workflow_models.Workflow.objects.all()
    main_form = caluma_form_models.Form.objects.get(pk="main-form")

    for workflow in workflows.filter(
        pk__in=["building-permit", "preliminary-clarification"]
    ):
        workflow.allow_forms.clear()
        workflow.allow_forms.add(main_form)
        workflow.save()

    for form in forms:
        form.delete()

    yield workflows

    caluma_workflow_models.Case.objects.all().delete()
    caluma_workflow_models.Workflow.objects.all().delete()


@pytest.fixture
def caluma_workflow_config_sz(settings, caluma_forms, caluma_config_sz):
    caluma_form_models.Form.objects.create(slug="baugesuch"),

    call_command("loaddata", settings.ROOT_DIR("kt_schwyz/config-caluma-workflow.json"))

    workflows = caluma_workflow_models.Workflow.objects.all()

    return workflows


def yes(lang):
    return "ja" if lang == "de" else "yes"


def no(lang):
    return "nein" if lang == "de" else "no"


@pytest.fixture
def caluma_forms(settings):
    # forms
    caluma_form_models.Form.objects.create(
        slug="main-form", meta={"is-main-form": True}, name="Baugesuch"
    )
    caluma_form_models.Form.objects.create(slug="sb1")
    caluma_form_models.Form.objects.create(slug="sb2")
    caluma_form_models.Form.objects.create(slug="nfd")
    caluma_form_models.Form.objects.create(slug="circulation")
    caluma_form_models.Form.objects.create(slug="migriertes-dossier")

    # dynamic choice options get cached, so we clear them
    # to ensure the new "gemeinde" options will be valid
    cache.clear()

    # questions
    caluma_form_models.Question.objects.create(
        slug="gemeinde",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )
    caluma_form_models.Question.objects.create(
        slug="municipality", type=caluma_form_models.Question.TYPE_TEXT,
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

    # sb1 and sb2
    applicant_table = caluma_form_models.Form.objects.create(slug="personalien-tabelle")
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
    for form_id, question_id in FORM_QUESTION_MAP:
        caluma_form_models.FormQuestion.objects.create(
            form_id=form_id, question_id=question_id
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
