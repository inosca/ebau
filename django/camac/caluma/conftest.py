import functools

import pytest
from caluma.caluma_user.models import OIDCUser
from caluma.schema import schema
from jwt import encode as jwt_encode

from ..instance.conftest import (  # noqa: F401; pylint: disable=unused-variable
    caluma_forms,
    caluma_workflow,
)


@pytest.fixture
def token(admin_user):
    return jwt_encode(
        {"aud": admin_user.groups.first().name, "username": "joël-tester"}, "secret"
    )


@pytest.fixture
def caluma_admin_user(settings, token, admin_user):
    return OIDCUser(token, {"sub": admin_user.username})


@pytest.fixture
def caluma_admin_request(rf, caluma_admin_user):
    request = rf.get("/graphql")
    request.user = caluma_admin_user
    return request


@pytest.fixture
def caluma_admin_schema_executor(caluma_admin_request):
    return functools.partial(
        schema.execute, context=caluma_admin_request, middleware=[]
    )
