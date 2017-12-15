import pytest
from django.contrib.auth import get_user_model

from camac.tests.client import JSONAPIClient


@pytest.fixture
def client(db):
    return JSONAPIClient()


@pytest.fixture
def auth_client(db):
    """Return instance of a JSONAPIClient that is logged in as test user."""
    user = get_user_model().objects.create_user(
        username='user',
        password='123qweasd',
        disabled=False,
    )

    client = JSONAPIClient()
    client.user = user
    client.login('user', '123qweasd')

    return client
