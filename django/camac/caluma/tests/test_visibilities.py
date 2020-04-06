import functools

import pytest
from caluma.caluma_user.models import OIDCUser
from caluma.schema import schema
from jwt import encode as jwt_encode


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


@pytest.mark.parametrize("role__name", ["Support"])
def test_document_visibility_filter(
    db,
    rf,
    role,
    instance_factory,
    activation_factory,
    admin_user,
    caluma_admin_user,
    document_factory,
    circulation_state,
    circulation_state_factory,
):
    group = admin_user.groups.first()

    instance1 = instance_factory(group=group)
    activation_factory(
        circulation__instance=instance1,
        service=group.service,
        circulation_state=circulation_state,
    )

    instance2 = instance_factory(group=group)
    activation_factory(
        circulation__instance=instance2,
        service=group.service,
        circulation_state=circulation_state_factory(),
    )

    for instance in [instance1, instance2]:
        document_factory(meta={"camac-instance-id": instance.pk})

    request = rf.get(
        "/graphql",
        **{"HTTP_X_CAMAC_FILTERS": f"circulation_state={circulation_state.pk}"},
    )
    request.user = caluma_admin_user
    query = """
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
    result = schema.execute(query, context=request, middleware=[])

    assert not result.errors
    assert len(result.data["allDocuments"]["edges"]) == 1
