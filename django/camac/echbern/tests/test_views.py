from django.urls import reverse
from rest_framework import status

from .full_document_response import full_document


def test_application_retrieve(
    admin_client, admin_user, instance_factory, attachment, requests_mock
):
    i = instance_factory(user=admin_user)
    attachment.instance = i
    attachment.save()
    url = reverse("application", args=[i.pk])

    requests_mock.post("http://caluma:8000/graphql/", json=full_document)

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
