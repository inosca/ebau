import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name,amount", [("Applicant", 1), ("Municipality", 2)])
def test_form_list(admin_client, form, form_factory, form_state_factory, amount):
    form_factory(form_state=form_state_factory(name="Internal"))

    url = reverse("form-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == amount
    assert json["data"][0]["id"] == str(form.pk)


def test_form_detail(admin_client, form):
    url = reverse("form-detail", args=[form.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
