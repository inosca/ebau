import inspect
import logging

import pytest
from django.conf import settings
from factory.base import FactoryMetaClass
from keycloak import KeycloakOpenID
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory

from camac.core import factories as core_factories
from camac.document import factories as document_factories
from camac.instance import factories as instance_factories
from camac.user import factories as user_factories


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            register(obj)


factory_logger = logging.getLogger('factory')
factory_logger.setLevel(logging.INFO)

sorl_thumbnail_logger = logging.getLogger('sorl.thumbnail')
sorl_thumbnail_logger.setLevel(logging.INFO)

register_module(user_factories)
register_module(instance_factories)
register_module(core_factories)
register_module(document_factories)


class APIKeycloakClient(APIClient):
    def login(self, **credentials):
        keycloak = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id='portal',
            realm_name=settings.KEYCLOAK_REALM,
        )

        token = keycloak.token(**credentials)
        self.credentials(HTTP_AUTHORIZATION="{0} {1}".format(
            'Bearer', token['access_token']))


@pytest.fixture
def rf(db):
    return APIRequestFactory()


@pytest.fixture
def admin_rf(rf, admin_client):
    rf.defaults = admin_client._credentials
    return rf


@pytest.fixture
def client(db):
    return APIKeycloakClient()


@pytest.fixture
def admin_user(admin_user, group, group_location, user_group_factory):
    user_group_factory(group=group, user=admin_user, default_group=1)
    admin_user.identifier = '462afaba-aeb7-494a-8596-3497b81ed701'
    admin_user.save()
    return admin_user


@pytest.fixture
def admin_client(db, client, admin_user, user_group_factory):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user_group_factory(default_group=1, user=admin_user)
    client.login(username=admin_user.username, password='camac')
    return client
