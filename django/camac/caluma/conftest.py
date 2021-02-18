import functools

import pytest
from caluma.schema import schema


@pytest.fixture
def caluma_admin_request(rf, caluma_admin_user):
    request = rf.get("/graphql")
    request.user = caluma_admin_user
    return request


@pytest.fixture
def caluma_admin_schema_executor(caluma_admin_request):
    return functools.partial(
        schema.execute, context_value=caluma_admin_request, middleware=[]
    )
