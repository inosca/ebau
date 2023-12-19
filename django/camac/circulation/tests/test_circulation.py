import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers


@pytest.mark.parametrize(
    "role__name,instance__user,num_queries",
    [
        ("Applicant", LazyFixture("admin_user"), 11),
        ("Canton", LazyFixture("user"), 11),
        ("Municipality", LazyFixture("user"), 10),
        ("Service", LazyFixture("user"), 10),
    ],
)
def test_circulation_list(
    admin_client,
    instance_state,
    circulation,
    activation,
    num_queries,
    django_assert_num_queries,
):
    url = reverse("circulation-list")

    included = serializers.CirculationSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url,
            data={
                "instance_state": instance_state.pk,
                "include": ",".join(included.keys()),
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(circulation.pk)
    assert len(json["included"]) == len(included)


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_circulation_detail(admin_client, circulation):
    url = reverse("circulation-detail", args=[circulation.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "url,method,expected_status",
    [
        ("circulation-list", "get", status.HTTP_200_OK),
        ("circulation-list", "post", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("circulation-detail", "get", status.HTTP_200_OK),
        ("circulation-detail", "patch", status.HTTP_403_FORBIDDEN),
        ("circulation-detail", "delete", status.HTTP_204_NO_CONTENT),
    ],
)
def test_circulation_permissions(
    admin_client, circulation, url, method, expected_status
):
    assert (
        getattr(admin_client, method)(
            reverse(url, **({"args": [circulation.pk]} if "detail" in url else {}))
        ).status_code
        == expected_status
    )


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "has_activation,has_other_circulations,instance_state__name,expected_status",
    [
        (True, False, "circulation_init", status.HTTP_403_FORBIDDEN),
        (False, False, "circulation_init", status.HTTP_204_NO_CONTENT),
        (False, False, "circulation", status.HTTP_204_NO_CONTENT),
        (False, True, "circulation", status.HTTP_204_NO_CONTENT),
    ],
)
def test_delete_circulation(
    admin_client,
    instance_service,
    instance_state,
    circulation,
    circulation_factory,
    activation_factory,
    has_activation,
    has_other_circulations,
    expected_status,
):
    if has_activation:
        activation_factory(circulation=circulation)

    if has_other_circulations:
        circulation_factory(instance=circulation.instance)

    response = admin_client.delete(reverse("circulation-detail", args=[circulation.pk]))

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_end_circulation(
    admin_client,
    instance_service,
    circulation,
    activation,
    circulation_state,
    application_settings,
):
    application_settings["CIRCULATION_STATE_END"] = circulation_state.name

    response = admin_client.patch(reverse("circulation-end", args=[circulation.pk]))

    activation.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert activation.circulation_state == circulation_state
