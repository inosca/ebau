import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("user__username", ["guest"])
def test_swagger_schema(db, user, client, caplog):
    response = client.get(reverse("schema-json", args=[".json"]))
    assert response.status_code == status.HTTP_200_OK
    assert not len(caplog.messages)
