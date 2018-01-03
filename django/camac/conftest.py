import logging

import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register

from camac.instance.factories import (FormFactory, FormFieldFactory,
                                      FormStateFactory, InstanceFactory,
                                      InstanceStateFactory)
from camac.tests.client import JSONAPIClient
from camac.user.factories import (GroupFactory, RoleFactory, UserFactory,
                                  UserGroupFactory)

# TODO: automatically register all factory classes of all factory modules
register(FormStateFactory)
register(FormFactory)
register(FormFieldFactory)
register(UserFactory)
register(UserGroupFactory)
register(GroupFactory)
register(InstanceFactory)
register(InstanceStateFactory)
register(RoleFactory)


@pytest.fixture(autouse=True)
def caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture
def client(db):
    return JSONAPIClient()


@pytest.fixture
def auth_client(db, user_group_factory):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user = get_user_model().objects.create_user(
        username='user',
        password='123qweasd',
        disabled=False,
    )

    user_group_factory(default_group=1, user=user)

    client = JSONAPIClient()
    client.user = user
    client.login('user', '123qweasd')

    return client
