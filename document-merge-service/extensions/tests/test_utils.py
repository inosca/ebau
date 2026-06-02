import re

from django.conf import settings

from document_merge_service.extensions import utils


def test_get_service_data(requests_mock, mocker, rf):
    requests_mock.register_uri(
        "GET",
        re.compile(f"{settings.EXTENSIONS_ARGUMENTS['DJANGO_API']}/api/v1/me.*"),
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
                {
                    "type": "roles",
                    "id": "99",
                    "attributes": {"permission": "support"},
                },
            ]
        },
    )

    api_call_spy = mocker.spy(utils, "_get_service_data_from_api")

    req_1 = rf.request(HTTP_AUTHORIZATION="Bearer sometoken", HTTP_X_CAMAC_GROUP="42")
    req_2 = rf.request(HTTP_AUTHORIZATION="Bearer sometoken", HTTP_X_CAMAC_GROUP="43")
    req_3 = rf.request(HTTP_AUTHORIZATION="Bearer othertoken", HTTP_X_CAMAC_GROUP="42")

    assert utils.get_service_data(req_1) == {
        "service_ids": ["1"],
        "service_group_slugs": ["district"],
        "service_slugs": ["rsta-test"],
        "role_permissions": ["support"],
    }
    assert api_call_spy.call_count == 1

    # Second call gets a cache hit
    utils.get_service_data(req_1)
    assert api_call_spy.call_count == 1

    # Different x-camac-group, no cache hit
    utils.get_service_data(req_2)
    assert api_call_spy.call_count == 2

    # Different token, no cache hit
    utils.get_service_data(req_3)
    assert api_call_spy.call_count == 3
