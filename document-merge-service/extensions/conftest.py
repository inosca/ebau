from unittest.mock import patch

import pytest
from django.conf import settings

from document_merge_service.extensions.permissions import DMS_SETTINGS


@pytest.fixture
def mock_services(requests_mock):
    requests_mock.register_uri(
        "GET",
        f"{settings.EXTENSIONS_ARGUMENTS['DJANGO_API']}/api/v1/me?include=service,service.service_parent,service.municipality,service.service_group",
        json={
            "included": [
                {
                    "type": "public-service-groups",
                    "id": "20000",
                    "attributes": {"name": "Leitbehörde RSTA", "slug": "district"},
                },
                {
                    "type": "services",
                    "id": "1",
                    "attributes": {"slug": "rsta-test"},
                },
            ]
        },
    )


@pytest.fixture
def dms_settings():
    with patch.dict(DMS_SETTINGS) as mock:
        yield mock
