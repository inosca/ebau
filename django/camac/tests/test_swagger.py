import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("user__username", ["guest"])
def test_swagger_schema(db, client, user, group, user_group_factory):
    user_group_factory(group=group, user=user, default_group=1)
    url = reverse("schema-json", args=[".json"])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
