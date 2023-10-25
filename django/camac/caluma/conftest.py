import functools
from collections import namedtuple

import pytest
from caluma.schema import schema

from camac.caluma.utils import CamacRequest


@pytest.fixture
def caluma_admin_request(rf, caluma_admin_user):
    def wrapper(**kwargs):
        request = rf.get("/graphql", **kwargs)
        request.user = caluma_admin_user
        Info = namedtuple("Info", "context")
        request.camac_request = CamacRequest(Info(context=request)).request
        return request

    return wrapper


@pytest.fixture
def caluma_admin_schema_executor(caluma_admin_request):
    return functools.partial(
        schema.execute, context_value=caluma_admin_request(), middleware=[]
    )


@pytest.fixture
def caluma_admin_public_schema_executor(caluma_admin_request):
    return functools.partial(
        schema.execute,
        context_value=caluma_admin_request(HTTP_X_CAMAC_PUBLIC_ACCESS=True),
        middleware=[],
    )


@pytest.fixture
def caluma_admin_schema_executor_for_group(caluma_admin_request):
    def wrap(group):
        return functools.partial(
            schema.execute,
            context_value=caluma_admin_request(HTTP_X_CAMAC_GROUP=group),
            middleware=[],
        )

    return wrap
