import pytest
from django.conf import settings


@pytest.fixture
def mock_services(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{settings.EXTENSIONS_ARGUMENTS['DJANGO_API']}/api/v1/me?include=service,service.service_parent,service.municipality",
        json={"included": [{"type": "services", "id": "1"}]},
    )
