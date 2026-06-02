import pytest
from django.core.cache import cache
from factory import LazyAttribute
from pytest_factoryboy import register

from document_merge_service.api.data import django_file
from document_merge_service.api.factories import TemplateFactory
from document_merge_service.api.models import Template

# Service group that has configured shared template admins and the service slug
# that is one of those admins. The same slug must appear both in the settings
# (shared_template_settings) and in the mocked service data (mock_service_data)
# for a request to count as a shared template admin.
SERVICE_GROUP_SLUG = "district"
ADMIN_SERVICE_SLUG = "rsta-test"

register(
    TemplateFactory,
    "dms_template",
    engine=Template.DOCX_TEMPLATE,
    template=LazyAttribute(lambda _: django_file("docx-template.docx")),
)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def mock_service_data(mocker, request):
    """Mock the service data returned for the current request.

    By default the request belongs to service "1" in service group "district",
    but is neither a shared template admin nor a support user.

    Configured via indirect parametrization with the following options:

    - `is_shared_admin`: Make the service a shared template admin for the
                         service group "district" (by including
                         `ADMIN_SERVICE_SLUG` in the service slugs).
    - `is_support`: Give the request the "support" role permission.

    Example:
        @pytest.mark.parametrize(
            "mock_service_data",
            [{"is_support": True}],
            indirect=True,
        )
        def test_something(mock_service_data):
            ...

    """
    kwargs = getattr(request, "param", {})
    is_shared_admin = kwargs.get("is_shared_admin", False)
    is_support = kwargs.get("is_support", False)

    return mocker.patch(
        "document_merge_service.extensions.utils._get_service_data_from_api",
        return_value={
            "service_ids": ["1"],
            "service_group_slugs": [SERVICE_GROUP_SLUG],
            "service_slugs": [ADMIN_SERVICE_SLUG] if is_shared_admin else [],
            "role_permissions": ["support"] if is_support else [],
        },
    )


@pytest.fixture(autouse=True)
def shared_template_settings(mocker):
    return mocker.patch(
        "document_merge_service.extensions.permissions.DMS_SETTINGS",
        {
            "SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP": {
                SERVICE_GROUP_SLUG: [ADMIN_SERVICE_SLUG]
            },
            "ENABLE_SYSTEM_TEMPLATE_EDITING": True,
        },
    )
