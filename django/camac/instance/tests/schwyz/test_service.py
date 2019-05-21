import pytest
from django.urls import reverse
from rest_framework import status

from camac.markers import only_schwyz

# module-level skip if we're not testing Schwyz variant
pytestmark = only_schwyz


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Fachstelle", 1), ("Kanton", 1), ("Gemeinde", 1)],
)
def test_service_list(admin_client, service, size):
    url = reverse("service-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
