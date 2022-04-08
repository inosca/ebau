import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,instance__user",
    [
        ("Applicant", LazyFixture("admin_user")),
    ],
)
def test_instance_form_name_filter(
    application_settings,
    admin_client,
    instance,
    instance_factory,
    instance_resource_factory,
    instance_state_factory,
    ir_role_acl_factory,
):
    role = admin_client.user.groups.first().role

    ir1 = instance_resource_factory()
    ir2 = instance_resource_factory()

    other_instance_state = instance_state_factory()

    ir_role_acl_factory(
        role=role, instance_state=instance.instance_state, instance_resource=ir1
    )
    ir_role_acl_factory(
        role=role, instance_state=other_instance_state, instance_resource=ir1
    )
    ir_role_acl_factory(
        role=role, instance_state=other_instance_state, instance_resource=ir2
    )

    url = reverse("instance-resource-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # without the filter, both IRs are returned
    assert len(response.json()["data"]) == 2

    response = admin_client.get(url, {"instance": instance.pk})
    assert response.status_code == status.HTTP_200_OK
    # with the filter, only the first IR is returned
    assert len(response.json()["data"]) == 1
