import functools
from collections import namedtuple

import pytest
from caluma.schema import schema

from camac.caluma.utils import CamacRequest


@pytest.fixture
def caluma_admin_request(rf, caluma_admin_user):
    request = rf.get("/graphql")
    request.user = caluma_admin_user
    Info = namedtuple("Info", "context")
    request.camac_request = CamacRequest(Info(context=request)).request
    return request


@pytest.fixture
def caluma_admin_schema_executor(caluma_admin_request):
    return functools.partial(
        schema.execute, context_value=caluma_admin_request, middleware=[]
    )
