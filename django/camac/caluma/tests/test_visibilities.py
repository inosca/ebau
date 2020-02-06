import functools
from base64 import b64encode
from json import dumps

import pytest
from caluma.caluma_user.models import OIDCUser
from caluma.schema import schema


@pytest.fixture
def caluma_admin_user(settings, admin_user):
    token_body = b64encode(dumps({"aud": admin_user.groups.first().name}).encode())

    return OIDCUser(
        b".".join([b"some", token_body, b"token"]), {"sub": admin_user.username}
    )


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


@pytest.mark.parametrize(
    "role__name,expected_count", [("Support", 3), ("Service", 1), ("Applicant", 0)]
)
def test_document_visibility(
    db,
    role,
    expected_count,
    instance_factory,
    activation_factory,
    admin_user,
    document_factory,
    caluma_admin_schema_executor,
):
    group = admin_user.groups.first()

    instance = instance_factory(group=group)
    activation_factory(circulation__instance=instance, service=group.service)

    for instance in [instance, instance_factory(group=group), instance_factory()]:
        document_factory(meta={"camac-instance-id": instance.pk})

    result = caluma_admin_schema_executor(
        """
        query {
            allDocuments {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    )

    assert not result.errors
    assert len(result.data["allDocuments"]["edges"]) == expected_count


def test_document_visibility_no_camac_user(
    db, caluma_admin_request, caluma_admin_schema_executor
):
    caluma_admin_request.user = OIDCUser("sometoken", {"sub": "inexistentusername"})

    result = caluma_admin_schema_executor(
        """
        query {
            allDocuments {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    """
    )

    assert not result.errors
    assert len(result.data["allDocuments"]["edges"]) == 0
