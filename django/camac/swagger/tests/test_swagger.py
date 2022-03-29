import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("config", ["kt_bern", "kt_schwyz", "demo"])
def test_swagger_schema(db, user, client, settings, config, caplog):
    settings.APPLICATION = settings.APPLICATIONS[config]
    if settings.APPLICATION["ECH0211"]["API_ACTIVE"]:
        response = client.get(reverse("schema-json", args=[".json"]))
        assert response.status_code == status.HTTP_200_OK
        assert not len(caplog.messages)
