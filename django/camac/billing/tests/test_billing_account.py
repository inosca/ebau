import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.django_db
def test_billing_account_list_filter(
    admin_client,
    billing_v2_account_factory,
    service_group_factory,
    instance_state_factory,
    instance,
    service,
):
    instance_state1 = instance_state_factory(name="test1")
    instance_state2 = instance_state_factory(name="test2")

    account1 = billing_v2_account_factory.create(
        service_group=service.service_group,
    )
    account1.instance_states.add(instance_state1)
    account2 = billing_v2_account_factory.create(
        service_group=service.service_group,
    )
    account2.instance_states.add(instance_state2)
    billing_v2_account_factory.create_batch(
        2,
        service_group=service_group_factory(),
    )

    response = admin_client.get(
        reverse("billing-v2-account-list"),
        data={},
        headers={"Content-Type": "application/json"},
    )

    # test list all
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 2

    # test filtering by instance state
    response = admin_client.get(
        reverse("billing-v2-account-list"),
        data={"filter[instance_states]": instance_state1.pk},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
