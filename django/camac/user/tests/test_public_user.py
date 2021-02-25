from django.urls import reverse
from rest_framework import status


def test_public_user_list(admin_client, user):

    response = admin_client.get(reverse("publicuser-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 2


def test_public_user_username_filter(admin_client, user):
    url = reverse("publicuser-list")

    response = admin_client.get(url, data={"username": user.username})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["attributes"]["username"] == user.username
