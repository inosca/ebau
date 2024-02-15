import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
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


@pytest.mark.parametrize(
    "role__name,forms_all_versions,amount",
    [
        ("Applicant", True, 3),
        ("Applicant", False, 1),
        ("Municipality", True, 3),
        ("Municipality", False, 1),
        ("Service", True, 3),
        ("Service", False, 1),
    ],
)
def test_form_versioned_filter(
    admin_client, form, form_factory, forms_all_versions, amount
):
    form.family = form
    form.save()
    form_factory(family=form)
    form_factory(family=form)

    url = reverse("form-list")

    response = admin_client.get(url, {"forms_all_versions": forms_all_versions})
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == amount
    assert json["data"][0]["id"] == str(form.pk)


@pytest.mark.parametrize(
    "form__form_state,amount",
    [
        (LazyFixture("form_state"), 1),
        (LazyFixture(lambda form_state_factory: form_state_factory()), 0),
    ],
)
def test_form_state_filter(admin_client, form, form_state, amount):
    url = reverse("form-list")

    response = admin_client.get(url, {"form_state": str(form_state.pk)})
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == amount


def test_form_detail(admin_client, form):
    url = reverse("form-detail", args=[form.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
