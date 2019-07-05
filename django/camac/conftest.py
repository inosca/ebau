import inspect
import logging

import pytest
from factory import Faker
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory

from camac.applicants import factories as applicant_factories
from camac.core import factories as core_factories
from camac.document import factories as document_factories
from camac.faker import FreezegunAwareDatetimeProvider
from camac.instance import factories as instance_factories, models as instance_models
from camac.notification import factories as notification_factories
from camac.user import factories as user_factories


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
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


Faker.add_provider(FreezegunAwareDatetimeProvider)


@pytest.fixture
def rf(db):
    return APIRequestFactory()


@pytest.fixture
def admin_user(admin_user, group, group_location, user_group_factory):
    user_group_factory(group=group, user=admin_user, default_group=1)
    admin_user.username = "462afaba-aeb7-494a-8596-3497b81ed701"
    admin_user.save()
    return admin_user


@pytest.fixture
def admin_client(db, admin_user):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
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
    application_settings["USE_CALUMA_FORM"] = True


@pytest.fixture
def bern_instance_states(db, instance_state_factory):
    new, _ = instance_models.InstanceState.objects.get_or_create(pk=1)
    new.trans.create(name="Neu", language="de")
    subm, _ = instance_models.InstanceState.objects.get_or_create(pk=20000)
    subm.trans.create(name="eBau-Nummer zu vergeben", language="de")
