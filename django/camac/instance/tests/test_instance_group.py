import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_group_list(admin_client, instance, instance_group_factory):
    url = reverse("instance-group-list")

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
