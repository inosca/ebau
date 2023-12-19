import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Applicant", 0), ("Municipality", 1), ("Service", 1), ("Support", 3)],
)
def test_keyword_list(admin_client, keyword_factory, service, expected_count):
    keyword_factory(service=service)
    keyword_factory.create_batch(2)

    response = admin_client.get(reverse("keyword-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count
