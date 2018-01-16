import logging

import pytest
from pytest_factoryboy import register
from rest_framework_jwt.test import APIJWTClient

from camac.document.factories import (AttachmentFactory,
                                      AttachmentSectionFactory)
from camac.instance.factories import (FormFactory, FormFieldFactory,
                                      FormStateFactory, InstanceFactory,
                                      InstanceStateFactory)
from camac.user.factories import (GroupFactory, RoleFactory, UserFactory,
                                  UserGroupFactory)

factory_logger = logging.getLogger('factory')
factory_logger.setLevel(logging.INFO)

sorl_thumbnail_logger = logging.getLogger('sorl.thumbnail')
sorl_thumbnail_logger.setLevel(logging.INFO)

# TODO: automatically register all factory classes of all factory modules
register(AttachmentFactory)
register(AttachmentSectionFactory)
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
def client(db):
    return APIJWTClient()


@pytest.fixture
def admin_client(db, client, admin_user, user_group_factory):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user_group_factory(default_group=1, user=admin_user)
    client.login(username=admin_user.username, password='password')
    return client
