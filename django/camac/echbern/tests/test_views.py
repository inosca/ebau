from django.urls import reverse
from rest_framework import status


def test_application_retrieve(admin_client, admin_user, instance_factory):
    i = instance_factory(user=admin_user)
    url = reverse("application", args=[i.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_applications_list(admin_client, admin_user, instance, instance_factory):
    i = instance_factory(user=admin_user)
    url = reverse("applications")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(i.instance_id)
