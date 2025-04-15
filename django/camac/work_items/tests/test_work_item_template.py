import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,expected_names",
    [
        ("Applicant", set()),
        ("Municipality", {"global", "my-service", "my-service-group"}),
    ],
)
def test_work_item_template_list(
    work_item_template_factory,
    admin_client,
    expected_names,
    service,
    service_group,
    service_factory,
    service_group_factory,
):
    for name, services, service_groups in [
        ("global", None, None),
        ("my-service", [service], None),
        ("my-service-group", None, [service_group]),
        ("other-service", [service_factory()], None),
        ("other-service-group", None, [service_group_factory()]),
    ]:
        template = work_item_template_factory(name=name)
        if services:
            template.services.set(services)
        if service_groups:
            template.service_groups.set(service_groups)

    response = admin_client.get(reverse("work-item-template-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == len(expected_names)
    assert set([e["attributes"]["name"] for e in data]) == expected_names
