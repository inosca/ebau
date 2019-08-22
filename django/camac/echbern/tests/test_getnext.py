from django.urls import reverse
from rest_framework import status


def test_getnext_retrieve(admin_client, snapshot):
    url = reverse("getNext")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.content)
