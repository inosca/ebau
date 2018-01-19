import inspect
import logging

import pytest
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIRequestFactory
from rest_framework_jwt.test import APIJWTClient

from camac.core import factories as core_factories
from camac.instance import factories as instance_factories
from camac.user import factories as user_factories


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj)


factory_logger = logging.getLogger('factory')
factory_logger.setLevel(logging.INFO)

register_module(user_factories)
register_module(instance_factories)
register_module(core_factories)


@pytest.fixture
def rf(db):
    return APIRequestFactory()


@pytest.fixture
def admin_rf(rf, admin_client):
    rf.defaults = admin_client._credentials
    return rf


@pytest.fixture
def client(db):
    return APIJWTClient()


@pytest.fixture
def admin_user(admin_user, group, group_locations, user_group_factory):
    user_group_factory(group=group, user=admin_user, default_group=1)
    return admin_user


@pytest.fixture
def admin_client(db, client, admin_user, user_group_factory):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user_group_factory(default_group=1, user=admin_user)
    client.login(username=admin_user.username, password='password')
    return client
