import pytest
from graphql import GraphQLError
from rest_framework.exceptions import PermissionDenied, ValidationError

from camac.caluma.views import CamacAuthenticatedGraphQLView


@pytest.mark.parametrize("debug", [True, False])
@pytest.mark.parametrize(
    ("error", "expected_log"),
    [
        (
            PermissionDenied(),
            None,
        ),
        (
            GraphQLError("Some error"),
            None,
        ),
        (
            GraphQLError("Top error", original_error=ValidationError("Bottom error")),
            None,
        ),
        (
            Exception("Some error"),
            "Some error",
        ),
        (
            GraphQLError("Top error", original_error=Exception("Bottom error")),
            "Bottom error",
        ),
    ],
)
def test_error_logging(
    caluma_admin_request,
    caplog,
    settings,
    mocker,
    error,
    expected_log,
    debug,
):
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility.filter_queryset",
        side_effect=error,
    )

    settings.DEBUG = debug

    result = CamacAuthenticatedGraphQLView().execute_graphql_request(
        caluma_admin_request(),
        {},
        "query { allForms { totalCount } }",
        None,
        None,
    )

    assert result.errors
    assert result.errors[0] == error or result.errors[0].original_error == error

    if debug and expected_log:
        assert expected_log in caplog.messages
    else:
        assert not caplog.messages
