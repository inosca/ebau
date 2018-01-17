import logging

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIRequestFactory
from rest_framework_jwt.test import APIJWTClient

from camac.instance.factories import (FormFactory, FormFieldFactory,
                                      FormStateFactory, InstanceFactory,
                                      InstanceStateFactory)
from camac.user.factories import (GroupFactory, RoleFactory, UserFactory,
                                  UserGroupFactory)

factory_logger = logging.getLogger('factory')
factory_logger.setLevel(logging.INFO)

register(FormStateFactory)
register(FormFactory)
register(FormFieldFactory)
register(UserFactory)
register(UserGroupFactory)
register(GroupFactory)
register(InstanceFactory)
register(InstanceStateFactory)
register(RoleFactory)


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
def admin_group(group):
    return group


@pytest.fixture
def admin_user(admin_user, admin_group, user_group_factory):
    user_group_factory(group=admin_group, user=admin_user, default_group=1)
    return admin_user


@pytest.fixture
def admin_client(db, client, admin_user, user_group_factory):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user_group_factory(default_group=1, user=admin_user)
    client.login(username=admin_user.username, password='password')
    return client
